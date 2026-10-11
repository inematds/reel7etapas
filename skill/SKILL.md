---
name: reel7etapas
description: >-
  Ideia/texto de reel → reel 9:16 do Nei no modelo de 7 ETAPAS DE GATILHO (gancho → desejo → medo →
  facilidade → descoberta → benefício → comentário): avatar do Nei (estúdio HeyGen), uma imagem
  flux2-klein por etapa, manchete e painel por etapa, legenda palavra a palavra e fecho "COMENTA
  <PALAVRA>"; entrega no bot v3 e gera o mapa das etapas. Gatilho: "/reel7etapas", "reel em 7 etapas",
  "modelo de gatilhos", "faz o reel com gatilhos", ou um texto de reel com "comenta X" no fim.
---

# reel7etapas — uma ideia vira o reel de 7 etapas

Repo: `~/projetos/reel7etapas` (inematds/reel7etapas). Tudo roda por `reel7etapas.py`.
Exemplo de referência (o primeiro): `edicoes/2026-10-11-jarvis/roteiro.yaml` — "Seu próprio JARVIS".
Guia: https://inematds.github.io/reel7etapas/guia/

## O modelo (a ordem importa)

| # | Etapa | Pergunta que a etapa responde | Exemplo JARVIS |
|---|---|---|---|
| 1 | Gancho | Qual o resultado que qualquer um quer, em 2 s? | "VOCÊ DORME. ELE TRABALHA." |
| 2 | Desejo | O que a pessoa quer ter? | um funcionário dentro do PC |
| 3 | Medo | O que ela tem medo de perder/gastar? | tem gente pagando uma fortuna |
| 4 | Facilidade | Qual objeção faz desistir? Derrube. | não precisa ser programador |
| 5 | Descoberta | Qual é a solução, com nome e verbos? | crie o seu próprio JARVIS |
| 6 | Benefício | Como fica a vida depois? | um funcionário digital só seu |
| 7 | Comentário | Qual ação pequena ela faz agora? | COMENTA JARVIS |

Regras: mostrar o resultado antes da tecnologia; uma tese por vídeo; fundo escuro, luz dourada,
sem robô futurista; nada de jargão (IA, agente, LLM) antes da etapa 5.

## Passo a passo

1. **Roteiro.** `cd ~/projetos/reel7etapas && python3 reel7etapas.py novo <slug>` copia o exemplo.
   Reescreva `fala` (550–700 caracteres ≈ 40 s; "inema ponto club"; número/ano por extenso) e as 7
   `etapas`: `ancora` (palavra da fala, minúscula, sem acento, que aparece UMA vez depois da etapa
   anterior — evite a palavra do CTA e nomes próprios, o Whisper erra), `linha1/linha2`, `painel`,
   `cena` (prompt em inglês, sem texto), `gatilho` e `por_que` (só no mapa). A etapa 1 usa `capa`.
   A 7 pode ter `depois` (troca na palavra "comenta").
2. **Imagens:** `python3 reel7etapas.py imagens edicoes/<pasta>` (flux2-klein local, ~1 min).
3. **Trilha:** `python3 ~/projetos/cardshorts/cardshorts.py musica edicoes/<pasta>/build/trilha.wav "<prompt>"`
   (MusicGen local; sem trilha usa a reserva do reelcomenta).
4. **Prévia:** `python3 reel7etapas.py previa edicoes/<pasta>` → olhe `previa.jpg` (texto cortado, imagem errada).
5. **Avatar:** grave `avatar/APROVADO_HEYGEN` com a frase do pedido e a data, e rode
   `python3 reel7etapas.py avatar edicoes/<pasta>` em segundo plano (fila do estúdio: 5 min a 1 h).
6. **Montar e conferir:** `montar` (para se a fala ouvida divergir < 85%), `conferir` (olhe `conferencia.jpg`)
   e `mapa` (gera `mapa.jpg` com as 7 etapas e `capa.jpg`).
7. **Entregar:** `python3 reel7etapas.py enviar edicoes/<pasta> "<legenda>"` (bot v3).
   YouTube pelo `yt-pubx` (canal que o Nei disser; padrão lives1; short não leva thumb).

## Regras

- Avatar só pelo estúdio do HeyGen (assinatura), nunca API de geração; nunca aceitar troca de plano.
- Falhou? Linha no `FALHAS.md` (data | o que quebrou | menor correção | prompt/infra).
