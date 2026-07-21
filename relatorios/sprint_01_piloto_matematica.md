# Sprint 1 — Piloto de Matemática

## Resumo executivo

A base analítica contém **482 cursos de Matemática**, dos quais **8** pertencem à UFPA. Foram classificados **7** cursos da UFPA no grupo A (Conceito Enade 1) e **1** no grupo B (conceito superior).

A unidade analítica final é `CO_CURSO`. Todos os arquivos temáticos foram tratados separadamente e agregados antes da junção um-para-um.

## Grupos comparativos

| GRUPO_CODIGO   | GRUPO                    |   N_CURSOS |   N_PARTICIPANTES_OFICIAIS |
|:---------------|:-------------------------|-----------:|---------------------------:|
| A              | UFPA — Conceito 1        |          7 |                        317 |
| B              | UFPA — conceito superior |          1 |                         61 |
| C              | Outras IES do Pará       |          5 |                         85 |
| D              | Restante da Região Norte |         27 |                        413 |
| E              | Restante do Brasil       |        442 |                       9583 |

## Desempenho — cursos da UFPA

|   CO_CURSO | ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   PARTICIPANTES_NUM |   nt_ger_count |   nt_ger_mean |   nt_ger_median |   nt_ger_std |   nt_ger_percentil_brasil |
|-----------:|:-------------------------|---------------------:|--------------------:|---------------:|--------------:|----------------:|-------------:|--------------------------:|
|      86396 | Belém - EaD              |                    1 |                  16 |             16 |         34.74 |           33.79 |         9.73 |                      1.59 |
|    1300375 | Salinópolis - Presencial |                    1 |                  26 |             26 |         41.36 |           40.43 |         9.46 |                     13.15 |
|      12033 | Bragança - Presencial    |                    1 |                  34 |             34 |         41.75 |           41.54 |         9.81 |                     14.06 |
|      12074 | Cametá - Presencial      |                    1 |                  72 |             72 |         43.90 |           43.66 |         9.25 |                     20.86 |
|     114853 | Abaetetuba - Presencial  |                    1 |                  86 |             86 |         44.20 |           43.66 |         9.80 |                     22.00 |
|      12035 | Castanhal - Presencial   |                    1 |                  52 |             52 |         44.83 |           44.64 |         8.65 |                     24.94 |
|      12044 | Breves - Presencial      |                    1 |                  31 |             31 |         44.83 |           44.64 |         7.57 |                     25.17 |
|      11999 | Belém - Presencial       |                    3 |                  61 |             61 |         54.14 |           52.36 |        11.14 |                     73.47 |

## Contrastes exploratórios de NT_GER

| CONTRASTE   | VARIAVEL   |   N_A |   N_COMPARACAO |   DIF_MEDIA |   HEDGES_G |
|:------------|:-----------|------:|---------------:|------------:|-----------:|
| A vs B      | NT_GER     |   317 |             61 |     -10.818 |     -1.108 |
| A vs C      | NT_GER     |   317 |             85 |      -4.566 |     -0.458 |
| A vs D      | NT_GER     |   317 |            413 |      -0.794 |     -0.074 |
| A vs E      | NT_GER     |   317 |           9553 |      -5.434 |     -0.413 |

Os tamanhos de efeito descrevem diferenças de distribuição entre participantes nos arquivos de desempenho. Não estabelecem causalidade e não vinculam nota a respostas de outros arquivos.

## Benchmark comparável

|   CO_CURSO_ALVO | ROTULO_ALVO              | modalidade   |   participantes_alvo |   n_cursos_comparaveis | criterio                                                                                                 |
|----------------:|:-------------------------|:-------------|---------------------:|-----------------------:|:---------------------------------------------------------------------------------------------------------|
|           12033 | Bragança - Presencial    | Presencial   |                   34 |                     37 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|           12035 | Castanhal - Presencial   | Presencial   |                   52 |                     21 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|           12044 | Breves - Presencial      | Presencial   |                   31 |                     38 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|           12074 | Cametá - Presencial      | Presencial   |                   72 |                     12 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|           86396 | Belém - EaD              | EaD          |                   16 |                     10 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|          114853 | Abaetetuba - Presencial  | Presencial   |                   86 |                      9 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|         1300375 | Salinópolis - Presencial | Presencial   |                   26 |                     47 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |

## Processo formativo

| escala                                            |   n_itens |   n_casos_completos |   cronbach_alpha | decisao                                                             |
|:--------------------------------------------------|----------:|--------------------:|-----------------:|:--------------------------------------------------------------------|
| QE_I20-QE_I66 (exploratória, sem uso como índice) |        47 |                3793 |            0.990 | Não formar índice único nesta sprint; resultado apenas diagnóstico. |

O alfa total é apenas diagnóstico. Não foi criado índice único para QE_I20–QE_I66 porque o bloco reúne dimensões teoricamente distintas.

## Produtos gráficos

1. painel das ofertas da UFPA;
2. posição relativa nacional;
3. boxplot e ECDF de NT_GER;
4. indicadores socioeconômicos agregados;
5. heatmap do processo formativo;
6. recomendação do curso e da instituição.

## Limitações

- não há chave individual entre arquivos;
- associações entre desempenho, perfil e percepção são ecológicas;
- percentuais de cursos pequenos podem ser instáveis;
- o benchmark comparável desta sprint usa filtros determinísticos, não pareamento causal;
- os itens de processo formativo ainda exigem validação dimensional antes de índices.

## Decisão para a próxima sprint

Validar os gráficos, os indicadores derivados e os critérios do benchmark antes de iniciar a redação ABNT definitiva ou replicar o protocolo para outras áreas.