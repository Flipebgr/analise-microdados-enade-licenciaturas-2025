# Estado operacional do projeto

## Referência de continuidade

- Branch operacional: `feature/pipeline-multiedicao`.
- Ponto de partida desta atualização documental: `5dee4f90961ef2a59806ce093f3285dbfe4862e5`.
- Confirme o hash atual com `git log -1 --oneline`; este documento não substitui o estado do Git.
- Fontes oficiais permanecem em `dados_brutos/` e não devem ser alteradas.
- A unidade de integração entre arquivos temáticos é exclusivamente `CO_CURSO`, após agregação e validação de unicidade.

## Entregas registradas

- Fase 1 (`051bd3b`): contratos explícitos das edições Enade 2017 e Enade das Licenciaturas 2025, além de configuração de área por edição.
- Fase 2 (`5a6fc6a`): inventário e leitura filtrada dos arquivos temáticos, inclusive diretamente do ZIP.
- Fase 3 (`cf3d729`): agregação de desempenho por curso, preservando os componentes específicos de cada edição.
- Fase 4 (`f614a02`): indicadores do Questionário do Estudante declarados no contrato de cada edição.
- Fase 5 (`2df6680` e `20b3415`): processo formativo por item; códigos 7 e 8 permanecem fora da escala analítica e têm percentuais próprios com denominador `n_total`.
- Fase 6 (`250b066`): loader de Conceito Enade por edição, com tabela original, proveniência, `SC` separado da faixa numérica e validações de schema.
- Fase 7 (`992dbff`): primeira implementação da CLI genérica por edição/área e da orquestração que caracteriza o `arq1`, reconcilia o Conceito e combina somente tabelas agregadas one-to-one por `CO_CURSO`.
- Fase 8 (`e75142f`, com correções consolidadas em `31ad957` — `fix(fase-8): valida evidencias e publica artefatos com rollback`): pacote `evidencias.json` schema `2.0`, validação semântica integral, participação oficial separada dos microdados, proveniência dos TXT utilizados, suporte ZIP/diretório e publicação conjunta com staging e rollback. O commit corretivo é ancestral do ponto de partida atual. Auditoria detalhada em `AUDITORIA_FASE_8.md`.
- Fase 9: planejada e ainda não iniciada. A Fase 9A deve preceder a Fase 9B.

## Trabalho realizado recentemente

- As correções da Fase 8 foram versionadas no commit `31ad957`; não existem mais apenas como alterações locais sem commit.
- Antes desta atualização exclusivamente documental, a árvore de trabalho estava limpa em `feature/pipeline-multiedicao`, no commit `5dee4f90961ef2a59806ce093f3285dbfe4862e5`, sincronizado com o remoto.

## Estado validado

- O piloto de Ciências Biológicas — Bacharelado 2017 usa `CO_GRUPO=1601`, `CO_IES=569` e tem como referência de regressão `CO_CURSO=12027`.
- Na execução do piloto, a base reuniu 268 cursos e reconciliou a oferta focal com 23 inscritos oficiais, 13 participantes oficiais e Conceito Enade 3.
- A execução de Biologia 2025 reuniu 428 cursos, mantendo o contrato próprio da edição.
- O baseline atual registra 218 testes sem integração aprovados, 19 testes de integração aprovados e 237 testes totais aprovados. `ruff check .` passou.
- As CLIs reais de 2017 e 2025 foram aprovadas e publicaram CSVs e `evidencias.json` consistentes com schema `2.0` em ambas as execuções.

## Limites atuais

- A Fase 7 gera CSVs de validação e análise em `dados_processados/<ano>/<slug>/`; na análise, a Fase 8 grava também `evidencias.json` ao lado desses CSVs.
- Não há junção individual entre arquivos temáticos e as tabelas individuais de auditoria não entram na base integrada.
- O piloto UFPA possui Conceito 3; não deve ser criado artificialmente um grupo de UFPA com Conceito 1.
- A matriz teórica de dimensões do processo formativo permanece pendente. Não formar índice global ou dimensões sem a validação teórica e psicométrica correspondente.

## Próximo passo recomendado

Iniciar a definição formal da Fase 9A (contraste focal → benchmarks → efeitos/incerteza) conforme `documentacao/PLANO_EVOLUCAO_PIPELINE_com_entrega_biologia`. A Fase 9A ainda não foi implementada e deve começar pela formalização da pergunta, dos universos, dos critérios, dos estimandos, das medidas de efeito e da incerteza, com contratos e testes próprios antes da integração. A Fase 9B será o motor de alertas mecânicos apoiado nesses resultados. A Fase 10 continua sendo o teste end-to-end permanente. O piloto tem Conceito 3; não fabricar Grupo A de Conceito 1.

## Decisões e pendências operacionais

- Pacotes schema `1.0` precisam ser regenerados. O schema `2.0` exige todos os blocos e seus denominadores; capacidade e aplicabilidade do processo são explícitas.
- Falhas tratáveis da publicação preservam a geração anterior. Interrupção abrupta durante a troca pode exigir recuperar o backup e remover o lock após inspeção; ver `EXECUCAO.md`.
- As correções auditadas da Fase 8 já estão versionadas em `31ad957`, commit ancestral do ponto de partida `5dee4f90961ef2a59806ce093f3285dbfe4862e5` na branch `feature/pipeline-multiedicao`.
