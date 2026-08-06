# Sprint 11 — Validação analítica de Ciências Biológicas com foco em Soure

## Resumo executivo

Foram auditados **428 cursos de Ciências Biológicas**, incluindo **5 ofertas da UFPA**. A oferta focal é Soure (`CO_CURSO=104640`). Não existe oferta UFPA com Conceito Enade 1; portanto, a validação preserva Soure como caso focal e usa referências territoriais e estruturais.

## Soure — participação e desempenho

|   CO_CURSO |   INSCRITOS |   PARTICIPANTES |   TAXA_PARTICIPACAO_OFICIAL |   NT_GER |   NT_OBJ |   NT_DIS |   PERCENTIL_BRASIL |   PERCENTIL_NORTE |   PERCENTIL_PARA |
|-----------:|------------:|----------------:|----------------------------:|---------:|---------:|---------:|-------------------:|------------------:|-----------------:|
| 104640.000 |      65.000 |          49.000 |                       0.754 |   53.505 |   50.567 |    6.526 |             27.228 |            40.000 |           41.176 |

## Sensibilidade do benchmark de Soure

| CENARIO                      |   CO_CURSO_ALVO |   N_CURSOS |   nt_ger_mean_ALVO |   nt_ger_mean_MEDIA_BENCHMARK |   nt_ger_mean_MEDIANA_BENCHMARK |   nt_ger_mean_DP_BENCHMARK |   nt_ger_mean_DIFERENCA |   nt_obj_mean_ALVO |   nt_obj_mean_MEDIA_BENCHMARK |   nt_obj_mean_MEDIANA_BENCHMARK |   nt_obj_mean_DP_BENCHMARK |   nt_obj_mean_DIFERENCA |   nt_dis_mean_ALVO |   nt_dis_mean_MEDIA_BENCHMARK |   nt_dis_mean_MEDIANA_BENCHMARK |   nt_dis_mean_DP_BENCHMARK |   nt_dis_mean_DIFERENCA |   taxa_presenca_microdados_ALVO |   taxa_presenca_microdados_MEDIA_BENCHMARK |   taxa_presenca_microdados_MEDIANA_BENCHMARK |   taxa_presenca_microdados_DP_BENCHMARK |   taxa_presenca_microdados_DIFERENCA |
|:-----------------------------|----------------:|-----------:|-------------------:|------------------------------:|--------------------------------:|---------------------------:|------------------------:|-------------------:|------------------------------:|--------------------------------:|---------------------------:|------------------------:|-------------------:|------------------------------:|--------------------------------:|---------------------------:|------------------------:|--------------------------------:|-------------------------------------------:|---------------------------------------------:|----------------------------------------:|-------------------------------------:|
| modalidade                   |          104640 |        341 |             53.505 |                        58.375 |                          58.015 |                      6.314 |                  -4.870 |             50.567 |                        57.735 |                          57.500 |                      5.566 |                  -7.167 |              6.526 |                         6.094 |                           6.192 |                      1.178 |                   0.432 |                           0.754 |                                      0.822 |                                        0.871 |                                   0.193 |                               -0.068 |
| modalidade_categoria         |          104640 |        177 |             53.505 |                        58.955 |                          58.404 |                      5.679 |                  -5.450 |             50.567 |                        58.156 |                          57.925 |                      5.203 |                  -7.588 |              6.526 |                         6.215 |                           6.274 |                      0.959 |                   0.310 |                           0.754 |                                      0.833 |                                        0.863 |                                   0.160 |                               -0.079 |
| modalidade_categoria_orgacad |          104640 |         96 |             53.505 |                        61.413 |                          61.567 |                      5.455 |                  -7.908 |             50.567 |                        60.279 |                          60.343 |                      5.131 |                  -9.712 |              6.526 |                         6.595 |                           6.736 |                      0.849 |                  -0.069 |                           0.754 |                                      0.840 |                                        0.870 |                                   0.134 |                               -0.086 |
| estrutura_porte_0_5_2_0      |          104640 |         56 |             53.505 |                        62.137 |                          62.567 |                      4.582 |                  -8.632 |             50.567 |                        60.907 |                          61.066 |                      4.390 |                 -10.339 |              6.526 |                         6.706 |                           6.898 |                      0.657 |                  -0.180 |                           0.754 |                                      0.855 |                                        0.873 |                                   0.097 |                               -0.101 |
| estrutura_porte_0_75_1_5     |          104640 |         24 |             53.505 |                        62.381 |                          62.369 |                      4.511 |                  -8.876 |             50.567 |                        61.160 |                          61.499 |                      4.267 |                 -10.593 |              6.526 |                         6.726 |                           6.912 |                      0.666 |                  -0.201 |                           0.754 |                                      0.849 |                                        0.876 |                                   0.115 |                               -0.095 |

