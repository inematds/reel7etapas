#!/usr/bin/env python3
"""reel7etapas — uma ideia vira um reel 9:16 em 7 etapas de gatilho:
gancho → desejo → medo → facilidade → descoberta → benefício → comentário.
Cada etapa entra numa palavra da fala do avatar do Nei e troca imagem (com câmera própria), manchete e destaque.

  reel7etapas.py novo <slug>             cria edicoes/<data>-<slug>/roteiro.yaml a partir do exemplo
  reel7etapas.py fazer <pasta>           tudo, com portões: imagens → avatar → montar → validar → mapa
  reel7etapas.py imagens <pasta>         7 imagens no Codex image_gen (flux2-klein local só como reserva) + cor neutra + portão
  reel7etapas.py cor <pasta>             tira o amarelado das imagens prontas (sem gerar de novo)
  reel7etapas.py avatar <pasta>          fala no estúdio do HeyGen (exige avatar/APROVADO_HEYGEN) — usa o reelcomenta
  reel7etapas.py montar <pasta>          monta <pasta>/video.mp4 (zona segura, legenda e loudness conferidos no render)
  reel7etapas.py validar <pasta>         portões finais + qa_short.py do makeshorts + folha de revisão em tamanho real
  reel7etapas.py mapa <pasta>            mapa.jpg (as 7 etapas com quadro, gatilho e porquê) + capa.jpg
  reel7etapas.py publicar <pasta>        bot do Telegram + YouTube (yt-pubx, canal do roteiro; padrão lives1)
  reel7etapas.py enviar <pasta> [texto]  só o bot

Contrato visual (perfil 'divulgacao' do makeshorts): 1080x1920, 30 fps, −14 LUFS, legenda ≤ 3 palavras / 22 caracteres
com fonte ≥ 64 px, imagem mudando a cada ≤ 3,5 s, nada fora da zona segura (topo ~1%, base ~7%, lados 6%, coluna de botões 12%).
"""
import base64, concurrent.futures as cf, hashlib, json, math, os, re, shutil, subprocess, sys, urllib.request
from datetime import date
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFilter, ImageStat

HOME = Path.home()
RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(os.environ.get("R7_REELCOMENTA", HOME / "projetos/reelcomenta"))))
import reelcomenta as rc  # noqa: E402  (transcrição, recorte do rosto, estúdio HeyGen, envio ao bot)
from reelcomenta import W, H, FPS, ANTON, MBLK, MXB, AMB, VERM, BRANCO, ESC, DEJAVU, fnt, ease, cor, run, dur  # noqa: E402

QA_SHORT = Path(os.environ.get("R7_QA_SHORT", HOME / "projetos/makeshorts/.claude/skills/makeshorts/scripts/qa_short.py"))
YT_PUBX = Path(os.environ.get("R7_YT_PUBX", HOME / "projetos/yt-pubx/yt-pubx"))
FLUX_API = os.environ.get("R7_IMAGEM_API", "http://localhost:8000/generate")
EXEMPLO = RAIZ / "edicoes/2026-10-11-jarvis/roteiro.yaml"

# ---- geometria: tudo que é texto ou caixa precisa caber em SAFE (x0, y0, x1, y1)
SAFE = (65, 24, 950, 1790)
HEAD_Y = 66                                  # topo da manchete (colada no alto: não cobre a cena)
LEG_Y = 1220                                  # centro vertical da legenda
AVX, AVY, AVW, AVH = 700, 1300, 360, 408      # avatar (embaixo à direita; 12/10: subiu 62 px a pedido do Nei)
CARD = (65, 1300, 680, 1708)                  # destaque / CTA à esquerda do avatar (acompanha o avatar)
LEG_MIN, HEAD_MIN = 64, 80                    # fonte mínima (px)
MAX_PAL, MAX_CAR = 3, 22                      # legenda
MUDA_MAX = 3.3                                # imagem muda (corte de enquadramento) a cada ≤ 3,3 s
XF = 0.3                                      # crossfade entre etapas
FIM_EXTRA = 2.6                               # cartão final depois da última palavra
FRACAS = {"de", "do", "da", "dos", "das", "o", "a", "os", "as", "e", "que", "seu", "sua", "um", "uma", "no", "na", "em",
          "por", "para", "pra", "com", "te", "eu", "você", "ao", "se", "já", "é", "só", "mais"}

ESTILO = ("Fotografia realista natural, vertical 9:16, com cara de foto real (pele com textura, ambiente comum), sem brilho "
          "de propaganda. LUZ NEUTRA E LIMPA: branco que parece branco, cores naturais, UMA cor forte de destaque no assunto; "
          "sem tom amarelado, sem sépia, sem luz dourada, sem pôr do sol. UM assunto só, grande e nítido (rosto com emoção "
          "forte ou objeto-símbolo ocupando 40 a 60% da largura), fácil de entender num celular em meio segundo. "
          "COMPOSIÇÃO OBRIGATÓRIA: o assunto "
          "principal (rostos, mãos, tela, objeto-chave) fica inteiro na faixa central da imagem, entre 30% e 60% da altura; "
          "os 20% de cima são fundo calmo (parede, teto, janela) porque ali entra o título, e os 40% de baixo são "
          "superfície ou fundo sem nada importante, porque ali entram o apresentador e um cartão. Sem texto, sem letras legíveis, sem números, sem logotipos, sem marcas, "
          "sem robôs, sem visual de ficção científica.")
# a luz conta a história: o problema é frio, a solução é dia claro (o âmbar da marca fica só no texto desenhado por cima)
LUZ = ["luz neutra e contrastada", "luz clara e neutra de dia", "luz fria levemente azulada, clima tenso (mas o assunto bem visível)",
       "luz clara e neutra de dia", "luz neutra com o objeto-chave em destaque", "luz clara de dia, cores vivas e limpas",
       "luz clara e neutra de dia"]
AMARELO_CORRIGE, AMARELO_ALVO, AMARELO_MAX = 18.0, 12.0, 25.0   # (R+G)/2 - B da imagem inteira, escala 0-255


def log(*a):
    print("[reel7etapas]", *a, flush=True)


def falha(portao, msg):
    sys.exit(f"[reel7etapas] PORTÃO '{portao}' REPROVOU: {msg}")


# ---- layouts (roteiro 'layout:'): onde ficam a imagem da etapa, o avatar, a manchete, o cartão e a legenda.
# 'padrao' é o original. Nos outros, a capa (etapa 1) continua em tela cheia e o layout entra na etapa 2.
LAYOUTS = {
    "dividido":  dict(img=(0, 0, 1080, 1100), av=(0, 1100, 1080, 820), forma="ret", head_y=66, card=(65, 590, 640, 998), leg_y=1050),
    "invertido": dict(img=(0, 880, 1080, 1040), av=(0, 0, 1080, 880), forma="ret", head_y=895, card=(65, 1280, 640, 1688), leg_y=1742),
    "circulo":   dict(img=None, av=(290, 1270, 500, 500), forma="circulo", head_y=66, card=(65, 640, 640, 1048), leg_y=1180),
}
LAY = None          # layout ativo (None = padrão)
AV_CAPA = True      # avatar já no quadro 0 (pedido do Nei 12/10: o rosto dele é autoridade); capa.avatar: false desliga
AVC = (190, 740, 700, 794)   # avatar GRANDE na capa (x, y, w, h; mesma proporção da caixa pequena); encolhe para AVX/AVY na etapa 2


