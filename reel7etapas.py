#!/usr/bin/env python3
"""reel7etapas — uma ideia vira um reel 9:16 em 7 etapas de gatilho:
gancho → desejo → medo → facilidade → descoberta → benefício → comentário.
Cada etapa entra numa palavra da fala do avatar do Nei e troca a imagem de fundo, a manchete e o painel.

  reel7etapas.py novo <slug>             cria edicoes/<data>-<slug>/roteiro.yaml a partir do exemplo
  reel7etapas.py imagens <pasta>         gera as 7 imagens de fundo (flux2-klein local, porta 8000)
  reel7etapas.py previa <pasta>          prévia com tempo estimado (antes do avatar)
  reel7etapas.py avatar <pasta>          fala no estúdio do HeyGen (exige avatar/APROVADO_HEYGEN) — usa o reelcomenta
  reel7etapas.py montar <pasta>          monta <pasta>/video.mp4
  reel7etapas.py conferir <pasta>        folha de quadros + volume
  reel7etapas.py mapa <pasta>            mapa.jpg (as 7 etapas com quadro, gatilho e porquê) + capa.jpg
  reel7etapas.py enviar <pasta> [texto]  manda o vídeo pelo bot do Telegram (v3)
"""
import base64, hashlib, json, math, os, shutil, subprocess, sys, urllib.request
from datetime import date
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFilter

HOME = Path.home()
RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(os.environ.get("R7_REELCOMENTA", HOME / "projetos/reelcomenta"))))
import reelcomenta as rc  # noqa: E402  (transcrição, recorte do rosto, fontes, estúdio HeyGen, envio)
from reelcomenta import W, H, FPS, ANTON, MBLK, MXB, AMB, VERM, BRANCO, ESC, AVX, AVY, AVW, AVH, DEJAVU, fnt, ease, borda, cor, caber, run, dur  # noqa: E402


def log(*a):
    print("[reel7etapas]", *a, flush=True)

IMAGEM_API = os.environ.get("R7_IMAGEM_API", "http://localhost:8000/generate")
IMAGEM_MODELO = os.environ.get("R7_IMAGEM_MODELO", "flux2-klein")
ESTILO = "cinematic photograph, dark moody scene, warm golden rim light, shallow depth of field, no text, no letters, no logos, "
XF = 0.35  # crossfade entre etapas (s)
EXEMPLO = RAIZ / "edicoes/2026-10-11-jarvis/roteiro.yaml"


def carregar(pasta):
    r = rc.carregar(pasta)
    if len(r.get("etapas") or []) != 7:
        sys.exit("o roteiro precisa de exatamente 7 etapas")
    return r


# ======================================================================= tempos
class Linha:
    """início de cada etapa (e da troca 'depois' da última), achado pelas âncoras na fala"""

    def __init__(self, r, pal, dur_av):
        self.pal = pal
        def em(palavra, depois):
            alvo = rc.slug(palavra).replace("-", " ")
            for p in pal:
                if p["t"] >= depois and (alvo in rc.slug(p["w"]).replace("-", " ") or alvo in " ".join(rc.cs.norm(p["w"]))):
                    return p["t"]
            sys.exit(f"âncora '{palavra}' não achada na fala depois de {depois:.1f} s")
        self.ini, t = [0.0], 0.0
        for e in r["etapas"][1:]:
            t = em(e["ancora"], t + 0.01); self.ini.append(t)
        dep = r["etapas"][-1].get("depois")
        self.depois = em(dep["ancora"], t + 0.01) if dep else None
        self.fim = pal[-1]["f"]
        self.total = max(dur_av, self.fim) + 1.8

    def etapa(self, t):
        return max(i for i, s in enumerate(self.ini) if t >= s)

    def resumo(self):
        return " · ".join(f"{i + 1}:{s:.1f}" for i, s in enumerate(self.ini)) + f" · fim {self.fim:.1f} · total {self.total:.1f}"


# ======================================================================= imagens
def imagens(r):
    pasta = r["_dir"] / "img"; pasta.mkdir(exist_ok=True)
    out = []
    for i, e in enumerate(r["etapas"]):
        prompt = ESTILO + e["cena"]
        seed = e.get("seed", 7 + i)
        dst = pasta / f"{i + 1}-{e['id']}-{hashlib.md5(f'{prompt}{seed}'.encode()).hexdigest()[:8]}.png"
        out.append(dst)
        if dst.exists():
            continue
        log(f"imagem {i + 1} {e['id']}")
        req = urllib.request.Request(IMAGEM_API, headers={"content-type": "application/json"},
                                     data=json.dumps({"model": IMAGEM_MODELO, "prompt": prompt, "width": 768, "height": 1344,
                                                      "steps": 4, "seed": seed}).encode())
        with urllib.request.urlopen(req, timeout=1800) as resp:
            dst.write_bytes(base64.b64decode(json.loads(resp.read())["image"]))
    return out


