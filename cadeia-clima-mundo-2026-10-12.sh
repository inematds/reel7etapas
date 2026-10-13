#!/usr/bin/env bash
# Série "clima no mundo" (12/10/2026): 4 reels de 7 etapas. Avatares no estúdio em paralelo (fila longa),
# imagens no Codex uma edição por vez, depois montar + validar + mapa. NÃO publica (revisão antes).
# uso: systemd-run --user --unit=r7e-clima --setenv=PATH="$PATH" --setenv=DISPLAY=:99 bash <este arquivo>
set -uo pipefail
export PATH="$HOME/.npm-global/bin:$PATH"   # systemd usa /usr/bin/codex antigo
cd "$HOME/projetos/reel7etapas"
ST=edicoes/clima-mundo-STATUS.txt
log(){ echo "$(date '+%F %T') $*" >> "$ST"; }
ED=(edicoes/2026-10-12-clima-tailandia edicoes/2026-10-12-clima-japao edicoes/2026-10-12-clima-furacoes edicoes/2026-10-12-clima-planeta)
log "início"
for e in "${ED[@]}"; do
  mkdir -p "$e/avatar"
  echo 'Nei, 12/10/2026: "avatar no estudio nao gasta assinatura entao ta liberado sempre" — série clima no mundo' > "$e/avatar/APROVADO_HEYGEN"
  ( python3 reel7etapas.py avatar "$e" > "$e/avatar.log" 2>&1 && log "$(basename $e): avatar ok" || log "$(basename $e): FALHOU avatar ($(tail -1 $e/avatar.log | cut -c1-160))" ) &
  sleep 90
done
for e in "${ED[@]}"; do
  python3 reel7etapas.py imagens "$e" > "$e/imagens.log" 2>&1 && log "$(basename $e): imagens ok" || log "$(basename $e): FALHOU imagens ($(tail -1 $e/imagens.log | cut -c1-160))"
done
wait
for e in "${ED[@]}"; do
  [ -s "$e/avatar/avatar.mp4" ] || { log "$(basename $e): sem avatar, não montado"; continue; }
  { python3 reel7etapas.py montar "$e" && python3 reel7etapas.py validar "$e" && python3 reel7etapas.py mapa "$e"; } > "$e/montar.log" 2>&1 \
    && log "$(basename $e): montado e validado" || log "$(basename $e): FALHOU montar/validar ($(grep -h -i 'falha\|erro\|reprov' $e/montar.log | tail -1 | cut -c1-200))"
done
log "fim"
