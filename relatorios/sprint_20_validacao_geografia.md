# Sprint 20 — Validação analítica de Geografia

## Escopo

Foram auditados **254 cursos de Geografia**, incluindo **4 ofertas da UFPA**. Não existe oferta UFPA com Conceito Enade 1; o Grupo A permanece vazio.

O contraste institucional principal é entre as duas ofertas UFPA Conceito 3 e as duas ofertas UFPA Conceito 4. Conceito 3 não é tratado como insuficiência e o contraste não é causal.

A unidade principal permanece `CO_CURSO`; não há junções individuais entre arquivos temáticos. Relações entre temas distintos são ecológicas.

## Ofertas UFPA auditadas

|   CO_CURSO | ROTULO_OFERTA           |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   taxa_presenca_microdados |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |
|-----------:|:------------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------------------:|--------------:|--------------:|--------------:|
|      12052 | Altamira — Presencial   |                3.000 |              27 |              23.000 |                       0.852 |                      0.852 |        58.097 |        57.948 |         5.870 |
|    1330343 | Ananindeua — Presencial |                4.000 |              77 |              63.000 |                       0.818 |                      0.818 |        61.516 |        62.192 |         5.881 |
|      11991 | Belém — Presencial      |                4.000 |              71 |              57.000 |                       0.803 |                      0.803 |        66.844 |        68.139 |         6.167 |
|    1194057 | Cametá — Presencial     |                3.000 |              92 |              68.000 |                       0.739 |                      0.739 |        55.866 |        54.382 |         6.180 |

## Auditoria de N e participação

|   CO_CURSO | ROTULO_OFERTA           | GRUPO_CODIGO   |   PARTICIPANTES_NUM |   registros_microdados |   presentes_validos |   nt_ger_count |   nt_obj_count |   nt_dis_count |   reaplicacoes |   diferenca_participantes_oficial_nt_ger | alerta_n_superior_registros   | alerta_diferenca_participantes   |
|-----------:|:------------------------|:---------------|--------------------:|-----------------------:|--------------------:|---------------:|---------------:|---------------:|---------------:|-----------------------------------------:|:------------------------------|:---------------------------------|
|      11991 | Belém — Presencial      | B              |              57.000 |                     71 |                  57 |             57 |             57 |             57 |              0 |                                    0.000 | False                         | False                            |
|      12052 | Altamira — Presencial   | B              |              23.000 |                     27 |                  23 |             23 |             23 |             23 |              0 |                                    0.000 | False                         | False                            |
|    1194057 | Cametá — Presencial     | B              |              68.000 |                     92 |                  68 |             68 |             68 |             68 |              0 |                                    0.000 | False                         | False                            |
|    1330343 | Ananindeua — Presencial | B              |              63.000 |                     77 |                  63 |             63 |             63 |             63 |              0 |                                    0.000 | False                         | False                            |

## Contraste interno UFPA — Conceito 3 × Conceito 4

