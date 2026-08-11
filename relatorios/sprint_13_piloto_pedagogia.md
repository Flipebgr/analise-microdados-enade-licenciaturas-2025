# Sprint 13 — Pedagogia: base analítica e panorama inicial

## Síntese

A base analítica reúne **1200 cursos** de Pedagogia. Foram localizadas **7 ofertas da UFPA**. Não há oferta da UFPA com Conceito Enade 1; portanto, o Grupo A permanece vazio.

O contraste interno da UFPA compara a oferta de Castanhal, Conceito Enade 5, com as seis ofertas Conceito Enade 4. Esse contraste é descritivo e não transforma Conceito 4 em categoria de insuficiência.

A unidade principal de análise é `CO_CURSO`. Cada arquivo temático é tratado e agregado separadamente antes das junções one-to-one. Não há join individual entre arquivos temáticos distintos.

## Ofertas da UFPA

|   CO_CURSO | ROTULO_OFERTA           |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   nt_ger_count |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |   nt_ger_percentil_brasil |   nt_ger_percentil_norte |   nt_ger_percentil_para |
|-----------:|:------------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------:|--------------:|--------------:|--------------:|--------------------------:|-------------------------:|------------------------:|
|      38276 | Abaetetuba — Presencial |                    4 |             124 |                 111 |                       0.895 |            111 |        62.334 |        60.682 |         6.894 |                    65.899 |                   71.795 |                  59.259 |
|      12048 | Altamira — Presencial   |                    4 |              56 |                  51 |                       0.911 |             51 |        59.968 |        59.090 |         6.348 |                    55.979 |                   60.256 |                  51.852 |
|      11996 | Belém — Presencial      |                    4 |             341 |                 280 |                       0.821 |            280 |        65.261 |        64.197 |         6.952 |                    78.034 |                   82.051 |                  77.778 |
|      12061 | Bragança — Presencial   |                    4 |              83 |                  75 |                       0.904 |             75 |        64.559 |        64.373 |         6.530 |                    75.554 |                   80.769 |                  74.074 |
|      12111 | Breves — Presencial     |                    4 |              51 |                  42 |                       0.824 |             42 |        65.890 |        65.026 |         6.935 |                    80.514 |                   87.179 |                  85.185 |
|      12069 | Cametá — Presencial     |                    4 |             148 |                 122 |                       0.824 |            122 |        62.485 |        61.180 |         6.770 |                    66.342 |                   73.077 |                  62.963 |
|      12085 | Castanhal — Presencial  |                    5 |              86 |                  63 |                       0.733 |             63 |        65.463 |        64.438 |         6.956 |                    78.919 |                   83.333 |                  81.481 |

## Comparação regional e nacional