def carregar(pasta):
    global ESTILO, LAY, HEAD_Y, LEG_Y, CARD, AV_CAPA
    r = rc.carregar(pasta)
    if len(r.get("etapas") or []) != 7:
        falha("roteiro", "o roteiro precisa de exatamente 7 etapas")
    if r.get("estilo"):
        ESTILO = r["estilo"].strip()
    if r.get("layout", "padrao") != "padrao":
        LAY = LAYOUTS[r["layout"]]
        HEAD_Y, LEG_Y, CARD = LAY["head_y"], LAY["leg_y"], LAY["card"]
    AV_CAPA = (r["etapas"][0].get("capa") or {}).get("avatar", True) is not False
    return r


# ======================================================================= imagens
def _arq_img(r, i, e):
    return r["_dir"] / "img" / f"{i + 1}-{e['id']}.png"


def _prompt(e, i=None):
    luz = f" Luz desta etapa: {e.get('luz') or LUZ[i]}." if i is not None and not e.get("cor_livre") else ""
    return f"Cena: {e['cena'].strip()}\n\nEstilo: {ESTILO}{luz}"


def _amarelo(im):
    r, g, b = ImageStat.Stat(im.convert("RGB").resize((256, 256))).mean
    return (r + g) / 2 - b


def neutralizar(a):
    """tira o amarelado do gerador (puxa os canais para o cinza até o alvo, sem zerar o calor da pele); devolve (antes, depois)"""
    im = Image.open(a).convert("RGB"); antes = _amarelo(im)
    if antes <= AMARELO_CORRIGE:
        return antes, antes
    r, g, b = ImageStat.Stat(im.resize((256, 256))).mean; cinza = (r + g + b) / 3
    for k in range(1, 21):
        gs = [(cinza / c) ** (k / 20) for c in (r, g, b)]
        out = Image.merge("RGB", [ch.point(lambda v, m=m: min(255, int(v * m + .5))) for ch, m in zip(im.split(), gs)])
        if _amarelo(out) <= AMARELO_ALVO:
            break
    out.save(a); return antes, _amarelo(out)