| INDICADOR                |   N_CONCEITO_3 |   MEDIA_CONCEITO_3 |   MEDIANA_CONCEITO_3 |   DP_CONCEITO_3 |   N_CONCEITO_4 |   MEDIA_CONCEITO_4 |   MEDIANA_CONCEITO_4 |   DP_CONCEITO_4 |   DIFERENCA_C3_C4 |   D_PADRONIZADO_DESCRITIVO | INTERPRETACAO                                         |
|:-------------------------|---------------:|-------------------:|---------------------:|----------------:|---------------:|-------------------:|---------------------:|----------------:|------------------:|---------------------------:|:------------------------------------------------------|
| nt_ger_mean              |              2 |             56.982 |               56.982 |           1.578 |              2 |             64.180 |               64.180 |           3.768 |            -7.198 |                     -2.492 | contraste descritivo entre quatro ofertas; não causal |
| nt_obj_mean              |              2 |             56.165 |               56.165 |           2.521 |              2 |             65.165 |               65.165 |           4.205 |            -9.000 |                     -2.596 | contraste descritivo entre quatro ofertas; não causal |
| nt_dis_mean              |              2 |              6.025 |                6.025 |           0.220 |              2 |              6.024 |                6.024 |           0.202 |             0.001 |                      0.005 | contraste descritivo entre quatro ofertas; não causal |
| taxa_presenca_microdados |              2 |              0.795 |                0.795 |           0.080 |              2 |              0.810 |                0.810 |           0.011 |            -0.015 |                     -0.264 | contraste descritivo entre quatro ofertas; não causal |
| renda_ate_3sm_pct        |              2 |              0.916 |                0.916 |           0.044 |              2 |              0.844 |                0.844 |           0.025 |             0.072 |                      1.995 | contraste descritivo entre quatro ofertas; não causal |
| trabalha_pct             |              2 |              0.608 |                0.608 |           0.445 |              2 |              0.615 |                0.615 |           0.008 |            -0.006 |                     -0.021 | contraste descritivo entre quatro ofertas; não causal |
| acao_afirmativa_pct      |              2 |              0.753 |                0.753 |           0.086 |              2 |              0.631 |                0.631 |           0.112 |             0.122 |                      1.223 | contraste descritivo entre quatro ofertas; não causal |
| auxilio_permanencia_pct  |              2 |              0.310 |                0.310 |           0.221 |              2 |              0.173 |                0.173 |           0.001 |             0.137 |                      0.876 | contraste descritivo entre quatro ofertas; não causal |
| bolsa_academica_pct      |              2 |              0.432 |                0.432 |           0.253 |              2 |              0.411 |                0.411 |           0.110 |             0.021 |                      0.107 | contraste descritivo entre quatro ofertas; não causal |
| estudo_4h_ou_mais_pct    |              2 |              0.575 |                0.575 |           0.003 |              2 |              0.460 |                0.460 |           0.056 |             0.115 |                      2.882 | contraste descritivo entre quatro ofertas; não causal |
| qe_i68_media             |              2 |              9.546 |                9.546 |           0.228 |              2 |              8.116 |                8.116 |           0.676 |             1.430 |                      2.834 | contraste descritivo entre quatro ofertas; não causal |
| qe_i69_media             |              2 |              9.714 |                9.714 |           0.140 |              2 |              8.826 |                8.826 |           0.144 |             0.889 |                      6.261 | contraste descritivo entre quatro ofertas; não causal |

As diferenças são calculadas como média Conceito 3 menos média Conceito 4. Com apenas duas ofertas em cada estrato, tamanhos padronizados são exclusivamente descritivos.

## Sensibilidade dos benchmarks

|   CO_CURSO_ALVO | ROTULO_ALVO             |   CONCEITO_ALVO |   N_CURSOS |   nt_ger_mean_ALVO |   nt_ger_mean_MEDIA_BENCHMARK |   nt_ger_mean_DIFERENCA |   nt_ger_mean_Z |   nt_obj_mean_DIFERENCA |   nt_dis_mean_DIFERENCA |
|----------------:|:------------------------|----------------:|-----------:|-------------------:|------------------------------:|------------------------:|----------------:|------------------------:|------------------------:|
|           11991 | Belém — Presencial      |           4.000 |         32 |             66.844 |                        68.619 |                  -1.774 |          -0.200 |                  -1.789 |                  -0.172 |
|           12052 | Altamira — Presencial   |           3.000 |         44 |             58.097 |                        66.138 |                  -8.041 |          -0.794 |                  -9.441 |                  -0.244 |
|         1194057 | Cametá — Presencial     |           3.000 |         25 |             55.866 |                        68.134 |                 -12.268 |          -1.380 |                 -15.063 |                  -0.109 |
|         1330343 | Ananindeua — Presencial |           4.000 |         29 |             61.516 |                        68.186 |                  -6.671 |          -0.751 |                  -7.289 |                  -0.420 |

Foram avaliados cinco cenários por oferta, totalizando 20 combinações oferta-cenário. O benchmark reduz heterogeneidade observável, mas não constitui desenho causal.

## Perfil demográfico, socioeconômico e trajetória