| RECORTE                        | INDICADOR   |   N_CURSOS |   N_PARTICIPANTES |   MEDIA_CURSOS |   MEDIA_PONDERADA_PARTICIPANTES |   MEDIANA_CURSOS | DP_CURSOS          |    P25 |    P75 |
|:-------------------------------|:------------|-----------:|------------------:|---------------:|--------------------------------:|-----------------:|:-------------------|-------:|-------:|
| UFPA — Abaetetuba — Presencial | nt_ger_mean |          1 |           111.000 |         62.334 |                          62.334 |           62.334 | <NA>               | 62.334 | 62.334 |
| UFPA — Breves — Presencial     | nt_ger_mean |          1 |            42.000 |         65.890 |                          65.890 |           65.890 | <NA>               | 65.890 | 65.890 |
| UFPA — Castanhal — Presencial  | nt_ger_mean |          1 |            63.000 |         65.463 |                          65.463 |           65.463 | <NA>               | 65.463 | 65.463 |
| UFPA — Cametá — Presencial     | nt_ger_mean |          1 |           122.000 |         62.485 |                          62.485 |           62.485 | <NA>               | 62.485 | 62.485 |
| UFPA — Bragança — Presencial   | nt_ger_mean |          1 |            75.000 |         64.559 |                          64.559 |           64.559 | <NA>               | 64.559 | 64.559 |
| UFPA — Altamira — Presencial   | nt_ger_mean |          1 |            51.000 |         59.968 |                          59.968 |           59.968 | <NA>               | 59.968 | 59.968 |
| UFPA — Belém — Presencial      | nt_ger_mean |          1 |           280.000 |         65.261 |                          65.261 |           65.261 | <NA>               | 65.261 | 65.261 |
| UFPA agregada                  | nt_ger_mean |          7 |           744.000 |         63.709 |                          63.988 |           64.559 | 2.1735682030830143 | 62.410 | 65.362 |
| Região Norte sem UFPA          | nt_ger_mean |         71 |          2582.000 |         56.088 |                          53.826 |           56.374 | 8.578173638632064  | 51.181 | 62.002 |
| Região Norte completa          | nt_ger_mean |         78 |          3326.000 |         56.771 |                          56.099 |           57.476 | 8.489395391971687  | 51.704 | 63.833 |
| Nordeste                       | nt_ger_mean |        264 |         13735.000 |         56.990 |                          55.582 |           56.593 | 9.703203245105962  | 49.862 | 63.984 |
| Sudeste                        | nt_ger_mean |        452 |         43057.000 |         59.132 |                          51.921 |           59.221 | 9.536643625781242  | 51.853 | 65.400 |
| Sul                            | nt_ger_mean |        217 |         37001.000 |         59.520 |                          51.869 |           60.185 | 8.154641921096168  | 53.921 | 65.054 |
| Centro-Oeste                   | nt_ger_mean |        118 |          3563.000 |         54.947 |                          53.968 |           54.746 | 9.18767168380872   | 49.758 | 61.685 |
| Brasil geral                   | nt_ger_mean |       1129 |        100682.000 |         58.105 |                          52.612 |           58.122 | 9.326802508731966  | 51.642 | 64.474 |
| Brasil sem UFPA                | nt_ger_mean |       1122 |         99938.000 |         58.070 |                          52.527 |           58.053 | 9.343974873239498  | 51.615 | 64.467 |
| Restante do Brasil sem Norte   | nt_ger_mean |       1051 |         97356.000 |         58.204 |                          52.493 |           58.152 | 9.38212384477206   | 51.618 | 64.490 |

## Benchmarks comparáveis por oferta UFPA

|   CO_CURSO_ALVO | ROTULO_ALVO             |   CONCEITO_ALVO |   PARTICIPANTES_ALVO |   N_CURSOS_COMPARAVEIS | CRITERIO                                                                                                         |   nt_ger_mean_ALVO |   nt_ger_mean_MEDIA_BENCHMARK |   nt_ger_mean_DIFERENCA |   nt_ger_mean_Z |   nt_obj_mean_ALVO |   nt_obj_mean_MEDIA_BENCHMARK |   nt_obj_mean_DIFERENCA |   nt_obj_mean_Z |   nt_dis_mean_ALVO |   nt_dis_mean_MEDIA_BENCHMARK |   nt_dis_mean_DIFERENCA |   nt_dis_mean_Z |
|----------------:|:------------------------|----------------:|---------------------:|-----------------------:|:-----------------------------------------------------------------------------------------------------------------|-------------------:|------------------------------:|------------------------:|----------------:|-------------------:|------------------------------:|------------------------:|----------------:|-------------------:|------------------------------:|------------------------:|----------------:|
|           11996 | Belém — Presencial      |               4 |                  280 |                      6 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             65.261 |                        75.027 |                  -9.766 |          -2.387 |             64.197 |                        76.027 |                 -11.830 |          -2.597 |              6.952 |                         7.103 |                  -0.151 |          -0.515 |
|           12048 | Altamira — Presencial   |               4 |                   51 |                     82 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             59.968 |                        65.424 |                  -5.455 |          -0.631 |             59.090 |                        65.771 |                  -6.681 |          -0.756 |              6.348 |                         6.403 |                  -0.055 |          -0.060 |
|           12061 | Bragança — Presencial   |               4 |                   75 |                     57 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             64.559 |                        67.659 |                  -3.100 |          -0.327 |             64.373 |                        68.225 |                  -3.852 |          -0.401 |              6.530 |                         6.539 |                  -0.009 |          -0.009 |
|           12069 | Cametá — Presencial     |               4 |                  122 |                     36 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             62.485 |                        72.410 |                  -9.925 |          -1.392 |             61.180 |                        73.056 |                 -11.875 |          -1.563 |              6.770 |                         6.983 |                  -0.212 |          -0.369 |
|           12085 | Castanhal — Presencial  |               5 |                   63 |                     70 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             65.463 |                        66.885 |                  -1.422 |          -0.159 |             64.438 |                        67.332 |                  -2.894 |          -0.318 |              6.956 |                         6.510 |                   0.446 |           0.463 |
|           12111 | Breves — Presencial     |               4 |                   42 |                     78 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             65.890 |                        64.845 |                   1.045 |           0.123 |             65.026 |                        65.138 |                  -0.111 |          -0.013 |              6.935 |                         6.368 |                   0.567 |           0.616 |
|           38276 | Abaetetuba — Presencial |               4 |                  111 |                     40 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             62.334 |                        71.870 |                  -9.536 |          -1.269 |             60.682 |                        72.532 |                 -11.850 |          -1.496 |              6.894 |                         6.922 |                  -0.028 |          -0.044 |

