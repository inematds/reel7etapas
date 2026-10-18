"""Diagramas do r7e (D10, 18/10/2026): cada função devolve uma lista de PNGs 1080x1920 que se montam passo a passo
(vão em 'passos:' na etapa). O conteúdo fica na faixa y 440–1180: em cima entra a manchete, embaixo a legenda e o avatar.

Uso no roteiro: o script de cada edição (ex.: edicoes/<pasta>/diagramas.py) importa daqui e grava em img/.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
F = Path.home() / ".local/share/fonts"
ANTON, MBLK, MXB = str(F / "Anton-Regular.ttf"), str(F / "Montserrat-Black.ttf"), str(F / "Montserrat-ExtraBold.ttf")
FUNDO, CARTAO, BORDA = (12, 12, 16), (24, 24, 32), (48, 48, 60)
BRANCO, CINZA, AMAR, VERM, VERDE, AZUL, ESC = (255, 255, 255), (170, 176, 190), (250, 204, 21), (255, 64, 48), (34, 197, 94), (59, 158, 255), (12, 12, 16)
TOPO, BASE = 440, 1150
X0, X1 = 70, 950        # direita livre: coluna de botões do TikTok/Instagram
CX = (X0 + X1) / 2


def fnt(p, s):
    return ImageFont.truetype(p, s)


def caber(texto, fonte, tam, larg, minimo=30):
    while tam > minimo and fnt(fonte, tam).getlength(texto) > larg:
        tam -= 2
    return fnt(fonte, tam)


def fundo():
    im = Image.new("RGB", (W, H), FUNDO)
    brilho = Image.new("L", (W, H), 0)
    ImageDraw.Draw(brilho).ellipse((-200, 300, W + 200, 1400), fill=46)
    brilho = brilho.filter(ImageFilter.GaussianBlur(160))
    im.paste((40, 34, 10), mask=brilho)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 60):
        d.line((x, 0, x, H), fill=(18, 18, 24))
    for y in range(0, H, 60):
        d.line((0, y, W, y), fill=(18, 18, 24))
    return im


def caixa(d, xy, cor_borda=BORDA, fundo_=CARTAO, raio=26, larg=4):
    d.rounded_rectangle(xy, raio, fill=fundo_, outline=cor_borda, width=larg)


def texto_c(d, cx, y, s, fonte, cor, larg=860, tam=64, minimo=30):
    f = caber(s, fonte, tam, larg, minimo)
    d.text((cx, y), s, font=f, fill=cor, anchor="mt")
    return f.getbbox("Ág")[3]


def seta_baixo(d, cx, y0, y1, cor=AMAR):
    d.line((cx, y0, cx, y1 - 18), fill=cor, width=10)
    d.polygon([(cx - 28, y1 - 30), (cx + 28, y1 - 30), (cx, y1 + 4)], fill=cor)


def salvar(ims, pasta, nome):
    pasta = Path(pasta); pasta.mkdir(parents=True, exist_ok=True)
    out = []
    for k, im in enumerate(ims, 1):
        a = pasta / f"{nome}-{k}.png"; im.save(a); out.append(a)
    return out


# ------------------------------------------------------------------ primitivas
def fluxo(nos, pasta, nome, cores=None):
    """nos: [(titulo, sub)] em coluna, com seta entre eles; o último na cor de destaque (cores[i] = borda/realce)"""
    n = len(nos); cores = cores or [AMAR] * (n - 1) + [VERM]
    seta = 56; h = int((BASE - TOPO - seta * (n - 1)) / n)
    ims = []
    for passo in range(1, n + 1):
        im = fundo(); d = ImageDraw.Draw(im)
        y = TOPO
        for i, (tit, sub) in enumerate(nos[:passo]):
            caixa(d, (X0, y, X1, y + h), cor_borda=cores[i], larg=6 if i == passo - 1 else 4)
            ty = y + (h - (64 + (40 if sub else 0))) / 2
            texto_c(d, CX, ty, tit, ANTON, cores[i] if i == n - 1 else BRANCO, tam=72)
            if sub:
                texto_c(d, CX, ty + 84, sub, MXB, CINZA, tam=36)
            if i < passo - 1:
                seta_baixo(d, CX, y + h + 6, y + h + seta - 6, cores[i])
            y += h + seta
        ims.append(im)
    return salvar(ims, pasta, nome)


def antes_depois(esq, dir_, pasta, nome):
    """esq/dir_: (titulo, [linhas], cor). Passo 1: só a esquerda; passo 2: as duas."""
    ims = []
    meio = CX; gap = 24
    for passo in (1, 2):
        im = fundo(); d = ImageDraw.Draw(im)
        for k, (tit, linhas, cor) in enumerate((esq, dir_)):
            if k == 1 and passo == 1:
                break
            x0 = X0 if k == 0 else meio + gap / 2; x1 = meio - gap / 2 if k == 0 else X1
            caixa(d, (x0, TOPO, x1, BASE), cor_borda=cor, larg=6)
            d.rounded_rectangle((x0, TOPO, x1, TOPO + 130), 26, fill=cor)
            d.rectangle((x0, TOPO + 100, x1, TOPO + 130), fill=cor)
            texto_c(d, (x0 + x1) / 2, TOPO + 30, tit, ANTON, ESC if cor in (AMAR, VERDE) else BRANCO, larg=x1 - x0 - 40, tam=76)
            passo_y = (BASE - TOPO - 150) / len(linhas)
            for j, ln in enumerate(linhas):
                f = caber(ln, MBLK, 58, x1 - x0 - 40, 30)
                yc = TOPO + 150 + passo_y * (j + 0.5)
                d.text(((x0 + x1) / 2, yc), ln, font=f, fill=BRANCO, anchor="mm")
                if j < len(linhas) - 1:
                    d.line((x0 + 60, yc + passo_y / 2, x1 - 60, yc + passo_y / 2), fill=(60, 60, 72), width=3)
        ims.append(im)
    return salvar(ims, pasta, nome)


def cartoes(itens, pasta, nome, cor=AMAR):
    """itens: [(titulo, sub)] numerados 1..n, entram um a um"""
    n = len(itens); gap = 30; h = int((BASE - TOPO - gap * (n - 1)) / n)
    ims = []
    for passo in range(1, n + 1):
        im = fundo(); d = ImageDraw.Draw(im)
        for i, (tit, sub) in enumerate(itens[:passo]):
            y = TOPO + i * (h + gap)
            caixa(d, (X0, y, X1, y + h), cor_borda=cor if i == passo - 1 else BORDA, larg=6 if i == passo - 1 else 4)
            r = min(64, h / 2 - 18); cx, cy = X0 + 40 + r, y + h / 2
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=cor)
            d.text((cx, cy), str(i + 1), font=fnt(ANTON, int(r * 1.3)), fill=ESC, anchor="mm")
            tx = cx + r + 34; larg = X1 - 30 - tx
            ft = caber(tit, ANTON, 70, larg, 36)
            if sub:
                d.text((tx, cy - 8), tit, font=ft, fill=BRANCO, anchor="ls")
                d.text((tx, cy + 14), sub, font=caber(sub, MXB, 36, larg, 24), fill=CINZA, anchor="lt")
            else:
                d.text((tx, cy), tit, font=ft, fill=BRANCO, anchor="lm")
        ims.append(im)
    return salvar(ims, pasta, nome)


def barras(itens, pasta, nome, titulo=None):
    """itens: [(rotulo, valor, texto_valor, cor)]; barras horizontais proporcionais, entram uma a uma"""
    vmax = max(v for _, v, _, _ in itens); n = len(itens)
    y0 = TOPO + (90 if titulo else 0); bloco = (BASE - y0) / n
    ims = []
    for passo in range(1, n + 1):
        im = fundo(); d = ImageDraw.Draw(im)
        if titulo:
            texto_c(d, CX, TOPO, titulo, MBLK, CINZA, tam=42)
        for i, (rot, v, tv, cor) in enumerate(itens[:passo]):
            y = y0 + i * bloco + 10
            d.text((X0, y), rot, font=caber(rot, MBLK, 46, X1 - X0, 28), fill=BRANCO)
            by = y + 70; bh = min(150, bloco - 110)
            bw = max(40, (X1 - X0) * v / vmax)
            d.rounded_rectangle((X0, by, X1, by + bh), 20, fill=(28, 28, 36))
            d.rounded_rectangle((X0, by, X0 + bw, by + bh), 20, fill=cor)
            f = fnt(ANTON, int(bh * 0.72))
            dentro = f.getlength(tv) + 50 < bw
            d.text((X0 + bw - 24 if dentro else X0 + bw + 24, by + bh / 2), tv, font=f,
                   fill=(ESC if cor in (AMAR, VERDE) else BRANCO) if dentro else cor, anchor="rm" if dentro else "lm")
        ims.append(im)
    return salvar(ims, pasta, nome)


def linha_tempo(pontos, pasta, nome):
    """pontos: [(ano, texto)] em coluna; o último em amarelo (é o agora)"""
    n = len(pontos); passo_y = (BASE - TOPO - 60) / (n - 1)
    xl = X0 + 150
    ims = []
    for passo in range(1, n + 1):
        im = fundo(); d = ImageDraw.Draw(im)
        d.line((xl, TOPO + 30, xl, TOPO + 30 + passo_y * (passo - 1)), fill=(80, 80, 96), width=10)
        for i, (ano, txt) in enumerate(pontos[:passo]):
            y = TOPO + 30 + i * passo_y; ult = i == n - 1
            cor = AMAR if ult else BRANCO
            d.ellipse((xl - 26, y - 26, xl + 26, y + 26), fill=AMAR if ult else (90, 90, 110), outline=FUNDO, width=6)
            d.text((xl - 50, y), ano, font=fnt(ANTON, 64), fill=cor, anchor="rm")
            d.text((xl + 56, y), txt, font=caber(txt, MBLK, 52, X1 - xl - 70, 28), fill=cor, anchor="lm")
        ims.append(im)
    return salvar(ims, pasta, nome)


def terminal(linhas, pasta, nome, titulo="terminal"):
    """janela de terminal com as linhas aparecendo; linhas: [(texto, cor)]"""
    ims = []
    for passo in range(1, len(linhas) + 1):
        im = fundo(); d = ImageDraw.Draw(im)
        d.rounded_rectangle((X0 - 20, TOPO, X1 + 20, BASE), 24, fill=(8, 8, 12), outline=(60, 60, 72), width=4)
        d.rounded_rectangle((X0 - 20, TOPO, X1 + 20, TOPO + 70), 24, fill=(30, 30, 38))
        d.rectangle((X0 - 20, TOPO + 46, X1 + 20, TOPO + 70), fill=(30, 30, 38))
        for k, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
            d.ellipse((X0 + 10 + k * 46, TOPO + 22, X0 + 38 + k * 46, TOPO + 50), fill=c)
        d.text((CX, TOPO + 36), titulo, font=fnt(MXB, 30), fill=CINZA, anchor="mm")
        y = TOPO + 110
        for txt, cor in linhas[:passo]:
            d.text((X0 + 10, y), txt, font=caber(txt, MXB, 40, X1 - X0 - 10, 24), fill=cor)
            y += 74
        ims.append(im)
    return salvar(ims, pasta, nome)


def painel(titulo, campos, pasta, nome):
    """mockup de tela de configuração: campos [(rotulo, valor, destaque?)]; passo 1 sem destaque, passo 2 com o círculo"""
    ims = []
    for passo in (1, 2):
        im = fundo(); d = ImageDraw.Draw(im)
        caixa(d, (X0, TOPO, X1, BASE), cor_borda=(70, 70, 84), fundo_=(242, 242, 246), larg=4)
        d.rounded_rectangle((X0, TOPO, X1, TOPO + 110), 26, fill=(225, 225, 232)); d.rectangle((X0, TOPO + 80, X1, TOPO + 110), fill=(225, 225, 232))
        d.text((X0 + 40, TOPO + 55), titulo, font=caber(titulo, MBLK, 44, X1 - X0 - 80), fill=(20, 20, 26), anchor="lm")
        y = TOPO + 160
        for rot, val, dest in campos:
            d.text((X0 + 40, y), rot, font=fnt(MXB, 34), fill=(90, 90, 100))
            bx = (X0 + 40, y + 50, X1 - 40, y + 150)
            d.rounded_rectangle(bx, 16, fill=BRANCO, outline=(200, 200, 210), width=3)
            d.text((bx[0] + 30, (bx[1] + bx[3]) / 2), val, font=fnt(MBLK, 50), fill=(20, 20, 26), anchor="lm")
            if dest and passo == 2:
                d.rounded_rectangle((bx[0] - 14, bx[1] - 14, bx[2] + 14, bx[3] + 14), 24, outline=VERM, width=10)
            y += 210
        ims.append(im)
    return salvar(ims, pasta, nome)


def frase(linhas, pasta, nome):
    """frase grande em passos: linhas [(texto, cor)] — cada passo acrescenta uma linha"""
    ims = []
    n = len(linhas); alt = (BASE - TOPO) / n
    for passo in range(1, n + 1):
        im = fundo(); d = ImageDraw.Draw(im)
        for i, (txt, cor) in enumerate(linhas[:passo]):
            f = caber(txt, ANTON, 190, X1 - X0, 60)
            d.text((CX, TOPO + alt * i + alt / 2), txt, font=f, fill=cor, anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
        ims.append(im)
    return salvar(ims, pasta, nome)


def site(print_png, pasta, nome, selo="GRÁTIS", corte=(0, 0, 1080, 1180)):
    """print real de uma página (prova): cartão com cantos e sombra; passo 2 com o selo carimbado"""
    pr = Image.open(print_png).convert("RGB").crop(corte)
    larg = X1 - X0; alt = BASE - TOPO
    k = min(larg / pr.width, alt / pr.height); pr = pr.resize((int(pr.width * k), int(pr.height * k)), Image.LANCZOS)
    x = int(CX - pr.width / 2); y = TOPO + int((alt - pr.height) / 2)
    m = Image.new("L", pr.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pr.width - 1, pr.height - 1), 28, fill=255)
    ims = []
    for passo in (1, 2):
        im = fundo()
        sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle((x, y + 16, x + pr.width, y + pr.height + 16), 28, fill=200)
        im.paste((0, 0, 0), mask=sh.filter(ImageFilter.GaussianBlur(18)))
        im.paste(pr, (x, y), m)
        d = ImageDraw.Draw(im); d.rounded_rectangle((x - 3, y - 3, x + pr.width + 3, y + pr.height + 3), 30, outline=AMAR, width=5)
        if passo == 2 and selo:
            f = fnt(ANTON, 120); tw = f.getlength(selo)
            s = Image.new("RGBA", (int(tw + 90), 190), (0, 0, 0, 0)); ds = ImageDraw.Draw(s)
            ds.rounded_rectangle((6, 6, s.width - 6, s.height - 6), 26, fill=VERDE + (255,), outline=BRANCO + (255,), width=8)
            ds.text((s.width / 2, s.height / 2), selo, font=f, fill=BRANCO, anchor="mm", stroke_width=4, stroke_fill=(0, 60, 20))
            s = s.rotate(-8, expand=True, resample=Image.BICUBIC)
            im.paste(s, (int(x + pr.width - s.width + 30), int(y + pr.height - s.height + 40)), s)
        ims.append(im)
    return salvar(ims, pasta, nome)
