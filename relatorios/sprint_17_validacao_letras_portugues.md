# Sprint 17 — Validação analítica de Letras–Português

## Escopo

Foram auditados **340 cursos de Letras–Português**, incluindo **8 ofertas localizadas da UFPA**. O Grupo A contém apenas Belém EaD (`CO_CURSO=115161`), Conceito Enade 1.

A oferta inicialmente informada de Soure permanece como não localizada nas fontes de 2025 e não recebe CO_CURSO, conceito, participação ou desempenho artificiais.

A unidade principal permanece `CO_CURSO`; não há junções individuais entre temas. Relações entre perfil, processo formativo, recomendação e desempenho são ecológicas.

## Ofertas UFPA auditadas

|   CO_CURSO | ROTULO_OFERTA           |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   taxa_presenca_microdados |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |   nt_ger_percentil_brasil |   nt_ger_percentil_norte |   nt_ger_percentil_para |
|-----------:|:------------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------------------:|--------------:|--------------:|--------------:|--------------------------:|-------------------------:|------------------------:|
|     114850 | Abaetetuba — Presencial |                3.000 |              95 |              82.000 |                       0.863 |                      0.863 |        56.532 |        53.218 |         6.979 |                    47.335 |                   61.111 |                  62.500 |
|     114876 | Altamira — Presencial   |                2.000 |              57 |              47.000 |                       0.825 |                      0.825 |        49.951 |        46.747 |         6.277 |                    24.138 |                   25.000 |                  25.000 |
|     115161 | Belém — EaD             |                1.000 |              67 |              56.000 |                       0.836 |                      0.836 |        44.651 |        41.952 |         5.545 |                    12.226 |                   13.889 |                   6.250 |
|      27645 | Belém — Presencial      |                4.000 |             182 |             150.000 |                       0.824 |                      0.824 |        66.941 |        65.459 |         7.287 |                    78.997 |                   91.667 |                  93.750 |
|     114874 | Bragança — Presencial   |                3.000 |              51 |              49.000 |                       0.961 |                      0.961 |        59.288 |        56.559 |         7.020 |                    55.486 |                   75.000 |                  75.000 |
|     115013 | Breves — Presencial     |                3.000 |              34 |              25.000 |                       0.735 |                      0.735 |        54.033 |        50.916 |         6.650 |                    42.006 |                   52.778 |                  56.250 |
|     114846 | Cametá — Presencial     |                3.000 |              87 |              69.000 |                       0.793 |                      0.793 |        52.850 |        48.481 |         7.033 |                    37.304 |                   41.667 |                  50.000 |
|     114857 | Castanhal — Presencial  |                3.000 |              44 |              38.000 |                       0.864 |                      0.864 |        61.106 |        59.968 |         6.566 |                    61.442 |                   80.556 |                  87.500 |

## Auditoria de N e participação

|   CO_CURSO | ROTULO_OFERTA           | GRUPO_CODIGO   |   PARTICIPANTES_NUM |   registros_microdados |   presentes_validos |   nt_ger_count |   nt_obj_count |   nt_dis_count |   reaplicacoes |   diferenca_participantes_oficial_nt_ger | alerta_n_superior_registros   | alerta_diferenca_participantes   |
|-----------:|:------------------------|:---------------|--------------------:|-----------------------:|--------------------:|---------------:|---------------:|---------------:|---------------:|-----------------------------------------:|:------------------------------|:---------------------------------|
|      27645 | Belém — Presencial      | B              |             150.000 |                    182 |                 150 |            150 |            150 |            150 |              0 |                                    0.000 | False                         | False                            |
|     114846 | Cametá — Presencial     | B              |              69.000 |                     87 |                  69 |             69 |             69 |             69 |              0 |                                    0.000 | False                         | False                            |
|     114850 | Abaetetuba — Presencial | B              |              82.000 |                     95 |                  82 |             82 |             82 |             82 |              0 |                                    0.000 | False                         | False                            |
|     114857 | Castanhal — Presencial  | B              |              38.000 |                     44 |                  38 |             38 |             38 |             38 |              0 |                                    0.000 | False                         | False                            |
|     114874 | Bragança — Presencial   | B              |              49.000 |                     51 |                  49 |             49 |             49 |             49 |              0 |                                    0.000 | False                         | False                            |
|     114876 | Altamira — Presencial   | B              |              47.000 |                     57 |                  47 |             47 |             47 |             47 |              0 |                                    0.000 | False                         | False                            |
|     115013 | Breves — Presencial     | B              |              25.000 |                     34 |                  25 |             25 |             25 |             25 |              0 |                                    0.000 | False                         | False                            |
|     115161 | Belém — EaD             | A              |              56.000 |                     67 |                  56 |             56 |             56 |             56 |              0 |                                    0.000 | False                         | False                            |

