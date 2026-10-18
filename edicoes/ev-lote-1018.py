#!/usr/bin/env python3
"""Lote 18/10/2026: os 6 reels r7e (D9/D10) refeitos no motor do eventosextremospub com o MESMO avatar.
Pedido do Nei: "ainda não ficou bom, ficou padrão ... olha o eventosextremospub como ele faz muito mais viral ... refaça todos
com o mesmo avatar e me manda, e pode distribuir no lives7, mas na fila". Piloto: eventosextremospub/edicoes/2026-10-18-r7e-hacker.

uso: python3 edicoes/ev-lote-1018.py <pasta-dos-prints-raw>   → cria eventosextremospub/edicoes/2026-10-18-r7e-<slug>/ com
     avatar (cópia), falas.json, capa/pedido.txt, capa/preto.png, prints/*.png, ficha.json
"""
import json, re, shutil, sys
from pathlib import Path

import yaml

R7 = Path(__file__).resolve().parent
EV = Path.home() / "projetos/eventosextremospub/edicoes"
MODELO = EV / "2026-10-18-do-chat-ao-agente"
RAW = Path(sys.argv[1])
sys.path.insert(0, str(R7.parent))
import ev_util  # noqa: E402

ESTILO = ("Estilo foto cinematográfica realista, moderna, tons escuros (preto #0c0c10) com acentos de luz amarela (#FACC15), "
          "vermelha de alerta (#ff2a1f) só onde houver perigo, e branca; luz limpa e nítida, contraste alto, sem desfoque forte. "
          "Sem logotipo de empresa, sem marca d'água, sem pessoas reconhecíveis (rostos de lado, na sombra ou de costas). "
          "Robô, quando houver: humanoide industrial estilo Tesla Optimus, com visor preto na frente, nunca fofo ou cartoon. "
          "Nenhum texto nas imagens, EXCETO na abertura.png.")
ABRE = ("Texto ESCRITO DENTRO da arte, grande, em português, fonte bold sem serifa: no topo, branco, \"{a}\"; logo abaixo, maior, "
        "em {cor}, \"{b}\". Todo o texto na METADE DE CIMA da imagem; a metade de baixo sem texto. Confira a grafia exata, com acentos.")
COMUM = {"inema ponto club": "inema.club", "dois mil e vinte e sete": "2027", "dois mil e trinta": "2030"}