class Fundo:
    """imagem de cada etapa cobrindo 9:16 com zoom lento (subpixel) e crossfade na troca"""

    def __init__(self, arqs, L):
        self.L = L
        self.ims = []
        for a in arqs:
            im = Image.open(a).convert("RGB")
            k = max(W / im.width, H / im.height) * 1.12
            self.ims.append(im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS))
        self.grad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(self.grad)
        for y in range(560):
            d.line((0, y, W, y), fill=(0, 0, 0, int(200 * (1 - y / 560))))
        for y in range(1000, H):
            d.line((0, y, W, y), fill=(0, 0, 0, int(215 * min(1, (y - 1000) / 320))))

    def um(self, i, t):
        im = self.ims[i]
        ini = self.L.ini[i]; fim = self.L.ini[i + 1] if i + 1 < len(self.L.ini) else self.L.total
        p = max(0.0, min(1.0, (t - ini) / max(1.0, fim - ini + XF)))
        # janela de recorte (proporção 9:16), centrada, encolhendo com o tempo = aproxima devagar
        cw = im.width / 1.12 * (1.12 - 0.10 * p)
        ch = cw * H / W
        x0 = (im.width - cw) / 2; y0 = (im.height - ch) / 2 + (i % 2 * 2 - 1) * 12 * p
        return im.transform((W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), resample=Image.BILINEAR)

    def quadro(self, t):
        i = self.L.etapa(t)
        im = self.um(i, t)
        if i > 0 and t - self.L.ini[i] < XF:
            im = Image.blend(self.um(i - 1, t), im, ease((t - self.L.ini[i]) / XF))
        im = im.convert("RGBA"); im.alpha_composite(self.grad)
        return im


# ======================================================================= desenho
class Desenho:
    def __init__(self, r, L):
        self.r, self.L = r, L
        self.blocos = [L.pal[i:i + 3] for i in range(0, len(L.pal), 3)]

    def atual(self, t):
        i = self.L.etapa(t); e = dict(self.r["etapas"][i])
        if e.get("depois") and self.L.depois is not None and t >= self.L.depois:
            e.update(e["depois"])
        return i, e

    def capa(self, d, e, a=255):
        c = e["capa"]
        f1 = caber(d, c["linha1"], ANTON, 200, W - 80); f2 = caber(d, c["linha2"], ANTON, 200, W - 80)
        borda(d, (W / 2, 640), c["linha1"], f1, BRANCO + (a,), 10, "mm")
        borda(d, (W / 2, 850), c["linha2"], f2, AMB + (a,), 10, "mm")
        if c.get("sub"):
            fs = caber(d, c["sub"], MBLK, 78, W - 140)
            larg = d.textlength(c["sub"], font=fs)
            d.rounded_rectangle((W / 2 - larg / 2 - 34, 985, W / 2 + larg / 2 + 34, 1095), 22, fill=AMB + (a,))
            d.text((W / 2, 1040), c["sub"], font=fs, fill=ESC + (a,), anchor="mm")

    def topo(self, d, t, e, i):
        d.text((40, 70), "INEMA.CLUB", font=fnt(MXB, 32), fill=BRANCO + (225,))
        if i == 0:
            return
        ini = self.L.depois if (e.get("depois") is None and self.L.depois and t >= self.L.depois) else self.L.ini[i]
        dx = int((1 - ease((t - ini) / 0.35)) * -70)
        borda(d, (40 + dx, 140), e["linha1"], caber(d, e["linha1"], ANTON, 120, W - 80), BRANCO, 8)
        borda(d, (40 + dx, 270), e["linha2"], caber(d, e["linha2"], ANTON, 150, W - 80), cor(e.get("cor")), 8)

    def painel(self, d, t, e, i):
        p = e.get("painel")
        if i == 0 or not p:
            return
        x, y, w, h = 40, 1290, 580, 460
        d.rounded_rectangle((x, y, x + w, y + h), 26, fill=ESC + (215,))
        d.rectangle((x, y + 24, x + 8, y + h - 24), fill=cor(p.get("cor")) + (255,))
        if p.get("grande"):
            d.text((x + 40, y + 50), p["titulo"], font=caber(d, p["titulo"], ANTON, 100, w - 70), fill=BRANCO)
            d.text((x + 40, y + 190), p["texto"], font=caber(d, p["texto"], ANTON, 190, w - 70), fill=AMB)
        else:
            d.text((x + 40, y + 50), p["titulo"], font=caber(d, p["titulo"], ANTON, 110, w - 70), fill=cor(p.get("cor")))
            d.text((x + 40, y + 205), p["texto"], font=fnt(MXB, 46), fill=BRANCO, spacing=10)
        n = 7
        for k in range(n):
            cx = x + w - 30 - (n - k) * 26
            d.ellipse((cx, y + 30, cx + 14, y + 44), fill=(AMB if k <= i else (80, 90, 100)) + (255,))

    def legenda(self, d, t):
        for bl in self.blocos:
            if bl[0]["t"] - 0.05 <= t < bl[-1]["f"] + 0.25:
                pal = [p["w"].upper() for p in bl]
                f = caber(d, " ".join(pal), MBLK, 66, W - 60)
                larg = [d.textlength(p + " ", font=f) for p in pal]
                xx = (W - sum(larg)) / 2
                for p, l, raw in zip(pal, larg, bl):
                    borda(d, (xx, 1150), p, f, AMB if raw["t"] <= t else BRANCO, 7)
                    xx += l
                return

    def quadro(self, t, legenda=True):
        L = self.L
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        if t >= L.total - 1.8 and t >= L.fim + 0.2:
            a = int(255 * ease((t - (L.total - 1.8)) / 0.4))
            d.rectangle((0, 0, W, H), fill=ESC + (a,))
            fin = self.r.get("final") or ["INEMA.CLUB"]
            d.text((W / 2, 800), fin[0], font=caber(d, fin[0], ANTON, 170, W - 80), fill=AMB + (a,), anchor="mm")
            for k, s in enumerate(fin[1:]):
                d.text((W / 2, 960 + k * 84), s, font=caber(d, s, MXB if k else ANTON, 64 if k else 96, W - 100), fill=BRANCO + (a,), anchor="mm")
            return im
        i, e = self.atual(t)
        if i == 0:
            self.capa(d, e)
        self.topo(d, t, e, i); self.painel(d, t, e, i)
        if legenda and i > 0:
            self.legenda(d, t)
        return im