O benchmark é recalculado sob filtros progressivos de modalidade, categoria administrativa, organização acadêmica e porte. A estabilidade das diferenças é usada como diagnóstico de robustez, não como prova causal.

## Desempenho individual no mesmo arquivo temático

| VARIAVEL     |   N_VALIDO |   MEDIA |   MEDIANA |    DP |    P25 |    P75 |    MIN |    MAX |
|:-------------|-----------:|--------:|----------:|------:|-------:|-------:|-------:|-------:|
| NT_GER       |         49 |  53.505 |    51.240 | 7.812 | 47.080 | 59.740 | 33.920 | 70.640 |
| NT_OBJ       |         49 |  50.567 |    51.100 | 7.407 | 44.200 | 55.300 | 37.600 | 68.300 |
| NT_DIS       |         49 |   6.526 |     7.000 | 1.980 |  5.750 |  8.000 |  0.000 |  9.750 |
| QT_ACERTOS   |         49 |  33.469 |    34.000 | 8.603 | 26.000 | 39.000 | 19.000 | 54.000 |
| PROFICIENCIA |         49 |  -0.535 |    -0.500 | 0.463 | -0.933 | -0.238 | -1.344 |  0.572 |

| VARIAVEL_X   | VARIAVEL_Y   |   N |   SPEARMAN_RHO |   P_VALOR_EXPLORATORIO | OBSERVACAO                                                            |
|:-------------|:-------------|----:|---------------:|-----------------------:|:----------------------------------------------------------------------|
| NT_GER       | NT_OBJ       |  49 |         0.8598 |                 0.0000 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| NT_GER       | NT_DIS       |  49 |         0.6717 |                 0.0000 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| NT_GER       | QT_ACERTOS   |  49 |         0.8598 |                 0.0000 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| NT_GER       | PROFICIENCIA |  49 |         0.8598 |                 0.0000 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| NT_OBJ       | NT_DIS       |  49 |         0.2983 |                 0.0374 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| NT_OBJ       | QT_ACERTOS   |  49 |         1.0000 |                 0.0000 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| NT_OBJ       | PROFICIENCIA |  49 |         1.0000 |                 0.0000 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| NT_DIS       | QT_ACERTOS   |  49 |         0.2983 |                 0.0374 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| NT_DIS       | PROFICIENCIA |  49 |         0.2983 |                 0.0374 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |
| QT_ACERTOS   | PROFICIENCIA |  49 |         1.0000 |                 0.0000 | mesmo arquivo temático; relações com nota/acertos podem ser mecânicas |

As correlações individuais acima usam apenas variáveis do mesmo arquivo de desempenho. Relações entre nota, acertos e proficiência podem ser parcialmente mecânicas.

## Perfil diferencial