## Recortes exclusivos

| RECORTE_PEDAGOGIA   | INDICADOR                |   N_CURSOS |   MEDIA_CURSOS |   MEDIANA_CURSOS | DP_CURSOS            |    P25 |    P75 |
|:--------------------|:-------------------------|-----------:|---------------:|-----------------:|:---------------------|-------:|-------:|
| UFPA — Conceito 5   | nt_ger_mean              |          1 |         65.463 |           65.463 | <NA>                 | 65.463 | 65.463 |
| UFPA — Conceito 5   | nt_obj_mean              |          1 |         64.438 |           64.438 | <NA>                 | 64.438 | 64.438 |
| UFPA — Conceito 5   | nt_dis_mean              |          1 |          6.956 |            6.956 | <NA>                 |  6.956 |  6.956 |
| UFPA — Conceito 5   | taxa_presenca_microdados |          1 |          0.733 |            0.733 | <NA>                 |  0.733 |  0.733 |
| UFPA — Conceito 5   | renda_ate_3sm_pct        |          1 |          0.923 |            0.923 | nan                  |  0.923 |  0.923 |
| UFPA — Conceito 5   | trabalha_pct             |          1 |          0.754 |            0.754 | nan                  |  0.754 |  0.754 |
| UFPA — Conceito 5   | acao_afirmativa_pct      |          1 |          0.785 |            0.785 | nan                  |  0.785 |  0.785 |
| UFPA — Conceito 5   | auxilio_permanencia_pct  |          1 |          0.154 |            0.154 | nan                  |  0.154 |  0.154 |
| UFPA — Conceito 5   | bolsa_academica_pct      |          1 |          0.127 |            0.127 | nan                  |  0.127 |  0.127 |
| UFPA — Conceito 5   | estudo_4h_ou_mais_pct    |          1 |          0.508 |            0.508 | nan                  |  0.508 |  0.508 |
| UFPA — Conceito 5   | qe_i68_media             |          1 |          9.554 |            9.554 | <NA>                 |  9.554 |  9.554 |
| UFPA — Conceito 5   | qe_i69_media             |          1 |          9.600 |            9.600 | <NA>                 |  9.600 |  9.600 |
| UFPA — Conceito 4   | nt_ger_mean              |          6 |         63.416 |           63.522 | 2.225073911073887    | 62.372 | 65.085 |
| UFPA — Conceito 4   | nt_obj_mean              |          6 |         62.425 |           62.689 | 2.4252693365970943   | 60.807 | 64.329 |
| UFPA — Conceito 4   | nt_dis_mean              |          6 |          6.738 |            6.832 | 0.2470206072676529   |  6.590 |  6.924 |
| UFPA — Conceito 4   | taxa_presenca_microdados |          6 |          0.863 |            0.860 | 0.044201000274382014 |  0.824 |  0.902 |
| UFPA — Conceito 4   | renda_ate_3sm_pct        |          6 |          0.906 |            0.904 | 0.039116321328968834 |  0.890 |  0.924 |
| UFPA — Conceito 4   | trabalha_pct             |          6 |          0.537 |            0.560 | 0.16712048283498873  |  0.403 |  0.622 |
| UFPA — Conceito 4   | acao_afirmativa_pct      |          6 |          0.822 |            0.821 | 0.07568374467201394  |  0.782 |  0.872 |
| UFPA — Conceito 4   | auxilio_permanencia_pct  |          6 |          0.273 |            0.239 | 0.10524347215806336  |  0.210 |  0.305 |
| UFPA — Conceito 4   | bolsa_academica_pct      |          6 |          0.315 |            0.333 | 0.07739795530322056  |  0.306 |  0.366 |
| UFPA — Conceito 4   | estudo_4h_ou_mais_pct    |          6 |          0.563 |            0.549 | 0.14336457220869178  |  0.452 |  0.688 |
| UFPA — Conceito 4   | qe_i68_media             |          6 |          9.286 |            9.275 | 0.21170176410621377  |  9.112 |  9.409 |
| UFPA — Conceito 4   | qe_i69_media             |          6 |          9.365 |            9.420 | 0.27425698175985985  |  9.192 |  9.560 |
| Outras IES do Pará  | nt_ger_mean              |         20 |         56.213 |           56.240 | 9.668782622397405    | 50.635 | 64.393 |
| Outras IES do Pará  | nt_obj_mean              |         20 |         56.331 |           56.808 | 9.538428390620606    | 50.802 | 65.039 |
| Outras IES do Pará  | nt_dis_mean              |         20 |          5.574 |            5.576 | 1.0827462731474273   |  4.882 |  6.388 |
| Outras IES do Pará  | taxa_presenca_microdados |         22 |          0.791 |            0.902 | 0.30002211517040495  |  0.774 |  0.972 |
| Outras IES do Pará  | renda_ate_3sm_pct        |         20 |          0.887 |            0.905 | 0.07592710509287733  |  0.869 |  0.943 |
| Outras IES do Pará  | trabalha_pct             |         20 |          0.693 |            0.731 | 0.16717520694995833  |  0.547 |  0.794 |
| Outras IES do Pará  | acao_afirmativa_pct      |         20 |          0.328 |            0.283 | 0.22856378133534497  |  0.142 |  0.495 |
| Outras IES do Pará  | auxilio_permanencia_pct  |         20 |          0.151 |            0.104 | 0.1825173612204296   |  0.018 |  0.201 |
| Outras IES do Pará  | bolsa_academica_pct      |         20 |          0.244 |            0.193 | 0.2285802483832778   |  0.052 |  0.394 |
| Outras IES do Pará  | estudo_4h_ou_mais_pct    |         20 |          0.517 |            0.550 | 0.12064006622933356  |  0.433 |  0.603 |
| Outras IES do Pará  | qe_i68_media             |         20 |          9.406 |            9.317 | 0.2975913351538529   |  9.168 |  9.614 |
| Outras IES do Pará  | qe_i69_media             |         20 |          9.105 |            9.133 | 0.5682293267766538   |  8.859 |  9.541 |
| Norte sem Pará      | nt_ger_mean              |         51 |         56.038 |           56.374 | 8.214979476804068    | 51.181 | 61.370 |
| Norte sem Pará      | nt_obj_mean              |         51 |         56.281 |           56.231 | 8.073632859409924    | 50.683 | 61.774 |
| Norte sem Pará      | nt_dis_mean              |         51 |          5.507 |            5.500 | 1.0359986063405682   |  4.762 |  6.250 |
| Norte sem Pará      | taxa_presenca_microdados |         53 |          0.772 |            0.800 | 0.20828744576693337  |  0.733 |  0.917 |
| Norte sem Pará      | renda_ate_3sm_pct        |         52 |          0.894 |            0.918 | 0.0971405270475747   |  0.856 |  0.960 |
| Norte sem Pará      | trabalha_pct             |         52 |          0.690 |            0.746 | 0.2148897018940429   |  0.615 |  0.841 |
| Norte sem Pará      | acao_afirmativa_pct      |         52 |          0.386 |            0.357 | 0.22942976041119797  |  0.219 |  0.565 |
| Norte sem Pará      | auxilio_permanencia_pct  |         52 |          0.278 |            0.183 | 0.26579478965154646  |  0.030 |  0.468 |
| Norte sem Pará      | bolsa_academica_pct      |         52 |          0.422 |            0.500 | 0.32214951037003187  |  0.089 |  0.676 |
| Norte sem Pará      | estudo_4h_ou_mais_pct    |         52 |          0.512 |            0.505 | 0.16502446610589536  |  0.415 |  0.591 |
| Norte sem Pará      | qe_i68_media             |         52 |          9.308 |            9.409 | 0.5139688527651327   |  9.065 |  9.649 |
| Norte sem Pará      | qe_i69_media             |         52 |          9.181 |            9.413 | 0.7127390280559334   |  8.852 |  9.669 |
| Brasil sem Norte    | nt_ger_mean              |       1051 |         58.204 |           58.152 | 9.38212384477206     | 51.618 | 64.490 |
| Brasil sem Norte    | nt_obj_mean              |       1051 |         59.098 |           58.878 | 9.307405651674408    | 52.561 | 65.392 |
| Brasil sem Norte    | nt_dis_mean              |       1051 |          5.463 |            5.531 | 1.21758713408637     |  4.607 |  6.357 |
| Brasil sem Norte    | taxa_presenca_microdados |       1118 |          0.808 |            0.873 | 0.2187797772874968   |  0.733 |  0.963 |
| Brasil sem Norte    | renda_ate_3sm_pct        |       1063 |          0.763 |            0.797 | 0.19233706691358743  |  0.664 |  0.917 |
| Brasil sem Norte    | trabalha_pct             |       1063 |          0.872 |            0.900 | 0.1378282504326812   |  0.822 |  0.975 |
| Brasil sem Norte    | acao_afirmativa_pct      |       1063 |          0.295 |            0.250 | 0.21378922682234125  |  0.125 |  0.456 |
| Brasil sem Norte    | auxilio_permanencia_pct  |       1063 |          0.124 |            0.027 | 0.20242667629758293  |  0.000 |  0.162 |
| Brasil sem Norte    | bolsa_academica_pct      |       1063 |          0.269 |            0.143 | 0.2871785575667885   |  0.029 |  0.479 |
| Brasil sem Norte    | estudo_4h_ou_mais_pct    |       1063 |          0.439 |            0.429 | 0.17962220448541177  |  0.333 |  0.537 |
| Brasil sem Norte    | qe_i68_media             |       1063 |          9.107 |            9.190 | 0.6452181084815827   |  8.786 |  9.525 |
| Brasil sem Norte    | qe_i69_media             |       1063 |          8.779 |            9.008 | 1.039830672936693    |  8.333 |  9.519 |