R = {
 "ferramentas": dict(r7="era-ferramentas", grupos=[2, 1, 1, 1, 1, 1, 2], troca={"três coisas": "3 coisas"},
   marca="INEMA · A ERA DAS FERRAMENTAS", selo="OPINIÃO · NEI",
   fonte="<b>opinião do Nei Maldaner</b> · imagens: ilustração",
   abre=("A ERA DAS FERRAMENTAS ACABOU", "QUEM CAÇA APP É SUPERFICIAL", "vermelho #ff2a1f",
         "uma pessoa de costas afundada até o peito numa avalanche de dezenas de caixas e cartões luminosos de aplicativos genéricos (sem logos) caindo do alto, num quarto escuro; luz amarela vazando das caixas"),
   imgs=[("git.png", "um cofre-biblioteca gigante e escuro com prateleiras infinitas de pastas de código luminosas em amarelo; um robô humanoide de visor preto puxa uma pasta brilhante e entrega a uma mão humana; sensação de que tudo já existe"),
         ("perdeu.png", "cena dividida: à esquerda, uma pessoa exausta de costas diante de dez janelas de aplicativos abertas, luz vermelha; à direita, outra pessoa relaxada de costas enquanto um robô de visor preto trabalha num monitor com um check amarelo grande"),
         ("aprende.png", "mão escrevendo num caderno numa mesa escura à noite, ao lado de um notebook com uma conversa de IA; uma lâmpada amarela luminosa acesa sobre a mesa; sensação de 'entendi'"),
         ("tres.png", "três objetos luminosos alinhados numa mesa preta como produto de luxo: um alvo dourado, uma pasta aberta com um mapa luminoso e uma prancheta com um check amarelo"),
         ("qualquer.png", "uma pessoa de costas, confiante, comandando com um gesto três robôs humanoides de visor preto, cada um segurando uma ferramenta luminosa diferente (chave inglesa, pincel, engrenagem); luz amarela")],
   telas=[["capa/abertura-desce.png", None], ["capa/git.png", "f2"], ["capa/perdeu.png", "f3"], ["capa/aprende.png", "f4"],
          ["capa/tres.png", "f5"], ["capa/qualquer.png", "f6"], ["prints/club-c.png", "f7", "inema.club"]],
   paineis=[{"de": ["f1", "Quem"], "k": "CAÇADOR DE APP", "borda": "red", "itens": [["f1", "corre", "🏃 corre atrás do app novo"], ["f1", "superficial", "🫥 fica no superficial"]]},
            {"de": "f2", "k": "TÁ TUDO NO GIT", "itens": [["f2", "código", "📦 o código já existe"], ["f2", "graça", "🆓 de graça no GitHub"], ["f2", "Codex", "🤖 Claude e Codex fazem"]]},
            {"de": "f3", "k": "NÃO SABE PEDIR?", "borda": "red", "itens": [["f3", "perdeu", "❌ perdeu"], ["f3", "testa", "🧪 você testa o app da semana"], ["f3", "inteiro", "✅ o outro já entregou"]]},
            {"de": "f4", "k": "SE APRENDE RÁPIDO", "itens": [["f4", "aprende", "⚡ aprende rápido"], ["f4", "programador", "✅ sem programar"]]},
            {"de": "f5", "k": "PEDIR BEM = 3 COISAS", "itens": [["f5", "quer", "1️⃣ o que você quer"], ["f5", "contexto", "2️⃣ o contexto"], ["f5", "conferir", "3️⃣ como conferir"]]},
            {"de": "f6", "k": "QUALQUER FERRAMENTA", "borda": "vd", "itens": [["f6", "qualquer", "🧰 qualquer ferramenta"], ["f6", "saiu", "🆕 até a que nem saiu"]]}],
   cta=("VOCÊ SABE PEDIR? 👇", "me pede o link aqui nos comentários"), club="aprenda a pedir pra IA",
   cores={"ferramentas": "#FACC15", "acabou": "#ff2a1f", "superficial": "#ff2a1f", "github": "#FACC15", "claude": "#FACC15",
          "codex": "#FACC15", "perdeu": "#ff2a1f", "aprende": "#FACC15", "contexto": "#FACC15", "conferir": "#FACC15", "qualquer": "#FACC15"}),
 "2027": dict(r7="faturar-2027", grupos=[3, 1, 2, 1, 1, 1, 2],
   troca={"anos noventa": "anos 90", "anos dois mil": "anos 2000", "dois mil e dez": "2010"},
   marca="INEMA · QUEM FATURA EM 2027", selo="OPINIÃO · NEI",
   fonte="<b>opinião do Nei Maldaner</b> · formação Profissional 2027 no inema.club · imagens: ilustração",
   abre=("QUEM VAI FATURAR EM 2027", "NÃO É QUEM CRIA SOFTWARE", "amarelo #FACC15",
         "em primeiro plano, um programador de costas, exausto, sozinho de madrugada diante de três telas de código; ao fundo, numa sala iluminada em dourado, um consultor de costas apertando a mão de um empresário"),
   imgs=[("perdidas.png", "um empresário de terno, de costas, perdido no meio de um labirinto escuro de dezenas de telas luminosas com setas para todos os lados; luz amarela e branca"),
         ("eras.png", "linha de objetos sobre um piso preto refletindo luz amarela, da esquerda para a direita: um monitor antigo de tubo com um modem, um notebook com um site, um smartphone, e por último uma esfera dourada luminosa de IA flutuando"),
         ("papeis.png", "três silhuetas profissionais de costas lado a lado num palco escuro com luz de recorte amarela: uma segurando um mapa (consultor), outra com uma lupa diante de um painel (auditor), outra diante de um quadro com um grupo (treinador)"),
         ("primeiro.png", "uma pessoa de costas chegando primeiro ao topo de uma escada luminosa amarela no escuro, enquanto outras silhuetas ainda estão nos degraus de baixo")],
   telas=[["capa/abertura-desce.png", None], ["capa/perdidas.png", "f2"], ["capa/eras.png", "f3"], ["capa/papeis.png", "f4"],
          ["prints/prof2027-c.png", "f5", "inematds.github.io/profissional2027x"], ["capa/primeiro.png", "f6"], ["prints/club-c.png", "f7", "inema.club"]],
   paineis=[{"de": ["f1", "ajuda"], "k": "QUEM FATURA EM 2027", "itens": [["f1", "cria", "❌ quem só cria software"], ["f1", "ajuda", "✅ quem ajuda os outros a criar"], ["f1", "Acorda", "⏰ acorda!"]]},
            {"de": "f2", "k": "EMPRESAS PERDIDAS", "borda": "red", "itens": [["f2", "perdidas", "😵 perdidas"], ["f2", "opção", "🔀 opção demais de IA"], ["f2", "pagar", "💰 vão pagar quem mostrar o caminho"]]},
            {"de": "f3", "k": "JÁ ACONTECEU 3 VEZES", "itens": [["f3", "internet", "🌐 anos 90: internet"], ["f3", "sites", "🖥️ anos 2000: sites"], ["f3", "celular", "📱 2010: celular"], ["f3", "ensinou", "💰 faturou quem ensinou"]]},
            {"de": "f4", "k": "SEJA O GUIA", "itens": [["f4", "consultor", "🧭 consultor"], ["f4", "auditor", "🔍 auditor"], ["f4", "treinador", "🎓 treinador de IA"]]},
            {"de": "f5", "k": "PROFISSIONAL 2027", "borda": "vd", "itens": [["f5", "kits", "🧰 kits prontos"], ["f5", "rápido", "⚡ aprende rápido"], ["f5", "atender", "🤝 começa a atender"]]},
            {"de": "f6", "k": "CHEGA PRIMEIRO", "borda": "red", "itens": [["f6", "agora", "⏳ aprende agora"], ["f6", "primeiro", "🥇 chega antes dos outros"]]}],
   cta=("CONSULTOR, AUDITOR OU TREINADOR? 👇", "me pede o link aqui nos comentários"), club="formação gratuita Profissional 2027",
   cores={"faturar": "#FACC15", "software": "#ff2a1f", "ajuda": "#FACC15", "acorda": "#ff2a1f", "perdidas": "#ff2a1f",
          "caminho": "#FACC15", "ensinou": "#FACC15", "consultor": "#FACC15", "auditor": "#FACC15", "treinador": "#FACC15", "primeiro": "#FACC15"}),
 "saas": dict(r7="saas-morrendo", grupos=[1, 1, 1, 1, 1, 1, 2], troca={},
   marca="INEMA · O FIM DO SAAS", selo="ALERTA INEMA",
   fonte="<b>opinião do Nei Maldaner</b> · formação Profissional 2030 no inema.club · imagens: ilustração",
   abre=("O SAAS ESTÁ MORRENDO", "E TEM GENTE APOSTANDO TUDO NELE", "vermelho #ff2a1f",
         "um cartão de crédito preto gigante com o símbolo de assinatura (duas setas em círculo) gravado em dourado, rachando ao meio e explodindo em estilhaços sobre uma mesa preta, luz forte vinda de cima"),
   imgs=[("refaz.png", "um robô humanoide de visor preto montando sozinho, peça por peça, uma interface de aplicativo luminosa dourada flutuando no ar, numa oficina escura; ao lado, um calendário de mesa sem letras com dois dias marcados em amarelo"),
         ("quebra.png", "escritório de uma empresa de software abandonado à noite: cadeiras viradas, caixas de mudança, monitores apagados e empoeirados, uma única luminária amarela acesa"),
         ("ciclos.png", "um corredor escuro com quatro portas em sequência, cada uma mais moderna que a anterior (madeira velha, vidro, metal, e a última uma porta de luz dourada aberta); uma pessoa de costas indo para a última"),
         ("dica.png", "uma consultora de costas ao lado do dono de uma pequena oficina, os dois olhando um tablet com painéis amarelos luminosos; oficina escura com luz quente de destaque")],
   telas=[["capa/abertura-desce.png", None], ["capa/refaz.png", "f2"], ["capa/quebra.png", "f3"], ["capa/ciclos.png", "f4"],
          ["capa/dica.png", "f5"], ["prints/prof2030-c.png", "f6", "inematds.github.io/prof2030"], ["prints/club-c.png", "f7", "inema.club"]],
   paineis=[{"de": ["f1", "apostando"], "k": "MODELO DE ASSINATURA", "borda": "red", "itens": [["f1", "assina", "💳 você assina todo mês"], ["f1", "morrendo", "📉 está morrendo"], ["f1", "apostando", "🎰 e tem gente apostando tudo"]]},
            {"de": "f2", "k": "A IA REFAZ", "itens": [["f2", "programa", "🧩 o programa da assinatura"], ["f2", "medida", "✂️ sob medida"], ["f2", "semana", "📅 num fim de semana"]]},
            {"de": "f3", "k": "FORMATO VELHO", "borda": "red", "itens": [["f3", "velho", "🏚️ quem fica no velho"], ["f3", "quebra", "💥 quebra junto"]]},
            {"de": "f4", "k": "JÁ VI ISSO ANTES", "itens": [["f4", "passei", "🔁 várias vezes"], ["f4", "igual", "📌 sempre igual"]]},
            {"de": "f5", "k": "A DICA PARA 2027", "borda": "vd", "itens": [["f5", "dica", "💡 a dica"], ["f5", "novo", "🆕 o formato novo"], ["f5", "jeito", "🏢 IA do jeito de cada empresa"]]},
            {"de": "f6", "k": "PROFISSIONAL 2030", "borda": "vd", "itens": [["f6", "formação", "🎓 formação Profissional 2030"], ["f6", "graça", "🆓 de graça"]]}],
   cta=("VOCÊ AINDA PAGA QUAL ASSINATURA? 👇", "me pede o link aqui nos comentários"), club="formação Profissional 2030, grátis",
   cores={"saas": "#ff2a1f", "morrendo": "#ff2a1f", "apostando": "#ff2a1f", "refaz": "#FACC15", "velho": "#ff2a1f",
          "quebra": "#ff2a1f", "dica": "#FACC15", "novo": "#FACC15", "graca": "#FACC15"}),
 "chat": dict(r7="chat-ao-agente", grupos=[2, 1, 1, 1, 1, 1, 2], troca={},
   marca="INEMA · DO CHAT AO AGENTE", selo="EVENTOS INEMA",
   fonte="<b>inematds.github.io/do-chat-ao-agente-v72</b> · imagens: ilustração · print da página",
   abre=("VOCÊ AINDA COPIA E COLA?", "SAI NA FRENTE: DO CHAT AO AGENTE", "amarelo #FACC15",
         "uma pessoa de costas, exausta, de madrugada, copiando e colando entre duas janelas no notebook, cercada de post-its; atrás de uma parede de vidro, vários robôs humanoides de visor preto trabalhando sozinhos em mesas com telas, em luz dourada"),
   imgs=[("copiacola.png", "close de mãos num teclado à noite, monitor com uma janela de chat e várias janelas abertas, setas luminosas de copiar e colar indo e voltando, xícara de café; cansaço"),
         ("terminal.png", "monitor com um terminal escuro, árvore de pastas e arquivos (formas ilegíveis), um robô de visor preto ao lado digitando sozinho; um check amarelo grande brilhando; mesa organizada"),
         ("colega.png", "escritório à noite: em primeiro plano, uma pessoa de costas afundada em papéis e janelas abertas; ao fundo, um colega relaxado de braços atrás da cabeça, com o trabalho entregue e um painel amarelo na tela"),
         ("gratis.png", "uma porta dourada luminosa entreaberta num corredor escuro, começando a se fechar; uma ampulheta dourada no chão com a areia caindo")],
   telas=[["capa/abertura-desce.png", None], ["capa/copiacola.png", "f2"], ["capa/terminal.png", "f3"], ["capa/colega.png", "f4"],
          ["prints/chat72-c.png", "f5", "inematds.github.io/do-chat-ao-agente-v72"], ["capa/gratis.png", "f6"], ["prints/club-c.png", "f7", "inema.club"]],
   paineis=[{"de": ["f1", "chat"], "k": "SAI NA FRENTE", "itens": [["f1", "chat", "💬 continua usando o chat"], ["f1", "agentes", "🤖 e os agentes produzem"]]},
            {"de": "f2", "k": "NO CHAT", "borda": "red", "itens": [["f2", "pergunta", "❓ você pergunta"], ["f2", "copia", "📋 copia"], ["f2", "cola", "📌 cola"]]},
            {"de": "f3", "k": "NO TERMINAL", "borda": "vd", "itens": [["f3", "arquivos", "📁 abre os seus arquivos"], ["f3", "executa", "⚙️ executa"], ["f3", "pronto", "✅ entrega pronto"]]},
            {"de": "f4", "k": "SÓ NO CHAT?", "borda": "red", "itens": [["f4", "colega", "🏃 o colega entrega antes"], ["f4", "dia", "📆 todo dia"]]},
            {"de": "f5", "k": "DO CHAT AO AGENTE", "itens": [["f5", "curso", "🎓 o curso"], ["f5", "zero", "0️⃣ passo a passo do zero"]]},
            {"de": "f6", "k": "GRÁTIS AGORA", "borda": "vd", "itens": [["f6", "grátis", "🆓 grátis agora"], ["f6", "PRO", "🔒 depois só no PRO"]]}],
   cta=("VOCÊ AINDA COPIA E COLA? 👇", "me pede o link aqui nos comentários"), club="curso Do chat ao agente",
   cores={"chat": "#FACC15", "agentes": "#FACC15", "copia": "#ff2a1f", "cola": "#ff2a1f", "terminal": "#FACC15",
          "pronto": "#FACC15", "colega": "#ff2a1f", "gratis": "#FACC15", "pro": "#ff2a1f"}),
 "demissao": dict(r7="demissao-gestores", grupos=[1, 1, 2, 1, 1, 1, 2], troca={"nove aulas": "9 aulas", "quinze minutos": "15 minutos"},
   marca="INEMA · GESTÃO 2027", selo="ALERTA INEMA",
   fonte="<b>opinião do Nei Maldaner</b> · formação Empresas de 2027 no inema.club · imagens: ilustração",
   abre=("DEMISSÃO EM MASSA", "DE GERENTES E EXECUTIVOS", "vermelho #ff2a1f",
         "corredor de escritório corporativo escuro, vários executivos de terno de costas saindo em fila, cada um carregando uma caixa de papelão com seus objetos; luz fria e uma faixa de luz vermelha no fim do corredor"),
   imgs=[("tres.png", "três pilares de luz numa sala escura, cada um com um símbolo flutuando em dourado: um grupo de pessoas, um conjunto de engrenagens e a cabeça de um robô de visor preto"),
         ("fila.png", "fila de executivos de terno, de costas, esperando num corredor escuro diante de uma porta com luz vermelha; um deles olha um celular com uma janela de IA aberta, perdido"),
         ("aulas.png", "um cronômetro dourado luminoso marcando um quarto de volta sobre uma mesa preta, ao lado de um celular com uma conversa de IA aberta; luz amarela limpa"),
         ("comando.png", "uma executiva de costas, confiante, diante de um painel gigante luminoso com quadros amarelos de tarefas e indicadores, comandando com um gesto dois robôs humanoides de visor preto")],
   telas=[["capa/abertura-desce.png", None], ["capa/tres.png", "f2"], ["capa/fila.png", "f3"], ["prints/emp27-c.png", "f4", "inematds.github.io/empresas-2027-v62"],
          ["capa/aulas.png", "f5"], ["capa/comando.png", "f6"], ["prints/club-c.png", "f7", "inema.club"]],
   paineis=[{"de": ["f1", "demissão"], "k": "DEMISSÃO EM MASSA", "borda": "red", "itens": [["f1", "gerentes", "👔 gerentes"], ["f1", "executivos", "💼 executivos"]]},
            {"de": "f2", "k": "QUEM SAI", "borda": "red", "itens": [["f2", "pessoas", "👥 não gere pessoas"], ["f2", "processos", "⚙️ nem processos"], ["f2", "agentes", "🤖 nem agentes"]]},
            {"de": "f3", "k": "GENTE BOA NA FILA", "borda": "red", "itens": [["f3", "demore", "🙏 espero que demore"], ["f3", "agente", "🤖 não sabe lidar com agente"], ["f3", "fila", "⏳ está na fila"]]},
            {"de": "f4", "k": "EMPRESAS DE 2027", "itens": [["f4", "formação", "🎓 formação rápida"], ["f4", "executivos", "💼 para executivos"]]},
            {"de": "f5", "k": "RÁPIDA DE VERDADE", "borda": "vd", "contador": {"ate": 9, "em": ["f5", "9"], "cor": "#FACC15", "unid": "AULAS DE 15 MIN"},
             "l": "sem instalar nada · no chat que você já usa"},
            {"de": "f6", "k": "VOCÊ NO COMANDO", "borda": "vd", "itens": [["f6", "regras", "📜 escreve as regras do agente"], ["f6", "medir", "📊 mede o trabalho dele"]]}],
   cta=("VOCÊ JÁ GERENCIA AGENTES? 👇", "me pede o link aqui nos comentários"), club="formação Empresas de 2027",
   cores={"demissao": "#ff2a1f", "massa": "#ff2a1f", "gerentes": "#ff2a1f", "executivos": "#ff2a1f", "pessoas": "#FACC15",
          "processos": "#FACC15", "agentes": "#FACC15", "fila": "#ff2a1f", "regras": "#FACC15", "medir": "#FACC15"}),
 "gestor": dict(r7="novas-funcoes-gestao", grupos=[1, 1, 3, 1, 1, 1, 2],
   troca={"regra cinco, quatro, três: cinco perguntas, quatro níveis": "regra 5-4-3: 5 perguntas, 4 níveis", "e três casos": "e 3 casos"},
   marca="INEMA · O NOVO GESTOR", selo="GESTÃO INEMA",
   fonte="<b>guia Diga o que importa</b> (grátis) · curso Constituição dos Agentes · inema.club · imagens: ilustração",
   abre=("SEU NOVO FUNCIONÁRIO", "NÃO É GENTE", "vermelho #ff2a1f",
         "reunião de equipe numa sala escura com luz dramática: entre as pessoas sentadas à mesa, de costas ou de lado, um robô humanoide estilo Tesla Optimus de visor preto, com um crachá no peito, sentado numa cadeira; a gestora de pé olhando para ele"),
   imgs=[("funcoes.png", "uma gestora de costas no centro de um escritório escuro: à esquerda, uma equipe de pessoas em mesas; à direita, uma equipe de robôs humanoides de visor preto em mesas; linhas de luz amarela ligando os dois lados a ela"),
         ("facil.png", "uma gestora experiente de costas, braços cruzados, confiante, no chão de uma pequena fábrica à noite, com a equipe trabalhando sob luzes amarelas"),
         ("time.png", "três figuras numa sala escura ligadas por linhas de luz amarela: uma gestora apontando um caminho, um técnico com um notebook, e um robô humanoide de visor preto executando uma tarefa num painel")],
   telas=[["capa/abertura-desce.png", None], ["capa/funcoes.png", "f2"], ["capa/facil.png", "f3"], ["capa/time.png", "f4"],
          ["prints/diga-c.png", "f5", "inematds.github.io/diga-o-que-importa"], ["prints/const-c.png", "f6", "inematds.github.io/constituicao-agentes-v62"], ["prints/club-c.png", "f7", "inema.club"]],
   paineis=[{"de": ["f1", "chefiar"], "k": "FUNCIONÁRIO QUE NÃO É GENTE", "borda": "red", "itens": [["f1", "funcionário", "🤖 funcionário que não é gente"], ["f1", "chefiar", "👔 alguém vai chefiar"]]},
            {"de": "f2", "k": "NOVAS FUNÇÕES", "itens": [["f2", "transformação", "🔄 a transformação"], ["f2", "funções", "🧭 aprender as novas funções"]]},
            {"de": "f3", "k": "PRA GESTOR É FÁCIL", "borda": "vd", "itens": [["f3", "processo", "⚙️ o processo"], ["f3", "cliente", "🤝 o cliente"], ["f3", "equipe", "👥 a equipe"], ["f3", "ajusta", "🔧 só ajusta"]]},
            {"de": "f4", "k": "UM TIME DE 3", "itens": [["f4", "gestor", "🧭 gestor: o quê e o porquê"], ["f4", "técnico", "🛠️ técnico: o como"], ["f4", "executa", "🤖 agente: executa"]]},
            {"de": "f5", "k": "REGRA 5-4-3", "itens": [["f5", "perguntas", "5️⃣ perguntas"], ["f5", "níveis", "4️⃣ níveis de autonomia"], ["f5", "casos", "3️⃣ casos de teste"]]},
            {"de": "f6", "k": "A CONSTITUIÇÃO DO AGENTE", "borda": "vd", "itens": [["f6", "faz", "✅ o que ele faz"], ["f6", "nunca", "⛔ o que nunca faz"], ["f6", "chama", "📞 quando chama você"]]}],
   cta=("VOCÊ JÁ CHEFIA UM AGENTE? 👇", "me pede o link aqui nos comentários"), club="guia grátis + Constituição dos Agentes",
   cores={"funcionario": "#FACC15", "gente": "#ff2a1f", "chefiar": "#FACC15", "transformacao": "#FACC15", "facil": "#FACC15",
          "ajusta": "#FACC15", "gestor": "#FACC15", "tecnico": "#FACC15", "agente": "#FACC15", "constituicao": "#FACC15"}),
}
PRINTS = {"prof2027-c.png": "prof2027.png", "prof2030-c.png": "prof2030.png", "chat72-c.png": "chat72.png",
          "emp27-c.png": "emp27.png", "diga-c.png": "diga.png", "const-c.png": "const.png"}


