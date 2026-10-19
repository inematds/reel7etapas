# reel7etapas

[![reel7etapas](guia/assets/banner.jpg)](https://inematds.github.io/reel7etapas/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

> **Novo padrão (18/10/2026): [r7ex](https://github.com/inematds/r7ex).** O roteiro de 7 etapas daqui continua; o vídeo
> agora é montado no acabamento de telejornal do eventosextremospub, num repo próprio e independente. Para reel novo,
> use o r7ex. Este repo segue como o motor antigo (Pillow) e o histórico. Resumo abaixo; a explicação completa está no
> README do r7ex.

## Como chegamos ao r7ex (18/10/2026)

| Lote | Conteúdo | Forma | Resultado |
|---|---|---|---|
| 1. r7e antigo | assunto do dia, nicho, gancho = **promessa**, medo fraco | foto de banco de imagens desfocada, rosto em meia tela, Anton com âmbar | sem visualização no TikTok/Instagram |
| 2. "-gatilho" (mesmo avatar) | fala igual | só o gancho: gatilho + número, imagem nítida, #FACC15 com contorno | melhor, "ainda padrão" |
| 3. D10 | **plano antes da fala**, teses fortes, gatilho primeiro, CTA inema.club, prints reais | este motor, com tarja e diagramas Pillow | "ficou padrão" |
| 4. **r7ex** | o mesmo do lote 3 (mesmo avatar) | motor do eventosextremospub: título na arte, preto e dourado, painéis, contador, karaokê | padrão novo |

- Exemplos: evento extremo de referência https://www.youtube.com/shorts/DfdtX9HbkWg;
  lote 1 https://www.youtube.com/shorts/E5Y94BLfuJU; lote 3 https://www.youtube.com/shorts/xpDV5qQe5oE;
  r7ex https://youtube.com/shorts/DG30IdeqWcg.
- **O conteúdo** acertou no lote 3 (plano, gatilho com número, fala nova). **A forma** acertou no lote 4.

### Como mudar neste repo (motor antigo)
- **Layout:** `reel7etapas.py`: `LAYOUTS` (abre, quadro, caixa…), `letra: forte|tarja` no roteiro, `capa.desfoque`,
  `capa.avatar`; diagramas em `diagramas.py`.
- **Estrutura:** as 7 `etapas` do `roteiro.yaml` (exatamente 7; âncora = palavra da fala onde a etapa começa;
  `passos:` para diagrama em sequência).
- **Planejamento:** regras no `skill/SKILL.md` (gancho = gatilho D9; propósito e plano D10) e no kit inema-design.

## O que é

O reel7etapas é um modelo para escrever vídeos curtos (Reels, Shorts, TikTok) e uma ferramenta que monta esses vídeos sozinha. O roteiro segue sempre a mesma ordem de 7 etapas, pensada para segurar quem está rolando a tela e terminar com um pedido simples: comentar uma palavra. Serve para quem cria conteúdo e quer um caminho repetível, em vez de começar do zero a cada vídeo. Para só usar o modelo, basta ler a tabela das 7 etapas; para gerar o vídeo, a ferramenta usa o avatar do Nei no HeyGen, imagens geradas pelo Codex e um script em Python.

**Uma ideia vira um reel 9:16 em 7 etapas de gatilho** — gancho → desejo → medo → facilidade → descoberta → benefício → comentário — com o avatar do Nei falando, uma imagem por etapa, manchete e painel que trocam na palavra certa da fala, legenda palavra a palavra e o fecho "COMENTA &lt;PALAVRA&gt;".

📖 Guia: **https://inematds.github.io/reel7etapas/guia/**

![As 7 etapas no exemplo JARVIS](edicoes/2026-10-11-jarvis/mapa.jpg)

## O modelo

| # | Etapa | O que faz | Exemplo (JARVIS) |
|---|---|---|---|
| 1 | Gancho | mostra o resultado desejado em 2 s, antes da tecnologia | "VOCÊ DORME. ELE TRABALHA." |
| 2 | Desejo | a pessoa se imagina com o que quer | um funcionário dentro do PC |
| 3 | Medo | o risco de estar gastando à toa | tem gente pagando uma fortuna |
| 4 | Facilidade | derruba a objeção que faz desistir | não precisa ser programador |
| 5 | Descoberta | dá nome à solução, com verbos simples | crie o seu próprio JARVIS |
| 6 | Benefício | como fica a vida depois | um funcionário digital só seu |
| 7 | Comentário | uma ação pequena: comentar uma palavra | COMENTA JARVIS |

▶ Reel: https://www.youtube.com/shorts/V92t50ceCRg

## Uso

```bash
python3 reel7etapas.py novo <slug>               # cria edicoes/<data>-<slug>/roteiro.yaml a partir do exemplo
echo "aprovado" > edicoes/<pasta>/avatar/APROVADO_HEYGEN
python3 reel7etapas.py fazer    edicoes/<pasta>  # imagens (Codex) → avatar → montar → validar → mapa, com portões
python3 reel7etapas.py imagens  edicoes/<pasta> 3 7   # refaz só as imagens 3 e 7
python3 reel7etapas.py validar  edicoes/<pasta>  # zona segura, legenda, ritmo, −14 LUFS, qa_short.py + folhas de revisão
python3 reel7etapas.py publicar edicoes/<pasta>  # bot do Telegram + YouTube (yt-pubx)
```

Portões que bloqueiam: imagem vertical, clara e sem repetição; tudo dentro da zona segura do Reels/Shorts; legenda com no máximo 3 palavras e fonte ≥ 64 px; imagem mudando a cada ≤ 3,5 s; fala igual ao roteiro; −14 LUFS; `qa_short.py` do makeshorts aprovado.

Fecho padrão da fala: "Tá tudo no inema ponto club. Ou comenta &lt;PALAVRA&gt; que eu te mando o link."

Exemplo completo: [`edicoes/2026-10-11-jarvis/roteiro.yaml`](edicoes/2026-10-11-jarvis/roteiro.yaml). Para o Claude Code ou o Codex, a skill está em [`skill/SKILL.md`](skill/SKILL.md).

## Dependências

[reelcomenta](https://github.com/inematds/reelcomenta) (transcrição, recorte do rosto, estúdio HeyGen, envio), cardshorts (MusicGen, Whisper), explicavideos (estúdio HeyGen), Codex CLI (`image_gen`; flux2-klein local só como reserva), makeshorts (`qa_short.py`), ffmpeg, Pillow, OpenCV, PyYAML.

Parte do ecossistema **[INEMA.CLUB](https://inema.club)**. Licença MIT.
