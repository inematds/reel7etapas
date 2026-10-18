# Handoffs — trabalhos abertos

Cada linha é um assunto em andamento: leia o snapshot do assunto que for continuar. Gravado por handoff-grava.py.

<!-- handoff-indice:inicio -->
- `r7e-gatilho-d10` · handoffs/history/2026-10-18T230041Z-r7e-gatilho-d10.md · 18/10 20:00
- `evento-do-chat-ao-agente` · handoffs/history/2026-10-18T223248Z-evento-do-chat-ao-agente.md · 18/10 19:32
<!-- handoff-indice:fim -->

---

Cópia integral do snapshot mais recente (handoffs/history/2026-10-18T230041Z-r7e-gatilho-d10.md):

# Handoff — 2026-10-18 — r7e: gancho gatilho (D9) + propósito/plano (D10); 5 reels D10 no v3; 2 reels de gestão (lives3) esperando avatar

## Projeto e escopo
~/projetos/reel7etapas (repo inematds/reel7etapas) + kit ~/projetos/inema-design (D9/D10) + ~/projetos/wifi (heygen-aviso, LIMITES). Pedido do Nei: o r7e não tinha gancho/emoção e não dava visualização no TikTok/Instagram (comparado ao reel do evento extremo/clima); avaliar formato, letra, imagem e prompt; refazer forte e viral.

