# Sprint 10 — Ciências Biológicas com estudo focal de Soure

## Síntese

A base analítica reúne **428 cursos** de Ciências Biológicas. Foram localizadas **5 ofertas da UFPA**. Não há oferta da UFPA com Conceito Enade 1; por isso, o contraste principal não reproduz o desenho usado nas áreas com Conceito 1.

A oferta de **Soure (CO_CURSO 104640)** é o caso focal. A análise geral da área é preservada, mas Soure é contrastada com as demais ofertas da UFPA, outras IES do Pará, Norte sem Pará, Brasil sem Norte e benchmark estruturalmente comparável.

A unidade de análise principal é `CO_CURSO`. Arquivos temáticos são tratados e agregados separadamente antes de qualquer junção. Não há join individual entre arquivos distintos.

## Ofertas da UFPA

|   CO_CURSO | ROTULO_OFERTA         |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   nt_ger_count |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |   nt_ger_percentil_brasil |   nt_ger_percentil_norte |   nt_ger_percentil_para |
|-----------:|:----------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------:|--------------:|--------------:|--------------:|--------------------------:|-------------------------:|------------------------:|
|      18491 | Altamira — Presencial |                    4 |              46 |                  39 |                       0.848 |             39 |        54.754 |        52.962 |         6.192 |                    33.416 |                   47.500 |                  52.941 |
|    1148030 | Belém — EaD           |                    3 |             141 |                 101 |                       0.716 |            101 |        51.902 |        50.515 |         5.745 |                    20.297 |                   27.500 |                  23.529 |
|      12023 | Belém — Presencial    |                    4 |             114 |                  94 |                       0.825 |             94 |        58.363 |        57.529 |         6.170 |                    59.158 |                   80.000 |                  82.353 |
|      18487 | Bragança — Presencial |                    4 |              41 |                  36 |                       0.878 |             36 |        60.165 |        59.286 |         6.368 |                    69.059 |                   90.000 |                  88.235 |
|     104640 | Soure — Presencial    |                    3 |              65 |                  49 |                       0.754 |             49 |        53.505 |        50.567 |         6.526 |                    27.228 |                   40.000 |                  41.176 |

## Oferta focal de Soure

|   CO_CURSO | ROTULO_OFERTA      |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   nt_ger_count |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |   nt_ger_percentil_brasil |   nt_ger_percentil_norte |   nt_ger_percentil_para |
|-----------:|:-------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------:|--------------:|--------------:|--------------:|--------------------------:|-------------------------:|------------------------:|
|     104640 | Soure — Presencial |                    3 |              65 |                  49 |                       0.754 |             49 |        53.505 |        50.567 |         6.526 |                    27.228 |                   40.000 |                  41.176 |

## Comparações regionais e nacionais