## Comparações regionais e nacionais

| RECORTE                        | INDICADOR   |   N_CURSOS |   N_PARTICIPANTES |   MEDIA_CURSOS |   MEDIA_PONDERADA_PARTICIPANTES |   MEDIANA_CURSOS |   DP_CURSOS |    P25 |    P75 |   AMPLITUDE_IQR |   DIF_MEDIA_PONDERADA | ALERTA_IQR_NEGATIVO   |
|:-------------------------------|:------------|-----------:|------------------:|---------------:|--------------------------------:|-----------------:|------------:|-------:|-------:|----------------:|----------------------:|:----------------------|
| UFPA — Belém — EaD             | nt_ger_mean |          1 |            56.000 |         44.651 |                          44.651 |           44.651 |     nan     | 44.651 | 44.651 |           0.000 |                 0.000 | False                 |
| UFPA — Breves — Presencial     | nt_ger_mean |          1 |            25.000 |         54.033 |                          54.033 |           54.033 |     nan     | 54.033 | 54.033 |           0.000 |                 0.000 | False                 |
| UFPA — Altamira — Presencial   | nt_ger_mean |          1 |            47.000 |         49.951 |                          49.951 |           49.951 |     nan     | 49.951 | 49.951 |           0.000 |                 0.000 | False                 |
| UFPA — Bragança — Presencial   | nt_ger_mean |          1 |            49.000 |         59.288 |                          59.288 |           59.288 |     nan     | 59.288 | 59.288 |           0.000 |                 0.000 | False                 |
| UFPA — Castanhal — Presencial  | nt_ger_mean |          1 |            38.000 |         61.106 |                          61.106 |           61.106 |     nan     | 61.106 | 61.106 |           0.000 |                 0.000 | False                 |
| UFPA — Abaetetuba — Presencial | nt_ger_mean |          1 |            82.000 |         56.532 |                          56.532 |           56.532 |     nan     | 56.532 | 56.532 |           0.000 |                 0.000 | False                 |
| UFPA — Cametá — Presencial     | nt_ger_mean |          1 |            69.000 |         52.850 |                          52.850 |           52.850 |     nan     | 52.850 | 52.850 |           0.000 |                 0.000 | False                 |
| UFPA — Belém — Presencial      | nt_ger_mean |          1 |           150.000 |         66.941 |                          66.941 |           66.941 |     nan     | 66.941 | 66.941 |           0.000 |                 0.000 | False                 |
| UFPA agregada                  | nt_ger_mean |          8 |           516.000 |         55.669 |                          57.654 |           55.282 |       6.920 | 52.125 | 59.743 |           7.617 |                 1.985 | False                 |
| Região Norte sem UFPA          | nt_ger_mean |         28 |           773.000 |         54.556 |                          55.194 |           53.506 |       9.496 | 50.244 | 59.446 |           9.202 |                 0.638 | False                 |
| Região Norte completa          | nt_ger_mean |         36 |          1289.000 |         54.803 |                          56.179 |           53.815 |       8.909 | 50.399 | 59.678 |           9.279 |                 1.375 | False                 |
| Nordeste                       | nt_ger_mean |        121 |          3646.000 |         55.946 |                          58.205 |           55.157 |       9.444 | 48.987 | 62.147 |          13.161 |                 2.259 | False                 |
| Sudeste                        | nt_ger_mean |         77 |          2437.000 |         59.856 |                          63.047 |           61.745 |      12.409 | 50.250 | 69.134 |          18.884 |                 3.191 | False                 |
| Sul                            | nt_ger_mean |         54 |          3040.000 |         60.875 |                          53.931 |           59.757 |      11.450 | 53.867 | 69.819 |          15.952 |                -6.944 | False                 |
| Centro-Oeste                   | nt_ger_mean |         31 |           569.000 |         56.402 |                          58.226 |           53.949 |      10.644 | 50.275 | 63.606 |          13.331 |                 1.824 | False                 |
| Brasil geral                   | nt_ger_mean |        319 |         10981.000 |         57.639 |                          57.860 |           57.187 |      10.810 | 50.085 | 64.830 |          14.744 |                 0.220 | False                 |
| Brasil sem UFPA                | nt_ger_mean |        311 |         10465.000 |         57.690 |                          57.870 |           57.347 |      10.894 | 50.085 | 64.883 |          14.797 |                 0.180 | False                 |
| Restante do Brasil sem Norte   | nt_ger_mean |        283 |          9692.000 |         58.000 |                          58.083 |           57.980 |      10.989 | 50.085 | 64.995 |          14.910 |                 0.083 | False                 |

