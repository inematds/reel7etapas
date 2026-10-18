#!/usr/bin/env bash
# Fila do estúdio HeyGen (18/10, D10): um envio por vez no navegador; o download de cada um corre em paralelo.
cd ~/projetos/reel7etapas || exit 1
for d in edicoes/2026-10-18-opencode-v3 edicoes/2026-10-18-era-ferramentas edicoes/2026-10-18-faturar-2027 \
         edicoes/2026-10-18-saas-morrendo edicoes/2026-10-18-chat-ao-agente; do
  ( timeout 18000 python3 reel7etapas.py avatar "$d" > "$d/avatar.log" 2>&1; echo "$(date +%H:%M) $d rc=$?" >> edicoes/fila-avatar-1018.done ) &
  pid=$!
  # espera o estúdio devolver o id (vídeo enviado) ou o processo terminar, no máximo 20 min
  for _ in $(seq 1 120); do
    [ -s "$d/avatar/video_id.txt" ] && break
    kill -0 "$pid" 2>/dev/null || break
    sleep 10
  done
  echo "$(date +%H:%M) enviado: $d ($(cat "$d/avatar/video_id.txt" 2>/dev/null || echo 'sem id'))" >> edicoes/fila-avatar-1018.done
done
wait
echo "$(date +%H:%M) FIM" >> edicoes/fila-avatar-1018.done