| RECORTE                      | INDICADOR   |   N_CURSOS |   N_PARTICIPANTES |   MEDIA_CURSOS |   MEDIA_PONDERADA_PARTICIPANTES |   MEDIANA_CURSOS | DP_CURSOS          |    P25 |    P75 |
|:-----------------------------|:------------|-----------:|------------------:|---------------:|--------------------------------:|-----------------:|:-------------------|-------:|-------:|
| UFPA — Belém — EaD           | nt_ger_mean |          1 |           101.000 |         51.902 |                          51.902 |           51.902 | <NA>               | 51.902 | 51.902 |
| UFPA — Soure — Presencial    | nt_ger_mean |          1 |            49.000 |         53.505 |                          53.505 |           53.505 | <NA>               | 53.505 | 53.505 |
| UFPA — Altamira — Presencial | nt_ger_mean |          1 |            39.000 |         54.754 |                          54.754 |           54.754 | <NA>               | 54.754 | 54.754 |
| UFPA — Bragança — Presencial | nt_ger_mean |          1 |            36.000 |         60.165 |                          60.165 |           60.165 | <NA>               | 60.165 | 60.165 |
| UFPA — Belém — Presencial    | nt_ger_mean |          1 |            94.000 |         58.363 |                          58.363 |           58.363 | <NA>               | 58.363 | 58.363 |
| UFPA agregada                | nt_ger_mean |          5 |           319.000 |         55.738 |                          55.333 |           54.754 | 3.4337089200582414 | 53.505 | 58.363 |
| Região Norte sem UFPA        | nt_ger_mean |         35 |           828.000 |         55.042 |                          55.129 |           55.464 | 4.6184250939256986 | 51.688 | 57.134 |
| Região Norte completa        | nt_ger_mean |         40 |          1147.000 |         55.129 |                          55.186 |           55.447 | 4.456321268178757  | 51.880 | 57.280 |
| Nordeste                     | nt_ger_mean |        128 |          3628.000 |         56.508 |                          57.744 |           56.392 | 5.552409165244105  | 52.450 | 59.682 |
| Sudeste                      | nt_ger_mean |        129 |          3467.000 |         59.110 |                          60.632 |           59.073 | 7.189296406617683  | 54.172 | 64.426 |
| Sul                          | nt_ger_mean |         68 |          2392.000 |         58.633 |                          57.098 |           58.826 | 6.817177486847     | 53.976 | 62.579 |
| Centro-Oeste                 | nt_ger_mean |         39 |           731.000 |         55.233 |                          57.180 |           55.284 | 5.301626731938055  | 51.716 | 57.994 |
| Brasil geral                 | nt_ger_mean |        404 |         11365.000 |         57.437 |                          58.195 |           57.150 | 6.390668323282056  | 53.087 | 61.846 |
| Brasil sem UFPA              | nt_ger_mean |        399 |         11046.000 |         57.458 |                          58.277 |           57.161 | 6.418605208956363  | 53.078 | 61.935 |
| Restante do Brasil sem Norte | nt_ger_mean |        364 |         10218.000 |         57.691 |                          58.532 |           57.565 | 6.523496859217238  | 53.420 | 62.371 |

## Benchmark comparável de Soure

|   CO_CURSO_ALVO | ROTULO_ALVO        |   participantes_alvo |   n_cursos_comparaveis | criterio                                                                                                |
|----------------:|:-------------------|---------------------:|-----------------------:|:--------------------------------------------------------------------------------------------------------|
|          104640 | Soure — Presencial |                   49 |                     56 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x Soure |

## Comparação focal

