# Sprint 16 — Base analítica de Letras–Português

## Síntese

A base analítica reúne **340 cursos** de Letras–Português. Foram localizadas **8 ofertas da UFPA**, das quais **1** possui Conceito Enade 1.

A oferta inicialmente informada de **Soure** não foi localizada nem no cadastro `microdados2025_arq1.txt` da área 904 nem na planilha oficial de Conceito Enade 2025. Ela é preservada na auditoria da relação informada, mas não recebe CO_CURSO artificial, não é tratada como Conceito 1 e fica fora dos grupos comparativos.

A unidade de análise é `CO_CURSO`. Cada arquivo temático é agregado separadamente antes das junções one-to-one.

## Ofertas localizadas da UFPA

|   CO_CURSO | ROTULO_OFERTA           |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   nt_ger_count |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |   nt_ger_percentil_brasil |
|-----------:|:------------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------:|--------------:|--------------:|--------------:|--------------------------:|
|     114850 | Abaetetuba — Presencial |                    3 |              95 |                  82 |                       0.863 |             82 |        56.532 |        53.218 |         6.979 |                    47.335 |
|     114876 | Altamira — Presencial   |                    2 |              57 |                  47 |                       0.825 |             47 |        49.951 |        46.747 |         6.277 |                    24.138 |
|     115161 | Belém — EaD             |                    1 |              67 |                  56 |                       0.836 |             56 |        44.651 |        41.952 |         5.545 |                    12.226 |
|      27645 | Belém — Presencial      |                    4 |             182 |                 150 |                       0.824 |            150 |        66.941 |        65.459 |         7.287 |                    78.997 |
|     114874 | Bragança — Presencial   |                    3 |              51 |                  49 |                       0.961 |             49 |        59.288 |        56.559 |         7.020 |                    55.486 |
|     115013 | Breves — Presencial     |                    3 |              34 |                  25 |                       0.735 |             25 |        54.033 |        50.916 |         6.650 |                    42.006 |
|     114846 | Cametá — Presencial     |                    3 |              87 |                  69 |                       0.793 |             69 |        52.850 |        48.481 |         7.033 |                    37.304 |
|     114857 | Castanhal — Presencial  |                    3 |              44 |                  38 |                       0.864 |             38 |        61.106 |        59.968 |         6.566 |                    61.442 |

## Auditoria da relação inicialmente informada