def _codex(r, i, e):
    dst = _arq_img(r, i, e); rel = dst.relative_to(r["_dir"])
    dst.unlink(missing_ok=True)
    pedido = (f"Use sua ferramenta de geração de imagem (image_gen) para criar UMA imagem no maior formato VERTICAL (retrato) "
              f"disponível e salve o PNG em {rel} dentro deste diretório. Não edite nenhum outro arquivo.\n\n{_prompt(e, i)}")
    lg = r["_b"] / f"codex-{i + 1}.log"
    with open(lg, "w") as f:
        try:
            subprocess.run(["codex", "exec", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox"], input=pedido,
                           text=True, cwd=r["_dir"], stdout=f, stderr=subprocess.STDOUT, timeout=600)
        except subprocess.TimeoutExpired:
            pass
    if dst.exists() and dst.stat().st_size > 50_000:
        return "codex"
    req = urllib.request.Request(FLUX_API, headers={"content-type": "application/json"}, data=json.dumps(
        {"model": "flux2-klein", "prompt": "cinematic photograph, no text, " + e["cena"], "width": 768, "height": 1344,
         "steps": 4, "seed": 7 + i}).encode())
    with urllib.request.urlopen(req, timeout=1800) as resp:
        dst.write_bytes(base64.b64decode(json.loads(resp.read())["image"]))
    return "flux2-klein (reserva)"


def _dhash(im):
    g = im.convert("L").resize((9, 8), Image.LANCZOS); px = list(g.getdata())
    return sum(1 << k for k in range(64) if px[(k // 8) * 9 + k % 8] > px[(k // 8) * 9 + k % 8 + 1])


def portao_imagens(r):
    """retrato, centro claro o bastante e nenhuma imagem parecida com outra; devolve a lista de etapas reprovadas"""
    ruins, hs = {}, []
    for i, e in enumerate(r["etapas"]):
        a = _arq_img(r, i, e)
        if not a.exists():
            ruins[i] = "não existe"; hs.append(None); continue
        im = Image.open(a).convert("RGB")
        if im.height / im.width < 1.3:
            ruins[i] = f"não é vertical ({im.width}x{im.height})"
        w, h = im.size
        lum = ImageStat.Stat(im.crop((int(w * .2), int(h * .2), int(w * .8), int(h * .8))).convert("L")).mean[0]
        if lum < e.get("luz_min", 55):
            ruins[i] = f"escura demais (luz {lum:.0f}/255)"
        if not e.get("cor_livre") and _amarelo(im) > AMARELO_MAX:
            ruins[i] = f"amarelada demais ({_amarelo(im):.0f} > {AMARELO_MAX:.0f})"
        hs.append(_dhash(im))
    for i in range(7):
        for j in range(i + 1, 7):
            if hs[i] is not None and hs[j] is not None and bin(hs[i] ^ hs[j]).count("1") < 12:
                ruins.setdefault(j, f"parecida demais com a etapa {i + 1}")
    return ruins


def cmd_imagens(pasta, refazer=()):
    r = carregar(pasta); (r["_dir"] / "img").mkdir(exist_ok=True)
    reg_f = r["_b"] / "imagens.json"
    reg = json.loads(reg_f.read_text()) if reg_f.exists() else {}
    falta = []
    for i, e in enumerate(r["etapas"]):
        h = hashlib.md5(_prompt(e, i).encode()).hexdigest()[:10]
        if i in refazer or not _arq_img(r, i, e).exists() or reg.get(str(i + 1), {}).get("hash") != h:
            falta.append((i, e, h))
    for tentativa in range(3):
        if falta:
            log(f"gerando {len(falta)} imagem(ns) no Codex: {', '.join(str(i + 1) for i, _, _ in falta)}")
            with cf.ThreadPoolExecutor(7) as ex:
                for (i, e, h), g in zip(falta, ex.map(lambda x: _codex(r, x[0], x[1]), falta)):
                    reg[str(i + 1)] = {"hash": h, "gerador": g}; log(f"  {i + 1} {e['id']}: {g}")
            reg_f.write_text(json.dumps(reg, ensure_ascii=False, indent=1))
        cmd_cor(pasta, r)
        ruins = portao_imagens(r)
        if not ruins:
            log("portão das imagens: OK (vertical, clara, cor neutra, sem repetição)"); return
        for i, m in ruins.items():
            log(f"  etapa {i + 1}: {m}")
        falta = [(i, r["etapas"][i], reg.get(str(i + 1), {}).get("hash", "")) for i in ruins]
    falha("imagens", "; ".join(f"{i + 1}: {m}" for i, m in ruins.items()))


# ======================================================================= tempos e legenda
class Linha:
    def __init__(self, r, pal, dur_av):
        self.pal = pal
        def em(palavra, depois):
            alvo = rc.slug(palavra).replace("-", " ")
            for p in pal:
                if p["t"] >= depois and (alvo in rc.slug(p["w"]).replace("-", " ") or alvo in " ".join(rc.cs.norm(p["w"]))):
                    return p["t"]
            falha("ancoras", f"âncora '{palavra}' não achada na fala depois de {depois:.1f} s")
        self.ini, t = [0.0], 0.0
        for e in r["etapas"][1:]:
            t = em(e["ancora"], t + 0.01); self.ini.append(t)
        cta = r.get("cta") or {}
        self.cta = em(cta["ancora"], t + 0.01) if cta.get("ancora") else None
        self.fim = pal[-1]["f"]
        self.total = max(dur_av, self.fim) + FIM_EXTRA
        for a, b in zip(self.ini, self.ini[1:]):
            if b - a < 0.5:
                falha("ancoras", f"duas etapas a menos de 0,5 s ({a:.1f} e {b:.1f})")

    def etapa(self, t):
        return max(i for i, s in enumerate(self.ini) if t >= s)

    def fim_etapa(self, i):
        return self.ini[i + 1] if i + 1 < len(self.ini) else self.total

    def resumo(self):
        return " · ".join(f"{i + 1}:{s:.1f}" for i, s in enumerate(self.ini)) + f" · cta {self.cta or 0:.1f} · fim {self.fim:.1f} · total {self.total:.1f}"


LEG_TAM = 66                                  # fonte de desenho da legenda (≥ LEG_MIN)


def cabe_legenda(ws):
    s = " ".join(w.strip() for w in ws).upper()
    return len(s) <= MAX_CAR and fnt(MBLK, LEG_TAM).getlength(s) <= SAFE[2] - SAFE[0] - 30


def blocos_legenda(pal, desde):
    """≤ 3 palavras e cabendo na largura; dentro de cada frase escolhe os cortes de menor custo
    (bloco de 1 palavra e bloco terminando em palavra fraca custam mais)"""
    def fraca(w):
        return re.sub(r"[^\wÀ-ÿ]", "", w.lower()) in FRACAS
    ps = []
    for p in pal:
        if p["t"] < desde - 0.05:
            continue
        w = p["w"].strip()
        if ps and (w.startswith(".") or not re.search(r"[\wÀ-ÿ]", w)):   # ".club", "!" soltos colam na anterior
            ps[-1] = dict(ps[-1], w=ps[-1]["w"].strip() + w, f=p["f"])
        else:
            ps.append(dict(p, w=w))
    frases, cur = [], []
    for p in ps:
        cur.append(p)
        if re.search(r"[.,!?:;]$", p["w"].strip()):
            frases.append(cur); cur = []
    if cur:
        frases.append(cur)
    out = []
    for fr in frases:
        n = len(fr); best = [0.0] + [math.inf] * n; corte = [0] * (n + 1)
        for j in range(1, n + 1):
            for i in range(max(0, j - MAX_PAL), j):
                ws = [x["w"] for x in fr[i:j]]
                if not cabe_legenda(ws) and j - i > 1:
                    continue
                c = best[i] + 1 + (2.5 if j - i == 1 and n > 1 else 0) + (3 if fraca(ws[-1]) and j < n else 0)
                if c < best[j]:
                    best[j], corte[j] = c, i
        j, partes = n, []
        while j > 0:
            partes.insert(0, fr[corte[j]:j]); j = corte[j]
        out += partes
    return out


def srt(blocos, arq):
    def ts(s):
        ms = int(round(s * 1000))                 # arredonda antes de separar (3,9999… viraria 03,000)
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    linhas = []
    for k, b in enumerate(blocos):
        fim = max(b[-1]["f"] + 0.25, b[0]["t"] + 0.3)
        if k + 1 < len(blocos):
            fim = min(fim, blocos[k + 1][0]["t"] - 0.02)      # nunca invade o bloco seguinte
        linhas += [str(k + 1), f"{ts(b[0]['t'])} --> {ts(fim)}", " ".join(p["w"].strip() for p in b).upper(), ""]
    Path(arq).write_text("\n".join(linhas))


# ======================================================================= fundo com câmera
class Fundo:
    """cada etapa: movimento de câmera contínuo + cortes de reenquadramento a cada ≤ 3,3 s; troca de etapa com fade e punch"""

    def __init__(self, r, L):
        self.r, self.L = r, L
        self.ims = [Image.open(_arq_img(r, i, e)).convert("RGB") for i, e in enumerate(r["etapas"])]
        self.grad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(self.grad)
        for y in range(700):
            d.line((0, y, W, y), fill=(0, 0, 0, int(205 * (1 - y / 700) ** 1.3)))
        for y in range(900, H):
            d.line((0, y, W, y), fill=(0, 0, 0, int(225 * min(1, (y - 900) / 520) ** 1.2)))
        self.planos = [self._planos(i) for i in range(7)]

    def _planos(self, i):
        ini, fim = self.L.ini[i], self.L.fim_etapa(i)
        n = max(1, math.ceil((fim - ini) / MUDA_MAX))
        return [(ini + (fim - ini) * k / n, ini + (fim - ini) * (k + 1) / n, k) for k in range(n)]

    def _janela(self, i, t):
        e = self.r["etapas"][i]; im = self.ims[i]
        cam = e.get("camera", ["push", "pull", "pan_dir", "push", "sobe", "pan_esq", "push"][i])
        fx, fy = e.get("foco", [0.5, 0.45])
        for a, b, k in self.planos[i]:
            if a <= t < b or (k == len(self.planos[i]) - 1 and t >= a):
                break
        p = ease((t - a) / max(0.1, b - a)) if b > a else 0
        if k % 2 == 1:                       # plano fechado no foco (corte de reenquadramento)
            z = 1.38 + 0.06 * p; cx, cy = fx, fy
        else:
            z, cx, cy = {"push": (1.0 + 0.12 * p, .5, .5), "pull": (1.12 - 0.12 * p, .5, .5),
                         "pan_dir": (1.16, .42 + .16 * p, .5), "pan_esq": (1.16, .58 - .16 * p, .5),
                         "sobe": (1.16, .5, .58 - .16 * p)}.get(cam, (1.0 + 0.12 * p, .5, .5))
        if i > 0 and t - self.L.ini[i] < 0.5:  # punch na entrada da etapa
            z *= 1 + 0.06 * (1 - ease((t - self.L.ini[i]) / 0.5))
        return im, z, cx, cy

    @staticmethod
    def _render(im, z, cx, cy, tam=(W, H)):
        w, h = tam
        k = max(w / im.width, h / im.height) * z
        ww, hh = w / k, h / k
        x0 = min(max(0, cx * im.width - ww / 2), im.width - ww); y0 = min(max(0, cy * im.height - hh / 2), im.height - hh)
        return im.transform((w, h), Image.AFFINE, (1 / k, 0, x0, 0, 1 / k, y0), resample=Image.BICUBIC)

    def _tela(self, i, t):
        """quadro da etapa i: tela cheia (padrão e capa) ou a imagem dentro da caixa do layout, com degradê próprio"""
        if LAY is None or LAY["img"] is None or i == 0:
            im = self._render(*self._janela(i, t)).convert("RGBA"); im.alpha_composite(self.grad); return im
        x, y, w, h = LAY["img"]
        if not hasattr(self, "grad_box"):
            g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
            for yy in range(min(h, 480)):
                d.line((0, yy, w, yy), fill=(0, 0, 0, int(200 * (1 - yy / 480) ** 1.3)))
            for yy in range(max(0, h - 360), h):
                d.line((0, yy, w, yy), fill=(0, 0, 0, int(215 * ((yy - (h - 360)) / 360) ** 1.2)))
            self.grad_box = g
        tela = Image.new("RGBA", (W, H), (8, 10, 14, 255))
        im = self._render(*self._janela(i, t), tam=(w, h)).convert("RGBA"); im.alpha_composite(self.grad_box)
        tela.paste(im, (x, y)); return tela

    def quadro(self, t):
        i = self.L.etapa(t)
        im = self._tela(i, t)
        if i > 0 and t - self.L.ini[i] < XF:
            im = Image.blend(self._tela(i - 1, t), im, ease((t - self.L.ini[i]) / XF))
        return im

    def cortes(self):
        return sorted({round(a, 2) for pl in self.planos for a, _, _ in pl})


# ======================================================================= camada de texto
def _alt_linha(s, fonte, tam_max, larg):
    """altura que Desenho.linha vai usar para s (mesmo encolhimento de fonte)"""
    tam = tam_max
    while tam > 40 and fnt(fonte, tam).getlength(s) > larg:
        tam -= 2
    f = fnt(fonte, tam); return f.getbbox("Ág")[3] - f.getbbox("Ág")[1]


class Desenho:
    def __init__(self, r, L, blocos):
        self.r, self.L, self.blocos = r, L, blocos
        self.cache = {}
        self.caixas = []        # (t, nome, bbox, fonte) — para o portão da zona segura
        self._t = None

    def _reg(self, _t, nome, bb, tam=None):
        """guarda a caixa do que foi desenhado (só nos quadros de validação: self._t != None)"""
        if self._t is not None:
            self.caixas.append((round(self._t, 2), nome, tuple(int(v) for v in bb), tam))

    def palavra(self, s, fonte, tam, rgb):
        """imagem da palavra com sombra suave (em cache)"""
        ch = (s, fonte, tam, rgb)
        if ch not in self.cache:
            f = fnt(fonte, tam); bb = f.getbbox(s); pad = 24
            w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
            sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((pad - bb[0] + 3, pad - bb[1] + 5), s, font=f, fill=(0, 0, 0, 230))
            sh = sh.filter(ImageFilter.GaussianBlur(7))
            ImageDraw.Draw(sh).text((pad - bb[0], pad - bb[1]), s, font=f, fill=rgb + (255,))
            self.cache[ch] = (sh, pad, bb)
        return self.cache[ch]

    def linha(self, base, t, t0, x, y, s, fonte, tam_max, rgb, larg, nome, anim=True, centro=False):
        """desenha uma linha com palavras que entram em sequência (escala + fade); devolve a altura usada"""
        tam = tam_max
        while tam > 40 and fnt(fonte, tam).getlength(s) > larg:
            tam -= 2
        f = fnt(fonte, tam); esp = f.getlength(" ")
        ws = s.split(); larg_tot = sum(f.getlength(w) for w in ws) + esp * (len(ws) - 1)
        xx = x - larg_tot / 2 if centro else x
        asc = f.getbbox("ÁÇ")[1]; desc_alt = f.getbbox("Ág")[3] - asc
        self._reg(t, nome, (xx, y + asc, xx + larg_tot, y + asc + desc_alt), tam)
        for k, w in enumerate(ws):
            img, pad, bb = self.palavra(w, fonte, tam, rgb)
            p = 1.0 if not anim else ease((t - t0 - 0.07 * k) / 0.28)
            if p > 0:
                sc = 1 + 0.3 * (1 - p)
                im = img if sc == 1 else img.resize((int(img.width * sc), int(img.height * sc)), Image.BILINEAR)
                if p < 1:
                    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v, p=p: int(v * p)))
                cxw = xx + f.getlength(w) / 2
                base.alpha_composite(im, (int(cxw - im.width / 2 + (bb[0] - pad) * 0), int(y + bb[1] - pad - (im.height - img.height) / 2)))
            xx += f.getlength(w) + esp
        return f.getbbox("Ág")[3] - f.getbbox("Ág")[1]

    def chip(self, base, d, t, t0, x, y, s, nome, centro=False, rgb_fundo=AMB, rgb_txt=ESC, tam=58):
        f = fnt(MBLK, tam)
        while f.getlength(s) > (SAFE[2] - SAFE[0]) - 70:
            tam -= 2; f = fnt(MBLK, tam)
        lw = f.getlength(s); p = ease((t - t0) / 0.35)
        if p <= 0:
            return
        x0 = x - lw / 2 - 30 if centro else x
        bb = (x0, y, x0 + lw + 60, y + tam + 40)
        self._reg(t, nome, bb, tam)
        a = int(255 * p)
        d.rounded_rectangle(bb, 20, fill=rgb_fundo + (a,))
        d.text(((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2), s, font=f, fill=rgb_txt + (a,), anchor="mm")

    def ganho(self, d, s):
        """quadro 0: faixa no topo com o que a pessoa ganha (pedido do Nei 12/10); até 2 linhas, fixa (sem animar)"""
        larg = SAFE[2] - SAFE[0] - 70; tam = 104
        linhas = [s]
        while tam > HEAD_MIN and fnt(ANTON, tam).getlength(s) > larg:
            tam -= 2
        if fnt(ANTON, tam).getlength(s) > larg and " " in s:
            tam = 104; ws = s.split()
            k = min(range(1, len(ws)), key=lambda k: max(fnt(ANTON, tam).getlength(" ".join(ws[:k])), fnt(ANTON, tam).getlength(" ".join(ws[k:]))))
            linhas = [" ".join(ws[:k]), " ".join(ws[k:])]
            while tam > HEAD_MIN and max(fnt(ANTON, tam).getlength(l) for l in linhas) > larg:
                tam -= 2
        if max(fnt(ANTON, tam).getlength(l) for l in linhas) > larg and len(s.split()) > 2:   # frase longa do Nei: 3 linhas
            tam = 104; ws = s.split(); fl = fnt(ANTON, tam).getlength
            a, b = min(((a, b) for a in range(1, len(ws) - 1) for b in range(a + 1, len(ws))),
                       key=lambda ab: max(fl(" ".join(ws[:ab[0]])), fl(" ".join(ws[ab[0]:ab[1]])), fl(" ".join(ws[ab[1]:]))))
            linhas = [" ".join(ws[:a]), " ".join(ws[a:b]), " ".join(ws[b:])]
            while tam > HEAD_MIN and max(fnt(ANTON, tam).getlength(l) for l in linhas) > larg:
                tam -= 2
        f = fnt(ANTON, tam); alt = int(tam * 1.12)
        y0 = HEAD_Y + 4; y1 = y0 + 36 + alt * len(linhas)
        d.rounded_rectangle((SAFE[0], y0, SAFE[2], y1), 26, fill=AMB + (245,))
        y = y0 + 18
        for ln in linhas:
            cx = (SAFE[0] + SAFE[2]) / 2
            bb = d.textbbox((cx, y), ln, font=f, anchor="ma")
            self._reg(0.0 if self._t is not None else None, "ganho", bb, tam)
            d.text((cx, y), ln, font=f, fill=ESC + (255,), anchor="ma"); y += alt
        return y1

    def manchete(self, base, d, t, e, t0, capa=False):
        if capa:
            c = e["capa"]; y = c.get("y", 880); cx = (SAFE[0] + SAFE[2]) / 2   # texto embaixo, cena visível
            topo = self.ganho(d, c["ganho"]) if c.get("ganho") else HEAD_Y + 40
            tam, tc = 172, 60
            if AV_CAPA:                        # avatar grande no quadro 0: o texto encolhe e fica entre o ganho e o avatar
                larg = SAFE[2] - SAFE[0] - 30; vao = AVC[1] - 24 - (topo + 24)
                def altura(tm):
                    k = max(40, int(60 * tm / 172))
                    while c.get("sub") and fnt(MBLK, k).getlength(c["sub"]) > (SAFE[2] - SAFE[0]) - 70:
                        k -= 2
                    h = sum(_alt_linha(c[n], ANTON, tm, larg) for n in ("linha1", "linha2")) + 16
                    return h + (30 + k + 40 if c.get("sub") else 0), k
                while tam > 64 and altura(tam)[0] > vao:
                    tam -= 4
                alt, tc = altura(tam)
                y = topo + 24 + max(0, (vao - alt) / 2)
            h1 = self.linha(base, t, t0, cx, y, c["linha1"], ANTON, tam, BRANCO, SAFE[2] - SAFE[0] - 30, "capa1", anim=False, centro=True)
            y += h1 + 16
            h2 = self.linha(base, t, t0, cx, y, c["linha2"], ANTON, tam, AMB, SAFE[2] - SAFE[0] - 30, "capa2", anim=False, centro=True)
            if c.get("sub"):
                self.chip(base, d, t + 1, t0, cx, y + h2 + (30 if AV_CAPA else 46), c["sub"], "capa-sub", centro=True, tam=tc)
            return
        y = HEAD_Y
        h1 = self.linha(base, t, t0, SAFE[0], y, e["linha1"], ANTON, 128, BRANCO, SAFE[2] - SAFE[0], "manchete1")
        y += h1 + 14
        h2 = self.linha(base, t, t0 + 0.12, SAFE[0], y, e["linha2"], ANTON, 156, cor(e.get("cor")), SAFE[2] - SAFE[0], "manchete2")
        if e.get("chip"):
            self.chip(base, d, t, t0 + 0.45, SAFE[0], y + h2 + 30, e["chip"], "chip", rgb_fundo=cor(e.get("cor")), tam=50)

    def legenda(self, base, t):
        for k, b in enumerate(self.blocos):
            fim = self.blocos[k + 1][0]["t"] if k + 1 < len(self.blocos) else b[-1]["f"] + 0.35
            if b[0]["t"] - 0.05 <= t < min(fim, b[-1]["f"] + 0.6):
                ws = [p["w"].strip().upper() for p in b]
                tam = LEG_TAM + 8
                f = fnt(MBLK, tam)
                while tam > LEG_MIN and f.getlength(" ".join(ws)) > SAFE[2] - SAFE[0] - 30:
                    tam -= 2; f = fnt(MBLK, tam)
                esp = f.getlength(" "); tot = sum(f.getlength(w) for w in ws) + esp * (len(ws) - 1)
                xx = (SAFE[0] + SAFE[2]) / 2 - tot / 2
                asc = f.getbbox("ÁÇ")[1]; alt = f.getbbox("Ág")[3] - asc
                y = LEG_Y - alt / 2 - asc
                self._reg(t, "legenda", (xx, y + asc, xx + tot, y + asc + alt), tam)
                fundo = Image.new("RGBA", (int(tot + 56), int(alt + 34)), (0, 0, 0, 0))
                ImageDraw.Draw(fundo).rounded_rectangle((0, 0, fundo.width - 1, fundo.height - 1), 22, fill=(8, 10, 14, 150))
                base.alpha_composite(fundo, (int(xx - 28), int(y + asc - 17)))   # contraste sobre qualquer fundo
                for w, p in zip(ws, b):
                    img, pad, bb = self.palavra(w, MBLK, tam, AMB if p["t"] <= t else BRANCO)
                    base.alpha_composite(img, (int(xx + bb[0] - pad), int(y + bb[1] - pad)))
                    xx += f.getlength(w) + esp
                return

    def _texto_card(self, d, x, y, s, fonte, tmax, tmin, larg, rgb, a, nome, dx=0):
        """escreve dentro do cartão: reduz até tmin; se ainda não couber, quebra em duas linhas; registra cada linha"""
        tam = tmax
        while tam > tmin and fnt(fonte, tam).getlength(s) > larg:
            tam -= 2
        linhas = [s]
        if fnt(fonte, tam).getlength(s) > larg and " " in s:
            ws = s.split(); melhor = None
            for k in range(1, len(ws)):
                a1, a2 = " ".join(ws[:k]), " ".join(ws[k:])
                m = max(fnt(fonte, tam).getlength(a1), fnt(fonte, tam).getlength(a2))
                if melhor is None or m < melhor[0]:
                    melhor = (m, [a1, a2])
            linhas = melhor[1]
        f = fnt(fonte, tam)
        for ln in linhas:
            bb = d.textbbox((x, y), ln, font=f)
            self._reg(None, "card:" + nome, (bb[0] - dx, bb[1], bb[2] - dx, bb[3]), tam)   # posição final (sem o deslize)
            d.text((x, y), ln, font=f, fill=rgb + (a,)); y += int(tam * 1.18)
        return y

    def cartao(self, base, d, t, t0, dados, nome):
        """destaque à direita do avatar: título grande + texto curto (entra deslizando)"""
        p = ease((t - t0) / 0.4)
        if p <= 0:
            return
        x0, y0, x1, y1 = CARD; dx = int((1 - p) * 80); a = int(235 * p)
        d.rounded_rectangle((x0 + dx, y0, x1 - 5 + dx, y1), 26, fill=ESC + (int(a * 0.88),))
        d.rectangle((x0 + dx, y0 + 26, x0 + 8 + dx, y1 - 26), fill=cor(dados.get("cor")) + (a,))
        self._reg(t, nome, (x0, y0, x1 - 5, y1))
        larg = x1 - x0 - 85; x = x0 + 40 + dx
        y = self._texto_card(d, x, y0 + 36, dados.get("titulo", ""), ANTON, 120, 64, larg, cor(dados.get("cor"), AMB), a, nome, dx) + 12
        for ln in dados.get("texto", "").split("\n"):
            y = self._texto_card(d, x, y, ln, MXB, 48, 38, larg, BRANCO, a, nome, dx)

    def cta(self, base, d, t, t0):
        c = self.r["cta"]; p = ease((t - t0) / 0.4)
        if p <= 0:
            return
        x0, y0, x1, y1 = CARD; a = int(255 * p)
        d.rounded_rectangle((x0, y0, x1 - 5, y1), 26, fill=AMB + (int(a * 0.96),))
        self._reg(t, "cta", (x0, y0, x1 - 5, y1))
        larg = x1 - x0 - 75; x = x0 + 36
        y = self._texto_card(d, x, y0 + 30, c.get("linha1", "ou comenta"), MBLK, 54, 40, larg - 150, ESC, a, "cta")
        y = self._texto_card(d, x, y, c["palavra"], ANTON, 140, 70, larg, ESC, a, "cta")
        y = self._texto_card(d, x, y + 4, c.get("linha2", "que eu te mando o link"), MXB, 42, 36, larg, ESC, a, "cta")
        # balão de comentário + seta pulsando para a coluna de botões, no canto de cima (ao lado do "ou comenta")
        bx, by = x1 - 150, y0 + 30; vai = 9 * math.sin(t * 7)
        d.rounded_rectangle((bx, by, bx + 62, by + 46), 13, outline=ESC + (a,), width=6)
        d.polygon([(bx + 13, by + 44), (bx + 30, by + 44), (bx + 9, by + 61)], fill=ESC + (a,))
        d.polygon([(bx + 76 + vai, by + 9), (bx + 110 + vai, by + 23), (bx + 76 + vai, by + 37)], fill=ESC + (a,))

    def quadro(self, t, legenda=True, registrar=False):
        L, r = self.L, self.r
        self._t = t if registrar else None
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        i = L.etapa(t); e = r["etapas"][i]
        f = fnt(MXB, 30)
        d.text((SAFE[0], SAFE[1] + 4), "INEMA.CLUB", font=f, fill=BRANCO + (220,))
        self._reg(t, "marca", (SAFE[0], SAFE[1] + 4, SAFE[0] + f.getlength("INEMA.CLUB"), SAFE[1] + 36))
        if LAY is not None and LAY["forma"] == "circulo" and i > 0:      # aro dourado do avatar redondo
            ax, ay, aw, ah = LAY["av"]
            d.ellipse((ax - 10, ay - 10, ax + aw + 10, ay + ah + 10), fill=AMB + (255,))
        tt = t
        if i == 0:
            self.manchete(im, d, tt, e, 0.0, capa=True)
        else:
            self.manchete(im, d, tt, e, L.ini[i])
            if L.cta is not None and i == 6 and t >= L.cta:
                self.cta(im, d, t, L.cta)
            elif e.get("destaque"):
                self.cartao(im, d, t, L.ini[i] + 0.3, e["destaque"], "destaque")
            if legenda and t < L.fim + 0.4:
                self.legenda(im, t)
        return im


def quadro_completo(F, D, t, legenda=True, registrar=False):
    im = F.quadro(t); im.alpha_composite(D.quadro(t, legenda, registrar)); return im


# ======================================================================= montagem
def preparar(r):
    pal = rc.palavras_reais(r)
    sem = rc.semelhanca(r["fala"], pal); log(f"fala do avatar × roteiro: {sem:.0%}")
    if sem < 0.85:
        falha("fala", f"a fala ouvida diverge do roteiro ({sem:.0%} < 85%)")
    L = Linha(r, pal, dur(r["_av"]))
    blocos = blocos_legenda(pal, L.ini[1])
    return pal, L, blocos


def portao_desenho(D):
    erros = []
    for t, nome, (x0, y0, x1, y1), tam in D.caixas:
        if AV_CAPA and t < D.L.ini[1] and x1 > AVC[0] and x0 < AVC[0] + AVC[2] and y1 > AVC[1] and y0 < AVC[1] + AVC[3]:
            erros.append(f"{t:.1f}s {nome} da capa cobre o avatar {(x0, y0, x1, y1)}")
        if x0 < SAFE[0] - 1 or y0 < SAFE[1] - 1 or x1 > SAFE[2] + 1 or y1 > SAFE[3] + 1:
            erros.append(f"{t:.1f}s {nome} fora da zona segura {(x0, y0, x1, y1)}")
        if nome.startswith("card:") and (x0 < CARD[0] or x1 > CARD[2] - 25 or y0 < CARD[1] or y1 > CARD[3] - 10):
            erros.append(f"{t:.1f}s texto de {nome[5:]} fora do cartão {(x0, y0, x1, y1)}")
        if tam is not None and nome == "legenda" and tam < LEG_MIN:
            erros.append(f"{t:.1f}s legenda com fonte {tam}px < {LEG_MIN}")
        if tam is not None and nome.startswith("manchete") and tam < HEAD_MIN:
            erros.append(f"{t:.1f}s {nome} com fonte {tam}px < {HEAD_MIN}")
    return sorted(set(erros))


def trilha(r):
    m = r.get("musica")
    if m:
        return Path(m) if Path(m).is_absolute() else r["_dir"] / m
    t = r["_b"] / "trilha.wav"
    return t if t.exists() else rc.CFG["musica_reserva"]


def loudnorm(entrada, saida, alvo=-14.0):
    """loudnorm em duas passadas (mede e aplica) — cai dentro de −14 ±1 LUFS"""
    med = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(entrada), "-af", f"loudnorm=I={alvo}:TP=-1.5:LRA=11:print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(med[med.rindex("{"):med.rindex("}") + 1])
    af = (f"loudnorm=I={alvo}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
          f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    run(["ffmpeg", "-v", "error", "-y", "-i", entrada, "-af", af, "-ar", "48000", saida])


def cmd_montar(pasta):
    r = carregar(pasta); B = r["_b"]
    if portao_imagens(r):
        falha("imagens", "rode 'imagens' antes (alguma etapa reprovada)")
    pal, L, blocos = preparar(r)
    log(L.resumo())
    srt(blocos, B / "legendas.srt")
    F = Fundo(r, L); D = Desenho(r, L, blocos)
    n = int(L.total * FPS); base = B / "base.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", str(base)], stdin=subprocess.PIPE)
    for k in range(n):
        t = k / FPS
        enc.stdin.write(quadro_completo(F, D, t, registrar=(k % 5 == 0)).convert("RGB").tobytes())
        if k % 300 == 0:
            log(f"quadro {k}/{n}")
    enc.stdin.close(); enc.wait()
    erros = portao_desenho(D)
    (B / "portao_desenho.txt").write_text("\n".join(erros) or "OK")
    if erros:
        falha("zona-segura/fonte", f"{len(erros)} problema(s), primeiro: {erros[0]} (lista em build/portao_desenho.txt)")
    log("portão zona segura + fonte mínima: OK")
    # áudio: voz + trilha com ducking → −14 LUFS
    mix = B / "mix.wav"; vol = r.get("volume_musica", 0.18)
    run(["ffmpeg", "-v", "error", "-y", "-i", r["_av"], "-stream_loop", "-1", "-i", trilha(r), "-filter_complex",
         f"[0:a]aresample=48000,apad,atrim=0:{L.total:.3f},asplit=2[voz][sc];[1:a]volume={vol},aresample=48000[mu];"
         f"[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300[md];"
         f"[voz][md]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={L.total - 1.2:.2f}:d=1.2[a]",
         "-map", "[a]", "-t", f"{L.total:.3f}", mix])
    loudnorm(mix, B / "mix_norm.wav")
    # avatar: já no quadro 0 (AV_CAPA, parado) ou entra subindo na etapa 2; fica até o fim (último quadro congelado)
    crop = rc.recorte_rosto(r); crop_capa = crop; i0 = L.ini[1]
    ax, ay, aw, ah = (AVX, AVY, AVW, AVH) if LAY is None else LAY["av"]
    if LAY is not None:                     # recorte na proporção da caixa do layout, centrado no rosto achado
        cw0, ch0, x00 = (int(v) for v in crop.split(":")[:3]); centro = x00 + cw0 / 2
        vw, vh = (int(v) for v in subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                            "-of", "csv=p=0", str(r["_av"])], text=True).strip().split(","))
        ch = vh; cw = int(round(ch * aw / ah))
        if cw > vw:
            cw = vw; ch = int(round(vw * ah / aw))
        crop = f"{cw}:{ch}:{int(max(0, min(vw - cw, centro - cw / 2)))}:0"
    tag = B / "tag.txt"; tag.write_text(r.get("tag", "NEI MALDANER  |  INEMA"))
    yexp = f"if(lt(t,{i0 + 0.35:.2f}),{ay}+(1-(t-{i0:.2f})/0.35)*140,{ay})" if (LAY is None or LAY["forma"] == "ret") else str(ay)
    en = f"gte(t,{i0:.2f})"
    if LAY is not None and LAY["forma"] == "circulo":
        mask = B / "mascara.png"; mk = Image.new("L", (aw, ah), 0); ImageDraw.Draw(mk).ellipse((0, 0, aw - 1, ah - 1), fill=255); mk.save(mask)
        moldura = f"format=rgba[avr];movie={mask},format=gray,scale={aw}:{ah}[mk];[avr][mk]alphamerge[av];"
    else:
        moldura = (f"drawbox=x=0:y=0:w=iw:h=ih:color=0xE2A23B@1:t=6,"
                   f"drawbox=x=6:y={ah - 44}:w={aw - 12}:h=38:color=0x0b0f14@0.85:t=fill,"
                   f"drawtext=fontfile={DEJAVU}:textfile={tag}:x=18:y={ah - 34}:fontsize=19:fontcolor=white[av];")
    fc = (f"[1:v]trim=start={i0:.3f},setpts=PTS-STARTPTS+{i0:.3f}/TB,crop={crop},scale={aw}:{ah},setsar=1,fps={FPS},"
          f"tpad=stop_mode=clone:stop_duration=10,{moldura}"
          f"[0:v][av]overlay=x={ax}:y='{yexp}':enable='{en}':eof_action=repeat,format=yuv420p[v]")
    if AV_CAPA:                          # capa: avatar GRANDE (AVC) até a etapa 2; daí a caixa normal entra subindo
        cx_, cy_, cw_, ch_ = AVC
        fc = fc.replace("[1:v]", "[a2]", 1).replace("[0:v][av]", "[cap][av]", 1)
        fc = (f"[1:v]split[a1][a2];[a1]crop={crop_capa},scale={cw_}:{ch_},setsar=1,fps={FPS},"
              f"drawbox=x=0:y=0:w=iw:h=ih:color=0xE2A23B@1:t=10,"
              f"drawbox=x=10:y={ch_ - 66}:w={cw_ - 20}:h=56:color=0x0b0f14@0.85:t=fill,"
              f"drawtext=fontfile={DEJAVU}:textfile={tag}:x=30:y={ch_ - 52}:fontsize=30:fontcolor=white[avc];"
              f"[0:v][avc]overlay=x={cx_}:y={cy_}:enable='lt(t,{i0:.3f})'[cap];" + fc)
    saida = r["_dir"] / "video.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", base, "-i", r["_av"], "-i", B / "mix_norm.wav", "-filter_complex", fc,
         "-map", "[v]", "-map", "2:a", "-t", f"{L.total:.3f}", "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-r", str(FPS),
         "-maxrate", "8M", "-bufsize", "16M", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida])
    (B / "tempos.json").write_text(json.dumps({"ini": L.ini, "cta": L.cta, "fim": L.fim, "total": L.total, "cortes": F.cortes()}))
    log("vídeo", saida, f"{dur(saida):.1f} s", f"{saida.stat().st_size / 1e6:.1f} MB")
    return saida