def frases(txt):
    return [s for s in re.split(r"(?<=[.?!])\s+", txt.strip()) if s]


for slug, c in R.items():
    E = EV / f"2026-10-18-r7e-{slug}"
    for d in ("avatar", "capa", "prints", "build"):
        (E / d).mkdir(parents=True, exist_ok=True)
    src = R7 / f"2026-10-18-{c['r7']}"
    rot = yaml.safe_load((src / "roteiro.yaml").read_text())
    if not (E / "avatar/avatar.mp4").exists():
        shutil.copy(src / "avatar/avatar.mp4", E / "avatar/avatar.mp4")
    shutil.copy(MODELO / "avatar/retempo.py", E / "avatar/retempo.py")
    shutil.copy(MODELO / "capa/preto.png", E / "capa/preto.png")
    (E / "avatar/APROVADO_HEYGEN").write_text(f"Reaproveita o avatar já gerado e aprovado em {src} (Nei, 18/10/2026: \"refaça todos eles com o "
                                              "mesmo avatar\"). Nenhuma geração nova no HeyGen.\n")
    fs = frases(rot["fala"]); assert sum(c["grupos"]) == len(fs), (slug, len(fs), fs)
    falas, k = [], 0
    for i, g in enumerate(c["grupos"]):
        fala = " ".join(fs[k:k + g]); k += g
        leg = fala
        for a, b in {**COMUM, **c["troca"]}.items():
            leg = leg.replace(a, b)
        falas.append({"id": f"f{i + 1}", "fala": fala, "legenda": leg})
    (E / "falas.json").write_text(json.dumps(falas, ensure_ascii=False, indent=1))
    a, b, cor, cena = c["abre"]
    linhas = [f"1. abertura.png — capa de impacto: {cena}. " + ABRE.format(a=a, b=b, cor=cor)]
    linhas += [f"{i + 2}. {nome} — {desc}." for i, (nome, desc) in enumerate(c["imgs"])]
    (E / "capa/pedido.txt").write_text(f"Gere {len(linhas)} imagens com a ferramenta de geração de imagem (image_gen) e salve nesta pasta, "
                                       f"em PNG, formato RETRATO 9:16 (o maior tamanho vertical disponível). {ESTILO}\n\n" + "\n".join(linhas) +
                                       "\n\nAo final, liste os arquivos salvos.\n")
    for _, *rest in c["telas"]:
        pass
    usados = {t[0].split("/")[-1] for t in c["telas"] if t[0].startswith("prints/")}
    ev_util.print_card(RAW / "inemaclub.png", E / "prints/club-c.png", escuro=True)
    for p in usados - {"club-c.png"}:
        ev_util.print_card(RAW / PRINTS[p], E / "prints" / p, escuro=True)
    telas = []
    for t in c["telas"]:
        d = {"src": t[0], "de": t[1]}
        if len(t) > 2:
            d["selo"] = t[2]
        telas.append(d)
    ficha = {"marca": c["marca"], "selo": c["selo"], "telas": telas, "paineis": c["paineis"],
             "cta": {"em": ["f7", "pede"], "a": c["cta"][0], "b": c["cta"][1]},
             "club": {"em": ["f7", "inema.club"], "a": "inema.club", "b": c["club"]}, "fonte": c["fonte"], "cores": c["cores"]}
    (E / "ficha.json").write_text(json.dumps(ficha, ensure_ascii=False, indent=1))
    print(slug, "ok:", E.name, "·", len(falas), "falas ·", len(linhas), "imagens ·", len(usados), "prints")
