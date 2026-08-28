# Sprint 19 — Geografia: base analítica e panorama inicial

## Síntese

A base analítica reúne **254 cursos** de Geografia. Foram localizadas **4 ofertas da UFPA**. Não existe oferta UFPA com Conceito Enade 1 nesta área; o Grupo A permanece vazio.

As quatro ofertas da UFPA estão distribuídas entre Conceito Enade 3 e Conceito Enade 4. O contraste institucional principal é, portanto, Conceito 3 versus Conceito 4, sem tratar Conceito 3 como insuficiência e sem atribuir causalidade ao conceito.

A unidade principal é `CO_CURSO`. Cada arquivo temático é tratado e agregado separadamente antes das junções one-to-one.

## Ofertas da UFPA

|   CO_CURSO | ROTULO_OFERTA           |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   nt_ger_count |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |   nt_ger_percentil_brasil |   nt_ger_percentil_norte |   nt_ger_percentil_para |
|-----------:|:------------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------:|--------------:|--------------:|--------------:|--------------------------:|-------------------------:|------------------------:|
|      12052 | Altamira — Presencial   |                    3 |              27 |                  23 |                       0.852 |             23 |        58.097 |        57.948 |         5.870 |                    38.326 |                   50.000 |                  44.444 |
|    1330343 | Ananindeua — Presencial |                    4 |              77 |                  63 |                       0.818 |             63 |        61.516 |        62.192 |         5.881 |                    49.339 |                   77.273 |                  77.778 |
|      11991 | Belém — Presencial      |                    4 |              71 |                  57 |                       0.803 |             57 |        66.844 |        68.139 |         6.167 |                    65.639 |                   90.909 |                  88.889 |
|    1194057 | Cametá — Presencial     |                    3 |              92 |                  68 |                       0.739 |             68 |        55.866 |        54.382 |         6.180 |                    26.872 |                   40.909 |                  22.222 |

## Auditoria entre fontes

|   CO_CURSO |   CO_MUNIC_CURSO |   CO_MODALIDADE | NO_CADASTRO_MICRODADOS   | MUNICIPIO   | MODALIDADE   |   INSCRITOS |   PARTICIPANTES |   PCT_PADRAO_PROFICIENCIA |   CONCEITO_ENADE | SITUACAO_CONCEITO     | NA_PLANILHA_CONCEITO   | STATUS_FONTES              |
|-----------:|-----------------:|----------------:|:-------------------------|:------------|:-------------|------------:|----------------:|--------------------------:|-----------------:|:----------------------|:-----------------------|:---------------------------|
|      11991 |          1501402 |               1 | True                     | Belém       | Presencial   |          71 |              57 |                     0.877 |                4 | Conceito superior a 1 | True                   | Localizada nas duas fontes |
|      12052 |          1500602 |               1 | True                     | Altamira    | Presencial   |          27 |              23 |                     0.739 |                3 | Conceito superior a 1 | True                   | Localizada nas duas fontes |
|    1194057 |          1502103 |               1 | True                     | Cametá      | Presencial   |          92 |              68 |                     0.632 |                3 | Conceito superior a 1 | True                   | Localizada nas duas fontes |
|    1330343 |          1500800 |               1 | True                     | Ananindeua  | Presencial   |          77 |              63 |                     0.778 |                4 | Conceito superior a 1 | True                   | Localizada nas duas fontes |

As quatro ofertas foram localizadas tanto no cadastro dos microdados quanto na planilha de Conceito Enade 2025.

## Comparação regional e nacional