Pará, Norte e Brasil completos permanecem benchmarks descritivos sobrepostos e não são usados como grupos independentes em testes.

## Sensibilidade dos grupos A–E

| cenario                | grupo   |   n_cursos |   media_cursos |   mediana_cursos |   media_ponderada_participantes |
|:-----------------------|:--------|-----------:|---------------:|-----------------:|--------------------------------:|
| todos                  | A       |          1 |         44.651 |           44.651 |                          44.651 |
| todos                  | B       |          7 |         57.243 |           56.532 |                          59.237 |
| todos                  | C       |          8 |         54.196 |           52.005 |                          54.912 |
| todos                  | D       |         20 |         54.700 |           53.937 |                          55.338 |
| todos                  | E       |        283 |         58.000 |           57.980 |                          58.083 |
| n_minimo_10            | A       |          1 |         44.651 |           44.651 |                          44.651 |
| n_minimo_10            | B       |          7 |         57.243 |           56.532 |                          59.237 |
| n_minimo_10            | C       |          8 |         54.196 |           52.005 |                          54.912 |
| n_minimo_10            | D       |         14 |         54.673 |           55.376 |                          55.671 |
| n_minimo_10            | E       |        202 |         58.636 |           58.047 |                          58.142 |
| presencial             | B       |          7 |         57.243 |           56.532 |                          59.237 |
| presencial             | C       |          7 |         55.450 |           52.110 |                          56.286 |
| presencial             | D       |         18 |         55.766 |           55.376 |                          55.689 |
| presencial             | E       |        181 |         60.319 |           61.504 |                          62.874 |
| universidades_federais | A       |          1 |         44.651 |           44.651 |                          44.651 |
| universidades_federais | B       |          7 |         57.243 |           56.532 |                          59.237 |
| universidades_federais | C       |          6 |         55.029 |           52.005 |                          56.200 |
| universidades_federais | D       |         12 |         55.077 |           55.376 |                          55.703 |
| universidades_federais | E       |         87 |         63.054 |           63.941 |                          64.872 |

O cenário presencial pode excluir a única oferta do Grupo A, pois Belém EaD é educação a distância. Essa ausência é informativa sobre comparabilidade e não é preenchida artificialmente.

## Sensibilidade do benchmark da oferta Conceito 1