| RECORTE_FOCAL      | INDICADOR                |   N_CURSOS |   MEDIA_CURSOS |   MEDIANA_CURSOS | DP_CURSOS           |    P25 |    P75 |
|:-------------------|:-------------------------|-----------:|---------------:|-----------------:|:--------------------|-------:|-------:|
| Soure              | nt_ger_mean              |          1 |         53.505 |           53.505 | <NA>                | 53.505 | 53.505 |
| Soure              | nt_obj_mean              |          1 |         50.567 |           50.567 | <NA>                | 50.567 | 50.567 |
| Soure              | nt_dis_mean              |          1 |          6.526 |            6.526 | <NA>                |  6.526 |  6.526 |
| Soure              | taxa_presenca_microdados |          1 |          0.754 |            0.754 | <NA>                |  0.754 |  0.754 |
| Soure              | renda_ate_3sm_pct        |          1 |          0.904 |            0.904 | nan                 |  0.904 |  0.904 |
| Soure              | trabalha_pct             |          1 |          0.365 |            0.365 | nan                 |  0.365 |  0.365 |
| Soure              | acao_afirmativa_pct      |          1 |          0.731 |            0.731 | nan                 |  0.731 |  0.731 |
| Soure              | auxilio_permanencia_pct  |          1 |          0.269 |            0.269 | nan                 |  0.269 |  0.269 |
| Soure              | bolsa_academica_pct      |          1 |          0.340 |            0.340 | nan                 |  0.340 |  0.340 |
| Soure              | estudo_4h_ou_mais_pct    |          1 |          0.385 |            0.385 | nan                 |  0.385 |  0.385 |
| Soure              | qe_i68_media             |          1 |          8.635 |            8.635 | <NA>                |  8.635 |  8.635 |
| Soure              | qe_i69_media             |          1 |          8.788 |            8.788 | <NA>                |  8.788 |  8.788 |
| UFPA sem Soure     | nt_ger_mean              |          4 |         56.296 |           56.559 | 3.693641827384726   | 54.041 | 58.814 |
| UFPA sem Soure     | nt_obj_mean              |          4 |         55.073 |           55.245 | 4.04210630877251    | 52.350 | 57.968 |
| UFPA sem Soure     | nt_dis_mean              |          4 |          6.119 |            6.181 | 0.26448968006981527 |  6.064 |  6.236 |
| UFPA sem Soure     | taxa_presenca_microdados |          4 |          0.817 |            0.836 | 0.07040844245458963 |  0.797 |  0.855 |
| UFPA sem Soure     | renda_ate_3sm_pct        |          4 |          0.842 |            0.826 | 0.10481353881871269 |  0.768 |  0.900 |
| UFPA sem Soure     | trabalha_pct             |          4 |          0.539 |            0.537 | 0.1415223725238532  |  0.432 |  0.644 |
| UFPA sem Soure     | acao_afirmativa_pct      |          4 |          0.682 |            0.688 | 0.08003629120279161 |  0.630 |  0.741 |
| UFPA sem Soure     | auxilio_permanencia_pct  |          4 |          0.167 |            0.176 | 0.13961801841931779 |  0.083 |  0.259 |
| UFPA sem Soure     | bolsa_academica_pct      |          4 |          0.528 |            0.657 | 0.3454520493069609  |  0.473 |  0.712 |
| UFPA sem Soure     | estudo_4h_ou_mais_pct    |          4 |          0.549 |            0.530 | 0.09957064113957866 |  0.507 |  0.572 |
| UFPA sem Soure     | qe_i68_media             |          4 |          8.780 |            8.692 | 0.4279167990524314  |  8.442 |  9.029 |
| UFPA sem Soure     | qe_i69_media             |          4 |          9.077 |            9.047 | 0.27424235991257384 |  8.899 |  9.225 |
| Outras IES do Pará | nt_ger_mean              |         12 |         55.167 |           54.959 | 4.416762135561982   | 52.061 | 56.656 |
| Outras IES do Pará | nt_obj_mean              |         12 |         54.006 |           53.436 | 4.0275462890750715  | 51.259 | 54.618 |
| Outras IES do Pará | nt_dis_mean              |         12 |          5.981 |            6.161 | 0.7231075778037315  |  5.462 |  6.484 |
| Outras IES do Pará | taxa_presenca_microdados |         13 |          0.767 |            0.840 | 0.25774971525226337 |  0.717 |  0.938 |
| Outras IES do Pará | renda_ate_3sm_pct        |         12 |          0.891 |            0.941 | 0.10187621886827046 |  0.809 |  0.964 |
| Outras IES do Pará | trabalha_pct             |         12 |          0.585 |            0.525 | 0.19863702188691912 |  0.438 |  0.723 |
| Outras IES do Pará | acao_afirmativa_pct      |         12 |          0.497 |            0.546 | 0.17445120464900135 |  0.489 |  0.586 |
| Outras IES do Pará | auxilio_permanencia_pct  |         12 |          0.350 |            0.347 | 0.23445230159289335 |  0.192 |  0.501 |
| Outras IES do Pará | bolsa_academica_pct      |         12 |          0.557 |            0.649 | 0.2367201303993342  |  0.397 |  0.722 |
| Outras IES do Pará | estudo_4h_ou_mais_pct    |         12 |          0.638 |            0.597 | 0.1474971116642298  |  0.538 |  0.677 |
| Outras IES do Pará | qe_i68_media             |         12 |          8.829 |            8.764 | 0.4567936091854665  |  8.594 |  9.118 |
| Outras IES do Pará | qe_i69_media             |         12 |          8.439 |            8.708 | 1.197109665396723   |  8.080 |  9.278 |
| Norte sem Pará     | nt_ger_mean              |         23 |         54.977 |           55.468 | 4.816381283632793   | 51.339 | 57.134 |
| Norte sem Pará     | nt_obj_mean              |         23 |         54.625 |           54.343 | 3.933300248907092   | 51.716 | 56.933 |
| Norte sem Pará     | nt_dis_mean              |         23 |          5.639 |            5.690 | 1.1033830102878133  |  4.947 |  6.434 |
| Norte sem Pará     | taxa_presenca_microdados |         23 |          0.771 |            0.811 | 0.1672398414881523  |  0.709 |  0.875 |
| Norte sem Pará     | renda_ate_3sm_pct        |         23 |          0.839 |            0.833 | 0.11360820236839084 |  0.757 |  0.917 |
| Norte sem Pará     | trabalha_pct             |         23 |          0.557 |            0.500 | 0.2144970355244705  |  0.462 |  0.675 |
| Norte sem Pará     | acao_afirmativa_pct      |         23 |          0.402 |            0.417 | 0.18144909870871895 |  0.303 |  0.500 |
| Norte sem Pará     | auxilio_permanencia_pct  |         23 |          0.376 |            0.375 | 0.2750845466598043  |  0.136 |  0.564 |
| Norte sem Pará     | bolsa_academica_pct      |         22 |          0.708 |            0.750 | 0.2123412037640649  |  0.644 |  0.807 |
| Norte sem Pará     | estudo_4h_ou_mais_pct    |         23 |          0.526 |            0.529 | 0.16973684189194474 |  0.467 |  0.644 |
| Norte sem Pará     | qe_i68_media             |         23 |          8.820 |            8.806 | 0.554326679682785   |  8.310 |  9.292 |
| Norte sem Pará     | qe_i69_media             |         23 |          8.925 |            9.042 | 0.6582398005939475  |  8.532 |  9.357 |
| Brasil sem Norte   | nt_ger_mean              |        364 |         57.691 |           57.565 | 6.523496859217238   | 53.420 | 62.371 |
| Brasil sem Norte   | nt_obj_mean              |        364 |         57.256 |           56.756 | 5.630492764760812   | 53.234 | 61.042 |
| Brasil sem Norte   | nt_dis_mean              |        364 |          5.943 |            6.060 | 1.3082226785228062  |  5.266 |  6.879 |
| Brasil sem Norte   | taxa_presenca_microdados |        387 |          0.781 |            0.844 | 0.22011988934260143 |  0.667 |  0.947 |
| Brasil sem Norte   | renda_ate_3sm_pct        |        368 |          0.749 |            0.800 | 0.21111460621715195 |  0.592 |  0.934 |
| Brasil sem Norte   | trabalha_pct             |        368 |          0.665 |            0.692 | 0.22749504173416862 |  0.500 |  0.833 |
| Brasil sem Norte   | acao_afirmativa_pct      |        368 |          0.369 |            0.416 | 0.20753860434751437 |  0.200 |  0.500 |
| Brasil sem Norte   | auxilio_permanencia_pct  |        368 |          0.300 |            0.253 | 0.27256135889322847 |  0.007 |  0.521 |
| Brasil sem Norte   | bolsa_academica_pct      |        367 |          0.547 |            0.625 | 0.3223160948159597  |  0.308 |  0.800 |
| Brasil sem Norte   | estudo_4h_ou_mais_pct    |        368 |          0.576 |            0.579 | 0.1898727232448521  |  0.455 |  0.700 |
| Brasil sem Norte   | qe_i68_media             |        368 |          8.678 |            8.737 | 0.8285536830554737  |  8.269 |  9.220 |
| Brasil sem Norte   | qe_i69_media             |        368 |          8.644 |            8.902 | 1.0431776109079158  |  8.235 |  9.333 |

