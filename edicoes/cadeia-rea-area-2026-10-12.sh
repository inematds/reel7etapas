#!/bin/bash
# cadeia 12/10: quando o avatar de cada reel REA chegar, roda 'fazer' (imagens já prontas → montar → validar → mapa).
# NÃO publica: a sessão seguinte confere as folhas (build/revisao) e o palavras.json (REA) e roda 'publicar'.
cd ~/projetos/reel7etapas || exit 1
for e in 2026-10-12-rea-area 2026-10-12-rea-clone-tudo; do
  until [ -s edicoes/$e/avatar/avatar.mp4 ]; do sleep 60; done
  sleep 20
  timeout 3600 python3 reel7etapas.py fazer edicoes/$e > edicoes/$e/fazer.log 2>&1
  echo "$e fazer rc=$?" >> edicoes/cadeia-rea-area-2026-10-12.log
done