| RECORTE_FOCAL      | INDICADOR                 |   N_CURSOS |   MEDIA_CURSOS |   MEDIANA_CURSOS |   DP_CURSOS |
|:-------------------|:--------------------------|-----------:|---------------:|-----------------:|------------:|
| Soure              | sexo_feminino_pct         |          1 |          0.600 |            0.600 |     nan     |
| Soure              | idade_media               |          1 |         27.508 |           27.508 |     nan     |
| Soure              | mae_superior_pct          |          1 |          0.184 |            0.184 |     nan     |
| Soure              | pai_superior_pct          |          1 |          0.054 |            0.054 |     nan     |
| Soure              | renda_ate_3sm_pct         |          1 |          0.904 |            0.904 |     nan     |
| Soure              | trabalha_pct              |          1 |          0.365 |            0.365 |     nan     |
| Soure              | trabalha_40h_pct          |          1 |          0.058 |            0.058 |     nan     |
| Soure              | acao_afirmativa_pct       |          1 |          0.731 |            0.731 |     nan     |
| Soure              | auxilio_permanencia_pct   |          1 |          0.269 |            0.269 |     nan     |
| Soure              | bolsa_academica_pct       |          1 |          0.340 |            0.340 |     nan     |
| Soure              | estudo_4h_ou_mais_pct     |          1 |          0.385 |            0.385 |     nan     |
| Soure              | pretende_magisterio_pct   |          1 |          0.731 |            0.731 |     nan     |
| Soure              | turno_noturno_pct         |          1 |          0.000 |            0.000 |     nan     |
| Soure              | anos_desde_ingresso_media |          1 |          4.631 |            4.631 |     nan     |
| Soure              | qe_i68_media              |          1 |          8.635 |            8.635 |     nan     |
| Soure              | qe_i69_media              |          1 |          8.788 |            8.788 |     nan     |
| Soure              | qe_i70_interesse_pct      |          1 |          0.981 |            0.981 |     nan     |
| UFPA sem Soure     | sexo_feminino_pct         |          4 |          0.638 |            0.643 |       0.052 |
| UFPA sem Soure     | idade_media               |          4 |         28.467 |           27.475 |       2.906 |
| UFPA sem Soure     | mae_superior_pct          |          4 |          0.194 |            0.194 |       0.030 |
| UFPA sem Soure     | pai_superior_pct          |          4 |          0.116 |            0.123 |       0.038 |
| UFPA sem Soure     | renda_ate_3sm_pct         |          4 |          0.842 |            0.826 |       0.105 |
| UFPA sem Soure     | trabalha_pct              |          4 |          0.539 |            0.537 |       0.142 |
| UFPA sem Soure     | trabalha_40h_pct          |          4 |          0.161 |            0.162 |       0.112 |
| UFPA sem Soure     | acao_afirmativa_pct       |          4 |          0.682 |            0.688 |       0.080 |
| UFPA sem Soure     | auxilio_permanencia_pct   |          4 |          0.167 |            0.176 |       0.140 |
| UFPA sem Soure     | bolsa_academica_pct       |          4 |          0.528 |            0.657 |       0.345 |
| UFPA sem Soure     | estudo_4h_ou_mais_pct     |          4 |          0.549 |            0.530 |       0.100 |
| UFPA sem Soure     | pretende_magisterio_pct   |          4 |          0.767 |            0.755 |       0.064 |
| UFPA sem Soure     | turno_noturno_pct         |          4 |          0.136 |            0.000 |       0.272 |
| UFPA sem Soure     | anos_desde_ingresso_media |          4 |          4.654 |            4.707 |       0.234 |
| UFPA sem Soure     | qe_i68_media              |          4 |          8.780 |            8.692 |       0.428 |
| UFPA sem Soure     | qe_i69_media              |          4 |          9.077 |            9.047 |       0.274 |
| UFPA sem Soure     | qe_i70_interesse_pct      |          4 |          0.880 |            0.911 |       0.101 |
| Outras IES do Pará | sexo_feminino_pct         |         13 |          0.654 |            0.667 |       0.078 |
| Outras IES do Pará | idade_media               |         13 |         29.612 |           27.852 |       3.923 |
| Outras IES do Pará | mae_superior_pct          |         12 |          0.188 |            0.163 |       0.093 |
| Outras IES do Pará | pai_superior_pct          |         12 |          0.080 |            0.061 |       0.094 |
| Outras IES do Pará | renda_ate_3sm_pct         |         12 |          0.891 |            0.941 |       0.102 |
| Outras IES do Pará | trabalha_pct              |         12 |          0.585 |            0.525 |       0.199 |
| Outras IES do Pará | trabalha_40h_pct          |         12 |          0.203 |            0.158 |       0.126 |
| Outras IES do Pará | acao_afirmativa_pct       |         12 |          0.497 |            0.546 |       0.174 |
| Outras IES do Pará | auxilio_permanencia_pct   |         12 |          0.350 |            0.347 |       0.234 |
| Outras IES do Pará | bolsa_academica_pct       |         12 |          0.557 |            0.649 |       0.237 |
| Outras IES do Pará | estudo_4h_ou_mais_pct     |         12 |          0.638 |            0.597 |       0.147 |
| Outras IES do Pará | pretende_magisterio_pct   |         12 |          0.831 |            0.833 |       0.087 |
| Outras IES do Pará | turno_noturno_pct         |         13 |          0.310 |            0.040 |       0.419 |
| Outras IES do Pará | anos_desde_ingresso_media |         13 |          4.673 |            4.463 |       1.215 |
| Outras IES do Pará | qe_i68_media              |         12 |          8.829 |            8.764 |       0.457 |
| Outras IES do Pará | qe_i69_media              |         12 |          8.439 |            8.708 |       1.197 |
| Outras IES do Pará | qe_i70_interesse_pct      |         12 |          0.917 |            0.946 |       0.090 |
| Norte sem Pará     | sexo_feminino_pct         |         23 |          0.679 |            0.667 |       0.121 |
| Norte sem Pará     | idade_media               |         23 |         28.636 |           28.042 |       4.352 |
| Norte sem Pará     | mae_superior_pct          |         23 |          0.263 |            0.258 |       0.152 |
| Norte sem Pará     | pai_superior_pct          |         23 |          0.137 |            0.100 |       0.134 |
| Norte sem Pará     | renda_ate_3sm_pct         |         23 |          0.839 |            0.833 |       0.114 |
| Norte sem Pará     | trabalha_pct              |         23 |          0.557 |            0.500 |       0.214 |
| Norte sem Pará     | trabalha_40h_pct          |         23 |          0.219 |            0.176 |       0.187 |
| Norte sem Pará     | acao_afirmativa_pct       |         23 |          0.402 |            0.417 |       0.181 |
| Norte sem Pará     | auxilio_permanencia_pct   |         23 |          0.376 |            0.375 |       0.275 |
| Norte sem Pará     | bolsa_academica_pct       |         22 |          0.708 |            0.750 |       0.212 |
| Norte sem Pará     | estudo_4h_ou_mais_pct     |         23 |          0.526 |            0.529 |       0.170 |
| Norte sem Pará     | pretende_magisterio_pct   |         23 |          0.712 |            0.750 |       0.215 |
| Norte sem Pará     | turno_noturno_pct         |         23 |          0.481 |            0.405 |       0.424 |
| Norte sem Pará     | anos_desde_ingresso_media |         23 |          5.294 |            4.958 |       1.326 |
| Norte sem Pará     | qe_i68_media              |         23 |          8.820 |            8.806 |       0.554 |
| Norte sem Pará     | qe_i69_media              |         23 |          8.925 |            9.042 |       0.658 |
| Norte sem Pará     | qe_i70_interesse_pct      |         23 |          0.872 |            0.929 |       0.182 |
| Brasil sem Norte   | sexo_feminino_pct         |        387 |          0.689 |            0.685 |       0.160 |
| Brasil sem Norte   | idade_media               |        387 |         28.351 |           26.810 |       4.660 |
| Brasil sem Norte   | mae_superior_pct          |        368 |          0.234 |            0.202 |       0.176 |
| Brasil sem Norte   | pai_superior_pct          |        368 |          0.146 |            0.111 |       0.156 |
| Brasil sem Norte   | renda_ate_3sm_pct         |        368 |          0.749 |            0.800 |       0.211 |
| Brasil sem Norte   | trabalha_pct              |        368 |          0.665 |            0.692 |       0.227 |
| Brasil sem Norte   | trabalha_40h_pct          |        368 |          0.304 |            0.265 |       0.249 |
| Brasil sem Norte   | acao_afirmativa_pct       |        368 |          0.369 |            0.416 |       0.208 |
| Brasil sem Norte   | auxilio_permanencia_pct   |        368 |          0.300 |            0.253 |       0.273 |
| Brasil sem Norte   | bolsa_academica_pct       |        367 |          0.547 |            0.625 |       0.322 |
| Brasil sem Norte   | estudo_4h_ou_mais_pct     |        368 |          0.576 |            0.579 |       0.190 |
| Brasil sem Norte   | pretende_magisterio_pct   |        368 |          0.733 |            0.750 |       0.178 |
| Brasil sem Norte   | turno_noturno_pct         |        387 |          0.508 |            0.568 |       0.470 |
| Brasil sem Norte   | anos_desde_ingresso_media |        387 |          4.397 |            4.267 |       1.530 |
| Brasil sem Norte   | qe_i68_media              |        368 |          8.678 |            8.737 |       0.829 |
| Brasil sem Norte   | qe_i69_media              |        368 |          8.644 |            8.902 |       1.043 |
| Brasil sem Norte   | qe_i70_interesse_pct      |        368 |          0.879 |            0.917 |       0.131 |