def quadro_completo(F, D, t, legenda=True):
    im = F.quadro(t); im.alpha_composite(D.quadro(t, legenda)); return im


# ======================================================================= comandos
def cmd_novo(ident):
    pasta = RAIZ / "edicoes" / f"{date.today().isoformat()}-{rc.slug(ident)}"
    if (pasta / "roteiro.yaml").exists():
        sys.exit(f"já existe: {pasta / 'roteiro.yaml'}")
    (pasta / "avatar").mkdir(parents=True, exist_ok=True)
    shutil.copy(EXEMPLO, pasta / "roteiro.yaml")
    log("criado", pasta / "roteiro.yaml", "— reescreva fala, âncoras, manchetes e cenas mantendo as 7 etapas")


def cmd_previa(pasta):
    r = carregar(pasta)
    pal = rc.palavras_reais(r) if r["_av"].exists() else rc.palavras_estimadas(r["fala"])
    L = Linha(r, pal, max(p["f"] for p in pal)); F = Fundo(imagens(r), L); D = Desenho(r, L)
    log(L.resumo())
    ts = [0.3] + [s + 1.2 for s in L.ini[1:]] + ([L.depois + 0.8] if L.depois else []) + [L.total - 0.5]
    ims = [quadro_completo(F, D, t).convert("RGB").resize((360, 640)) for t in ts]
    folha = Image.new("RGB", (360 * 5, 640 * math.ceil(len(ims) / 5)), ESC)
    for k, im in enumerate(ims):
        folha.paste(im, ((k % 5) * 360, (k // 5) * 640))
    out = r["_dir"] / "previa.jpg"; folha.save(out, quality=88); log("prévia", out)


def cmd_avatar(pasta):
    rc.cmd_avatar(pasta)


def trilha(r):
    m = r.get("musica")
    if m:
        return Path(m) if Path(m).is_absolute() else r["_dir"] / m
    t = r["_b"] / "trilha.wav"
    return t if t.exists() else rc.CFG["musica_reserva"]


def cmd_montar(pasta):
    r = carregar(pasta); B = r["_b"]
    pal = rc.palavras_reais(r)
    sem = rc.semelhanca(r["fala"], pal); log(f"fala do avatar × roteiro: {sem:.0%}")
    if sem < 0.85:
        sys.exit("a fala ouvida diverge do roteiro (< 85%); confira avatar/avatar.mp4")
    L = Linha(r, pal, dur(r["_av"])); F = Fundo(imagens(r), L); D = Desenho(r, L)
    log(L.resumo())
    base = B / "base.mp4"
    n = int(L.total * FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", str(base)], stdin=subprocess.PIPE)
    for k in range(n):
        enc.stdin.write(quadro_completo(F, D, k / FPS).convert("RGB").tobytes())
        if k % 300 == 0:
            log(f"quadro {k}/{n}")
    enc.stdin.close(); enc.wait()
    crop = rc.recorte_rosto(r); log("recorte do rosto", crop)
    tag = B / "tag.txt"; tag.write_text(r.get("tag", "NEI MALDANER  |  INEMA"))
    ate = L.fim + 0.3; i0 = L.ini[1]  # avatar aparece depois da capa
    vol = r.get("volume_musica", 0.20)
    en = f"between(t,{i0:.2f},{ate:.2f})"
    fc = (
        f"[1:v]crop={crop},scale={AVW}:{AVH},setsar=1,fps={FPS}[av];"
        f"[0:v]drawbox=x={AVX - 4}:y={AVY - 4}:w={AVW + 8}:h={AVH + 8}:color=0xE2A23B@1:t=fill:enable='{en}'[b1];"
        f"[b1][av]overlay={AVX}:{AVY}:eof_action=pass:enable='{en}',"
        f"drawbox=x={AVX}:y={AVY + AVH - 43}:w={AVW}:h=43:color=0x0b0f14@0.85:t=fill:enable='{en}',"
        f"drawtext=fontfile={DEJAVU}:textfile={tag}:x={AVX + 16}:y={AVY + AVH - 31}:fontsize=19:fontcolor=white:enable='{en}',format=yuv420p[v];"
        f"[1:a]aresample=48000,apad,atrim=0:{L.total:.3f},asplit=2[voz][sc];"
        f"[2:a]volume={vol},aresample=48000[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300[md];"
        f"[voz][md]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={L.total - 1.4:.2f}:d=1.4[a]"
    )
    saida = r["_dir"] / "video.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", base, "-i", r["_av"], "-stream_loop", "-1", "-i", trilha(r), "-filter_complex", fc,
         "-map", "[v]", "-map", "[a]", "-t", f"{L.total:.3f}", "-c:v", "libx264", "-crf", "21", "-preset", "slow",
         "-maxrate", "6M", "-bufsize", "12M", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida])
    log("vídeo", saida, f"{dur(saida):.1f} s", f"{saida.stat().st_size / 1e6:.1f} MB")
    (B / "tempos.json").write_text(json.dumps({"ini": L.ini, "depois": L.depois, "fim": L.fim, "total": L.total}))
    return saida


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
        t = ini[k] + min(1.5, (ini[k + 1] - ini[k]) * 0.6) if k else 0.4
        q = r["_b"] / f"mapa{k}.png"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", v, "-frames:v", "1", "-vf", f"scale={cw}:{chh}", q])
        x = pad + k * (cw + pad)
        M.paste(Image.open(q).convert("RGB"), (x, cab))
        d.rounded_rectangle((x, cab - 8, x + 74, cab + 66), 14, fill=AMB)
        d.text((x + 37, cab + 29), str(k + 1), font=fnt(ANTON, 56), fill=ESC, anchor="mm")
        y = cab + chh + 20
        d.text((x, y), e["nome"], font=caber(d, e["nome"], ANTON, 64, cw), fill=AMB)
        d.text((x, y + 82), quebra(d, e.get("gatilho", ""), fnt(MXB, 28), cw), font=fnt(MXB, 28), fill=BRANCO, spacing=6)
        d.text((x, y + 170), quebra(d, e.get("por_que", ""), fnt(MXB, 22), cw), font=fnt(MXB, 22), fill=(170, 180, 190), spacing=5)
    M.save(r["_dir"] / "mapa.jpg", quality=90); log("mapa", r["_dir"] / "mapa.jpg")
    pal = rc.palavras_reais(r)
    L = Linha(r, pal, dur(r["_av"])); F = Fundo(imagens(r), L); D = Desenho(r, L)
    quadro_completo(F, D, 0.4, legenda=False).convert("RGB").save(r["_dir"] / "capa.jpg", quality=92)
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


def main(a):
    cmds = {"imagens": lambda p: log(*imagens(carregar(p))), "previa": cmd_previa, "avatar": cmd_avatar, "montar": cmd_montar,
            "conferir": rc.cmd_conferir, "mapa": cmd_mapa}
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