| RECORTE_GEOGRAFIA   | INDICADOR                 |   N_CURSOS |   MEDIA_CURSOS |   MEDIANA_CURSOS |   DP_CURSOS |    P25 |    P75 |
|:--------------------|:--------------------------|-----------:|---------------:|-----------------:|------------:|-------:|-------:|
| UFPA — Conceito 3   | sexo_feminino_pct         |          2 |          0.470 |            0.470 |       0.089 |  0.439 |  0.501 |
| UFPA — Conceito 3   | idade_media               |          2 |         30.509 |           30.509 |       2.580 | 29.597 | 31.421 |
| UFPA — Conceito 3   | mae_superior_pct          |          2 |          0.150 |            0.150 |       0.014 |  0.146 |  0.155 |
| UFPA — Conceito 3   | pai_superior_pct          |          2 |          0.097 |            0.097 |       0.065 |  0.074 |  0.120 |
| UFPA — Conceito 3   | renda_ate_3sm_pct         |          2 |          0.916 |            0.916 |       0.044 |  0.900 |  0.931 |
| UFPA — Conceito 3   | trabalha_pct              |          2 |          0.608 |            0.608 |       0.445 |  0.451 |  0.766 |
| UFPA — Conceito 3   | trabalha_40h_pct          |          2 |          0.244 |            0.244 |       0.308 |  0.135 |  0.353 |
| UFPA — Conceito 3   | acao_afirmativa_pct       |          2 |          0.753 |            0.753 |       0.086 |  0.723 |  0.783 |
| UFPA — Conceito 3   | auxilio_permanencia_pct   |          2 |          0.310 |            0.310 |       0.221 |  0.232 |  0.388 |
| UFPA — Conceito 3   | bolsa_academica_pct       |          2 |          0.432 |            0.432 |       0.253 |  0.343 |  0.522 |
| UFPA — Conceito 3   | estudo_4h_ou_mais_pct     |          2 |          0.575 |            0.575 |       0.003 |  0.574 |  0.576 |
| UFPA — Conceito 3   | pretende_magisterio_pct   |          2 |          0.766 |            0.766 |       0.104 |  0.729 |  0.803 |
| UFPA — Conceito 3   | turno_noturno_pct         |          2 |          0.514 |            0.514 |       0.373 |  0.382 |  0.646 |
| UFPA — Conceito 3   | anos_desde_ingresso_media |          2 |          5.119 |            5.119 |       0.063 |  5.096 |  5.141 |
| UFPA — Conceito 3   | qe_i68_media              |          2 |          9.546 |            9.546 |       0.228 |  9.465 |  9.626 |
| UFPA — Conceito 3   | qe_i69_media              |          2 |          9.714 |            9.714 |       0.140 |  9.665 |  9.764 |
| UFPA — Conceito 3   | qe_i70_interesse_pct      |          2 |          0.942 |            0.942 |       0.026 |  0.932 |  0.951 |
| UFPA — Conceito 4   | sexo_feminino_pct         |          2 |          0.355 |            0.355 |       0.123 |  0.311 |  0.398 |
| UFPA — Conceito 4   | idade_media               |          2 |         29.220 |           29.220 |       0.589 | 29.011 | 29.428 |
| UFPA — Conceito 4   | mae_superior_pct          |          2 |          0.193 |            0.193 |       0.024 |  0.185 |  0.202 |
| UFPA — Conceito 4   | pai_superior_pct          |          2 |          0.103 |            0.103 |       0.077 |  0.076 |  0.130 |
| UFPA — Conceito 4   | renda_ate_3sm_pct         |          2 |          0.844 |            0.844 |       0.025 |  0.835 |  0.853 |
| UFPA — Conceito 4   | trabalha_pct              |          2 |          0.615 |            0.615 |       0.008 |  0.612 |  0.618 |
| UFPA — Conceito 4   | trabalha_40h_pct          |          2 |          0.239 |            0.239 |       0.052 |  0.221 |  0.258 |
| UFPA — Conceito 4   | acao_afirmativa_pct       |          2 |          0.631 |            0.631 |       0.112 |  0.591 |  0.671 |
| UFPA — Conceito 4   | auxilio_permanencia_pct   |          2 |          0.173 |            0.173 |       0.001 |  0.173 |  0.174 |
| UFPA — Conceito 4   | bolsa_academica_pct       |          2 |          0.411 |            0.411 |       0.110 |  0.372 |  0.450 |
| UFPA — Conceito 4   | estudo_4h_ou_mais_pct     |          2 |          0.460 |            0.460 |       0.056 |  0.440 |  0.480 |
| UFPA — Conceito 4   | pretende_magisterio_pct   |          2 |          0.912 |            0.912 |       0.022 |  0.904 |  0.920 |
| UFPA — Conceito 4   | turno_noturno_pct         |          2 |          0.792 |            0.792 |       0.294 |  0.688 |  0.896 |
| UFPA — Conceito 4   | anos_desde_ingresso_media |          2 |          4.731 |            4.731 |       0.417 |  4.584 |  4.879 |
| UFPA — Conceito 4   | qe_i68_media              |          2 |          8.116 |            8.116 |       0.676 |  7.877 |  8.355 |
| UFPA — Conceito 4   | qe_i69_media              |          2 |          8.826 |            8.826 |       0.144 |  8.775 |  8.877 |
| UFPA — Conceito 4   | qe_i70_interesse_pct      |          2 |          0.968 |            0.968 |       0.004 |  0.967 |  0.970 |

