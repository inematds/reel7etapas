"""Diagramas dos 5 reels de 18/10 (D10). Rodar da raiz do repo: python3 edicoes/diagramas-1018.py <pasta-dos-prints>"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import diagramas as dg  # noqa: E402

E = Path(__file__).resolve().parent
P = Path(sys.argv[1])          # prints das páginas (chat72.png, prof2030.png, prof2027.png)
A, V, VD, B = dg.AMAR, dg.VERM, dg.VERDE, dg.BRANCO

# ---- era das ferramentas
ed = E / "2026-10-18-era-ferramentas/img"
dg.fluxo([("VOCÊ PEDE", "em português, do seu jeito"), ("CLAUDE · CODEX", "acham o código no GitHub"),
          ("PRONTO", "de graça, feito pra você")], ed, "d2", cores=[A, A, VD])
dg.antes_depois(("CAÇA APP", ["testou 10 apps", "aprendeu 10 menus", "entregou: nada"], V),
                ("SABE PEDIR", ["1 pedido claro", "o agente trabalha", "entregue hoje"], VD), ed, "d3")
dg.cartoes([("O QUE VOCÊ QUER", "o resultado, não a ferramenta"), ("O CONTEXTO", "pra quem, com o quê, até quando"),
            ("COMO CONFERIR", "o que é ficar pronto")], ed, "d5")

# ---- faturar 2027
ed = E / "2026-10-18-faturar-2027/img"
dg.linha_tempo([("1990", "INTERNET"), ("2000", "SITES"), ("2010", "CELULAR"), ("2027", "IA: SUA VEZ")], ed, "d3")
dg.cartoes([("CONSULTOR", "diz o que usar e por onde começar"), ("AUDITOR", "confere se a IA está fazendo certo"),
            ("TREINADOR", "ensina a equipe a pedir")], ed, "d4")
dg.site(P / "prof2027.png", ed, "d5", selo="GRÁTIS", corte=(0, 0, 1080, 1100))

# ---- SaaS morrendo
ed = E / "2026-10-18-saas-morrendo/img"
dg.antes_depois(("ANTES", ["assinatura todo mês", "do jeito deles", "você se adapta"], V),
                ("AGORA", ["a IA refaz", "do seu jeito", "num fim de semana"], VD), ed, "d2")
dg.cartoes([("LOJA → SITE", "anos 2000"), ("SITE → APP", "anos 2010"), ("APP → AGENTE", "agora: 2027")], ed, "d4")
dg.site(P / "prof2030.png", ed, "d6", selo="GRÁTIS", corte=(0, 0, 1080, 1100))

# ---- do chat ao agente
ed = E / "2026-10-18-chat-ao-agente/img"
dg.antes_depois(("NO CHAT", ["você pergunta", "copia e cola", "testa e repete"], V),
                ("NO AGENTE", ["você pede", "ele abre e executa", "entrega pronto"], VD), ed, "d2")
dg.terminal([("$ claude", A), ("> junta minhas planilhas de vendas", B), ("  abri 12 arquivos", VD),
             ("  conferi os totais", VD), ("  pronto: relatorio-vendas.pdf", VD)], ed, "d3")
dg.site(P / "chat72.png", ed, "d5", selo="GRÁTIS", corte=(0, 0, 1080, 1180))
dg.frase([("GRÁTIS", VD), ("AGORA", B), ("DEPOIS: SÓ NO PRO", V)], ed, "d6")

# ---- hacker / opencode v3
ed = E / "2026-10-18-opencode-v3/img"
dg.fluxo([("CHAVE ROUBADA", "a senha que a IA usa pra cobrar"), ("HACKER USA", "a noite inteira, no seu nome"),
          ("US$ 1.700", "na sua fatura")], ed, "d2", cores=[A, A, V])
dg.painel("Limites de gasto", [("Limite mensal desta chave", "US$ 20,00", True),
                                ("Avisar por e-mail ao chegar em", "80%", False)], ed, "d4")
dg.cartoes([("LIMITE DE GASTO", "em cada chave"), ("UMA CHAVE POR USO", "roubou uma, cancela só ela"),
            ("ALARME", "avisa quando o gasto foge do normal")], ed, "d5")
dg.barras([("SEM LIMITE", 1700, "US$ 1.700", V), ("COM LIMITE", 20, "US$ 20", VD)], ed, "d6", titulo="uma noite de ataque")
print("diagramas ok")