|   CO_CURSO_ALVO | ROTULO_ALVO   | criterio    |   n_comparaveis |   nt_ger_alvo |   media_benchmark |   mediana_benchmark |   diferenca_media |   diferenca_mediana |
|----------------:|:--------------|:------------|----------------:|--------------:|------------------:|--------------------:|------------------:|--------------------:|
|          115161 | Belém — EaD   | porte_25pct |               1 |        44.651 |            43.100 |              43.100 |             1.551 |               1.551 |
|          115161 | Belém — EaD   | porte_50pct |               4 |        44.651 |            49.563 |              50.840 |            -4.913 |              -6.189 |
|          115161 | Belém — EaD   | porte_2x    |               4 |        44.651 |            49.563 |              50.840 |            -4.913 |              -6.189 |

Os critérios de porte ±25%, ±50% e até 2x preservam modalidade, categoria administrativa e organização acadêmica. O benchmark reduz heterogeneidade observável, mas não constitui desenho causal.

## Perfil demográfico, socioeconômico e trajetória

| GRUPO_CODIGO   | GRUPO                    | INDICADOR                 |   N_CURSOS |   MEDIA_CURSOS |   MEDIANA_CURSOS |   DP_CURSOS |    P25 |    P75 |
|:---------------|:-------------------------|:--------------------------|-----------:|---------------:|-----------------:|------------:|-------:|-------:|
| A              | UFPA — Conceito 1        | sexo_feminino_pct         |          1 |          0.836 |            0.836 |     nan     |  0.836 |  0.836 |
| A              | UFPA — Conceito 1        | idade_media               |          1 |         36.866 |           36.866 |     nan     | 36.866 | 36.866 |
| A              | UFPA — Conceito 1        | mae_superior_pct          |          1 |          0.167 |            0.167 |     nan     |  0.167 |  0.167 |
| A              | UFPA — Conceito 1        | pai_superior_pct          |          1 |          0.077 |            0.077 |     nan     |  0.077 |  0.077 |
| A              | UFPA — Conceito 1        | renda_ate_3sm_pct         |          1 |          0.817 |            0.817 |     nan     |  0.817 |  0.817 |
| A              | UFPA — Conceito 1        | trabalha_pct              |          1 |          0.700 |            0.700 |     nan     |  0.700 |  0.700 |
| A              | UFPA — Conceito 1        | trabalha_40h_pct          |          1 |          0.450 |            0.450 |     nan     |  0.450 |  0.450 |
| A              | UFPA — Conceito 1        | acao_afirmativa_pct       |          1 |          0.533 |            0.533 |     nan     |  0.533 |  0.533 |
| A              | UFPA — Conceito 1        | auxilio_permanencia_pct   |          1 |          0.000 |            0.000 |     nan     |  0.000 |  0.000 |
| A              | UFPA — Conceito 1        | bolsa_academica_pct       |          1 |          0.000 |            0.000 |     nan     |  0.000 |  0.000 |
| A              | UFPA — Conceito 1        | estudo_4h_ou_mais_pct     |          1 |          0.533 |            0.533 |     nan     |  0.533 |  0.533 |
| A              | UFPA — Conceito 1        | pretende_magisterio_pct   |          1 |          0.867 |            0.867 |     nan     |  0.867 |  0.867 |
| A              | UFPA — Conceito 1        | turno_noturno_pct         |          1 |          0.000 |            0.000 |     nan     |  0.000 |  0.000 |
| A              | UFPA — Conceito 1        | anos_desde_ingresso_media |          1 |          4.925 |            4.925 |     nan     |  4.925 |  4.925 |
| A              | UFPA — Conceito 1        | qe_i68_media              |          1 |          8.883 |            8.883 |     nan     |  8.883 |  8.883 |
| A              | UFPA — Conceito 1        | qe_i69_media              |          1 |          9.050 |            9.050 |     nan     |  9.050 |  9.050 |
| A              | UFPA — Conceito 1        | qe_i70_interesse_pct      |          1 |          0.967 |            0.967 |     nan     |  0.967 |  0.967 |
| B              | UFPA — conceito superior | sexo_feminino_pct         |          7 |          0.747 |            0.719 |       0.069 |  0.710 |  0.757 |
| B              | UFPA — conceito superior | idade_media               |          7 |         28.937 |           29.032 |       1.063 | 28.229 | 29.494 |
| B              | UFPA — conceito superior | mae_superior_pct          |          7 |          0.187 |            0.184 |       0.050 |  0.165 |  0.207 |
| B              | UFPA — conceito superior | pai_superior_pct          |          7 |          0.098 |            0.081 |       0.052 |  0.065 |  0.117 |
| B              | UFPA — conceito superior | renda_ate_3sm_pct         |          7 |          0.863 |            0.852 |       0.095 |  0.789 |  0.941 |
| B              | UFPA — conceito superior | trabalha_pct              |          7 |          0.477 |            0.480 |       0.144 |  0.435 |  0.554 |
| B              | UFPA — conceito superior | trabalha_40h_pct          |          7 |          0.188 |            0.174 |       0.143 |  0.133 |  0.191 |
| B              | UFPA — conceito superior | acao_afirmativa_pct       |          7 |          0.767 |            0.780 |       0.100 |  0.726 |  0.843 |
| B              | UFPA — conceito superior | auxilio_permanencia_pct   |          7 |          0.277 |            0.185 |       0.134 |  0.182 |  0.347 |
| B              | UFPA — conceito superior | bolsa_academica_pct       |          7 |          0.331 |            0.308 |       0.101 |  0.293 |  0.349 |
| B              | UFPA — conceito superior | estudo_4h_ou_mais_pct     |          7 |          0.581 |            0.564 |       0.073 |  0.536 |  0.632 |
| B              | UFPA — conceito superior | pretende_magisterio_pct   |          7 |          0.861 |            0.860 |       0.026 |  0.843 |  0.875 |
| B              | UFPA — conceito superior | turno_noturno_pct         |          7 |          0.391 |            0.379 |       0.149 |  0.309 |  0.469 |
| B              | UFPA — conceito superior | anos_desde_ingresso_media |          7 |          5.482 |            5.547 |       0.791 |  5.044 |  5.897 |
| B              | UFPA — conceito superior | qe_i68_media              |          7 |          8.702 |            8.593 |       0.546 |  8.311 |  9.153 |
| B              | UFPA — conceito superior | qe_i69_media              |          7 |          9.061 |            8.933 |       0.524 |  8.615 |  9.535 |
| B              | UFPA — conceito superior | qe_i70_interesse_pct      |          7 |          0.968 |            0.972 |       0.023 |  0.958 |  0.980 |

