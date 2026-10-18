"""Peças para montar um reel r7e no motor do eventosextremospub (18/10/2026, pedido do Nei: "olha o eventosextremospub,
muito mais viral"). Mesmo acabamento da edição 2026-10-18-do-chat-ao-agente de lá.

  python3 ev_util.py abertura <capa/abertura.png>           → capa/abertura-desce.png (desce 110 px: o título não bate na faixa do topo)
  python3 ev_util.py print <raw.png> <saida.png> [--escuro]  → print da página num cartão (1080x1920), metade de cima
  python3 ev_util.py vertical <png>...                       → leva cada PNG a 1080x1920 (o image_gen às vezes devolve 941x1672)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

W, H = 1080, 1920
AMAR = (250, 204, 21)


def vertical(p):
    im = Image.open(p).convert("RGB")
    if im.size != (W, H):
        k = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        x, y = (im.width - W) // 2, (im.height - H) // 2
        im = im.crop((x, y, x + W, y + H)); im.save(p)
    return p


def abertura(p, dy=110):
    im = Image.open(vertical(p)).convert("RGB")
    out = Image.new("RGB", (W, H), (12, 12, 16)); out.paste(im.crop((0, 0, W, H - dy)), (0, dy))
    g = Image.new("L", (W, dy + 60), 0); d = ImageDraw.Draw(g)
    for y in range(dy + 60):
        d.line((0, y, W, y), fill=int(255 * max(0, 1 - y / (dy + 60))))
    out.paste((12, 12, 16), (0, 0), g)
    dst = Path(p).with_name("abertura-desce.png"); out.save(dst); return dst


def print_card(raw, saida, escuro=False):
    """print 540x960@2x da página: corta o topo e põe num cartão com borda amarela, no alto da tela (y 210)"""
    pr = Image.open(raw).convert("RGB")
    pr = pr.crop((0, 0, pr.width, min(pr.height, int(pr.width * 1.02))))
    larg = 940; pr = pr.resize((larg, round(pr.height * larg / pr.width)), Image.LANCZOS)
    if escuro:
        pr = ImageEnhance.Brightness(pr).enhance(0.55)
    bg = Image.new("RGB", (W, H), (12, 12, 16))
    x, y = (W - larg) // 2, 210
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle((x, y + 18, x + larg, y + pr.height + 18), 30, fill=210)
    bg.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(22)))
    m = Image.new("L", pr.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pr.width - 1, pr.height - 1), 28, fill=255)
    bg.paste(pr, (x, y), m)
    ImageDraw.Draw(bg).rounded_rectangle((x - 3, y - 3, x + larg + 3, y + pr.height + 3), 30, outline=AMAR, width=5)
    bg.save(saida); return saida


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "abertura":
        print(abertura(a[1]))
    elif a[0] == "print":
        print(print_card(a[1], a[2], "--escuro" in a))
    elif a[0] == "vertical":
        for p in a[1:]:
            print(vertical(p))