## Processo formativo

| ITEM   |   N_CURSOS_CONCEITO_3 |   MEDIA_CONCEITO_3 |   N_CURSOS_CONCEITO_4 |   MEDIA_CONCEITO_4 |   DIFERENCA_C3_C4 |   MEDIA_OUTRAS_IES_PARA |   N_OUTRAS_IES_PARA |   MEDIA_NORTE_SEM_PARA |   N_NORTE_SEM_PARA |   MEDIA_BRASIL_SEM_NORTE |   N_BRASIL_SEM_NORTE | STATUS_INTERPRETACAO                                             |
|:-------|----------------------:|-------------------:|----------------------:|-------------------:|------------------:|------------------------:|--------------------:|-----------------------:|-------------------:|-------------------------:|---------------------:|:-----------------------------------------------------------------|
| QE_I33 |                     2 |              5.356 |                     2 |              4.040 |             1.316 |                   4.751 |                   5 |                  4.709 |                 13 |                    4.699 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I31 |                     2 |              5.472 |                     2 |              4.297 |             1.175 |                   4.795 |                   5 |                  4.790 |                 13 |                    4.911 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I21 |                     2 |              5.331 |                     2 |              4.177 |             1.153 |                   4.855 |                   5 |                  5.220 |                 13 |                    4.870 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I40 |                     2 |              5.344 |                     2 |              4.219 |             1.125 |                   5.014 |                   5 |                  4.944 |                 13 |                    5.124 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I34 |                     2 |              5.407 |                     2 |              4.324 |             1.083 |                   5.046 |                   5 |                  4.910 |                 13 |                    5.075 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I20 |                     2 |              5.354 |                     2 |              4.340 |             1.014 |                   4.996 |                   5 |                  5.268 |                 13 |                    4.942 |                  208 | interpretar substantivamente somente com o texto oficial do item |
| QE_I52 |                     2 |              5.328 |                     2 |              4.428 |             0.900 |                   5.033 |                   5 |                  4.919 |                 13 |                    4.849 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I35 |                     2 |              5.657 |                     2 |              4.762 |             0.895 |                   5.431 |                   5 |                  5.259 |                 13 |                    5.155 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I57 |                     2 |              5.401 |                     2 |              4.529 |             0.872 |                   4.979 |                   5 |                  5.023 |                 13 |                    4.946 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I32 |                     2 |              5.384 |                     2 |              4.576 |             0.808 |                   5.029 |                   5 |                  4.926 |                 13 |                    4.996 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I36 |                     2 |              5.699 |                     2 |              4.914 |             0.785 |                   5.493 |                   5 |                  5.308 |                 13 |                    5.318 |                  209 | interpretar substantivamente somente com o texto oficial do item |
| QE_I45 |                     2 |              5.269 |                     2 |              4.487 |             0.782 |                   5.024 |                   5 |                  4.853 |                 13 |                    4.916 |                  209 | interpretar substantivamente somente com o texto oficial do item |

QE_I20–QE_I66 permanecem item a item. A interpretação substantiva dos códigos exige vínculo com o texto oficial e não é criado índice único.

## Recomendação

