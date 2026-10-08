# Estado operacional do projeto

## Referência de continuidade

- Branch operacional: `feature/pipeline-multiedicao`.
- Commit-base desta implementação: `b93a020be1a27e2ac7a8e69c9b9046623e1889a8`.
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
- Fase 9A: implementação local corrigida e validada, aguardando revisão/aceite; adiciona grupos comparativos, benchmarks, estimandos, efeitos, incerteza, associações ecológicas e pacote de evidências schema `3.0`. Ainda não foi commitada nem enviada ao remoto. A Fase 9B continua planejada e não foi iniciada.

## Trabalho realizado recentemente

- As correções da Fase 8 foram versionadas no commit `31ad957`; não existem mais apenas como alterações locais sem commit.
- O trabalho desta tarefa foi feito em `feature/pipeline-multiedicao`, sobre o commit-base `b93a020be1a27e2ac7a8e69c9b9046623e1889a8`. As alterações da Fase 9A permanecem locais para revisão.
- A especificação metodológica aprovada foi registrada em `PLANO_EVOLUCAO_PIPELINE_com_entrega_biologia` e `METODOLOGIA.md` antes da implementação.

## Estado validado

- O piloto de Ciências Biológicas — Bacharelado 2017 usa `CO_GRUPO=1601`, `CO_IES=569` e tem como referência de regressão `CO_CURSO=12027`.
- Na execução do piloto, a base reuniu 268 cursos e reconciliou a oferta focal com 23 inscritos oficiais, 13 participantes oficiais e Conceito Enade 3.
- A execução de Biologia 2025 reuniu 428 cursos, mantendo o contrato próprio da edição.
- O baseline final registra 267 testes sem integração aprovados, 19 testes de integração aprovados e 286 testes totais aprovados. `ruff check .` e `git diff --check` passaram.
- As CLIs reais de análise 2017 e 2025 foram executadas com as fontes locais e publicaram evidências schema `3.0`. O piloto 2017 reuniu 268 cursos e manteve `CO_CURSO=12027` como foco, ainda no Grupo B. Biologia 2025 reuniu 428 cursos e cinco ofertas focais.
- Para `geral_mean` versus Brasil amplo, o piloto 2017 publicou diferença `1,070733` e IC95% `[0,298801; 1,861839]`. O estimando multifoco 2025 usou os cinco focos elegíveis, média focal `55,737826`, diferença `-2,557343` e IC95% `[-5,192812; 0,205854]`. Recálculos independentes reproduziram esses valores e as associações pós-elegibilidade.
- Os artefatos finais de ambas as edições têm valores e `n_valido` nos membros de benchmark, estimativas secundárias ponderadas e resultados de sensibilidade a outliers; as associações registram cenário sem outliers quando o N permite.

## Limites atuais

- A Fase 7 gera CSVs de validação e análise em `dados_processados/<ano>/<slug>/`; na análise, as Fases 8 e 9A publicam `evidencias.json` e os CSVs de comparação. Schema `2.0` histórico continua validável; schema `3.0` inclui as referências dos artefatos da Fase 9A.
- Não há junção individual entre arquivos temáticos e as tabelas individuais de auditoria não entram na base integrada.
- O piloto UFPA possui Conceito 3; não deve ser criado artificialmente um grupo de UFPA com Conceito 1.
- A matriz teórica de dimensões do processo formativo permanece pendente. Não formar índice global ou dimensões sem a validação teórica e psicométrica correspondente.

## Próximo passo recomendado

Revisar o resultado local validado da Fase 9A e, se aprovado, autorizar seu commit/push antes de qualquer trabalho na Fase 9B. A Fase 9B será o motor de alertas mecânicos apoiado nesses resultados e permanece fora desta tarefa. A Fase 10 continua sendo o teste end-to-end permanente. O piloto tem Conceito 3; não fabricar Grupo A de Conceito 1.

## Decisões e pendências operacionais

- Pacotes schema `1.0` precisam ser regenerados. O schema `2.0` histórico exige exatamente seus blocos e denominadores e rejeita campos exclusivos do `3.0`; não há conversão silenciosa. Capacidade e aplicabilidade do processo são explícitas.
- Falhas tratáveis da publicação preservam a geração anterior. Interrupção abrupta durante a troca pode exigir recuperar o backup e remover o lock após inspeção; ver `EXECUCAO.md`.
- As correções auditadas da Fase 8 já estão versionadas em `31ad957`, commit ancestral do ponto de partida `5dee4f90961ef2a59806ce093f3285dbfe4862e5` na branch `feature/pipeline-multiedicao`.
