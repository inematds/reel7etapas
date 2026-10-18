---
name: reel7etapas
description: >-
  Ideia/texto de reel → reel 9:16 do Nei no modelo de 7 ETAPAS DE GATILHO (gancho → desejo → medo →
  facilidade → descoberta → benefício → comentário): avatar do Nei (estúdio HeyGen), uma imagem do
  Codex por etapa com movimento de câmera, manchete e destaque na palavra certa, legenda curta, fecho
  "TUDO NO INEMA.CLUB · ou comenta <PALAVRA>"; portões de qualidade e publicação no bot + YouTube.
  Gatilho: "/reel7etapas", "reel em 7 etapas", "modelo de gatilhos", "faz o reel com gatilhos", ou
  um texto de reel com "comenta X" no fim.
---

# reel7etapas — uma ideia vira o reel de 7 etapas

Repo: `~/projetos/reel7etapas` (inematds/reel7etapas). Tudo roda por `reel7etapas.py`.
Exemplo de referência: `edicoes/2026-10-11-jarvis/roteiro.yaml` — "Seu próprio JARVIS" (v2: https://www.youtube.com/shorts/V92t50ceCRg).
Guia: https://inematds.github.io/reel7etapas/guia/

**Sem portão de aprovação do Nei** (pedido de 11/10/2026): você valida — portões do motor + leitura das
folhas em tamanho real — e publica já impecável. Ele confere depois.

## Propósito e plano (D10 do inema-design, Nei 18/10/2026 — vem ANTES de tudo)

**Objetivo: trazer público para o inema.club.** "Se não viralizar, não atingiu o objetivo." CTA fixo: "Tá tudo no
inema ponto club. Ou me pede o link aqui nos comentários."

Antes de escrever a fala, grave `plano.md` na pasta da edição:
1. **Pessoa:** público geral (IA traduzida para o dia a dia), não o nicho que já usa Claude/Codex.
2. **O que ela quer:** ganhar algo, resolver uma dor ou chegar a um desejo. Uma frase.
3. **Gancho:** o gatilho (medo, novidade ou provocação) com o fato/número e a fonte (D9).
4. **Nota de potencial 0–10:** "um desconhecido rolando o feed para aqui?". Abaixo de 7, troque o ângulo ou proponha outro tema
   ("faxina no setup", "camada de contexto" = nicho, nota baixa).
5. **Visuais que ensinam:** pelo menos 2 diagramas/visuais por reel (barra comparando, antes/depois, fluxo, print real
   com o detalhe em destaque), além das fotos.
6. **Cada etapa forte:** as 7 etapas são checklist de gatilhos, não ordem obrigatória; nenhuma etapa morna.

Só depois do plano: fala → avatar (novo, no estúdio, com `APROVADO_HEYGEN` daquela produção) → imagens → montar.
**Rosto desde o quadro 0** em meia tela, passando a PiP na etapa 2 (nunca tela cheia; D8).

## O modelo (a ordem importa)

| # | Etapa | Pergunta que a etapa responde | Exemplo JARVIS |
|---|---|---|---|
| 1 | Gancho | Qual o resultado que qualquer um quer, em 2 s? | "VOCÊ DORME. ELE TRABALHA." |
| 2 | Desejo | O que a pessoa quer ter? | um funcionário dentro do PC |
| 3 | Medo | O que ela tem medo de perder/gastar? | tem gente pagando uma fortuna |
| 4 | Facilidade | Qual objeção faz desistir? Derrube. | não precisa ser programador |
| 5 | Descoberta | Qual é a solução, com nome e verbos? | crie o seu próprio JARVIS |
| 6 | Benefício | Como fica a vida depois? | um funcionário digital só seu |
| 7 | Comentário | Onde está e qual ação pequena ela faz agora? | TUDO NO INEMA.CLUB · ou comenta JARVIS |

Regras de texto: resultado antes da tecnologia; uma tese por vídeo; sem jargão (IA, agente, LLM)
antes da etapa 5. **Fecho padrão da fala (14/10):** "Tá tudo no inema ponto club. Quer o link? Me pede aqui nos
comentários." — sem palavra-chave enquanto a resposta não for automatizada; no roteiro,
`cta: {ancora: link, linha1: "quer o link?", palavra: "ME PEDE", linha2: "aqui nos comentários"}`.
**Gancho com conflito concreto** (uma cena que o dono de negócio reconhece, ex. "o cliente pede um desconto que
ninguém aprovou; o agente aceita") e **sem promessa de perfeição** ("reduz erro", "sabe quando chamar você").
**Cenário único:** as 6 cenas no mesmo lugar e com a mesma pessoa descrita igual em cada `cena`; mostrar a coisa
de verdade (print) com `imagem: img/<arquivo>.png` na etapa (mockup em janela sobre fundo claro, sem `destaque`
para o print aparecer). Crítica de 13/10 do reel da constituição.
**Visual (escolha do Nei, 14/10):** padrão = B (`abre`): o avatar abre o vídeo aberto, largura toda, SEM moldura,
sobre a capa desfocada e escurecida (`capa.desfoque: 0` desliga); da etapa 2 em diante, imagem em tela cheia, cartão
à esquerda e avatar no quadradinho à direita. Opção A = `layout: quadro`: avatar aberto do começo ao fim (termina em
y 1800, fora do título do Shorts); em cima, fundo liso, manchete e a imagem num quadro sem texto por cima (sem cartão
de destaque). `layout: caixa` = o antigo (caixa com moldura também na capa). Os dois estão no guia (#visuais).
Se houver número na etapa Medo, com fonte.

## Passo a passo

**Gancho = GATILHO (D9 do inema-design, Nei 18/10/2026 — vence o "capa = ganho" abaixo, que fica só no histórico):**
o quadro 0, a faixa (`capa.ganho`), a manchete e a 1ª frase da fala mexem com a pessoa — **medo, novidade ou
provocação** — com fato/número concreto e fonte (ex.: "HACKERS ROUBARAM AS CHAVES · US$ 1.700 NUMA NOITE",
"US$ 6 → 23 CENTAVOS", "SE FECHAREM A SUA CONTA, SEU NEGÓCIO VAI JUNTO?"). Nunca promessa/benefício no quadro 0 e
nunca desarmar o medo na 1ª frase ("mas dá pra dormir tranquilo" vai para a facilidade). Imagem do gancho = o
flagrante, NÍTIDA (`capa.desfoque: 0`), luz dramática liberada (na etapa 1: `cor_livre: true`, `luz_min: 25` e `estilo:` próprio com a luz e a
composição; com `cor_livre` o motor ignora `luz:`; modelo nos roteiros `*-gatilho` de 18/10). Capa sem avatar
(`layout: caixa` + `capa.avatar: false`, manchete em `capa.y: 1110`) e `letra: forte` (#FACC15 + contorno). O
ganho/alívio entra da etapa 4 em diante. Título do post (yt-pubx/TikTok/Instagram) com o mesmo gatilho.

1. **Roteiro.** `cd ~/projetos/reel7etapas && python3 reel7etapas.py novo <slug>`. Reescreva `fala`
   (550–700 caracteres ≈ 40 s; "inema ponto club"; número/ano por extenso) e as 7 `etapas`:
   `ancora` (palavra da fala que aparece uma vez depois da etapa anterior; evite nomes próprios — o
   Whisper erra), `linha1/linha2` (curtas), `destaque` opcional `{titulo, texto, cor}`, `camera`
   (`push|pull|pan_dir|pan_esq|sobe`, alterne), `foco` [x,y] do plano fechado, `cena` (prompt em
   português, concreto, com pessoas/objetos reais — o motor já impõe estilo e composição), `gatilho`
   e `por_que` (só no mapa). Etapa 1 usa `capa` (`ganho:` = faixa no topo do quadro 0 com o que a pessoa ganha, ex. "O SEU PRÓPRIO SOFTWARE, SEM PAGAR ASSINATURA"; em teste desde 12/10). Se o Nei disser "o ganho é X", use X como ideia e reescreva para ficar impactante e viral (pedido dele em 12/10: "o ganho pode ser ajustado por você"), mantendo o sentido: MAIÚSCULAS, curto (≤ 2 linhas, ~6 palavras), ganho concreto da pessoa. Se ele não disser, escreva você o ganho a partir da promessa do reel; nunca deixe o quadro 0 sem ganho. O avatar do Nei aparece GRANDE no quadro 0 (centro, 700×794; motor 12/10: o rosto dele é autoridade) e encolhe para o canto na etapa 2; o texto da capa encolhe sozinho para caber entre o ganho e o avatar, então ganho curto (≤ 2 linhas) deixa a capa legível. `capa.avatar: false` desliga só se o Nei pedir. `cta: {ancora: comenta, palavra: X, linha2: ...}`.
2. **Trilha (opcional):** `python3 ~/projetos/cardshorts/cardshorts.py musica edicoes/<pasta>/build/trilha.wav "<prompt>"`.
3. **Avatar:** grave `avatar/APROVADO_HEYGEN` (frase do pedido + data). `fazer` chama o estúdio se faltar
   o `avatar/avatar.mp4` (fila de 5 min a 1 h — rode em segundo plano).
4. **Fazer:** `python3 reel7etapas.py fazer edicoes/<pasta>` = imagens (Codex image_gen, 7 em paralelo;
   flux2-klein local só se o Codex falhar) → portão das imagens → avatar → montar → validar → mapa.
5. **Revisar você mesmo:** leia cada imagem em ≥ 540 px (assunto na faixa 30–60% da altura? nada fora
   do assunto?) e `build/revisao/folha-*.jpg` (quadro 0, cada etapa, CTA, fim). Refaça o que falhar:
   `imagens <pasta> 3 7` refaz só as etapas 3 e 7; depois `montar` + `validar`.
6. **Publicar:** `python3 reel7etapas.py publicar edicoes/<pasta>` (bot v3 + YouTube pelo yt-pubx,
   `canal:` do roteiro, padrão lives1). Depois: portal (`atualiza-portal`) e, se pedido, INEMA.NCIA (`postar-telegram`).

## Portões (bloqueiam; a mensagem diz qual e por quê)

- imagens: vertical, centro com luz ≥ 55/255, nenhuma parecida com outra (dHash) — refaz até 3×
- zona segura: todo texto/caixa em x 65–950, y 192–1536 (topo 10%, base 20%, coluna de botões 12%)
- fonte: legenda ≥ 64 px, manchete ≥ 80 px; texto dos cartões não sai do cartão (quebra em 2 linhas)
- legenda: ≤ 3 palavras, cabe na largura, cortes por frase sem terminar em palavra fraca
- ritmo: imagem muda a cada ≤ 3,5 s (cortes de reenquadramento dentro da etapa)
- fala do avatar ≥ 85% igual ao roteiro; âncoras ≥ 0,5 s uma da outra
- duração: reel 9:16 nunca chega a 3 min — roteiro planejado para ≤ 2:40 (160 s); passar um pouco é tolerado, ≥ 180 s reprova (Nei, 16/10/2026)
- áudio −14 LUFS (loudnorm em 2 passadas) e `qa_short.py` do makeshorts (perfil divulgacao) aprovado

## Regras

- `cena` clara: de dia, luz de janela. Nunca "à noite", "sala escura" ou "ambiente escuro", a não ser que o assunto exija, porque o estilo do motor já é escuro e o portão de luz (≥ 55) reprova. Isso aconteceu 2× em 11/10.
- `cena` com luz NEUTRA: nunca "luz dourada", "cores quentes", "pôr do sol" nem objeto dourado em toda cena (o gerador do Codex já puxa para o amarelo). O âmbar da marca fica só no texto desenhado por cima. O motor pede luz por etapa (medo frio, benefício dia claro; troque com `luz:` na etapa) e o `cor` neutraliza o que vier acima de 18; acima de 25 depois disso o portão reprova. Imagem que precisa ser quente (fogo, pôr do sol): `cor_livre: true` na etapa. Aconteceu no REA sem travas (12/10): 7 imagens com amarelo 23–53.
- Sigla ou nome próprio na fala (REA, JARVIS, inema.club): depois do avatar, ler as palavras de `build/palavras.json` e corrigir o que o Whisper errou ("ria" → REA, "inema" + ".club" → inema.club) antes do `montar`. O arquivo fica em cache enquanto o avatar não muda.

- Imagem: Codex `image_gen` pela assinatura; flux2-klein só reserva ou pedido explícito.
- Avatar só pelo estúdio do HeyGen (assinatura), nunca API de geração; nunca aceitar troca de plano.
- Falhou? Linha no `FALHAS.md` (data | o que quebrou | menor correção | prompt/infra).