| RECORTE                        | INDICADOR   |   N_CURSOS |   N_PARTICIPANTES |   MEDIA_CURSOS |   MEDIA_PONDERADA_PARTICIPANTES |   MEDIANA_CURSOS | DP_CURSOS          |    P25 |    P75 |
|:-------------------------------|:------------|-----------:|------------------:|---------------:|--------------------------------:|-----------------:|:-------------------|-------:|-------:|
| UFPA — Ananindeua — Presencial | nt_ger_mean |          1 |            63.000 |         61.516 |                          61.516 |           61.516 | <NA>               | 61.516 | 61.516 |
| UFPA — Cametá — Presencial     | nt_ger_mean |          1 |            68.000 |         55.866 |                          55.866 |           55.866 | <NA>               | 55.866 | 55.866 |
| UFPA — Altamira — Presencial   | nt_ger_mean |          1 |            23.000 |         58.097 |                          58.097 |           58.097 | <NA>               | 58.097 | 58.097 |
| UFPA — Belém — Presencial      | nt_ger_mean |          1 |            57.000 |         66.844 |                          66.844 |           66.844 | <NA>               | 66.844 | 66.844 |
| UFPA agregada                  | nt_ger_mean |          4 |           211.000 |         60.581 |                          60.762 |           59.806 | 4.77839140084645   | 57.540 | 62.848 |
| Região Norte sem UFPA          | nt_ger_mean |         18 |           527.000 |         55.163 |                          56.172 |           57.811 | 8.640793724571655  | 48.077 | 60.726 |
| Região Norte completa          | nt_ger_mean |         22 |           738.000 |         56.148 |                          57.484 |           58.375 | 8.263022411842309  | 51.170 | 61.379 |
| Nordeste                       | nt_ger_mean |         66 |          2308.000 |         62.403 |                          62.704 |           61.957 | 9.151424881774155  | 56.851 | 68.966 |
| Sudeste                        | nt_ger_mean |         67 |          2011.000 |         64.227 |                          67.784 |           64.234 | 11.98206052461306  | 56.292 | 73.169 |
| Sul                            | nt_ger_mean |         43 |          2037.000 |         62.911 |                          57.688 |           62.018 | 10.333589846082921 | 57.646 | 70.227 |
| Centro-Oeste                   | nt_ger_mean |         29 |           407.000 |         58.830 |                          60.736 |           56.869 | 11.659180443050978 | 52.068 | 66.978 |
| Brasil geral                   | nt_ger_mean |        227 |          7501.000 |         61.975 |                          62.083 |           61.659 | 10.739781364070355 | 55.563 | 68.858 |
| Brasil sem UFPA                | nt_ger_mean |        223 |          7290.000 |         62.000 |                          62.122 |           61.725 | 10.820210318235988 | 55.406 | 68.967 |
| Restante do Brasil sem Norte   | nt_ger_mean |        205 |          6763.000 |         62.600 |                          62.585 |           62.198 | 10.802735408338961 | 55.780 | 69.872 |

## Benchmarks comparáveis por oferta UFPA

|   CO_CURSO_ALVO | ROTULO_ALVO             |   CONCEITO_ALVO |   PARTICIPANTES_ALVO |   N_CURSOS_COMPARAVEIS | CRITERIO                                                                                                         |   nt_ger_mean_ALVO |   nt_ger_mean_MEDIA_BENCHMARK |   nt_ger_mean_DIFERENCA |   nt_ger_mean_Z |   nt_obj_mean_ALVO |   nt_obj_mean_MEDIA_BENCHMARK |   nt_obj_mean_DIFERENCA |   nt_obj_mean_Z |   nt_dis_mean_ALVO |   nt_dis_mean_MEDIA_BENCHMARK |   nt_dis_mean_DIFERENCA |   nt_dis_mean_Z |
|----------------:|:------------------------|----------------:|---------------------:|-----------------------:|:-----------------------------------------------------------------------------------------------------------------|-------------------:|------------------------------:|------------------------:|----------------:|-------------------:|------------------------------:|------------------------:|----------------:|-------------------:|------------------------------:|------------------------:|----------------:|
|           11991 | Belém — Presencial      |               4 |                   57 |                     32 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             66.844 |                        68.619 |                  -1.774 |          -0.200 |             68.139 |                        69.927 |                  -1.789 |          -0.182 |              6.167 |                         6.338 |                  -0.172 |          -0.277 |
|           12052 | Altamira — Presencial   |               3 |                   23 |                     44 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             58.097 |                        66.138 |                  -8.041 |          -0.794 |             57.948 |                        67.389 |                  -9.441 |          -0.882 |              5.870 |                         6.114 |                  -0.244 |          -0.253 |
|         1194057 | Cametá — Presencial     |               3 |                   68 |                     25 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             55.866 |                        68.134 |                 -12.268 |          -1.380 |             54.382 |                        69.445 |                 -15.063 |          -1.521 |              6.180 |                         6.289 |                  -0.109 |          -0.175 |
|         1330343 | Ananindeua — Presencial |               4 |                   63 |                     29 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x da oferta UFPA |             61.516 |                        68.186 |                  -6.671 |          -0.751 |             62.192 |                        69.481 |                  -7.289 |          -0.742 |              5.881 |                         6.301 |                  -0.420 |          -0.669 |

