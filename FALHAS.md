# FALHAS — reel7etapas

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-10-11 | reel JARVIS v1 saiu sem plano de direção visual: painel e avatar fora da zona segura, legenda cortada sem sentido, imagens repetidas ou que confundem, motion só com zoom lento | antes do `montar`: storyboard por etapa (imagem, câmera, entrada do texto, transição) aprovado + portão de zona segura + imagens olhadas em tamanho real, com troca da que falhar | prompt |
| 2026-10-11 | motor v2 antes de publicar: legenda de 22 caracteres estourava a largura na Montserrat Black; SRT com blocos sobrepostos; texto do cartão do CTA saía da caixa | corte da legenda também por pixels (fonte 66) + segmentação por frase; fim do bloco limitado ao início do seguinte; texto de cartão registrado no portão e quebrado em 2 linhas | infra |