## Processo formativo

| ITEM   | REFERENCIA                  |   MEDIA_CONCEITO1 |   N_VALIDO_CONCEITO1 |   N_CURSOS_REFERENCIA |   MEDIA_REFERENCIA |   MEDIANA_REFERENCIA |   DP_REFERENCIA |   DIFERENCA_CONCEITO1_REFERENCIA |
|:-------|:----------------------------|------------------:|---------------------:|----------------------:|-------------------:|---------------------:|----------------:|---------------------------------:|
| QE_I20 | UFPA — conceitos superiores |             2.186 |                   43 |                     7 |              4.551 |                4.766 |           0.421 |                           -2.365 |
| QE_I21 | UFPA — conceitos superiores |             2.455 |                   44 |                     7 |              4.516 |                4.766 |           0.475 |                           -2.061 |
| QE_I31 | UFPA — conceitos superiores |             5.035 |                   57 |                     7 |              4.424 |                4.295 |           0.684 |                            0.611 |
| QE_I42 | UFPA — conceitos superiores |             4.927 |                   55 |                     7 |              4.379 |                4.100 |           0.575 |                            0.549 |
| QE_I40 | UFPA — conceitos superiores |             5.310 |                   58 |                     7 |              4.774 |                4.944 |           0.363 |                            0.537 |
| QE_I45 | UFPA — conceitos superiores |             4.982 |                   57 |                     7 |              4.478 |                4.500 |           0.421 |                            0.505 |
| QE_I55 | UFPA — conceitos superiores |             5.339 |                   59 |                     7 |              4.939 |                5.093 |           0.582 |                            0.400 |
| QE_I32 | UFPA — conceitos superiores |             5.172 |                   58 |                     7 |              4.783 |                4.705 |           0.307 |                            0.389 |
| QE_I23 | UFPA — conceitos superiores |             4.576 |                   59 |                     7 |              4.954 |                4.880 |           0.432 |                           -0.378 |
| QE_I52 | UFPA — conceitos superiores |             4.949 |                   59 |                     7 |              4.591 |                4.857 |           0.621 |                            0.358 |
| QE_I28 | UFPA — conceitos superiores |             5.138 |                   58 |                     7 |              5.493 |                5.519 |           0.224 |                           -0.355 |
| QE_I34 | UFPA — conceitos superiores |             4.466 |                   58 |                     7 |              4.818 |                4.930 |           0.295 |                           -0.352 |

