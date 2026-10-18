# Plano — opencode v3 (piloto D9 + D10, 18/10/2026)

## Propósito
Levar gente ao inema.club (passo a passo das 3 proteções). CTA: "Tá tudo no inema ponto club. Ou me pede o link aqui nos comentários."

## Pessoa
Qualquer um que paga uma IA (ChatGPT, Claude, Gemini) com cartão, não só programador. Não sabe o que é "chave de API", mas sabe o que é "senha" e "conta no cartão".

## O que ela quer
Não acordar com uma conta absurda no cartão por causa de um ataque que ela nem entendeu (dor) → dormir tranquila (desejo).

## Gancho (D9)
Medo com número e fonte: hackers roubaram as chaves de milhares de pessoas no OpenCode; relatos de US$ 1.700 de conta numa noite (relatos de usuários afetados, out/2026).

## Nota de potencial: 8/10
Medo concreto (dinheiro no cartão), notícia recente, solução simples. Risco: "chave" soa técnico → na tela e na fala, "chave = a senha que a IA usa pra cobrar de você".

## Fala (≈ 600 caracteres, para o avatar novo)
Hackers invadiram o OpenCode e roubaram as chaves de acesso de milhares de pessoas. Teve gente que acordou com mil e setecentos dólares de conta numa noite só. A chave é a senha que a IA usa pra cobrar de você, e a sua pode ser a próxima. Imagina dormir sabendo que, mesmo se roubarem, o prejuízo tem teto. Você não precisa ser especialista. São três ajustes: limite de gasto em cada chave, uma chave pra cada uso e um alarme que avisa quando o gasto foge do normal. Roubaram uma? Você cancela só aquela, e o resto segue funcionando. O susto vira um aviso no celular, não uma conta de mil dólares. Tá tudo no inema ponto club. Ou me pede o link aqui nos comentários.

## Etapas e visuais (rosto do quadro 0 em meia tela embaixo → PiP na etapa 2)
| # | Gatilho | Tela (manchete) | Visual | Tipo |
|---|---|---|---|---|
| 1 | MEDO (gancho) | faixa "HACKERS ROUBARAM AS CHAVES" · "US$ 1.700 NUMA NOITE" | foto: homem de madrugada, rosto iluminado pelo celular com a fatura vermelha | foto nítida |
| 2 | MEDO (é com você) | "A SUA PODE SER A PRÓXIMA" | DIAGRAMA 1 — fluxo: chave 🔑 → hacker → contador da conta subindo US$ 0 → 1.700 | diagrama |
| 3 | DESEJO | "PREJUÍZO COM TETO" | foto: a mesma pessoa dormindo tranquila, celular na mesa com aviso verde | foto |
| 4 | FACILIDADE | "SEM SER ESPECIALISTA" | print/mockup do painel de limite de gasto ("limite mensal US$ 20") com o campo em destaque | prova real |
| 5 | DESCOBERTA | "3 AJUSTES" | DIAGRAMA 2 — 3 cartões entrando um a um: limite · 1 chave por uso · alarme | diagrama |
| 6 | BENEFÍCIO | "SUSTO VIRA AVISO" | DIAGRAMA 3 — antes/depois em barras: sem limite US$ 1.700 × com limite US$ 20 | diagrama |
| 7 | CTA | "TUDO NO INEMA.CLUB" · "ou me pede o link" | celular com comentários | foto |

## Letra (o amarelo ainda não impacta)
- Manchete branca grande com contorno preto grosso; a palavra-chave numa TARJA sólida (amarelo com letra preta), não amarelo solto.
- Número e medo em vermelho com contorno.
- Amarelo só como preenchimento (tarja, faixa, moldura), nunca como letra fina sobre a foto.

## Motor (o que falta)
- Capa com avatar meia tela + imagem nítida em cima: `layout: abre` + `capa.desfoque: 0` (já existe).
- Tarja na palavra-chave da manchete: novo (`letra: tarja`).
- Diagramas: PNG desenhado (HTML → imagem) entra por `imagem:` na etapa (já existe); animação (contador subindo, cartões entrando) precisa de clipe por etapa — novo.

## Depende do Nei
- OK para gerar o avatar desta fala no estúdio do HeyGen (`APROVADO_HEYGEN` desta produção).