# ======================================================================= validação final
def cmd_validar(pasta):
    r = carregar(pasta); B = r["_b"]; v = r["_dir"] / "video.mp4"
    tp = json.loads((B / "tempos.json").read_text())
    cortes = tp["cortes"] + [tp["total"]]
    maior = max(b - a for a, b in zip(cortes, cortes[1:]))
    if maior > 3.6:
        falha("ritmo", f"imagem parada por {maior:.1f} s (máx 3,5)")
    log(f"ritmo: maior trecho sem troca de imagem {maior:.1f} s")
    rel = B / "qa.json"
    qa = subprocess.run([sys.executable, str(QA_SHORT), str(v), "--profile", r.get("perfil_qa", "divulgacao"), "--srt", str(B / "legendas.srt"),
                         "--sheet", str(B / "qa.png"), "--report", str(rel)], capture_output=True, text=True)
    print(qa.stdout[-2500:])
    if qa.returncode != 0:
        falha("qa_short", "qa_short.py reprovou (veja acima e build/qa.json)")
    # folha de revisão em tamanho real: quadro 0, o meio de cada etapa, o CTA e o fim
    ts = [0.0] + [a + min(1.4, (b - a) * 0.6) for a, b in zip(tp["ini"][1:], tp["ini"][2:] + [tp["fim"]])]
    if tp.get("cta"):
        ts.append(tp["cta"] + 1.0)
    ts.append(tp["total"] - 0.4)
    pasta_rev = B / "revisao"; shutil.rmtree(pasta_rev, ignore_errors=True); pasta_rev.mkdir()
    for k, t in enumerate(ts):
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", v, "-frames:v", "1", "-vf", "scale=540:960", pasta_rev / f"{k:02d}-{t:05.1f}s.jpg"])
    ims = sorted(pasta_rev.glob("*.jpg"))
    for parte in range(math.ceil(len(ims) / 4)):
        grupo = ims[parte * 4:parte * 4 + 4]
        folha = Image.new("RGB", (540 * len(grupo), 960), ESC)
        for j, a in enumerate(grupo):
            folha.paste(Image.open(a), (j * 540, 0))
        folha.save(pasta_rev / f"folha-{parte + 1}.jpg", quality=90)
    log("validar: OK — revise as folhas em", pasta_rev)


