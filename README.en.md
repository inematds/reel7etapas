# reel7etapas

[![reel7etapas](guia/assets/banner-en.jpg)](https://inematds.github.io/reel7etapas/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

reel7etapas is a template for writing short videos (Reels, Shorts, TikTok) and a tool that assembles those videos on its own. The script always follows the same 7-step order, designed to hold someone who is scrolling and to end with a simple ask: comment one word. It is for creators who want a repeatable path instead of starting from scratch with every video. To just use the template, reading the 7-step table is enough; to generate the video, the tool uses Nei's avatar in HeyGen, images made on your own computer and a Python script.

**An idea becomes a 9:16 reel in 7 trigger steps** — hook → desire → fear → ease → discovery → benefit → comment — with Nei's avatar speaking, one image per step, a headline and panel that switch on the right word of the speech, word-by-word captions and the closing "COMENTA &lt;PALAVRA&gt;" (COMMENT &lt;WORD&gt;).

📖 Guide: **https://inematds.github.io/reel7etapas/guia/en/**

![The 7 steps in the JARVIS example](edicoes/2026-10-11-jarvis/mapa.jpg)

## The template

| # | Step | What it does | Example (JARVIS) |
|---|---|---|---|
| 1 | Hook | shows the desired result in 2 s, before the technology | "VOCÊ DORME. ELE TRABALHA." (YOU SLEEP. HE WORKS.) |
| 2 | Desire | the person pictures themselves with what they want | an employee inside the PC |
| 3 | Fear | the risk of wasting money | some people are paying a fortune |
| 4 | Ease | knocks down the objection that makes people give up | you don't need to be a programmer |
| 5 | Discovery | names the solution, with simple verbs | create your own JARVIS |
| 6 | Benefit | how life looks afterwards | a digital employee that's all yours |
| 7 | Comment | one small action: comment a word | COMENTA JARVIS (COMMENT JARVIS) |

▶ Reel: https://www.youtube.com/shorts/PIa_eXWFk7s

## Usage

```bash
python3 reel7etapas.py novo <slug>              # creates edicoes/<data>-<slug>/roteiro.yaml from the example
python3 reel7etapas.py imagens edicoes/<pasta>  # 7 images on the local flux2-klein
python3 reel7etapas.py previa  edicoes/<pasta>  # previa.jpg with estimated timing
echo "aprovado" > edicoes/<pasta>/avatar/APROVADO_HEYGEN
python3 reel7etapas.py avatar  edicoes/<pasta>  # HeyGen studio, waits and downloads
python3 reel7etapas.py montar  edicoes/<pasta>  # video.mp4
python3 reel7etapas.py conferir edicoes/<pasta> # conferencia.jpg + volume
python3 reel7etapas.py mapa    edicoes/<pasta>  # mapa.jpg (the 7 steps) + capa.jpg
python3 reel7etapas.py enviar  edicoes/<pasta> "texto"  # Telegram bot
```

Full example: [`edicoes/2026-10-11-jarvis/roteiro.yaml`](edicoes/2026-10-11-jarvis/roteiro.yaml). For Claude Code or Codex, the skill is at [`skill/SKILL.md`](skill/SKILL.md).

## Dependencies

[reelcomenta](https://github.com/inematds/reelcomenta) (transcription, face crop, HeyGen studio, delivery), cardshorts (MusicGen, Whisper), explicavideos (HeyGen studio), local flux2-klein server (`localhost:8000`), ffmpeg, Pillow, OpenCV, PyYAML.

Part of the **[INEMA.CLUB](https://inema.club)** ecosystem. MIT license.
