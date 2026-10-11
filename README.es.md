# reel7etapas

[![reel7etapas](guia/assets/banner-es.jpg)](https://inematds.github.io/reel7etapas/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

reel7etapas es un modelo para escribir videos cortos (Reels, Shorts, TikTok) y una herramienta que monta esos videos sola. El guion sigue siempre el mismo orden de 7 etapas, pensado para retener a quien está deslizando la pantalla y terminar con un pedido simple: comentar una palabra. Sirve para quien crea contenido y quiere un camino repetible, en lugar de empezar de cero en cada video. Para usar solo el modelo, basta leer la tabla de las 7 etapas; para generar el video, la herramienta usa el avatar de Nei en HeyGen, imágenes generadas por Codex y un script en Python.

**Una idea se convierte en un reel 9:16 en 7 etapas de gatillo** — gancho → deseo → miedo → facilidad → descubrimiento → beneficio → comentario — con el avatar de Nei hablando, una imagen por etapa, titular y panel que cambian en la palabra justa del discurso, subtítulos palabra por palabra y el cierre "COMENTA &lt;PALABRA&gt;".

📖 Guía: **https://inematds.github.io/reel7etapas/guia/es/**

![Las 7 etapas en el ejemplo JARVIS](edicoes/2026-10-11-jarvis/mapa.jpg)

## El modelo

| # | Etapa | Qué hace | Ejemplo (JARVIS) |
|---|---|---|---|
| 1 | Gancho | muestra el resultado deseado en 2 s, antes de la tecnología | "VOCÊ DORME. ELE TRABALHA." (TÚ DUERMES. ÉL TRABAJA.) |
| 2 | Deseo | la persona se imagina con lo que quiere | un empleado dentro del PC |
| 3 | Miedo | el riesgo de estar gastando en vano | hay gente pagando una fortuna |
| 4 | Facilidad | derriba la objeción que hace desistir | no hace falta ser programador |
| 5 | Descubrimiento | le pone nombre a la solución, con verbos simples | crea tu propio JARVIS |
| 6 | Beneficio | cómo queda la vida después | un empleado digital solo tuyo |
| 7 | Comentario | una acción pequeña: comentar una palabra | COMENTA JARVIS |

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

Portones que bloquean: imagen vertical, clara y sin repetición; todo dentro de la zona segura de Reels/Shorts; subtítulo de máximo 3 palabras y fuente ≥ 64 px; imagen que cambia como máximo cada 3,5 s; habla igual al guion; −14 LUFS; `qa_short.py` de makeshorts aprobado.

Cierre estándar del habla: "Tá tudo no inema ponto club. Ou comenta &lt;PALAVRA&gt; que eu te mando o link." (Está todo en inema punto club. O comenta &lt;PALABRA&gt; y te mando el enlace.)

Ejemplo completo: [`edicoes/2026-10-11-jarvis/roteiro.yaml`](edicoes/2026-10-11-jarvis/roteiro.yaml). Para Claude Code o Codex, la skill está en [`skill/SKILL.md`](skill/SKILL.md).

## Dependencias

[reelcomenta](https://github.com/inematds/reelcomenta) (transcripción, recorte del rostro, estudio HeyGen, envío), cardshorts (MusicGen, Whisper), explicavideos (estudio HeyGen), Codex CLI (`image_gen`; flux2-klein local solo como respaldo), makeshorts (`qa_short.py`), ffmpeg, Pillow, OpenCV, PyYAML.

Parte del ecosistema **[INEMA.CLUB](https://inema.club)**. Licencia MIT.