QE_I20–QE_I66 são mantidos item a item. As diferenças acima ainda devem ser vinculadas aos textos oficiais no relatório final; não é criado índice único.

## Recomendação

| GRUPO_CODIGO   | INDICADOR            |   N_CURSOS |   MEDIA_CURSOS |   MEDIANA_CURSOS |   DP_CURSOS |
|:---------------|:---------------------|-----------:|---------------:|-----------------:|------------:|
| A              | qe_i68_media         |          1 |          8.883 |            8.883 |     nan     |
| A              | qe_i69_media         |          1 |          9.050 |            9.050 |     nan     |
| A              | qe_i70_interesse_pct |          1 |          0.967 |            0.967 |     nan     |
| B              | qe_i68_media         |          7 |          8.702 |            8.593 |       0.546 |
| B              | qe_i69_media         |          7 |          9.061 |            8.933 |       0.524 |
| B              | qe_i70_interesse_pct |          7 |          0.968 |            0.972 |       0.023 |
| C              | qe_i68_media         |          8 |          8.969 |            8.880 |       0.524 |
| C              | qe_i69_media         |          8 |          9.025 |            9.082 |       0.606 |
| C              | qe_i70_interesse_pct |          8 |          0.951 |            0.959 |       0.055 |
| D              | qe_i68_media         |         20 |          8.797 |            8.788 |       0.698 |
| D              | qe_i69_media         |         20 |          9.025 |            9.048 |       0.576 |
| D              | qe_i70_interesse_pct |         20 |          0.951 |            0.964 |       0.051 |
| E              | qe_i68_media         |        286 |          8.684 |            8.779 |       0.838 |
| E              | qe_i69_media         |        286 |          8.738 |            8.926 |       1.061 |
| E              | qe_i70_interesse_pct |        286 |          0.917 |            0.944 |       0.105 |

QE_I68, QE_I69 e QE_I70 são mantidos com seus significados próprios; não são automaticamente denominados satisfação.

## Associações ecológicas