| RECORTE_GEOGRAFIA   | INDICADOR            |   N_CURSOS |   MEDIA_CURSOS |   MEDIANA_CURSOS |   DP_CURSOS |
|:--------------------|:---------------------|-----------:|---------------:|-----------------:|------------:|
| UFPA — Conceito 3   | qe_i68_media         |          2 |          9.546 |            9.546 |       0.228 |
| UFPA — Conceito 3   | qe_i69_media         |          2 |          9.714 |            9.714 |       0.140 |
| UFPA — Conceito 3   | qe_i70_interesse_pct |          2 |          0.942 |            0.942 |       0.026 |
| UFPA — Conceito 4   | qe_i68_media         |          2 |          8.116 |            8.116 |       0.676 |
| UFPA — Conceito 4   | qe_i69_media         |          2 |          8.826 |            8.826 |       0.144 |
| UFPA — Conceito 4   | qe_i70_interesse_pct |          2 |          0.968 |            0.968 |       0.004 |
| Outras IES do Pará  | qe_i68_media         |          5 |          8.994 |            8.848 |       0.481 |
| Outras IES do Pará  | qe_i69_media         |          5 |          9.275 |            9.250 |       0.427 |
| Outras IES do Pará  | qe_i70_interesse_pct |          5 |          0.970 |            0.979 |       0.034 |
| Norte sem Pará      | qe_i68_media         |         13 |          8.890 |            8.909 |       0.555 |
| Norte sem Pará      | qe_i69_media         |         13 |          9.077 |            9.174 |       0.525 |
| Norte sem Pará      | qe_i70_interesse_pct |         13 |          0.937 |            0.932 |       0.043 |
| Brasil sem Norte    | qe_i68_media         |        209 |          8.800 |            8.797 |       0.703 |
| Brasil sem Norte    | qe_i69_media         |        209 |          8.913 |            9.043 |       0.819 |
| Brasil sem Norte    | qe_i70_interesse_pct |        209 |          0.935 |            0.957 |       0.077 |

QE_I68, QE_I69 e QE_I70 permanecem conceitualmente separados e não são automaticamente denominados satisfação.

## Comparações regionais e nacionais

| RECORTE                        | INDICADOR   |   N_CURSOS |   N_PARTICIPANTES |   MEDIA_CURSOS |   MEDIA_PONDERADA_PARTICIPANTES |   MEDIANA_CURSOS |   DP_CURSOS |    P25 |    P75 |   AMPLITUDE_IQR |   DIF_MEDIA_PONDERADA | ALERTA_IQR_NEGATIVO   |
|:-------------------------------|:------------|-----------:|------------------:|---------------:|--------------------------------:|-----------------:|------------:|-------:|-------:|----------------:|----------------------:|:----------------------|
| UFPA — Ananindeua — Presencial | nt_ger_mean |          1 |            63.000 |         61.516 |                          61.516 |           61.516 |     nan     | 61.516 | 61.516 |           0.000 |                 0.000 | False                 |
| UFPA — Cametá — Presencial     | nt_ger_mean |          1 |            68.000 |         55.866 |                          55.866 |           55.866 |     nan     | 55.866 | 55.866 |           0.000 |                 0.000 | False                 |
| UFPA — Altamira — Presencial   | nt_ger_mean |          1 |            23.000 |         58.097 |                          58.097 |           58.097 |     nan     | 58.097 | 58.097 |           0.000 |                 0.000 | False                 |
| UFPA — Belém — Presencial      | nt_ger_mean |          1 |            57.000 |         66.844 |                          66.844 |           66.844 |     nan     | 66.844 | 66.844 |           0.000 |                 0.000 | False                 |
| UFPA agregada                  | nt_ger_mean |          4 |           211.000 |         60.581 |                          60.762 |           59.806 |       4.778 | 57.540 | 62.848 |           5.308 |                 0.181 | False                 |
| Região Norte sem UFPA          | nt_ger_mean |         18 |           527.000 |         55.163 |                          56.172 |           57.811 |       8.641 | 48.077 | 60.726 |          12.649 |                 1.009 | False                 |
| Região Norte completa          | nt_ger_mean |         22 |           738.000 |         56.148 |                          57.484 |           58.375 |       8.263 | 51.170 | 61.379 |          10.209 |                 1.336 | False                 |
| Nordeste                       | nt_ger_mean |         66 |          2308.000 |         62.403 |                          62.704 |           61.957 |       9.151 | 56.851 | 68.966 |          12.115 |                 0.301 | False                 |
| Sudeste                        | nt_ger_mean |         67 |          2011.000 |         64.227 |                          67.784 |           64.234 |      11.982 | 56.292 | 73.169 |          16.877 |                 3.557 | False                 |
| Sul                            | nt_ger_mean |         43 |          2037.000 |         62.911 |                          57.688 |           62.018 |      10.334 | 57.646 | 70.227 |          12.582 |                -5.223 | False                 |
| Centro-Oeste                   | nt_ger_mean |         29 |           407.000 |         58.830 |                          60.736 |           56.869 |      11.659 | 52.068 | 66.978 |          14.910 |                 1.906 | False                 |
| Brasil geral                   | nt_ger_mean |        227 |          7501.000 |         61.975 |                          62.083 |           61.659 |      10.740 | 55.563 | 68.858 |          13.295 |                 0.108 | False                 |
| Brasil sem UFPA                | nt_ger_mean |        223 |          7290.000 |         62.000 |                          62.122 |           61.725 |      10.820 | 55.406 | 68.967 |          13.561 |                 0.122 | False                 |
| Restante do Brasil sem Norte   | nt_ger_mean |        205 |          6763.000 |         62.600 |                          62.585 |           62.198 |      10.803 | 55.780 | 69.872 |          14.092 |                -0.015 | False                 |