## Processo formativo

| ITEM   | REFERENCIA           |   MEDIA_SOURE |   N_VALIDO_SOURE |   N_CURSOS_REFERENCIA |   MEDIA_REFERENCIA |   DP_REFERENCIA |   DIFERENCA_SOURE_REFERENCIA | ROTULO_OFICIAL   | STATUS_INTERPRETACAO                                   |
|:-------|:---------------------|--------------:|-----------------:|----------------------:|-------------------:|----------------:|-----------------------------:|:-----------------|:-------------------------------------------------------|
| QE_I20 | Benchmark comparável |         4.533 |               45 |                    56 |              5.052 |           0.240 |                       -0.518 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I21 | Benchmark comparável |         4.543 |               46 |                    56 |              4.912 |           0.292 |                       -0.368 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I41 | Benchmark comparável |         4.723 |               47 |                    56 |              5.007 |           0.297 |                       -0.283 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I31 | Benchmark comparável |         4.475 |               40 |                    56 |              4.601 |           0.349 |                       -0.126 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I32 | Benchmark comparável |         4.829 |               35 |                    56 |              4.906 |           0.337 |                       -0.077 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I47 | Benchmark comparável |         5.120 |               50 |                    56 |              5.165 |           0.223 |                       -0.045 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I64 | Benchmark comparável |         5.300 |               50 |                    56 |              5.338 |           0.188 |                       -0.038 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I34 | Benchmark comparável |         4.979 |               47 |                    56 |              5.004 |           0.336 |                       -0.026 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I22 | Benchmark comparável |         5.216 |               51 |                    56 |              5.225 |           0.258 |                       -0.009 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I48 | Benchmark comparável |         5.280 |               50 |                    56 |              5.283 |           0.205 |                       -0.003 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I46 | Benchmark comparável |         5.265 |               49 |                    56 |              5.259 |           0.230 |                        0.006 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I43 | Benchmark comparável |         4.792 |               24 |                    56 |              4.757 |           0.584 |                        0.035 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I37 | Benchmark comparável |         5.412 |               51 |                    56 |              5.352 |           0.169 |                        0.060 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I61 | Benchmark comparável |         5.102 |               49 |                    56 |              5.038 |           0.275 |                        0.064 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I33 | Benchmark comparável |         4.222 |               45 |                    56 |              4.154 |           0.409 |                        0.068 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I60 | Benchmark comparável |         5.340 |               50 |                    56 |              5.263 |           0.202 |                        0.077 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I44 | Benchmark comparável |         5.000 |               20 |                    56 |              4.918 |           0.455 |                        0.082 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I45 | Benchmark comparável |         4.592 |               49 |                    56 |              4.502 |           0.462 |                        0.090 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I39 | Benchmark comparável |         4.822 |               45 |                    56 |              4.698 |           0.471 |                        0.125 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I36 | Benchmark comparável |         5.260 |               50 |                    56 |              5.131 |           0.221 |                        0.129 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I27 | Benchmark comparável |         5.404 |               52 |                    56 |              5.240 |           0.187 |                        0.164 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I65 | Benchmark comparável |         5.392 |               51 |                    56 |              5.219 |           0.225 |                        0.173 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I54 | Benchmark comparável |         4.958 |               48 |                    56 |              4.779 |           0.323 |                        0.179 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I42 | Benchmark comparável |         4.714 |               49 |                    56 |              4.529 |           0.565 |                        0.185 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I38 | Benchmark comparável |         5.320 |               50 |                    56 |              5.126 |           0.254 |                        0.194 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I50 | Benchmark comparável |         5.420 |               50 |                    56 |              5.201 |           0.244 |                        0.219 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I49 | Benchmark comparável |         5.160 |               50 |                    56 |              4.935 |           0.324 |                        0.225 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I35 | Benchmark comparável |         5.100 |               50 |                    56 |              4.859 |           0.306 |                        0.241 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I51 | Benchmark comparável |         5.235 |               51 |                    56 |              4.977 |           0.299 |                        0.258 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I63 | Benchmark comparável |         5.360 |               50 |                    56 |              5.091 |           0.250 |                        0.269 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I59 | Benchmark comparável |         5.286 |               49 |                    56 |              4.995 |           0.255 |                        0.290 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I25 | Benchmark comparável |         5.412 |               51 |                    56 |              5.085 |           0.250 |                        0.326 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I26 | Benchmark comparável |         5.240 |               50 |                    56 |              4.898 |           0.275 |                        0.342 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I58 | Benchmark comparável |         5.306 |               49 |                    56 |              4.957 |           0.290 |                        0.349 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I24 | Benchmark comparável |         5.180 |               50 |                    56 |              4.831 |           0.391 |                        0.349 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I66 | Benchmark comparável |         5.306 |               49 |                    56 |              4.944 |           0.266 |                        0.362 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I56 | Benchmark comparável |         5.300 |               50 |                    56 |              4.924 |           0.310 |                        0.376 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I53 | Benchmark comparável |         5.184 |               49 |                    56 |              4.804 |           0.269 |                        0.379 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I40 | Benchmark comparável |         5.217 |               46 |                    56 |              4.829 |           0.292 |                        0.388 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I29 | Benchmark comparável |         4.863 |               51 |                    56 |              4.414 |           0.423 |                        0.449 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I28 | Benchmark comparável |         5.596 |               52 |                    56 |              5.146 |           0.301 |                        0.451 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I30 | Benchmark comparável |         5.269 |               52 |                    56 |              4.786 |           0.366 |                        0.483 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I62 | Benchmark comparável |         5.220 |               50 |                    56 |              4.716 |           0.335 |                        0.504 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I55 | Benchmark comparável |         5.061 |               49 |                    56 |              4.548 |           0.486 |                        0.514 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I23 | Benchmark comparável |         5.098 |               51 |                    56 |              4.563 |           0.353 |                        0.535 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I57 | Benchmark comparável |         5.120 |               50 |                    56 |              4.417 |           0.460 |                        0.703 | <NA>             | interpretar apenas após vincular texto oficial do item |
| QE_I52 | Benchmark comparável |         5.078 |               51 |                    56 |              4.338 |           0.539 |                        0.741 | <NA>             | interpretar apenas após vincular texto oficial do item |

