# Sprint 08 — Validação analítica de Letras–Inglês

## Objetivo

Validar os produtos da Sprint 07 antes da redação do relatório técnico-científico final de Letras–Inglês (`CO_GRUPO=6407`). A unidade de análise permanece `CO_CURSO`.

## Escopo

A Sprint 08 audita participação e desempenho, indicadores percentuais, comparações regionais e nacionais, sensibilidade de desempenho, benchmark comparável, outliers e associações ecológicas entre indicadores agregados por curso.

## Regras metodológicas preservadas

- nenhuma junção individual entre arquivos temáticos;
- ausência de Conceito Enade não equivale a Conceito 1;
- grupos A–E são exclusivos para comparações independentes;
- Norte e Brasil completos são benchmarks descritivos sobrepostos;
- médias ponderadas usam participantes válidos em `NT_GER`;
- correlações entre temas diferentes são calculadas somente no nível agregado do curso;
- outliers são sinalizados, não removidos automaticamente;
- `QE_I20–QE_I66` não são condensados em índice único sem validação teórica.

## Produtos

A execução gera CSVs de auditoria e sensibilidade em `dados_processados/ingles/`, quatro figuras validadas em `figuras/ingles/` e `relatorios/sprint_08_validacao_letras_ingles.md`.

## Critérios de aceitação

- 138 cursos na base analítica;
- 5 ofertas localizadas da UFPA;
- 4 ofertas da UFPA com Conceito Enade 1;
- uma linha por `CO_CURSO`;
- nenhum N válido superior ao total de registros do curso;
- nenhum indicador percentual fora de 0–1;
- 4 cursos-alvo na sensibilidade do benchmark;
- recortes regional/nacional obrigatórios presentes;
- quatro figuras de validação geradas e não vazias.