## Perfil diferencial de Soure

| INDICADOR                | REFERENCIA           |   VALOR_SOURE |   N_CURSOS_REFERENCIA |   MEDIA_REFERENCIA |   DP_REFERENCIA |   DIFERENCA_SOURE_REFERENCIA |   Z_SOURE_REFERENCIA |
|:-------------------------|:---------------------|--------------:|----------------------:|-------------------:|----------------:|-----------------------------:|---------------------:|
| nt_ger_mean              | UFPA sem Soure       |        53.505 |                     4 |             56.296 |           3.694 |                       -2.791 |               -0.756 |
| nt_ger_mean              | Benchmark comparável |        53.505 |                    56 |             62.137 |           4.582 |                       -8.632 |               -1.884 |
| nt_ger_mean              | Pará sem UFPA        |        53.505 |                    12 |             55.167 |           4.417 |                       -1.662 |               -0.376 |
| nt_ger_mean              | Norte sem Pará       |        53.505 |                    23 |             54.977 |           4.816 |                       -1.472 |               -0.306 |
| nt_ger_mean              | Brasil sem Norte     |        53.505 |                   364 |             57.691 |           6.523 |                       -4.186 |               -0.642 |
| nt_obj_mean              | UFPA sem Soure       |        50.567 |                     4 |             55.073 |           4.042 |                       -4.505 |               -1.115 |
| nt_obj_mean              | Benchmark comparável |        50.567 |                    56 |             60.907 |           4.390 |                      -10.339 |               -2.355 |
| nt_obj_mean              | Pará sem UFPA        |        50.567 |                    12 |             54.006 |           4.028 |                       -3.438 |               -0.854 |
| nt_obj_mean              | Norte sem Pará       |        50.567 |                    23 |             54.625 |           3.933 |                       -4.057 |               -1.031 |
| nt_obj_mean              | Brasil sem Norte     |        50.567 |                   364 |             57.256 |           5.630 |                       -6.689 |               -1.188 |
| nt_dis_mean              | UFPA sem Soure       |         6.526 |                     4 |              6.119 |           0.264 |                        0.407 |                1.537 |
| nt_dis_mean              | Benchmark comparável |         6.526 |                    56 |              6.706 |           0.657 |                       -0.180 |               -0.274 |
| nt_dis_mean              | Pará sem UFPA        |         6.526 |                    12 |              5.981 |           0.723 |                        0.544 |                0.753 |
| nt_dis_mean              | Norte sem Pará       |         6.526 |                    23 |              5.639 |           1.103 |                        0.887 |                0.804 |
| nt_dis_mean              | Brasil sem Norte     |         6.526 |                   364 |              5.943 |           1.308 |                        0.583 |                0.445 |
| taxa_presenca_microdados | UFPA sem Soure       |         0.754 |                     4 |              0.817 |           0.070 |                       -0.063 |               -0.893 |
| taxa_presenca_microdados | Benchmark comparável |         0.754 |                    56 |              0.855 |           0.097 |                       -0.101 |               -1.048 |
| taxa_presenca_microdados | Pará sem UFPA        |         0.754 |                    13 |              0.767 |           0.258 |                       -0.013 |               -0.050 |
| taxa_presenca_microdados | Norte sem Pará       |         0.754 |                    23 |              0.771 |           0.167 |                       -0.018 |               -0.105 |
| taxa_presenca_microdados | Brasil sem Norte     |         0.754 |                   387 |              0.781 |           0.220 |                       -0.028 |               -0.125 |
| renda_ate_3sm_pct        | UFPA sem Soure       |         0.904 |                     4 |              0.842 |           0.105 |                        0.062 |                0.594 |
| renda_ate_3sm_pct        | Benchmark comparável |         0.904 |                    56 |              0.728 |           0.204 |                        0.176 |                0.861 |
| renda_ate_3sm_pct        | Pará sem UFPA        |         0.904 |                    12 |              0.891 |           0.102 |                        0.013 |                0.127 |
| renda_ate_3sm_pct        | Norte sem Pará       |         0.904 |                    23 |              0.839 |           0.114 |                        0.064 |                0.567 |
| renda_ate_3sm_pct        | Brasil sem Norte     |         0.904 |                   368 |              0.749 |           0.211 |                        0.154 |                0.731 |
| trabalha_pct             | UFPA sem Soure       |         0.365 |                     4 |              0.539 |           0.142 |                       -0.174 |               -1.228 |
| trabalha_pct             | Benchmark comparável |         0.365 |                    56 |              0.518 |           0.153 |                       -0.152 |               -0.994 |
| trabalha_pct             | Pará sem UFPA        |         0.365 |                    12 |              0.585 |           0.199 |                       -0.220 |               -1.107 |
| trabalha_pct             | Norte sem Pará       |         0.365 |                    23 |              0.557 |           0.214 |                       -0.192 |               -0.894 |
| trabalha_pct             | Brasil sem Norte     |         0.365 |                   368 |              0.665 |           0.227 |                       -0.300 |               -1.318 |
| acao_afirmativa_pct      | UFPA sem Soure       |         0.731 |                     4 |              0.682 |           0.080 |                        0.048 |                0.605 |
| acao_afirmativa_pct      | Benchmark comparável |         0.731 |                    56 |              0.499 |           0.071 |                        0.232 |                3.260 |
| acao_afirmativa_pct      | Pará sem UFPA        |         0.731 |                    12 |              0.497 |           0.174 |                        0.233 |                1.338 |
| acao_afirmativa_pct      | Norte sem Pará       |         0.731 |                    23 |              0.402 |           0.181 |                        0.329 |                1.814 |
| acao_afirmativa_pct      | Brasil sem Norte     |         0.731 |                   368 |              0.369 |           0.208 |                        0.362 |                1.742 |
| auxilio_permanencia_pct  | UFPA sem Soure       |         0.269 |                     4 |              0.167 |           0.140 |                        0.103 |                0.734 |
| auxilio_permanencia_pct  | Benchmark comparável |         0.269 |                    56 |              0.377 |           0.190 |                       -0.108 |               -0.566 |
| auxilio_permanencia_pct  | Pará sem UFPA        |         0.269 |                    12 |              0.350 |           0.234 |                       -0.081 |               -0.345 |
| auxilio_permanencia_pct  | Norte sem Pará       |         0.269 |                    23 |              0.376 |           0.275 |                       -0.106 |               -0.386 |
| auxilio_permanencia_pct  | Brasil sem Norte     |         0.269 |                   368 |              0.300 |           0.273 |                       -0.031 |               -0.114 |
| bolsa_academica_pct      | UFPA sem Soure       |         0.340 |                     4 |              0.528 |           0.345 |                       -0.188 |               -0.543 |
| bolsa_academica_pct      | Benchmark comparável |         0.340 |                    56 |              0.709 |           0.135 |                       -0.369 |               -2.723 |
| bolsa_academica_pct      | Pará sem UFPA        |         0.340 |                    12 |              0.557 |           0.237 |                       -0.217 |               -0.915 |
| bolsa_academica_pct      | Norte sem Pará       |         0.340 |                    22 |              0.708 |           0.212 |                       -0.368 |               -1.732 |
| bolsa_academica_pct      | Brasil sem Norte     |         0.340 |                   367 |              0.547 |           0.322 |                       -0.207 |               -0.641 |
| estudo_4h_ou_mais_pct    | UFPA sem Soure       |         0.385 |                     4 |              0.549 |           0.100 |                       -0.165 |               -1.654 |
| estudo_4h_ou_mais_pct    | Benchmark comparável |         0.385 |                    56 |              0.679 |           0.099 |                       -0.294 |               -2.969 |
| estudo_4h_ou_mais_pct    | Pará sem UFPA        |         0.385 |                    12 |              0.638 |           0.147 |                       -0.253 |               -1.716 |
| estudo_4h_ou_mais_pct    | Norte sem Pará       |         0.385 |                    23 |              0.526 |           0.170 |                       -0.142 |               -0.834 |
| estudo_4h_ou_mais_pct    | Brasil sem Norte     |         0.385 |                   368 |              0.576 |           0.190 |                       -0.192 |               -1.009 |
| qe_i68_media             | UFPA sem Soure       |         8.635 |                     4 |              8.780 |           0.428 |                       -0.145 |               -0.339 |
| qe_i68_media             | Benchmark comparável |         8.635 |                    56 |              8.605 |           0.437 |                        0.029 |                0.067 |
| qe_i68_media             | Pará sem UFPA        |         8.635 |                    12 |              8.829 |           0.457 |                       -0.194 |               -0.425 |
| qe_i68_media             | Norte sem Pará       |         8.635 |                    23 |              8.820 |           0.554 |                       -0.186 |               -0.335 |
| qe_i68_media             | Brasil sem Norte     |         8.635 |                   368 |              8.678 |           0.829 |                       -0.043 |               -0.052 |
| qe_i69_media             | UFPA sem Soure       |         8.788 |                     4 |              9.077 |           0.274 |                       -0.289 |               -1.053 |
| qe_i69_media             | Benchmark comparável |         8.788 |                    56 |              8.960 |           0.453 |                       -0.172 |               -0.378 |
| qe_i69_media             | Pará sem UFPA        |         8.788 |                    12 |              8.439 |           1.197 |                        0.349 |                0.292 |
| qe_i69_media             | Norte sem Pará       |         8.788 |                    23 |              8.925 |           0.658 |                       -0.136 |               -0.207 |
| qe_i69_media             | Brasil sem Norte     |         8.788 |                   368 |              8.644 |           1.043 |                        0.145 |                0.139 |

## Limitações

- não há identificação comum de estudante entre arquivos temáticos;
- relações entre indicadores de arquivos diferentes são ecológicas;
- o estudo focal de Soure é descritivo e comparativo, não causal;
- cursos pequenos podem apresentar estimativas instáveis;
- o benchmark é descritivo e sua composição será submetida à análise de sensibilidade;
- itens de processo formativo não são condensados em índice único sem validação.