## Estado aceito
- [confirmed] Kit inema-design: D9 (gancho do r7e = gatilho: medo/novidade/provocação, número com fonte, imagem nítida; "capa = ganho" foi para o HISTORICO) e D10 (objetivo = público no inema.club; plano antes da fala; rosto meia tela → PiP; ≥ 2 diagramas; etapas como checklist; CTA "tá tudo no inema.club, ou me pede o link") — commits 7e825bb e 55829ef (pushed).
- [confirmed] Skill skill/SKILL.md com D9/D10 — commits d926ec5, 2261b38, e756762 (pushed).
- [confirmed] Motor reel7etapas.py: `letra: forte` (#FACC15 + contorno 8), `letra: tarja` (2ª linha da manchete em caixa sólida; letra escura sem contorno/sombra), `passos:` (diagrama que se monta, sem zoom), moldura do avatar na cor ativa. diagramas.py novo (fluxo, antes_depois, cartoes, barras, linha_tempo, terminal, painel, frase, site) com área y 540–1165. Commit cc0cbe8 (pushed); as correções de depois (TOPO 540, tarja sem contorno, fluxo, frase) NÃO estão commitadas.
- [confirmed] 5 reels "-gatilho" (mesmo avatar antigo, capa nítida) enviados ao v3 mais cedo.
- [confirmed] 5 reels D10 com avatar novo, montados, validados (fala 97–99%), legendas corrigidas (Claude, IA) e enviados ao v3 (não publicados): opencode-v3, era-ferramentas, faturar-2027, saas-morrendo, chat-ao-agente.
- [confirmed] Clima da semana com avatar (eventosextremospub/edicoes/2026-10-18-semana/video-avatar.mp4, 67 s) enviado ao v3, msg 1622; a versão mapa já estava no lives10. Evento "Do chat ao agente" com avatar chegou ao v3 às 19:01 (msg 1624, via dochat-manda de outra sessão).
- [confirmed] HeyGen: sessão caiu (cookie heygen_session dura 30 dias; o novo vence 17/11/2026 17:44). Nei logou às 20:44 (janela aberta na tela :10 dele). Aviso vermelho no v3 1 dia antes: ~/projetos/wifi/heygen-aviso/aviso.py + timer systemd --user heygen-aviso (9h e 19h); teste enviado. Commit 39c046f no wifi (pushed). LIMITES.md atualizado.
- [confirmed] Memória: heygen-login-na-tela.md (só o login na tela :10; estúdio sempre com DISPLAY=:99 explícito — a sessão do Claude herda DISPLAY=:10.0).
- [confirmed] FALHAS.md do reel7etapas: 4 linhas de 18/10 (tarja sobre diagrama, portão de luz no gancho, cartões repetidos, Claude/IA na legenda) — não commitado.

## Proposto / tentado, não confirmado
- [?] 2 reels de gestão para o lives3 (edicoes/2026-10-18-demissao-gestores e 2026-10-18-novas-funcoes-gestao): roteiros, diagramas e fotos prontos e no portão; avatares ENVIADOS ao HeyGen (video_id aa446a0f2e0b406bb8356911b323aea7 e b30cd2f8b5f14297bfab63c06b623472) mas o download não terminou (processo morreu com a sessão). Falta: `DISPLAY=:99 python3 reel7etapas.py avatar <pasta>` (retoma pelo video_id.txt e baixa) → corrigir palavras.json (Claude/IA) → montar → validar → mapa → revisar folhas → `publicar` (canal lives3 + v3).
- [?] Reação do Nei aos 5 reels D10 no v3.

## Decisões
- CTA fixo: "Tá tudo no inema ponto club. Ou me pede o link aqui nos comentários."
- Capa D10: sem faixa; gancho inteiro na manchete de 2 linhas logo acima do avatar meia tela (layout abre, desfoque 0, titulo_pos baixo, luz_min 0 no gancho).
- Empresas de 2027 e Constituição dos Agentes aparecem como INEMA.CLUB PRO: não dizer "grátis" nesses reels.
- Os 5 D10 só no v3 (análise); os 2 de gestão vão para o lives3 (pedido "use o r7e forte viral lives3").

## Não fazer
- Não abrir o estúdio na tela do Nei (sempre DISPLAY=:99); só a janela de login vai para a tela :10.
- Não usar Metricool/API sem autorização explícita (não autorizado).
- Não trocar plano do HeyGen; não apagar rascunhos no HeyGen.

## Pendências em aberto
- "Do chat ao agente": a página de evento diz links exclusivos INEMA.PRO; o reel D10 diz "grátis agora, antes de ficar só no PRO" — Nei não respondeu.
- Commit das correções do motor/diagramas, FALHAS.md e roteiros/diagramas dos 2 de gestão.

## Próxima ação
Baixar os 2 avatares de gestão e terminar/publicar no lives3 + v3 (ver acima); depois commit + push do reel7etapas.


<!-- handoff-estado:inicio -->
## Estado gravado pelo script (não editar)

Gravado por handoff-grava.py no momento do handoff. `--conferir` compara com o projeto agora.

- commit: 317acfa00e634c0ccb22509fe9fba776e994464e · branch: main
- arquivos sujos fora de handoffs/: 433 (lista cortada)
- `FALHAS.md` · sha256:c7f3ef9f609c · sujo
- `diagramas.py` · sha256:1ebbb09ff545 · sujo
- `edicoes/.wes-imagens-ok` · sha256:e3b0c44298fc · sujo
- `edicoes/2026-10-11-google-carbon/capa.jpg` · sha256:520cdd52a5e6 · sujo
- `edicoes/2026-10-11-google-carbon/fazer.log` · sha256:54e31940ecca · sujo
- `edicoes/2026-10-11-google-carbon/mapa.jpg` · sha256:09f7b6b87d41 · sujo
- `edicoes/2026-10-11-rea-clona-qualquer-software/fazer.log` · sha256:8c11ecc3c9cb · sujo
- `edicoes/2026-10-11-rea-clona-qualquer-software/fazer2.log` · sha256:00d0a5506da7 · sujo
- `edicoes/2026-10-11-repos-claude/capa.jpg` · sha256:f2706a9d7cfb · sujo
- `edicoes/2026-10-11-repos-claude/fazer.log` · sha256:0c2361c4055c · sujo
- `edicoes/2026-10-11-repos-claude/mapa.jpg` · sha256:2e9455695f24 · sujo
- `edicoes/2026-10-11-videos-com-ia/fazer.log` · sha256:eb1495b7e11a · sujo
- `edicoes/2026-10-11-videos-com-ia/fazer2.log` · sha256:142b4127db11 · sujo
- `edicoes/2026-10-12-agent-skills-addy/fazer.out` · sha256:505c670211d0 · sujo
- `edicoes/2026-10-12-agent-skills-addy/fazer.sh` · sha256:2f91cb0466c1 · sujo
- `edicoes/2026-10-12-agent-skills-addy/imagens.out` · sha256:9a3903a21345 · sujo
- `edicoes/2026-10-12-clima-furacoes/avatar.log` · sha256:12bb41d98ac4 · sujo
- `edicoes/2026-10-12-clima-furacoes/avatar/APROVADO_HEYGEN` · sha256:378289105935 · sujo
- `edicoes/2026-10-12-clima-furacoes/avatar/fala.txt` · sha256:25adefee6d59 · sujo
- `edicoes/2026-10-12-clima-furacoes/avatar/video_id.txt` · sha256:ad7b9e02861d · sujo
- `edicoes/2026-10-12-clima-furacoes/capa.jpg` · sha256:743dcd73fabe · sujo
- `edicoes/2026-10-12-clima-furacoes/imagens.log` · sha256:d4df962d16c6 · sujo
- `edicoes/2026-10-12-clima-furacoes/mapa.jpg` · sha256:ea30cbddac56 · sujo
- `edicoes/2026-10-12-clima-furacoes/montar.log` · sha256:ecacc9a0122b · sujo
- `edicoes/2026-10-12-clima-furacoes/montar2.log` · sha256:669bf799ab8e · sujo
- `edicoes/2026-10-12-clima-japao/avatar.log` · sha256:d84deb9b3353 · sujo
- `edicoes/2026-10-12-clima-japao/avatar/APROVADO_HEYGEN` · sha256:378289105935 · sujo
- `edicoes/2026-10-12-clima-japao/avatar/baixar.log` · sha256:3f9984de7a2c · sujo
- `edicoes/2026-10-12-clima-japao/avatar/fala.txt` · sha256:93bc029d7332 · sujo
- `edicoes/2026-10-12-clima-japao/avatar/video_id.txt` · sha256:d0e26993cad2 · sujo
- `edicoes/2026-10-12-clima-japao/capa.jpg` · sha256:ec15ad33783d · sujo
- `edicoes/2026-10-12-clima-japao/imagens.log` · sha256:ffb045b658b2 · sujo
- `edicoes/2026-10-12-clima-japao/mapa.jpg` · sha256:1737664bdd99 · sujo
- `edicoes/2026-10-12-clima-japao/montar.log` · sha256:363170c68331 · sujo
- `edicoes/2026-10-12-clima-planeta/avatar.log` · sha256:769fc629a1c6 · sujo
- `edicoes/2026-10-12-clima-planeta/avatar/APROVADO_HEYGEN` · sha256:378289105935 · sujo
- `edicoes/2026-10-12-clima-planeta/avatar/fala.txt` · sha256:546514a7d4ef · sujo
- `edicoes/2026-10-12-clima-planeta/avatar/video_id.txt` · sha256:50c0a60f678c · sujo
- `edicoes/2026-10-12-clima-planeta/capa.jpg` · sha256:0b88124ef149 · sujo
- `edicoes/2026-10-12-clima-planeta/imagens.log` · sha256:a0f15f351526 · sujo
- `edicoes/2026-10-12-clima-planeta/mapa.jpg` · sha256:f1768e9d7617 · sujo
- `edicoes/2026-10-12-clima-planeta/montar.log` · sha256:099adb58d7d9 · sujo
- `edicoes/2026-10-12-clima-tailandia/avatar.log` · sha256:6e8bb015d006 · sujo
- `edicoes/2026-10-12-clima-tailandia/avatar/APROVADO_HEYGEN` · sha256:378289105935 · sujo
- `edicoes/2026-10-12-clima-tailandia/avatar/baixar.log` · sha256:957827c2983b · sujo
- `edicoes/2026-10-12-clima-tailandia/avatar/fala.txt` · sha256:27188e23e020 · sujo
- `edicoes/2026-10-12-clima-tailandia/avatar/video_id.txt` · sha256:6b202607ceef · sujo
- `edicoes/2026-10-12-clima-tailandia/capa.jpg` · sha256:d6f99b19dfbc · sujo
- `edicoes/2026-10-12-clima-tailandia/imagens.log` · sha256:0fa6c79df108 · sujo
- `edicoes/2026-10-12-clima-tailandia/mapa.jpg` · sha256:3fb9a40cbfaf · sujo
- `edicoes/2026-10-12-clima-tailandia/montar.log` · sha256:da2d6df4ef6c · sujo
- `edicoes/2026-10-12-consultoria-2027/avatar/APROVADO_HEYGEN` · sha256:8e79e036f941 · sujo
- `edicoes/2026-10-12-consultoria-2027/avatar/fala.txt` · sha256:ece72afaaebd · sujo
- `edicoes/2026-10-12-consultoria-2027/avatar/video_id.txt` · sha256:f2d4666b9664 · sujo
- `edicoes/2026-10-12-consultoria-2027/roteiro.yaml` · sha256:f1dd8bd587ed · sujo
- `edicoes/2026-10-12-oscoach/avatar/APROVADO_HEYGEN` · sha256:903f04fc04a3 · sujo
- `edicoes/2026-10-12-oscoach/avatar/fala.txt` · sha256:481a5de0583b · sujo
- `edicoes/2026-10-12-oscoach/avatar/video_id.txt` · sha256:5d27ecb79632 · sujo
- `edicoes/2026-10-12-oscoach/capa.jpg` · sha256:3eaabbdf9713 · sujo
- `edicoes/2026-10-12-oscoach/espera-heygen.sh` · sha256:6ccf377ee7dd · sujo
- `edicoes/2026-10-12-oscoach/fazer.log` · sha256:81d19967b035 · sujo
- `edicoes/2026-10-12-oscoach/imagens.log` · sha256:a0f15f351526 · sujo
- `edicoes/2026-10-12-oscoach/mapa.jpg` · sha256:076fca2c0bf8 · sujo
- `edicoes/2026-10-12-oscoach/roteiro.yaml` · sha256:6a7306b61fc3 · sujo
- `edicoes/2026-10-12-oswork-antes-jarvis/fazer.log` · sha256:012b56f771e7 · sujo
- `edicoes/2026-10-12-oswork-jarvis-3d/fazer.log` · sha256:5f292a169afb · sujo
- `edicoes/2026-10-12-oswork-jarvis-3d/montar.log` · sha256:ab8e0f925977 · sujo
- `edicoes/2026-10-12-oswork-jarvis-exec/fazer.log` · sha256:81f438330c38 · sujo
- `edicoes/2026-10-12-oswork-jarvis-flat/fazer.log` · sha256:1d794106040f · sujo
- `edicoes/2026-10-12-oswork-jarvis-flat/montar.log` · sha256:8b4de70d7343 · sujo
- `edicoes/2026-10-12-oswork-jarvis-hq/fazer.log` · sha256:4cdbd53a9ac6 · sujo
- `edicoes/2026-10-12-oswork-jarvis-hq/montar.log` · sha256:0c890ca3ac84 · sujo
- `edicoes/2026-10-12-r7e-como-funciona/fazer.log` · sha256:e29e2e08528b · sujo
- `edicoes/2026-10-12-rea-area/avatar.log` · sha256:8b68c329cd9e · sujo
- `edicoes/2026-10-12-rea-area/fazer.log` · sha256:d2a7908a810e · sujo
- `edicoes/2026-10-12-rea-area/fazer2.log` · sha256:7ca1816b48ce · sujo
- `edicoes/2026-10-12-rea-area/imagens.log` · sha256:a0f15f351526 · sujo
- `edicoes/2026-10-12-rea-area/publicar.log` · sha256:e7df36774483 · sujo
- `edicoes/2026-10-12-rea-clone-tudo/avatar.log` · sha256:8c3e43f3e3e8 · sujo
- `edicoes/2026-10-12-rea-clone-tudo/fazer.log` · sha256:eefc1be44728 · sujo
- `edicoes/2026-10-12-rea-clone-tudo/fazer2.log` · sha256:e78aacb705bd · sujo
- `edicoes/2026-10-12-rea-clone-tudo/imagens.log` · sha256:a0f15f351526 · sujo
- `edicoes/2026-10-12-rea-clone-tudo/publicar.log` · sha256:992c24996d50 · sujo
- `edicoes/2026-10-12-rea-mundo-bilionario/avatar/studio.draft1.log` · sha256:5a3681db2310 · sujo
- `edicoes/2026-10-12-rea-mundo-bilionario/avatar/video_id.draft1.txt` · sha256:a95a5e9dcb37 · sujo
- `edicoes/2026-10-12-rea-mundo-bilionario/avatar2.log` · sha256:cce8ad7392df · sujo
- `edicoes/2026-10-12-rea-mundo-bilionario/fazer.log` · sha256:6d96fec8bd74 · sujo
- `edicoes/2026-10-12-rea-mundo-bilionario/fazer3.log` · sha256:5df196cb14a6 · sujo
- `edicoes/2026-10-12-rea-mundo-bilionario/video-v1.mp4` · sha256:af6445f3e292 · sujo
- `edicoes/2026-10-12-rea-nem-precisa/fazer.log` · sha256:b7c5c5f718dd · sujo
- `edicoes/2026-10-12-rea-nem-precisa/imagens.log` · sha256:9a3903a21345 · sujo
- `edicoes/2026-10-12-rea-nem-precisa/montar2.log` · sha256:9f1cd0c5c5e2 · sujo
- `edicoes/2026-10-12-rea-nem-precisa/publicar.log` · sha256:5c62aef4095d · sujo
- `edicoes/2026-10-12-rea-nem-precisa/validar2.log` · sha256:3cedebec0514 · sujo
- `edicoes/2026-10-12-rea-quatro-passos/fazer.log` · sha256:ff9fafc7ffea · sujo
- `edicoes/2026-10-12-rea-quatro-passos/montar2.log` · sha256:133243e3a411 · sujo
- `edicoes/2026-10-12-rea-sem-travas/fazer.log` · sha256:e8c2e93bc9f6 · sujo
- `edicoes/2026-10-12-rea-sem-travas/imagens.log` · sha256:9a3903a21345 · sujo
- `edicoes/2026-10-12-rea-sem-travas/montar2.log` · sha256:fecf117401a4 · sujo
- `edicoes/2026-10-12-rea-sem-travas/publicar.log` · sha256:7071eafbe3e2 · sujo
- `edicoes/2026-10-12-rea-sem-travas/validar2.log` · sha256:8d14ff01944f · sujo
- `edicoes/2026-10-12-rea-servidor/fazer.log` · sha256:b93182b1770a · sujo
- `edicoes/2026-10-13-clima-semana-mundo/avatar/fala.txt` · sha256:10a5a22ae769 · sujo
- `edicoes/2026-10-13-clima-semana-mundo/avatar/video_id.txt` · sha256:b323d84e25dd · sujo
- `edicoes/2026-10-13-clima-semana-mundo/capa.jpg` · sha256:e053b9ed1f1f · sujo
- `edicoes/2026-10-13-clima-semana-mundo/fazer.log` · sha256:7fd9ffaa777b · sujo
- `edicoes/2026-10-13-clima-semana-mundo/mapa.jpg` · sha256:39b804e6a237 · sujo
- `edicoes/2026-10-13-constituicao-agentes/fazer.log` · sha256:0725916eb0fc · sujo
- `edicoes/2026-10-13-rato-gene/avatar/APROVADO_HEYGEN` · sha256:87e6d568c298 · sujo
- `edicoes/2026-10-13-rato-gene/avatar/fala.txt` · sha256:596b46c69a2e · sujo
- `edicoes/2026-10-13-rato-gene/avatar/video_id.txt` · sha256:a76a83d4e0ba · sujo
- `edicoes/2026-10-13-rato-gene/capa.jpg` · sha256:338e5946bff1 · sujo
- `edicoes/2026-10-13-rato-gene/fazer.log` · sha256:e41b59306187 · sujo
- `edicoes/2026-10-13-rato-gene/mapa.jpg` · sha256:a8578aa0d52e · sujo
- `edicoes/2026-10-13-rato-gene/roteiro.yaml` · sha256:1b95f8976e05 · sujo
- `edicoes/2026-10-13-rea-area-es/avatar/APROVADO_HEYGEN` · sha256:4d3dc6ac4046 · sujo
- `edicoes/2026-10-13-rea-area-es/avatar/fala.txt` · sha256:7bb5aa8e5dd5 · sujo
- `edicoes/2026-10-13-rea-area-es/avatar/video_id.txt` · sha256:e577fe348ffc · sujo
- `edicoes/2026-10-13-rea-area-es/capa.jpg` · sha256:19176318cb59 · sujo
- `edicoes/2026-10-13-rea-area-es/mapa.jpg` · sha256:6f38d6f43cdc · sujo
- `edicoes/2026-10-13-rea-area-es/roteiro.yaml` · sha256:5c2bb77d8aad · sujo
- `edicoes/2026-10-13-rea-clona-qualquer-software-es/avatar/APROVADO_HEYGEN` · sha256:4d3dc6ac4046 · sujo
- `edicoes/2026-10-13-rea-clona-qualquer-software-es/avatar/fala.txt` · sha256:20954f80d321 · sujo
- `edicoes/2026-10-13-rea-clona-qualquer-software-es/avatar/video_id.txt` · sha256:a921f3ad9e79 · sujo
- `edicoes/2026-10-13-rea-clona-qualquer-software-es/capa.jpg` · sha256:cf255a39f260 · sujo
- `edicoes/2026-10-13-rea-clona-qualquer-software-es/mapa.jpg` · sha256:41fafdac1b60 · sujo
- `edicoes/2026-10-13-rea-clona-qualquer-software-es/roteiro.yaml` · sha256:089252867321 · sujo
- `edicoes/2026-10-13-rea-clone-tudo-es/avatar/APROVADO_HEYGEN` · sha256:4d3dc6ac4046 · sujo
- `edicoes/2026-10-13-rea-clone-tudo-es/avatar/fala.txt` · sha256:0c6ede81f2be · sujo
- `edicoes/2026-10-13-rea-clone-tudo-es/avatar/video_id.txt` · sha256:b277c3aae543 · sujo
- `edicoes/2026-10-13-rea-clone-tudo-es/capa.jpg` · sha256:b49e1f5006db · sujo
- `edicoes/2026-10-13-rea-clone-tudo-es/mapa.jpg` · sha256:04960f94d12c · sujo
- `edicoes/2026-10-13-rea-clone-tudo-es/roteiro.yaml` · sha256:9473a3cfb8c1 · sujo
- `edicoes/2026-10-13-rea-mundo-bilionario-es/avatar/APROVADO_HEYGEN` · sha256:4d3dc6ac4046 · sujo
- `edicoes/2026-10-13-rea-mundo-bilionario-es/avatar/fala.txt` · sha256:ef54ffaac012 · sujo
- `edicoes/2026-10-13-rea-mundo-bilionario-es/avatar/video_id.txt` · sha256:39b644aba124 · sujo
- `edicoes/2026-10-13-rea-mundo-bilionario-es/capa.jpg` · sha256:4f1bc524d1f7 · sujo
- `edicoes/2026-10-13-rea-mundo-bilionario-es/mapa.jpg` · sha256:e4410b041dd5 · sujo
- `edicoes/2026-10-13-rea-mundo-bilionario-es/roteiro.yaml` · sha256:3ad49ef2bf3a · sujo
- `edicoes/2026-10-13-rea-nem-precisa-es/avatar/APROVADO_HEYGEN` · sha256:4d3dc6ac4046 · sujo
- `edicoes/2026-10-13-rea-nem-precisa-es/avatar/fala.txt` · sha256:f52bd08e42e5 · sujo
- `edicoes/2026-10-13-rea-nem-precisa-es/avatar/video_id.txt` · sha256:cdca7264f180 · sujo
- `edicoes/2026-10-13-rea-nem-precisa-es/capa.jpg` · sha256:e3f75198afab · sujo
- `edicoes/2026-10-13-rea-nem-precisa-es/mapa.jpg` · sha256:f5df55c3caed · sujo
- `edicoes/2026-10-13-rea-nem-precisa-es/roteiro.yaml` · sha256:7b6b58fde1dd · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/avatar/APROVADO_HEYGEN` · sha256:4d3dc6ac4046 · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/avatar/antes-portugues/avatar.mp4` · sha256:563dac3d1bcc · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/avatar/antes-portugues/fala.txt` · sha256:b0794d32d5a6 · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/avatar/antes-portugues/studio.log` · sha256:315dc089f57d · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/avatar/antes-portugues/video_id.txt` · sha256:ccff041d37f6 · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/avatar/fala.txt` · sha256:a99bac8603bf · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/avatar/video_id.txt` · sha256:c1c1dc18e118 · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/capa.jpg` · sha256:c90ddf151065 · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/mapa.jpg` · sha256:55fca32fd6d2 · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/roteiro.yaml` · sha256:27cf7b9c9cfd · sujo
- `edicoes/2026-10-13-rea-quatro-passos-es/roteiro.yaml.antes-portugues` · sha256:a29a415c6bb4 · sujo
- `edicoes/2026-10-13-rea-sem-travas-es/avatar/APROVADO_HEYGEN` · sha256:4d3dc6ac4046 · sujo
- `edicoes/2026-10-13-rea-sem-travas-es/avatar/fala.txt` · sha256:eeea23a815fd · sujo
- `edicoes/2026-10-13-rea-sem-travas-es/avatar/video_id.txt` · sha256:94ec92a2cf86 · sujo
- `edicoes/2026-10-13-rea-sem-travas-es/capa.jpg` · sha256:5397ba42cbe4 · sujo
- `edicoes/2026-10-13-rea-sem-travas-es/mapa.jpg` · sha256:9005b92380df · sujo
- `edicoes/2026-10-13-rea-sem-travas-es/roteiro.yaml` · sha256:32f79b25002e · sujo
- `edicoes/2026-10-13-rea-servidor-es/avatar/APROVADO_HEYGEN` · sha256:4d3dc6ac4046 · sujo
- `edicoes/2026-10-13-rea-servidor-es/avatar/fala.txt` · sha256:125d9eae7973 · sujo
- `edicoes/2026-10-13-rea-servidor-es/avatar/video_id.txt` · sha256:e2a83e603ce0 · sujo
- `edicoes/2026-10-13-rea-servidor-es/capa.jpg` · sha256:5f211cb1aa52 · sujo
- `edicoes/2026-10-13-rea-servidor-es/mapa.jpg` · sha256:b333b0404f3b · sujo
- `edicoes/2026-10-13-rea-servidor-es/roteiro.yaml` · sha256:af0584fec2e9 · sujo
- `edicoes/2026-10-14-constituicao-limites/avatar/baixar.log` · sha256:8b8e17881a67 · sujo
- `edicoes/2026-10-14-constituicao-limites/imagens.log` · sha256:2a4a24f43ab6 · sujo
- `edicoes/2026-10-14-meta-muse-wonder/avatar/APROVADO_HEYGEN` · sha256:da81e4703eca · sujo
- `edicoes/2026-10-14-meta-muse-wonder/avatar/fala.txt` · sha256:f5819d0bee63 · sujo
- `edicoes/2026-10-14-meta-muse-wonder/avatar/video_id.txt` · sha256:a188189cb06d · sujo
- `edicoes/2026-10-14-meta-muse-wonder/capa.jpg` · sha256:64458c957909 · sujo
- `edicoes/2026-10-14-meta-muse-wonder/fazer.log` · sha256:7a531abab9ba · sujo
- `edicoes/2026-10-14-meta-muse-wonder/imagens.log` · sha256:a0f15f351526 · sujo
- `edicoes/2026-10-14-meta-muse-wonder/mapa.jpg` · sha256:f8e1a6318194 · sujo
- `edicoes/2026-10-14-meta-muse-wonder/roteiro.yaml` · sha256:215e697af856 · sujo
- `edicoes/2026-10-14-rea-clones-queda/avatar/APROVADO_HEYGEN` · sha256:49245e195ef3 · sujo
- `edicoes/2026-10-14-rea-clones-queda/avatar/fala.txt` · sha256:1cdc0fd0685a · sujo
- `edicoes/2026-10-14-rea-clones-queda/avatar/video_id.txt` · sha256:7bb9df6e9661 · sujo
- `edicoes/2026-10-14-rea-clones-queda/montar.log` · sha256:e96f3bf9a5dc · sujo
- `edicoes/2026-10-14-rea-clones-queda/roteiro.yaml` · sha256:94ed921818e9 · sujo
- `edicoes/2026-10-14-robo-sem-robo/avatar/APROVADO_HEYGEN` · sha256:e96d3b53c1af · sujo
- `edicoes/2026-10-14-robo-sem-robo/avatar/fala.txt` · sha256:419dbfe20b34 · sujo
- `edicoes/2026-10-14-robo-sem-robo/avatar/video_id.txt` · sha256:85409b530779 · sujo
- `edicoes/2026-10-14-robo-sem-robo/capa.jpg` · sha256:3bdfacf72d59 · sujo
- `edicoes/2026-10-14-robo-sem-robo/fazer.log` · sha256:15db932873a2 · sujo
- `edicoes/2026-10-14-robo-sem-robo/mapa.jpg` · sha256:18d50504b371 · sujo
- `edicoes/2026-10-14-robo-sem-robo/roteiro.yaml` · sha256:f945c1d1b50a · sujo
- `edicoes/2026-10-14-robo-uma-foto/avatar/APROVADO_HEYGEN` · sha256:c85836a71683 · sujo
- `edicoes/2026-10-14-robo-uma-foto/avatar/fala.txt` · sha256:761560fae3d7 · sujo
- `edicoes/2026-10-14-robo-uma-foto/avatar/video_id.txt` · sha256:31b48ac6c146 · sujo
- `edicoes/2026-10-14-robo-uma-foto/capa.jpg` · sha256:9b9749b9b7bc · sujo
- `edicoes/2026-10-14-robo-uma-foto/fazer.log` · sha256:26656f74cf36 · sujo
- `edicoes/2026-10-14-robo-uma-foto/imagens.log` · sha256:95962fb90b6b · sujo
- `edicoes/2026-10-14-robo-uma-foto/mapa.jpg` · sha256:93b01736f2f2 · sujo
- `edicoes/2026-10-14-robo-uma-foto/publicar.log` · sha256:9a4afda982db · sujo
- `edicoes/2026-10-14-robo-uma-foto/publicar2.log` · sha256:dd43d27871ba · sujo
- `edicoes/2026-10-14-robo-uma-foto/roteiro.yaml` · sha256:ef774f475358 · sujo
<!-- handoff-estado:fim -->