## Recortes exclusivos

| RECORTE_GEOGRAFIA   | INDICADOR                |   N_CURSOS |   MEDIA_CURSOS |   MEDIANA_CURSOS |   DP_CURSOS |    P25 |    P75 |
|:--------------------|:-------------------------|-----------:|---------------:|-----------------:|------------:|-------:|-------:|
| UFPA — Conceito 4   | nt_ger_mean              |          2 |         64.180 |           64.180 |       3.768 | 62.848 | 65.512 |
| UFPA — Conceito 4   | nt_obj_mean              |          2 |         65.165 |           65.165 |       4.205 | 63.679 | 66.652 |
| UFPA — Conceito 4   | nt_dis_mean              |          2 |          6.024 |            6.024 |       0.202 |  5.952 |  6.095 |
| UFPA — Conceito 4   | taxa_presenca_microdados |          2 |          0.810 |            0.810 |       0.011 |  0.807 |  0.814 |
| UFPA — Conceito 4   | renda_ate_3sm_pct        |          2 |          0.844 |            0.844 |       0.025 |  0.835 |  0.853 |
| UFPA — Conceito 4   | trabalha_pct             |          2 |          0.615 |            0.615 |       0.008 |  0.612 |  0.618 |
| UFPA — Conceito 4   | acao_afirmativa_pct      |          2 |          0.631 |            0.631 |       0.112 |  0.591 |  0.671 |
| UFPA — Conceito 4   | auxilio_permanencia_pct  |          2 |          0.173 |            0.173 |       0.001 |  0.173 |  0.174 |
| UFPA — Conceito 4   | bolsa_academica_pct      |          2 |          0.411 |            0.411 |       0.110 |  0.372 |  0.450 |
| UFPA — Conceito 4   | estudo_4h_ou_mais_pct    |          2 |          0.460 |            0.460 |       0.056 |  0.440 |  0.480 |
| UFPA — Conceito 4   | qe_i68_media             |          2 |          8.116 |            8.116 |       0.676 |  7.877 |  8.355 |
| UFPA — Conceito 4   | qe_i69_media             |          2 |          8.826 |            8.826 |       0.144 |  8.775 |  8.877 |
| UFPA — Conceito 3   | nt_ger_mean              |          2 |         56.982 |           56.982 |       1.578 | 56.424 | 57.540 |
| UFPA — Conceito 3   | nt_obj_mean              |          2 |         56.165 |           56.165 |       2.521 | 55.274 | 57.056 |
| UFPA — Conceito 3   | nt_dis_mean              |          2 |          6.025 |            6.025 |       0.220 |  5.947 |  6.103 |
| UFPA — Conceito 3   | taxa_presenca_microdados |          2 |          0.795 |            0.795 |       0.080 |  0.767 |  0.824 |
| UFPA — Conceito 3   | renda_ate_3sm_pct        |          2 |          0.916 |            0.916 |       0.044 |  0.900 |  0.931 |
| UFPA — Conceito 3   | trabalha_pct             |          2 |          0.608 |            0.608 |       0.445 |  0.451 |  0.766 |
| UFPA — Conceito 3   | acao_afirmativa_pct      |          2 |          0.753 |            0.753 |       0.086 |  0.723 |  0.783 |
| UFPA — Conceito 3   | auxilio_permanencia_pct  |          2 |          0.310 |            0.310 |       0.221 |  0.232 |  0.388 |
| UFPA — Conceito 3   | bolsa_academica_pct      |          2 |          0.432 |            0.432 |       0.253 |  0.343 |  0.522 |
| UFPA — Conceito 3   | estudo_4h_ou_mais_pct    |          2 |          0.575 |            0.575 |       0.003 |  0.574 |  0.576 |
| UFPA — Conceito 3   | qe_i68_media             |          2 |          9.546 |            9.546 |       0.228 |  9.465 |  9.626 |
| UFPA — Conceito 3   | qe_i69_media             |          2 |          9.714 |            9.714 |       0.140 |  9.665 |  9.764 |
| Outras IES do Pará  | nt_ger_mean              |          5 |         59.763 |           58.967 |       4.750 | 56.969 | 59.996 |
| Outras IES do Pará  | nt_obj_mean              |          5 |         59.628 |           58.347 |       4.972 | 57.442 | 59.009 |
| Outras IES do Pará  | nt_dis_mean              |          5 |          6.030 |            6.145 |       0.478 |  5.556 |  6.394 |
| Outras IES do Pará  | taxa_presenca_microdados |          5 |          0.774 |            0.825 |       0.096 |  0.703 |  0.837 |
| Outras IES do Pará  | renda_ate_3sm_pct        |          5 |          0.883 |            0.938 |       0.110 |  0.769 |  0.946 |
| Outras IES do Pará  | trabalha_pct             |          5 |          0.542 |            0.587 |       0.123 |  0.438 |  0.649 |
| Outras IES do Pará  | acao_afirmativa_pct      |          5 |          0.616 |            0.600 |       0.078 |  0.543 |  0.692 |
| Outras IES do Pará  | auxilio_permanencia_pct  |          5 |          0.314 |            0.312 |       0.075 |  0.250 |  0.370 |
| Outras IES do Pará  | bolsa_academica_pct      |          5 |          0.550 |            0.571 |       0.122 |  0.550 |  0.571 |
| Outras IES do Pará  | estudo_4h_ou_mais_pct    |          5 |          0.589 |            0.600 |       0.046 |  0.543 |  0.615 |
| Outras IES do Pará  | qe_i68_media             |          5 |          8.994 |            8.848 |       0.481 |  8.771 |  9.081 |
| Outras IES do Pará  | qe_i69_media             |          5 |          9.275 |            9.250 |       0.427 |  9.042 |  9.378 |
| Norte sem Pará      | nt_ger_mean              |         13 |         53.394 |           54.149 |       9.276 | 44.154 | 60.969 |
| Norte sem Pará      | nt_obj_mean              |         13 |         53.624 |           53.023 |      10.210 | 44.835 | 63.145 |
| Norte sem Pará      | nt_dis_mean              |         13 |          5.248 |            5.755 |       0.967 |  4.505 |  5.955 |
| Norte sem Pará      | taxa_presenca_microdados |         14 |          0.800 |            0.811 |       0.127 |  0.763 |  0.873 |
| Norte sem Pará      | renda_ate_3sm_pct        |         13 |          0.876 |            0.902 |       0.104 |  0.867 |  0.944 |
| Norte sem Pará      | trabalha_pct             |         13 |          0.574 |            0.600 |       0.164 |  0.433 |  0.643 |
| Norte sem Pará      | acao_afirmativa_pct      |         13 |          0.415 |            0.389 |       0.222 |  0.356 |  0.510 |
| Norte sem Pará      | auxilio_permanencia_pct  |         13 |          0.428 |            0.433 |       0.205 |  0.273 |  0.609 |
| Norte sem Pará      | bolsa_academica_pct      |         13 |          0.702 |            0.667 |       0.152 |  0.561 |  0.818 |
| Norte sem Pará      | estudo_4h_ou_mais_pct    |         13 |          0.571 |            0.550 |       0.131 |  0.508 |  0.652 |
| Norte sem Pará      | qe_i68_media             |         13 |          8.890 |            8.909 |       0.555 |  8.542 |  9.356 |
| Norte sem Pará      | qe_i69_media             |         13 |          9.077 |            9.174 |       0.525 |  8.814 |  9.314 |
| Brasil sem Norte    | nt_ger_mean              |        205 |         62.600 |           62.198 |      10.803 | 55.780 | 69.872 |
| Brasil sem Norte    | nt_obj_mean              |        205 |         63.656 |           63.469 |      11.437 | 56.378 | 71.543 |
| Brasil sem Norte    | nt_dis_mean              |        205 |          5.838 |            6.067 |       1.141 |  5.102 |  6.625 |
| Brasil sem Norte    | taxa_presenca_microdados |        231 |          0.723 |            0.791 |       0.256 |  0.592 |  0.911 |
| Brasil sem Norte    | renda_ate_3sm_pct        |        209 |          0.740 |            0.773 |       0.204 |  0.606 |  0.903 |
| Brasil sem Norte    | trabalha_pct             |        209 |          0.766 |            0.800 |       0.194 |  0.659 |  0.909 |
| Brasil sem Norte    | acao_afirmativa_pct      |        209 |          0.383 |            0.419 |       0.219 |  0.206 |  0.541 |
| Brasil sem Norte    | auxilio_permanencia_pct  |        209 |          0.258 |            0.216 |       0.245 |  0.016 |  0.424 |
| Brasil sem Norte    | bolsa_academica_pct      |        206 |          0.441 |            0.500 |       0.328 |  0.064 |  0.720 |
| Brasil sem Norte    | estudo_4h_ou_mais_pct    |        209 |          0.550 |            0.556 |       0.170 |  0.444 |  0.647 |
| Brasil sem Norte    | qe_i68_media             |        209 |          8.800 |            8.797 |       0.703 |  8.388 |  9.286 |
| Brasil sem Norte    | qe_i69_media             |        209 |          8.913 |            9.043 |       0.819 |  8.571 |  9.429 |