## Contraste interno UFPA

| RECORTE_PEDAGOGIA   | INDICADOR                |   N_CURSOS | MEDIA_CURSOS        | MEDIANA_CURSOS      | DP_CURSOS            | P25                 | P75                 |
|:--------------------|:-------------------------|-----------:|:--------------------|:--------------------|:---------------------|:--------------------|:--------------------|
| UFPA — Conceito 5   | nt_ger_mean              |          1 | 65.46317460317461   | 65.46317460317461   | <NA>                 | 65.46317460317461   | 65.46317460317461   |
| UFPA — Conceito 5   | nt_obj_mean              |          1 | 64.43809523809524   | 64.43809523809524   | <NA>                 | 64.43809523809524   | 64.43809523809524   |
| UFPA — Conceito 5   | nt_dis_mean              |          1 | 6.9563492063492065  | 6.9563492063492065  | <NA>                 | 6.9563492063492065  | 6.9563492063492065  |
| UFPA — Conceito 5   | taxa_presenca_microdados |          1 | 0.7325581395348837  | 0.7325581395348837  | <NA>                 | 0.7325581395348837  | 0.7325581395348837  |
| UFPA — Conceito 5   | renda_ate_3sm_pct        |          1 | 0.9230769230769231  | 0.9230769230769231  | nan                  | 0.9230769230769231  | 0.9230769230769231  |
| UFPA — Conceito 5   | trabalha_pct             |          1 | 0.7538461538461538  | 0.7538461538461538  | nan                  | 0.7538461538461538  | 0.7538461538461538  |
| UFPA — Conceito 5   | acao_afirmativa_pct      |          1 | 0.7846153846153846  | 0.7846153846153846  | nan                  | 0.7846153846153846  | 0.7846153846153846  |
| UFPA — Conceito 5   | auxilio_permanencia_pct  |          1 | 0.15384615384615385 | 0.15384615384615385 | nan                  | 0.15384615384615385 | 0.15384615384615385 |
| UFPA — Conceito 5   | qe_i68_media             |          1 | 9.553846153846154   | 9.553846153846154   | <NA>                 | 9.553846153846154   | 9.553846153846154   |
| UFPA — Conceito 5   | qe_i69_media             |          1 | 9.6                 | 9.6                 | <NA>                 | 9.6                 | 9.6                 |
| UFPA — Conceito 4   | nt_ger_mean              |          6 | 63.416170289382926  | 63.521956284153006  | 2.225073911073887    | 62.37171688081524   | 65.08541666666667   |
| UFPA — Conceito 4   | nt_obj_mean              |          6 | 62.42480257551256   | 62.688556791569084  | 2.4252693365970943   | 60.8065684536996    | 64.32919642857144   |
| UFPA — Conceito 4   | nt_dis_mean              |          6 | 6.7381641144864375  | 6.832317973711417   | 0.2470206072676529   | 6.590122950819673   | 6.924428893178893   |
| UFPA — Conceito 4   | taxa_presenca_microdados |          6 | 0.863076356576448   | 0.8597428073234525  | 0.044201000274382014 | 0.8237281399046105  | 0.9015011659541392  |
| UFPA — Conceito 4   | renda_ate_3sm_pct        |          6 | 0.9062025427338725  | 0.9039125431530495  | 0.039116321328968834 | 0.8896319979120448  | 0.9241231209735147  |
| UFPA — Conceito 4   | trabalha_pct             |          6 | 0.5370321872272158  | 0.560126582278481   | 0.16712048283498873  | 0.40255905511811024 | 0.6215581365000653  |
| UFPA — Conceito 4   | acao_afirmativa_pct      |          6 | 0.8219516186455565  | 0.8206061506462636  | 0.07568374467201394  | 0.7823013600572656  | 0.8721041318366372  |
| UFPA — Conceito 4   | auxilio_permanencia_pct  |          6 | 0.272679269985823   | 0.2393536038975162  | 0.10524347215806336  | 0.2103711162255466  | 0.3048407608842709  |
| UFPA — Conceito 4   | qe_i68_media             |          6 | 9.285698589324527   | 9.274659660855027   | 0.21170176410621377  | 9.111621305727166   | 9.40930667433832    |
| UFPA — Conceito 4   | qe_i69_media             |          6 | 9.364586094096262   | 9.419744225499151   | 0.27425698175985985  | 9.191840108928226   | 9.560270425776755   |
| Outras IES do Pará  | nt_ger_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Outras IES do Pará  | nt_obj_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Outras IES do Pará  | nt_dis_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Outras IES do Pará  | taxa_presenca_microdados |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Outras IES do Pará  | renda_ate_3sm_pct        |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Outras IES do Pará  | trabalha_pct             |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Outras IES do Pará  | acao_afirmativa_pct      |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Outras IES do Pará  | auxilio_permanencia_pct  |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Outras IES do Pará  | qe_i68_media             |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Outras IES do Pará  | qe_i69_media             |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Norte sem Pará      | nt_ger_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Norte sem Pará      | nt_obj_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Norte sem Pará      | nt_dis_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Norte sem Pará      | taxa_presenca_microdados |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Norte sem Pará      | renda_ate_3sm_pct        |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Norte sem Pará      | trabalha_pct             |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Norte sem Pará      | acao_afirmativa_pct      |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Norte sem Pará      | auxilio_permanencia_pct  |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Norte sem Pará      | qe_i68_media             |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Norte sem Pará      | qe_i69_media             |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Brasil sem Norte    | nt_ger_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Brasil sem Norte    | nt_obj_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Brasil sem Norte    | nt_dis_mean              |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Brasil sem Norte    | taxa_presenca_microdados |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Brasil sem Norte    | renda_ate_3sm_pct        |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Brasil sem Norte    | trabalha_pct             |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Brasil sem Norte    | acao_afirmativa_pct      |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Brasil sem Norte    | auxilio_permanencia_pct  |          0 | nan                 | nan                 | nan                  | nan                 | nan                 |
| Brasil sem Norte    | qe_i68_media             |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |
| Brasil sem Norte    | qe_i69_media             |          0 | <NA>                | <NA>                | <NA>                 | <NA>                | <NA>                |

## Limitações

- não há identificação comum de estudante entre arquivos temáticos;
- relações entre indicadores de arquivos distintos são ecológicas;
- o contraste Conceito 4 versus Conceito 5 é descritivo, não causal;
- os benchmarks controlam apenas características observáveis selecionadas;
- cursos com menor N podem apresentar estimativas mais instáveis;
- itens de processo formativo não são condensados em índice único sem validação.