Pará, Norte e Brasil completos são benchmarks descritivos sobrepostos, não grupos independentes em testes.

## Associações ecológicas

| INDICADOR_X               | INDICADOR_Y   |   N_CURSOS |   SPEARMAN_RHO |   P_VALOR_EXPLORATORIO | NIVEL_ANALISE     | RESSALVA                                             |
|:--------------------------|:--------------|-----------:|---------------:|-----------------------:|:------------------|:-----------------------------------------------------|
| bolsa_academica_pct       | nt_ger_mean   |        224 |         0.4144 |                 0.0000 | curso (ecológico) | não interpretar como associação individual ou causal |
| estudo_4h_ou_mais_pct     | nt_ger_mean   |        227 |         0.3876 |                 0.0000 | curso (ecológico) | não interpretar como associação individual ou causal |
| auxilio_permanencia_pct   | nt_ger_mean   |        227 |         0.3250 |                 0.0000 | curso (ecológico) | não interpretar como associação individual ou causal |
| acao_afirmativa_pct       | nt_ger_mean   |        227 |         0.2631 |                 0.0001 | curso (ecológico) | não interpretar como associação individual ou causal |
| qe_i68_media              | nt_ger_mean   |        227 |        -0.2440 |                 0.0002 | curso (ecológico) | não interpretar como associação individual ou causal |
| anos_desde_ingresso_media | nt_ger_mean   |        227 |         0.2195 |                 0.0009 | curso (ecológico) | não interpretar como associação individual ou causal |
| renda_ate_3sm_pct         | nt_ger_mean   |        227 |        -0.1978 |                 0.0028 | curso (ecológico) | não interpretar como associação individual ou causal |
| trabalha_pct              | nt_ger_mean   |        227 |        -0.1417 |                 0.0328 | curso (ecológico) | não interpretar como associação individual ou causal |
| qe_i69_media              | nt_ger_mean   |        227 |         0.0468 |                 0.4829 | curso (ecológico) | não interpretar como associação individual ou causal |
| turno_noturno_pct         | nt_ger_mean   |        227 |         0.0101 |                 0.8793 | curso (ecológico) | não interpretar como associação individual ou causal |

As correlações de Spearman usam cursos como unidades. Não representam associações individuais e não sustentam causalidade.

## Outliers

|   CO_CURSO | ROTULO_OFERTA   | RECORTE_GEOGRAFIA   | INDICADOR   |   VALOR |     Q1 |     Q3 |   LIMITE_INFERIOR |   LIMITE_SUPERIOR | OUTLIER_IQR   |
|-----------:|:----------------|:--------------------|:------------|--------:|-------:|-------:|------------------:|------------------:|:--------------|
|    1143415 | Araras — EaD    | Brasil sem Norte    | nt_ger_mean |  30.220 | 55.563 | 68.858 |            35.621 |            88.800 | True          |
|    1143415 | Araras — EaD    | Brasil sem Norte    | nt_dis_mean |   1.000 |  5.122 |  6.576 |             2.940 |             8.758 | True          |
|    1439551 | Marília — EaD   | Brasil sem Norte    | nt_dis_mean |   2.458 |  5.122 |  6.576 |             2.940 |             8.758 | True          |
|    1483499 | São Paulo — EaD | Brasil sem Norte    | nt_dis_mean |   2.450 |  5.122 |  6.576 |             2.940 |             8.758 | True          |

Outliers são sinalizados e preservados, não excluídos automaticamente.

## Decisões para o relatório final

- preservar o contraste Conceito 3 × Conceito 4 como descritivo;
- informar N, dispersão e participação para cada oferta;
- usar cinco cenários de benchmark por oferta;
- interpretar processo formativo somente com rótulos oficiais;
- manter QE_I68, QE_I69 e QE_I70 separados;
- manter associações entre temas no nível ecológico do curso.