| INDICADOR_X               | INDICADOR_Y   |   N_CURSOS |   SPEARMAN_RHO |   P_VALOR_EXPLORATORIO | NIVEL_ANALISE     | RESSALVA                                             |
|:--------------------------|:--------------|-----------:|---------------:|-----------------------:|:------------------|:-----------------------------------------------------|
| estudo_4h_ou_mais_pct     | nt_ger_mean   |        319 |         0.3994 |                 0.0000 | curso (ecológico) | não interpretar como associação individual ou causal |
| renda_ate_3sm_pct         | nt_ger_mean   |        319 |        -0.3905 |                 0.0000 | curso (ecológico) | não interpretar como associação individual ou causal |
| bolsa_academica_pct       | nt_ger_mean   |        318 |         0.3298 |                 0.0000 | curso (ecológico) | não interpretar como associação individual ou causal |
| acao_afirmativa_pct       | nt_ger_mean   |        319 |         0.2773 |                 0.0000 | curso (ecológico) | não interpretar como associação individual ou causal |
| qe_i68_media              | nt_ger_mean   |        319 |        -0.2560 |                 0.0000 | curso (ecológico) | não interpretar como associação individual ou causal |
| auxilio_permanencia_pct   | nt_ger_mean   |        319 |         0.1835 |                 0.0010 | curso (ecológico) | não interpretar como associação individual ou causal |
| anos_desde_ingresso_media | nt_ger_mean   |        319 |         0.0849 |                 0.1302 | curso (ecológico) | não interpretar como associação individual ou causal |
| trabalha_pct              | nt_ger_mean   |        319 |        -0.0353 |                 0.5296 | curso (ecológico) | não interpretar como associação individual ou causal |
| qe_i69_media              | nt_ger_mean   |        319 |        -0.0056 |                 0.9209 | curso (ecológico) | não interpretar como associação individual ou causal |
| turno_noturno_pct         | nt_ger_mean   |        319 |         0.0014 |                 0.9806 | curso (ecológico) | não interpretar como associação individual ou causal |

As correlações de Spearman usam cursos como unidades e não representam relações individuais nem sustentam causalidade.

## Outliers

|   CO_CURSO | ROTULO_OFERTA                  | GRUPO_CODIGO   | INDICADOR   |   VALOR |    Q1 |    Q3 |   LIMITE_INFERIOR |   LIMITE_SUPERIOR | OUTLIER_IQR   |
|-----------:|:-------------------------------|:---------------|:------------|--------:|------:|------:|------------------:|------------------:|:--------------|
|      55276 | Santa Cruz do Sul — Presencial | E              | nt_dis_mean |   3.250 | 5.939 | 7.261 |             3.956 |             9.244 | True          |
|      87502 | Itajaí — Presencial            | E              | nt_dis_mean |   3.950 | 5.939 | 7.261 |             3.956 |             9.244 | True          |
|     121411 | Presidente Dutra — Presencial  | E              | nt_dis_mean |   3.482 | 5.939 | 7.261 |             3.956 |             9.244 | True          |
|    1445622 | Araxá — EaD                    | E              | nt_dis_mean |   1.625 | 5.939 | 7.261 |             3.956 |             9.244 | True          |
|    1496680 | Curitiba — EaD                 | E              | nt_dis_mean |   3.955 | 5.939 | 7.261 |             3.956 |             9.244 | True          |
|    1508910 | Joinville — EaD                | E              | nt_dis_mean |   3.344 | 5.939 | 7.261 |             3.956 |             9.244 | True          |
|    1525883 | Teófilo Otoni — EaD            | E              | nt_dis_mean |   3.600 | 5.939 | 7.261 |             3.956 |             9.244 | True          |
|    1675036 | Jaciara — Presencial           | E              | nt_dis_mean |   3.683 | 5.939 | 7.261 |             3.956 |             9.244 | True          |

Outliers são sinalizados e preservados, não excluídos automaticamente.

## Decisões para o relatório final

- tratar Belém EaD como a única oferta UFPA Conceito 1, sem generalizar uma unidade para um grupo populacional;
- contrastar a oferta focal com as sete ofertas UFPA de conceito superior e com benchmarks estruturais;
- preservar Soure como não localizada nas fontes de 2025;
- informar N, dispersão, percentis e participação em todas as comparações de desempenho;
- interpretar QE_I20–QE_I66 somente após associação aos rótulos oficiais;
- manter QE_I68, QE_I69 e QE_I70 separados;
- manter todas as relações entre temas distintos no nível ecológico do curso.