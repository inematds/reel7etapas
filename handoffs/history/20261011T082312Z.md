# Handoff — reel7etapas (11/10/2026)

## Objetivo
Motor `reel7etapas.py` para transformar uma ideia em reel 9:16 no modelo de 7 etapas de gatilho (gancho → desejo → medo → facilidade → descoberta → benefício → comentário), com o avatar do Nei (estúdio HeyGen), e publicar no bot, no YouTube, no portal e no INEMA.NCIA. O Nei vai usar muito: o foco é o motor ser confiável.

## Estado (tudo no origin)
- Repo `inematds/reel7etapas` (último commit ee8d3d5). Guia PT/EN/ES: https://inematds.github.io/reel7etapas/guia/ (200 nos 3).
- Exemplo JARVIS v2 publicado: Short https://www.youtube.com/shorts/V92t50ceCRg (lives1, descrição corrigida com o link do guia), release `video-v1.1.0`, bot (vídeo + mapa + relatório), INEMA.NCIA https://t.me/c/2414677686/1032.
- Portal: card do projeto + quadro de vídeos atualizados (portal 09855ab, inemabuscas 8629bf3, inemapro bcb33e6).
- v1 continua publicado; **o Nei remove**: Short PIa_eXWFk7s, tópico NCIA /1012, release video-v1.0.0.

## Regras novas do Nei (11/10)
- Sem portão de aprovação: eu valido (portões do motor + folhas em tamanho real) e publico impecável. Memória: `reel-sem-aprovacao`.
- Imagem: Codex `image_gen` é o padrão; flux2-klein só reserva ou pedido explícito. Memória: `imagem-codex-padrao`. **Conflita com o CLAUDE.md global** ("flux2-klein por padrão"): perguntei se ajusto a linha; não editei.
- Fecho das próximas falas: "Tá tudo no inema ponto club. Ou comenta <PALAVRA> que eu te mando o link." (o avatar do JARVIS fica como está).

## Motor v2 (o que existe)
`novo` · `fazer` (imagens → avatar → montar → validar → mapa) · `imagens <pasta> [n…]` · `montar` · `validar` (ritmo + qa_short.py do makeshorts + folhas em build/revisao) · `mapa` · `publicar` (bot + yt-pubx). Portões: imagem vertical/clara/sem repetição (refaz até 3×), zona segura x 65–950 y 192–1536, legenda ≤3 palavras e ≥64 px por segmentação de frase, manchete ≥80 px, texto dos cartões dentro do cartão, imagem muda ≤3,5 s, fala ≥85%, −14 LUFS, qa_short aprovado. Testado de ponta a ponta (`novo` e `fazer`).

## Próxima ação exata
Nenhuma pendente do pedido. Ideias de melhoria nos outros reels: `IDEIAS-OUTROS-REELS.md` (top 5). Falhas registradas em `FALHAS.md`.

## Armadilhas
- Montserrat Black em 72 px não cabe "TEM GENTE PAGANDO": a legenda usa 66 px.
- O Whisper separa ".club"; o motor junta com a palavra anterior.
- O Codex às vezes põe o assunto no terço de cima; a regra de composição está no ESTILO do motor, mas confira com os olhos.