def cmd_mapa(pasta):
    """mapa.jpg: as 7 etapas lado a lado (quadro do vídeo + nome + gatilho + porquê) e capa.jpg"""
    r = carregar(pasta); v = r["_dir"] / "video.mp4"
    tp = json.loads((r["_b"] / "tempos.json").read_text())
    ini = tp["ini"] + [tp["fim"]]
    cw, chh = 420, 747
    pad, cab, rod = 30, 230, 300
    M = Image.new("RGB", (pad + 7 * (cw + pad), cab + chh + rod + pad), ESC); d = ImageDraw.Draw(M)
    d.text((pad, 40), "REEL EM 7 ETAPAS", font=fnt(ANTON, 96), fill=AMB)
    d.text((pad, 160), f"exemplo: {r.get('tema', '')}  ·  INEMA.CLUB", font=fnt(MXB, 40), fill=BRANCO)
    for k, e in enumerate(r["etapas"]):
        t = ini[k] + min(1.5, (ini[k + 1] - ini[k]) * 0.6) if k else 0.0
        if k == 6 and tp.get("cta"):
            t = tp["cta"] + 1.0
        q = r["_b"] / f"mapa{k}.png"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", v, "-frames:v", "1", "-vf", f"scale={cw}:{chh}", q])
        x = pad + k * (cw + pad)
        M.paste(Image.open(q).convert("RGB"), (x, cab))
        d.rounded_rectangle((x, cab - 8, x + 74, cab + 66), 14, fill=AMB)
        d.text((x + 37, cab + 29), str(k + 1), font=fnt(ANTON, 56), fill=ESC, anchor="mm")
        y = cab + chh + 20
        d.text((x, y), e["nome"], font=fnt(ANTON, 64), fill=AMB)
        d.text((x, y + 82), quebra(d, e.get("gatilho", ""), fnt(MXB, 28), cw), font=fnt(MXB, 28), fill=BRANCO, spacing=6)
        d.text((x, y + 170), quebra(d, e.get("por_que", ""), fnt(MXB, 22), cw), font=fnt(MXB, 22), fill=(170, 180, 190), spacing=5)
    M.save(r["_dir"] / "mapa.jpg", quality=90); log("mapa", r["_dir"] / "mapa.jpg")
    run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-i", v, "-frames:v", "1", "-q:v", "2", r["_dir"] / "capa.jpg"])
    log("capa", r["_dir"] / "capa.jpg")