## Contraste interno UFPA

| RECORTE_GEOGRAFIA   | INDICADOR                |   N_CURSOS | MEDIA_CURSOS        | MEDIANA_CURSOS      | DP_CURSOS             |     P25 |     P75 |
|:--------------------|:-------------------------|-----------:|:--------------------|:--------------------|:----------------------|--------:|--------:|
| UFPA — Conceito 4   | nt_ger_mean              |          2 | 64.17988304093568   | 64.17988304093568   | 3.767928064427965     |  62.848 |  65.512 |
| UFPA — Conceito 4   | nt_obj_mean              |          2 | 65.16532999164578   | 65.16532999164578   | 4.204833808258854     |  63.679 |  66.652 |
| UFPA — Conceito 4   | nt_dis_mean              |          2 | 6.023809523809524   | 6.023809523809524   | 0.20203050891044205   |   5.952 |   6.095 |
| UFPA — Conceito 4   | taxa_presenca_microdados |          2 | 0.8104993597951344  | 0.8104993597951344  | 0.010864636842815077  |   0.807 |   0.814 |
| UFPA — Conceito 4   | renda_ate_3sm_pct        |          2 | 0.8440779610194902  | 0.8440779610194902  | 0.025443122561434953  |   0.835 |   0.853 |
| UFPA — Conceito 4   | trabalha_pct             |          2 | 0.6146926536731634  | 0.6146926536731634  | 0.008481040853811652  |   0.612 |   0.618 |
| UFPA — Conceito 4   | acao_afirmativa_pct      |          2 | 0.6309345327336332  | 0.6309345327336332  | 0.11202041461076244   |   0.591 |   0.671 |
| UFPA — Conceito 4   | auxilio_permanencia_pct  |          2 | 0.17316341829085458 | 0.17316341829085458 | 0.0010601301067264465 |   0.173 |   0.174 |
| UFPA — Conceito 4   | qe_i68_media             |          2 | 8.116066966516742   | 8.116066966516742   | 0.6761863197403589    |   7.877 |   8.355 |
| UFPA — Conceito 4   | qe_i69_media             |          2 | 8.82583708145927    | 8.82583708145927    | 0.14382431781255692   |   8.775 |   8.877 |
| UFPA — Conceito 3   | nt_ger_mean              |          2 | 56.981783887468026  | 56.981783887468026  | 1.5777071392354194    |  56.424 |  57.540 |
| UFPA — Conceito 3   | nt_obj_mean              |          2 | 56.165089514066494  | 56.165089514066494  | 2.5211702395196025    |  55.274 |  57.056 |
| UFPA — Conceito 3   | nt_dis_mean              |          2 | 6.024856138107417   | 6.024856138107417   | 0.21961452619013086   |   5.947 |   6.103 |
| UFPA — Conceito 3   | taxa_presenca_microdados |          2 | 0.7954911433172303  | 0.7954911433172303  | 0.07970607839461892   |   0.767 |   0.824 |
| UFPA — Conceito 3   | renda_ate_3sm_pct        |          2 | 0.9156410256410257  | 0.9156410256410257  | 0.04387688231978066   |   0.900 |   0.931 |
| UFPA — Conceito 3   | trabalha_pct             |          2 | 0.6082051282051282  | 0.6082051282051282  | 0.4452959627164515    |   0.451 |   0.766 |
| UFPA — Conceito 3   | acao_afirmativa_pct      |          2 | 0.7528205128205128  | 0.7528205128205128  | 0.08557805146667963   |   0.723 |   0.783 |
| UFPA — Conceito 3   | auxilio_permanencia_pct  |          2 | 0.31025641025641026 | 0.31025641025641026 | 0.22119750590963794   |   0.232 |   0.388 |
| UFPA — Conceito 3   | qe_i68_media             |          2 | 9.545641025641025   | 9.545641025641025   | 0.22772464542828294   |   9.465 |   9.626 |
| UFPA — Conceito 3   | qe_i69_media             |          2 | 9.714358974358973   | 9.714358974358973   | 0.13997088078872147   |   9.665 |   9.764 |
| Outras IES do Pará  | nt_ger_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Outras IES do Pará  | nt_obj_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Outras IES do Pará  | nt_dis_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Outras IES do Pará  | taxa_presenca_microdados |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Outras IES do Pará  | renda_ate_3sm_pct        |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Outras IES do Pará  | trabalha_pct             |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Outras IES do Pará  | acao_afirmativa_pct      |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Outras IES do Pará  | auxilio_permanencia_pct  |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Outras IES do Pará  | qe_i68_media             |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Outras IES do Pará  | qe_i69_media             |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Norte sem Pará      | nt_ger_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Norte sem Pará      | nt_obj_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Norte sem Pará      | nt_dis_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Norte sem Pará      | taxa_presenca_microdados |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Norte sem Pará      | renda_ate_3sm_pct        |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Norte sem Pará      | trabalha_pct             |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Norte sem Pará      | acao_afirmativa_pct      |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Norte sem Pará      | auxilio_permanencia_pct  |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Norte sem Pará      | qe_i68_media             |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Norte sem Pará      | qe_i69_media             |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Brasil sem Norte    | nt_ger_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Brasil sem Norte    | nt_obj_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Brasil sem Norte    | nt_dis_mean              |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Brasil sem Norte    | taxa_presenca_microdados |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Brasil sem Norte    | renda_ate_3sm_pct        |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Brasil sem Norte    | trabalha_pct             |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Brasil sem Norte    | acao_afirmativa_pct      |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Brasil sem Norte    | auxilio_permanencia_pct  |          0 | nan                 | nan                 | nan                   | nan     | nan     |
| Brasil sem Norte    | qe_i68_media             |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |
| Brasil sem Norte    | qe_i69_media             |          0 | <NA>                | <NA>                | <NA>                  | nan     | nan     |

## Limitações

- não há identificação comum de estudante entre arquivos temáticos;
- relações entre indicadores de arquivos distintos são ecológicas;
- o contraste Conceito 3 versus Conceito 4 é descritivo, não causal;
- os benchmarks controlam apenas características observáveis selecionadas;
- cursos com menor N podem apresentar estimativas mais instáveis;
- QE_I20–QE_I66 não são condensados em índice único nesta sprint.