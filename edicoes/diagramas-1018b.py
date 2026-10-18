"""Diagramas dos 2 reels de gestão (18/10, D10, lives3). Rodar da raiz do repo: python3 edicoes/diagramas-1018b.py <pasta-dos-prints>"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import diagramas as dg  # noqa: E402

E = Path(__file__).resolve().parent
P = Path(sys.argv[1])          # prints: emp27.png (Empresas de 2027 v6.2), const.png (Constituição dos Agentes v6.2)
A, V, VD = dg.AMAR, dg.VERM, dg.VERDE

# ---- demissão em massa de gerentes
ed = E / "2026-10-18-demissao-gestores/img"
dg.cartoes([("PESSOAS", "a equipe de gente"), ("PROCESSOS", "como o trabalho anda"),
            ("AGENTES", "a equipe que não é gente")], ed, "d2")
dg.site(P / "emp27.png", ed, "d4", selo="9 AULAS", corte=(0, 0, 1080, 1180))
dg.frase([("9 AULAS", VD), ("15 MIN CADA", dg.BRANCO), ("SEM INSTALAR NADA", A)], ed, "d5")

# ---- novas funções do gestor
ed = E / "2026-10-18-novas-funcoes-gestao/img"
dg.antes_depois(("ANTES", ["chefia pessoas", "cobra o prazo", "confere no fim"], V),
                ("AGORA", ["pessoas + agentes", "define o critério", "mede todo dia"], VD), ed, "d2")
dg.fluxo([("GESTOR", "diz o quê e o porquê"), ("TÉCNICO", "garante o como"), ("AGENTE", "executa e chama você")],
         ed, "d4", cores=[A, A, VD])
dg.cartoes([("5 PERGUNTAS", "o que o agente precisa saber"), ("4 NÍVEIS", "de autonomia, do pergunta-tudo ao sozinho"),
            ("3 CASOS", "de teste antes de soltar")], ed, "d5")
dg.site(P / "const.png", ed, "d6", selo="5 AULAS", corte=(0, 0, 1080, 1180))
print("diagramas ok")
