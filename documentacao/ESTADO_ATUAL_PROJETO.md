# Estado operacional do projeto

## Referência de continuidade

- Branch operacional: `feature/pipeline-multiedicao`.
- Último commit registrado neste estado: `992dbff feat(fase-7): orquestra pipeline generico por area`.
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

## Estado validado

- O piloto de Ciências Biológicas — Bacharelado 2017 usa `CO_GRUPO=1601`, `CO_IES=569` e tem como referência de regressão `CO_CURSO=12027`.
- Na execução do piloto, a base reuniu 268 cursos e reconciliou a oferta focal com 23 inscritos oficiais, 13 participantes oficiais e Conceito Enade 3.
- A execução de Biologia 2025 reuniu 428 cursos, mantendo o contrato próprio da edição.
- A validação mais recente da Fase 7 registrou 149 testes aprovados; os testes de integração foram executados separadamente, com 17 aprovados e 132 não selecionados. `ruff check .` passou.

## Limites atuais

- A Fase 7 gera CSVs de validação e análise em `dados_processados/<ano>/<slug>/`; não gera `evidencias.json`, benchmarks, alertas ou relatório final.
- Não há junção individual entre arquivos temáticos e as tabelas individuais de auditoria não entram na base integrada.
- O piloto UFPA possui Conceito 3; não deve ser criado artificialmente um grupo de UFPA com Conceito 1.
- A matriz teórica de dimensões do processo formativo permanece pendente. Não formar índice global ou dimensões sem a validação teórica e psicométrica correspondente.

## Próximo passo recomendado

Iniciar a Fase 8: definir e validar o schema versionado de `evidencias.json`, derivado exclusivamente dos CSVs e agregados já validados. O pacote deve conservar proveniência, denominadores, ausências e, no processo formativo, os percentuais separados de códigos 7 e 8. Antes disso, revisar se a Fase 7 precisa de contratos explícitos para o contraste focal e benchmarks, pois eles não devem ser inferidos automaticamente para o piloto de Conceito 3.
