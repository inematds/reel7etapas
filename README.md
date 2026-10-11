# reel7etapas

[![reel7etapas](guia/assets/banner.jpg)](https://inematds.github.io/reel7etapas/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O reel7etapas é um modelo para escrever vídeos curtos (Reels, Shorts, TikTok) e uma ferramenta que monta esses vídeos sozinha. O roteiro segue sempre a mesma ordem de 7 etapas, pensada para segurar quem está rolando a tela e terminar com um pedido simples: comentar uma palavra. Serve para quem cria conteúdo e quer um caminho repetível, em vez de começar do zero a cada vídeo. Para só usar o modelo, basta ler a tabela das 7 etapas; para gerar o vídeo, a ferramenta usa o avatar do Nei no HeyGen, imagens feitas no computador e um script em Python.

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

## Uso

```bash
python3 reel7etapas.py novo <slug>              # cria edicoes/<data>-<slug>/roteiro.yaml a partir do exemplo
python3 reel7etapas.py imagens edicoes/<pasta>  # 7 imagens no flux2-klein local
python3 reel7etapas.py previa  edicoes/<pasta>  # previa.jpg com tempo estimado
echo "aprovado" > edicoes/<pasta>/avatar/APROVADO_HEYGEN
python3 reel7etapas.py avatar  edicoes/<pasta>  # estúdio do HeyGen, espera e baixa
python3 reel7etapas.py montar  edicoes/<pasta>  # video.mp4
python3 reel7etapas.py conferir edicoes/<pasta> # conferencia.jpg + volume
python3 reel7etapas.py mapa    edicoes/<pasta>  # mapa.jpg (as 7 etapas) + capa.jpg
python3 reel7etapas.py enviar  edicoes/<pasta> "texto"  # bot do Telegram
```

Exemplo completo: [`edicoes/2026-10-11-jarvis/roteiro.yaml`](edicoes/2026-10-11-jarvis/roteiro.yaml). Para o Claude Code ou o Codex, a skill está em [`skill/SKILL.md`](skill/SKILL.md).

## Dependências

[reelcomenta](https://github.com/inematds/reelcomenta) (transcrição, recorte do rosto, estúdio HeyGen, envio), cardshorts (MusicGen, Whisper), explicavideos (estúdio HeyGen), servidor flux2-klein local (`localhost:8000`), ffmpeg, Pillow, OpenCV, PyYAML.

Parte do ecossistema **[INEMA.CLUB](https://inema.club)**. Licença MIT.
