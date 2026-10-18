#!/usr/bin/env python3
"""cena.js de um reel r7e no motor do eventosextremospub a partir de uma ficha (ficha.json na pasta da edição).
Mesma lógica do gerar_cena.py da edição 2026-10-18-do-chat-ao-agente (modelo aprovado), generalizada (18/10/2026).

uso: python3 ev_cena.py <pasta-da-edicao>     (precisa de falas.json, avatar/tempos.json e ficha.json)

ficha.json:
 {"marca": "INEMA · ...", "selo": "ALERTA INEMA",
  "telas": [{"src": "capa/x.png", "de": "f2" | ["f2", "palavra", k?], "selo": "ilustração"|"inema.club"|null, "zoom": .07}],
            (a 1ª tela é a abertura, de -1.0; cada tela vai até o início da seguinte)
  "paineis": [{"de": "f1" | ["f1","palavra"], "ate": "f2"?, "k": "TÍTULO", "borda": "red|am|vd",
               "itens": [["f1", "palavra", "texto", k?]], "contador": {"ate": 1700, "de": 0, "dec": 0, "em": ["f1","1.700"],
               "cor": "#ff2a1f", "unid": "..."}, "l": "linha pequena"}],
  "cta": {"em": ["f7","pede"], "a": "...", "b": "..."}, "club": {"em": ["f7","inema.club"], "a": "inema.club", "b": "..."},
  "fonte": "<b>...</b> · ...", "cores": {"palavra": "#hex"}}
"""
import difflib, json, re, sys, unicodedata
from pathlib import Path

E = Path(sys.argv[1]).resolve()
T = json.loads((E / "avatar/tempos.json").read_text())
F = json.loads((E / "ficha.json").read_text())


def n(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())


def roteiro(t, texto):
    tok, W = texto.split(), t["palavras"]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, [n(x) for x in tok], [n(p["w"]) for p in W], autojunk=False).get_opcodes():
        if op == "equal":
            out += [{"w": tok[i1 + k], "t": W[j1 + k]["t"], "f": W[j1 + k]["f"]} for k in range(i2 - i1)]
        elif i2 > i1:
            a = W[j1]["t"] if j2 > j1 else (W[j1 - 1]["f"] if j1 else t["ini"])
            b = W[j2 - 1]["f"] if j2 > j1 else (W[j1]["t"] if j1 < len(W) else a + .3)
            d = (b - a) / (i2 - i1)
            out += [{"w": tok[i1 + k], "t": round(a + k * d, 3), "f": round(a + (k + 1) * d, 3)} for k in range(i2 - i1)]
    return out


ROT = {f["id"]: f.get("legenda") or f["fala"] for f in json.loads((E / "falas.json").read_text())}
for t in T:
    t["palavras"] = roteiro(t, ROT[t["id"]])
FALA = {t["id"]: t for t in T}
IDS = [t["id"] for t in T]


def em(fid, palavra, k=1):
    achou = 0
    for p in FALA[fid]["palavras"]:
        if n(palavra) == n(p["w"]) or (len(n(palavra)) > 3 and n(palavra) in n(p["w"])):
            achou += 1
            if achou == k:
                return p["t"]
    raise KeyError(f"{fid}: '{palavra}' não encontrada em: " + " ".join(p["w"] for p in FALA[fid]["palavras"]))


def quando(ref):
    if isinstance(ref, str):
        return FALA[ref]["ini"]
    return em(*ref)


def proxima_fala(ref):
    fid = ref if isinstance(ref, str) else ref[0]
    i = IDS.index(fid)
    return FALA[IDS[i + 1]]["ini"] if i + 1 < len(IDS) else None


DUR = round(FALA[IDS[-1]]["fim"] + 1.4, 2)
BR = {"lon": -52.0, "lat": -14.0, "zoom": 3.4}
camera = [{"t": 0, **BR, "pitch": 30, "bearing": 0}, {"t": DUR, **BR, "pitch": 40, "bearing": 20}]

telas = [{"src": "capa/preto.png", "ini": -1.0, "fim": DUR + 1, "fade": 0, "zoom": 0}]
TS = F["telas"]
for i, tl in enumerate(TS):
    a = -1.0 if i == 0 else quando(tl["de"]) - .1
    b = (quando(TS[i + 1]["de"]) - .1) if i + 1 < len(TS) else DUR + 1
    d = {"src": tl["src"], "ini": a, "fim": b, "fade": .3, "zoom": tl.get("zoom", .03 if i == 0 else .07)}
    selo = tl.get("selo", None if i == 0 else "ilustração")
    if selo:
        d["selo"] = selo
    telas.append(d)

BORDA = {"red": "rgba(255,42,31,.7)", "am": "rgba(250,204,21,.75)", "vd": "rgba(34,197,94,.7)"}
paineis = []
for p in F["paineis"]:
    a = quando(p["de"]) - (.1 if not isinstance(p["de"], str) else 0)
    b = (FALA[p["ate"]]["ini"] if p.get("ate") else proxima_fala(p["de"]) or DUR) - .05
    d = {"ini": a, "fim": b, "k": p["k"], "borda": BORDA[p.get("borda", "am")]}
    if p.get("itens"):
        d["itens"] = [{"t": em(x[0], x[1], x[3] if len(x) > 3 else 1), "txt": x[2]} for x in p["itens"]]
    if p.get("contador"):
        c = p["contador"]
        d["contador"] = {"de": c.get("de", 0), "ate": c["ate"], "dec": c.get("dec", 0), "ini": em(*c["em"]) - 1.0,
                         "dur": c.get("dur", 1.2), "cor": c.get("cor", "#FACC15"), "unid": c.get("unid", "")}
    if p.get("l"):
        d["l"] = p["l"]
    paineis.append(d)

cta = {"ini": em(*F["cta"]["em"]), "fim": DUR, "a": F["cta"]["a"], "b": F["cta"]["b"]}
club = {"ini": em(*F["club"]["em"]), "fim": DUR, "a": F["club"]["a"], "b": F["club"]["b"]}
fontes = [{"ini": .3, "fim": DUR, "html": F["fonte"]}]

CORES = {n(k): v for k, v in F.get("cores", {}).items()}
CORES.setdefault("inemaclub", "#FACC15"); CORES.setdefault("comentarios", "#FACC15"); CORES.setdefault("link", "#FACC15")
NUM = re.compile(r"\d")
legenda = []
for t in T:
    bloco = []
    for i, p in enumerate(t["palavras"]):
        w = p["w"]; k = n(w)
        cor = CORES.get(k) or ("#FACC15" if NUM.search(k) else None)
        bloco.append({"w": w, "t": p["t"], **({"cor": cor} if cor else {})})
        if len(bloco) == 3 or w[-1:] in ".?!,:" or i == len(t["palavras"]) - 1:
            legenda.append({"ini": bloco[0]["t"] - .05, "fim": p["f"] + .12, "palavras": bloco})
            bloco = []
for a, b in zip(legenda, legenda[1:]):
    a["fim"] = min(max(a["fim"], b["ini"]), b["ini"])

C = {"layout": "canto", "padding_baixo": 640, "duracao": DUR, "padding_topo": 0, "marca": F["marca"], "selo": F["selo"],
     "camera": camera, "telas": telas, "hero": [], "paineis": paineis, "cta": cta, "club": club, "fontes": fontes, "legenda": legenda}
(E / "cena.js").write_text("window.CENA=" + json.dumps(C, ensure_ascii=False) + ";")
print(f"cena.js ok, duração {DUR} · {len(telas)} telas · {len(paineis)} painéis · {len(legenda)} blocos")
