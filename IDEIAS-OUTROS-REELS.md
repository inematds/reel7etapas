# Onde a estratégia das 7 etapas entra nos outros reels (análise de 11/10/2026)

## Atenção antes de tudo: o funil "comenta PALAVRA"

`makeshorts` registra que o funil "comente PALAVRA → DM" **não está ligado** desde 01/10/2026: o ManyChat grátis caiu para 25 contatos/mês (`makeshorts/.claude/skills/makeshorts/SKILL.md:94-95`, `references/funil-dm.md:12`). O `roteirista-inema` também limita CTA a 30% dos vídeos e proíbe o modo comentário em dois vídeos seguidos.
O reel JARVIS fecha com "COMENTA JARVIS". Duas saídas: ligar o funil (ou responder à mão) ou dar à etapa 7 uma variante sem "comenta" ("manda pra quem…", "inema.club").

## Por projeto

| Projeto | Hoje | O que dá pra pegar das 7 etapas |
|---|---|---|
| reelcomenta | reel de terceiro + avatar + números com fonte; fecho "+300 cursos" | abertura com o **resultado** em 2 linhas; cartão de **Facilidade** entre a pergunta e o CTA; `cta.palavra` opcional (`reelcomenta.py:92-110`) |
| cardshorts | frase-choque + 4-5 cards, < 30 s | versão de 5 cenas: Gancho, Medo, Facilidade, Descoberta, CTA; gancho com resultado, não com ameaça |
| makeshorts | gancho 0-3 s + gancho secundário + entrega + CTA, 5 estruturas | "7 etapas" como 6ª estrutura (`references/roteiro.md:39`) |
| roteirista-inema | gancho, tensão, virada, CTA | formato alternativo: etapas 2-4 na tensão, 5-6 na virada; nada de jargão antes da virada; o Medo conta no limite de 40% de aversão à perda |
| reel-edita-inema | capa de impacto, CTA fixo "Saiba mais no inema.club" | manchete + imagem trocando por etapa na âncora; CTA configurável (`SKILL.md:122`) |
| reel-edita-inematds | cold open de 1-3 s | opção "resultado em 2 linhas" no cold open |
| inemaclub-textos (promover) | Dor → possibilidade → demonstração → trilha | encaixe mais natural: Gancho de resultado antes da Dor, Facilidade + Descoberta no meio; 12 públicos |
| explicavideos 9:16 | `reel_profile` com hook no quadro 0 | preset `reel_profile: "7etapas"` com 7 shots |

## O que o reel7etapas deve pegar de volta

- Número com fonte na etapa Medo ("uma fortuna" está sem fonte) — cartões do reelcomenta.
- Portão `qa_short.py` do makeshorts (quadro 0, trecho parado > 4 s, −14 LUFS) e revisor que re-transcreve o render final (reel-edita-inematds).
- Agendamento no Metricool com rótulo de IA; segmentação por público (inemaclub-textos).

## Top 5

1. Decidir o funil de DM: ligar ou ter etapa 7 sem "comenta".
2. `qa_short.py` no `conferir` do reel7etapas + fonte obrigatória no Medo.
3. Gancho de resultado + Facilidade na fórmula do inemaclub-textos (maior volume).
4. "7 etapas" como estrutura no makeshorts e no roteirista-inema.
5. reelcomenta: abertura com resultado, cartão de Facilidade, `cta.palavra`; reel-edita-inema com CTA configurável.