|   CO_GRUPO | MUNICIPIO_INFORMADO   | MODALIDADE_INFORMADA   | CONCEITO_INFORMADO   | MUNICIPIO_CHAVE   | MODALIDADE_CHAVE   | CO_CURSO   | MUNICIPIO   | MODALIDADE   | CONCEITO_ENADE   | SITUACAO_CONCEITO     | AREA             | STATUS_VALIDACAO          | CONCEITO_ENCONTRADO_NORMALIZADO   | CONCEITO_INFORMADO_NORMALIZADO   | CORRECAO_RECOMENDADA                                                                                                                                                                                      | FONTE_VALIDACAO                                                                                         |
|-----------:|:----------------------|:-----------------------|:---------------------|:------------------|:-------------------|:-----------|:------------|:-------------|:-----------------|:----------------------|:-----------------|:--------------------------|:----------------------------------|:---------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|
|        904 | Abaetetuba            | Presencial             | 3                    | ABAETETUBA        | PRESENCIAL         | 114850     | Abaetetuba  | Presencial   | 3                | Conceito superior a 1 | Letras-Português | Validado                  | 3                                 | 3                                | Nenhuma                                                                                                                                                                                                   | microdados2025_arq1.txt + conceito_enade_licenciaturas.xlsx                                             |
|        904 | Altamira              | Presencial             | 2                    | ALTAMIRA          | PRESENCIAL         | 114876     | Altamira    | Presencial   | 2                | Conceito superior a 1 | Letras-Português | Validado                  | 2                                 | 2                                | Nenhuma                                                                                                                                                                                                   | microdados2025_arq1.txt + conceito_enade_licenciaturas.xlsx                                             |
|        904 | Belém                 | EaD                    | 1                    | BELEM             | EAD                | 115161     | Belém       | EaD          | 1                | Conceito 1            | Letras-Português | Validado                  | 1                                 | 1                                | Nenhuma                                                                                                                                                                                                   | microdados2025_arq1.txt + conceito_enade_licenciaturas.xlsx                                             |
|        904 | Belém                 | Presencial             | 4                    | BELEM             | PRESENCIAL         | 27645      | Belém       | Presencial   | 4                | Conceito superior a 1 | Letras-Português | Validado                  | 4                                 | 4                                | Nenhuma                                                                                                                                                                                                   | microdados2025_arq1.txt + conceito_enade_licenciaturas.xlsx                                             |
|        904 | Bragança              | Presencial             | 3                    | BRAGANCA          | PRESENCIAL         | 114874     | Bragança    | Presencial   | 3                | Conceito superior a 1 | Letras-Português | Validado                  | 3                                 | 3                                | Nenhuma                                                                                                                                                                                                   | microdados2025_arq1.txt + conceito_enade_licenciaturas.xlsx                                             |
|        904 | Breves                | Presencial             | 3                    | BREVES            | PRESENCIAL         | 115013     | Breves      | Presencial   | 3                | Conceito superior a 1 | Letras-Português | Validado                  | 3                                 | 3                                | Nenhuma                                                                                                                                                                                                   | microdados2025_arq1.txt + conceito_enade_licenciaturas.xlsx                                             |
|        904 | Cametá                | Presencial             | 3                    | CAMETA            | PRESENCIAL         | 114846     | Cametá      | Presencial   | 3                | Conceito superior a 1 | Letras-Português | Validado                  | 3                                 | 3                                | Nenhuma                                                                                                                                                                                                   | microdados2025_arq1.txt + conceito_enade_licenciaturas.xlsx                                             |
|        904 | Castanhal             | Presencial             | 3                    | CASTANHAL         | PRESENCIAL         | 114857     | Castanhal   | Presencial   | 3                | Conceito superior a 1 | Letras-Português | Validado                  | 3                                 | 3                                | Nenhuma                                                                                                                                                                                                   | microdados2025_arq1.txt + conceito_enade_licenciaturas.xlsx                                             |
|        904 | Soure                 | Presencial             | sem conceito         | SOURE             | PRESENCIAL         | <NA>       | <NA>        | <NA>         | <NA>             | nan                   | Letras-Português | Não localizado nas fontes | SEM CONCEITO                      | SEM CONCEITO                     | Registrar a oferta informada de Soure como não localizada nas duas fontes de 2025; não atribuir CO_CURSO, inscritos, participantes, desempenho ou Conceito Enade e não incluí-la nos grupos comparativos. | não localizado no cadastro do microdados2025_arq1.txt nem na planilha conceito_enade_licenciaturas.xlsx |

## Comparações regionais e nacionais

| RECORTE                        | INDICADOR   |   N_CURSOS |   N_PARTICIPANTES |   MEDIA_CURSOS |   MEDIA_PONDERADA_PARTICIPANTES |   MEDIANA_CURSOS | DP_CURSOS          |    P25 |    P75 |
|:-------------------------------|:------------|-----------:|------------------:|---------------:|--------------------------------:|-----------------:|:-------------------|-------:|-------:|
| UFPA — Belém — EaD             | nt_ger_mean |          1 |            56.000 |         44.651 |                          44.651 |           44.651 | <NA>               | 44.651 | 44.651 |
| UFPA — Breves — Presencial     | nt_ger_mean |          1 |            25.000 |         54.033 |                          54.033 |           54.033 | <NA>               | 54.033 | 54.033 |
| UFPA — Altamira — Presencial   | nt_ger_mean |          1 |            47.000 |         49.951 |                          49.951 |           49.951 | <NA>               | 49.951 | 49.951 |
| UFPA — Bragança — Presencial   | nt_ger_mean |          1 |            49.000 |         59.288 |                          59.288 |           59.288 | <NA>               | 59.288 | 59.288 |
| UFPA — Castanhal — Presencial  | nt_ger_mean |          1 |            38.000 |         61.106 |                          61.106 |           61.106 | <NA>               | 61.106 | 61.106 |
| UFPA — Abaetetuba — Presencial | nt_ger_mean |          1 |            82.000 |         56.532 |                          56.532 |           56.532 | <NA>               | 56.532 | 56.532 |
| UFPA — Cametá — Presencial     | nt_ger_mean |          1 |            69.000 |         52.850 |                          52.850 |           52.850 | <NA>               | 52.850 | 52.850 |
| UFPA — Belém — Presencial      | nt_ger_mean |          1 |           150.000 |         66.941 |                          66.941 |           66.941 | <NA>               | 66.941 | 66.941 |
| UFPA agregada                  | nt_ger_mean |          8 |           516.000 |         55.669 |                          57.654 |           55.282 | 6.919808840798312  | 52.125 | 59.743 |
| Região Norte sem UFPA          | nt_ger_mean |         28 |           773.000 |         54.556 |                          55.194 |           53.506 | 9.49612727523599   | 50.244 | 59.446 |
| Região Norte completa          | nt_ger_mean |         36 |          1289.000 |         54.803 |                          56.179 |           53.815 | 8.908511397546235  | 50.399 | 59.678 |
| Nordeste                       | nt_ger_mean |        121 |          3646.000 |         55.946 |                          58.205 |           55.157 | 9.444274651556412  | 48.987 | 62.147 |
| Sudeste                        | nt_ger_mean |         77 |          2437.000 |         59.856 |                          63.047 |           61.745 | 12.408778081750143 | 50.250 | 69.134 |
| Sul                            | nt_ger_mean |         54 |          3040.000 |         60.875 |                          53.931 |           59.757 | 11.450170076893945 | 53.867 | 69.819 |
| Centro-Oeste                   | nt_ger_mean |         31 |           569.000 |         56.402 |                          58.226 |           53.949 | 10.643663872055841 | 50.275 | 63.606 |
| Brasil geral                   | nt_ger_mean |        319 |         10981.000 |         57.639 |                          57.860 |           57.187 | 10.809668761391247 | 50.085 | 64.830 |
| Brasil sem UFPA                | nt_ger_mean |        311 |         10465.000 |         57.690 |                          57.870 |           57.347 | 10.894051915247479 | 50.085 | 64.883 |
| Restante do Brasil sem Norte   | nt_ger_mean |        283 |          9692.000 |         58.000 |                          58.083 |           57.980 | 10.98902171519904  | 50.085 | 64.995 |