def quebra(d, s, f, larg):
    linhas, atual = [], ""
    for w in s.split():
        c = (atual + " " + w).strip()
        if d.textlength(c, font=f) > larg and atual:
            linhas.append(atual); atual = w
        else:
            atual = c
    return "\n".join(linhas + ([atual] if atual else []))


# ======================================================================= entrega
def cmd_publicar(pasta):
    r = carregar(pasta); v = r["_dir"] / "video.mp4"
    if not (r["_b"] / "qa.json").exists() or (r["_b"] / "qa.json").stat().st_mtime < v.stat().st_mtime:
        falha("publicar", "rode 'validar' depois do último 'montar'")
    m = r["_dir"] / "mapa.jpg"
    if not m.exists() or m.stat().st_mtime < v.stat().st_mtime:   # 'fazer' parado num portão não chega ao mapa
        cmd_mapa(pasta)
    rc.cmd_enviar(pasta, r.get("legenda_envio"))
    ctx = (r.get("contexto_youtube") or f"Short vertical do INEMA.CLUB: {r.get('tema', '')}. Fala: {r['fala'].strip()}") + (
        " Material gratuito em https://inema.club. Na descrição, inclua: 'Este reel foi feito com o modelo reel7etapas "
        "(gancho, desejo, medo, facilidade, descoberta, benefício e comentário). Guia do modelo: "
        "https://inematds.github.io/reel7etapas/guia/'. Português do Brasil.")
    canal = r.get("canal", "lives1")
    seco = subprocess.run([str(YT_PUBX), "publicar", str(v), "--canal", canal, "--contexto", ctx, "--dry-run"],
                          cwd=YT_PUBX.parent, capture_output=True, text=True, timeout=900).stdout
    plano = re.search(r"PLANO: (\S+)", seco)
    if not plano:
        falha("youtube", "o dry-run do yt-pubx não devolveu o plano:\n" + seco[-800:])
    pub = subprocess.run([str(YT_PUBX), "publicar", str(v), "--canal", canal, "--plano", plano.group(1)],
                         cwd=YT_PUBX.parent, capture_output=True, text=True, timeout=900).stdout
    url = re.search(r"URL: (\S+)", pub)
    if not url:
        falha("youtube", pub[-800:])
    vid = url.group(1).rsplit("=", 1)[-1]
    with open(r["_dir"] / "roteiro.yaml", "a") as f:
        f.write(f"youtube_{date.today().isoformat().replace('-', '')}: https://www.youtube.com/shorts/{vid}\n")
    log("YouTube:", f"https://www.youtube.com/shorts/{vid}")


