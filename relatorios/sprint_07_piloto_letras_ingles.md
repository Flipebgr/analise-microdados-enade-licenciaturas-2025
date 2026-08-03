# Sprint 07 — Piloto de Letras–Inglês

## Síntese

A base analítica reúne **138 cursos** de Letras–Inglês. Foram localizadas **5 ofertas da UFPA**, das quais **4** possuem Conceito Enade 1.

A unidade de análise é `CO_CURSO`. As tabelas temáticas foram agregadas separadamente e unidas apenas após a redução para uma linha por curso.

## Ofertas da UFPA

|   CO_CURSO | ROTULO_OFERTA         |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   nt_ger_count |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |   nt_ger_percentil_brasil |
|-----------:|:----------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------:|--------------:|--------------:|--------------:|--------------------------:|
|     114877 | Altamira — Presencial |                    1 |              22 |                  21 |                       0.955 |             21 |        31.844 |        25.043 |         5.905 |                     3.150 |
|      23777 | Belém — Presencial    |                    3 |             100 |                  85 |                       0.850 |             85 |        56.454 |        53.273 |         6.918 |                    70.866 |
|     114875 | Bragança — Presencial |                    1 |              44 |                  41 |                       0.932 |             41 |        45.193 |        38.778 |         7.085 |                    37.008 |
|     114847 | Cametá — Presencial   |                    1 |              17 |                  15 |                       0.882 |             15 |        34.617 |        26.147 |         6.850 |                    10.236 |
|      95652 | Soure — Presencial    |                    1 |              44 |                  37 |                       0.841 |             37 |        31.834 |        23.170 |         6.649 |                     2.362 |

## Comparações regionais e nacionais

| RECORTE                      | INDICADOR   |   N_CURSOS |   N_PARTICIPANTES |   MEDIA_CURSOS |   MEDIA_PONDERADA_PARTICIPANTES |   MEDIANA_CURSOS | DP_CURSOS          |    P25 |    P75 |
|:-----------------------------|:------------|-----------:|------------------:|---------------:|--------------------------------:|-----------------:|:-------------------|-------:|-------:|
| UFPA — Altamira — Presencial | nt_ger_mean |          1 |            21.000 |         31.844 |                          31.844 |           31.844 | <NA>               | 31.844 | 31.844 |
| UFPA — Bragança — Presencial | nt_ger_mean |          1 |            41.000 |         45.193 |                          45.193 |           45.193 | <NA>               | 45.193 | 45.193 |
| UFPA — Cametá — Presencial   | nt_ger_mean |          1 |            15.000 |         34.617 |                          34.617 |           34.617 | <NA>               | 34.617 | 34.617 |
| UFPA — Soure — Presencial    | nt_ger_mean |          1 |            37.000 |         31.834 |                          31.834 |           31.834 | <NA>               | 31.834 | 31.834 |
| UFPA — Belém — Presencial    | nt_ger_mean |          1 |            85.000 |         56.454 |                          56.454 |           56.454 | <NA>               | 56.454 | 56.454 |
| UFPA agregada                | nt_ger_mean |          5 |           199.000 |         39.988 |                          45.313 |           34.617 | 10.722393433750497 | 31.844 | 45.193 |
| Região Norte sem UFPA        | nt_ger_mean |          9 |           186.000 |         43.368 |                          43.460 |           39.947 | 7.149260539566853  | 38.853 | 47.486 |
| Região Norte completa        | nt_ger_mean |         14 |           385.000 |         42.161 |                          44.418 |           39.718 | 8.345816493348925  | 35.334 | 47.128 |
| Nordeste                     | nt_ger_mean |         49 |          1115.000 |         48.407 |                          50.492 |           47.623 | 10.64802306992923  | 41.906 | 54.051 |
| Sudeste                      | nt_ger_mean |         28 |           956.000 |         55.447 |                          52.073 |           54.059 | 11.122506057023022 | 48.508 | 64.629 |
| Sul                          | nt_ger_mean |         29 |          1109.000 |         54.357 |                          48.080 |           51.769 | 13.32444342220508  | 44.360 | 66.409 |
| Centro-Oeste                 | nt_ger_mean |          7 |           101.000 |         55.856 |                          58.475 |           52.302 | 9.943376076234372  | 48.850 | 61.894 |
| Brasil geral                 | nt_ger_mean |        127 |          3666.000 |         51.040 |                          49.757 |           49.704 | 11.859247071248    | 42.882 | 59.744 |
| Brasil sem UFPA              | nt_ger_mean |        122 |          3467.000 |         51.493 |                          50.012 |           49.981 | 11.721738537652842 | 43.164 | 60.325 |
| Restante do Brasil sem Norte | nt_ger_mean |        113 |          3281.000 |         52.140 |                          50.383 |           50.789 | 11.792470075781152 | 44.110 | 61.470 |

As médias ponderadas usam o número de participantes válidos em `NT_GER`. As médias simples tratam cada curso com o mesmo peso.

## Benchmark comparável

|   CO_CURSO_ALVO | ROTULO_ALVO           | modalidade   |   participantes_alvo |   n_cursos_comparaveis | criterio                                                                                                 |
|----------------:|:----------------------|:-------------|---------------------:|-----------------------:|:---------------------------------------------------------------------------------------------------------|
|           95652 | Soure — Presencial    | Presencial   |                   37 |                     21 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|          114847 | Cametá — Presencial   | Presencial   |                   15 |                     20 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|          114875 | Bragança — Presencial | Presencial   |                   41 |                     17 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|          114877 | Altamira — Presencial | Presencial   |                   21 |                     22 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |

## Limitações

- não há identificação comum de estudante entre arquivos temáticos;
- associações entre indicadores de arquivos diferentes são ecológicas;
- cursos pequenos podem apresentar estimativas instáveis;
- os benchmarks são descritivos e não constituem desenho causal;
- itens de processo formativo não foram condensados em índice único.