Os códigos QE_I20–QE_I66 permanecem sem interpretação substantiva automática. Antes do relatório final, cada código deverá ser vinculado ao texto oficial do item, com conferência da direção da escala e de possíveis itens invertidos.

## Associações ecológicas

| INDICADOR_X               | INDICADOR_Y   |   N_CURSOS |   SPEARMAN_RHO |   P_VALOR_EXPLORATORIO | NIVEL_ANALISE     |
|:--------------------------|:--------------|-----------:|---------------:|-----------------------:|:------------------|
| renda_ate_3sm_pct         | nt_ger_mean   |        404 |        -0.3403 |                 0.0000 | curso (ecológico) |
| trabalha_pct              | nt_ger_mean   |        404 |        -0.2332 |                 0.0000 | curso (ecológico) |
| acao_afirmativa_pct       | nt_ger_mean   |        404 |         0.2693 |                 0.0000 | curso (ecológico) |
| auxilio_permanencia_pct   | nt_ger_mean   |        404 |         0.1570 |                 0.0015 | curso (ecológico) |
| bolsa_academica_pct       | nt_ger_mean   |        402 |         0.4028 |                 0.0000 | curso (ecológico) |
| estudo_4h_ou_mais_pct     | nt_ger_mean   |        404 |         0.4202 |                 0.0000 | curso (ecológico) |
| turno_noturno_pct         | nt_ger_mean   |        404 |        -0.1192 |                 0.0166 | curso (ecológico) |
| anos_desde_ingresso_media | nt_ger_mean   |        404 |         0.1468 |                 0.0031 | curso (ecológico) |
| qe_i68_media              | nt_ger_mean   |        404 |        -0.1631 |                 0.0010 | curso (ecológico) |
| qe_i69_media              | nt_ger_mean   |        404 |         0.0492 |                 0.3243 | curso (ecológico) |