As médias ponderadas usam participantes válidos em NT_GER; as médias simples tratam cada curso com o mesmo peso.

## Benchmark comparável da oferta UFPA Conceito 1

|   CO_CURSO_ALVO | ROTULO_ALVO   | modalidade   |   participantes_alvo |   n_cursos_comparaveis | criterio                                                                                                 |
|----------------:|:--------------|:-------------|---------------------:|-----------------------:|:---------------------------------------------------------------------------------------------------------|
|          115161 | Belém — EaD   | EaD          |                   56 |                      4 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |

## Contraste UFPA Conceito 1 versus conceitos superiores

| INDICADOR                |   N_CURSOS_A |   MEDIA_A |   N_CURSOS_B |   MEDIA_B |   DIFERENCA_A_MENOS_B |   Z_DESCRITIVO_VS_B |
|:-------------------------|-------------:|----------:|-------------:|----------:|----------------------:|--------------------:|
| nt_ger_mean              |            1 |    44.651 |            7 |    57.243 |               -12.592 |              -2.201 |
| nt_obj_mean              |            1 |    41.952 |            7 |    54.478 |               -12.527 |              -1.885 |
| nt_dis_mean              |            1 |     5.545 |            7 |     6.830 |                -1.285 |              -3.720 |
| taxa_presenca_microdados |            1 |     0.836 |            7 |     0.838 |                -0.002 |              -0.029 |
| renda_ate_3sm_pct        |            1 |     0.817 |            7 |     0.863 |                -0.046 |              -0.483 |
| trabalha_pct             |            1 |     0.700 |            7 |     0.477 |                 0.223 |               1.550 |
| acao_afirmativa_pct      |            1 |     0.533 |            7 |     0.767 |                -0.234 |              -2.341 |
| auxilio_permanencia_pct  |            1 |     0.000 |            7 |     0.277 |                -0.277 |              -2.058 |
| qe_i68_media             |            1 |     8.883 |            7 |     8.702 |                 0.181 |               0.332 |
| qe_i69_media             |            1 |     9.050 |            7 |     9.061 |                -0.011 |              -0.021 |

## Limitações

- não há identificação comum de estudante entre arquivos temáticos;
- associações entre temas diferentes somente podem ser ecológicas;
- Soure não foi localizada nas duas fontes de 2025 e não recebe valores artificiais;
- o Grupo A contém uma única oferta da UFPA, o que restringe inferência entre cursos;
- benchmarks são descritivos e não constituem desenho causal;
- QE_I20–QE_I66 não são condensados em índice único nesta sprint.