def cmd_novo(ident):
    pasta = RAIZ / "edicoes" / f"{date.today().isoformat()}-{rc.slug(ident)}"
    if (pasta / "roteiro.yaml").exists():
        sys.exit(f"já existe: {pasta / 'roteiro.yaml'}")
    (pasta / "avatar").mkdir(parents=True, exist_ok=True)
    txt = re.sub(r"(?m)^(youtube.*|# v1 .*)\n", "", EXEMPLO.read_text())
    (pasta / "roteiro.yaml").write_text(txt)
    log("criado", pasta / "roteiro.yaml", "— reescreva fala, âncoras, manchetes, destaques e cenas mantendo as 7 etapas")


def cmd_cor(pasta, r=None):
    """neutraliza o amarelado das imagens da edição (idempotente: só mexe acima de AMARELO_CORRIGE)"""
    r = r or carregar(pasta)
    for i, e in enumerate(r["etapas"]):
        a = _arq_img(r, i, e)
        if a.exists() and not e.get("cor_livre"):
            antes, depois = neutralizar(a)
            if depois < antes:
                log(f"  {i + 1} {e['id']}: cor neutralizada (amarelo {antes:.0f} → {depois:.0f})")


def cmd_fazer(pasta):
    r = carregar(pasta)
    cmd_imagens(pasta)
    if not r["_av"].exists():
        if not (r["_dir"] / "avatar/APROVADO_HEYGEN").exists():
            falha("avatar", "falta avatar/APROVADO_HEYGEN")
        rc.cmd_avatar(pasta)
    cmd_montar(pasta); cmd_validar(pasta); cmd_mapa(pasta)
    log("Terminei: reel pronto e validado —", r["_dir"] / "video.mp4")


def main(a):
    cmds = {"imagens": lambda p: cmd_imagens(p, tuple(int(x) - 1 for x in a[2:])), "avatar": rc.cmd_avatar, "montar": cmd_montar,
            "validar": cmd_validar, "mapa": cmd_mapa, "cor": cmd_cor, "publicar": cmd_publicar, "fazer": cmd_fazer}
    if len(a) < 2 or a[0] not in list(cmds) + ["novo", "enviar"]:
        sys.exit(__doc__)
    if a[0] == "novo":
        cmd_novo(a[1])
    elif a[0] == "enviar":
        rc.cmd_enviar(a[1], a[2] if len(a) > 2 else None)
    else:
        cmds[a[0]](a[1])


if __name__ == "__main__":
    main(sys.argv[1:])
