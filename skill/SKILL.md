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
antes da etapa 5. **Fecho padrão da fala:** "Tá tudo no inema ponto club. Ou comenta <PALAVRA> que eu
te mando o link." (o funil de DM do "comenta" não está automatizado — o site é o caminho principal).
Se houver número na etapa Medo, com fonte.

## Passo a passo

1. **Roteiro.** `cd ~/projetos/reel7etapas && python3 reel7etapas.py novo <slug>`. Reescreva `fala`
   (550–700 caracteres ≈ 40 s; "inema ponto club"; número/ano por extenso) e as 7 `etapas`:
   `ancora` (palavra da fala que aparece uma vez depois da etapa anterior; evite nomes próprios — o
   Whisper erra), `linha1/linha2` (curtas), `destaque` opcional `{titulo, texto, cor}`, `camera`
   (`push|pull|pan_dir|pan_esq|sobe`, alterne), `foco` [x,y] do plano fechado, `cena` (prompt em
   português, concreto, com pessoas/objetos reais — o motor já impõe estilo e composição), `gatilho`
   e `por_que` (só no mapa). Etapa 1 usa `capa` (`ganho:` = faixa no topo do quadro 0 com o que a pessoa ganha, ex. "O SEU PRÓPRIO SOFTWARE, SEM PAGAR ASSINATURA"; em teste desde 12/10). Se o Nei disser "o ganho é X", X vai em `capa.ganho`, em MAIÚSCULAS, curto (≤ 2 linhas). Se ele não disser, escreva você o ganho a partir da promessa do reel; nunca deixe o quadro 0 sem ganho. `cta: {ancora: comenta, palavra: X, linha2: ...}`.
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
- áudio −14 LUFS (loudnorm em 2 passadas) e `qa_short.py` do makeshorts (perfil divulgacao) aprovado

## Regras

- Imagem: Codex `image_gen` pela assinatura; flux2-klein só reserva ou pedido explícito.
- Avatar só pelo estúdio do HeyGen (assinatura), nunca API de geração; nunca aceitar troca de plano.
- Falhou? Linha no `FALHAS.md` (data | o que quebrou | menor correção | prompt/infra).