Essas associações são calculadas entre indicadores agregados por curso e não representam relações individuais.

## Síntese preliminar a validar no relatório final

A análise de sensibilidade permite verificar se a distância observada para Soure em NT_GER e, especialmente, NT_OBJ permanece quando a referência é restringida a cursos estruturalmente semelhantes. NT_DIS deve ser interpretada separadamente, pois pode apresentar padrão distinto. Nenhuma dessas diferenças é interpretada como efeito causal.

### Cenário estrutural principal

| CENARIO                 |   CO_CURSO_ALVO |   N_CURSOS |   nt_ger_mean_ALVO |   nt_ger_mean_MEDIA_BENCHMARK |   nt_ger_mean_MEDIANA_BENCHMARK |   nt_ger_mean_DP_BENCHMARK |   nt_ger_mean_DIFERENCA |   nt_obj_mean_ALVO |   nt_obj_mean_MEDIA_BENCHMARK |   nt_obj_mean_MEDIANA_BENCHMARK |   nt_obj_mean_DP_BENCHMARK |   nt_obj_mean_DIFERENCA |   nt_dis_mean_ALVO |   nt_dis_mean_MEDIA_BENCHMARK |   nt_dis_mean_MEDIANA_BENCHMARK |   nt_dis_mean_DP_BENCHMARK |   nt_dis_mean_DIFERENCA |   taxa_presenca_microdados_ALVO |   taxa_presenca_microdados_MEDIA_BENCHMARK |   taxa_presenca_microdados_MEDIANA_BENCHMARK |   taxa_presenca_microdados_DP_BENCHMARK |   taxa_presenca_microdados_DIFERENCA |
|:------------------------|----------------:|-----------:|-------------------:|------------------------------:|--------------------------------:|---------------------------:|------------------------:|-------------------:|------------------------------:|--------------------------------:|---------------------------:|------------------------:|-------------------:|------------------------------:|--------------------------------:|---------------------------:|------------------------:|--------------------------------:|-------------------------------------------:|---------------------------------------------:|----------------------------------------:|-------------------------------------:|
| estrutura_porte_0_5_2_0 |          104640 |         56 |             53.505 |                        62.137 |                          62.567 |                      4.582 |                  -8.632 |             50.567 |                        60.907 |                          61.066 |                      4.390 |                 -10.339 |              6.526 |                         6.706 |                           6.898 |                      0.657 |                  -0.180 |                           0.754 |                                      0.855 |                                        0.873 |                                   0.097 |                               -0.101 |