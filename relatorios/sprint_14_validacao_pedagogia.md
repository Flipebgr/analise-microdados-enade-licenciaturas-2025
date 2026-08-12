# Sprint 14 — Validação analítica de Pedagogia

## Escopo

A validação mantém `CO_CURSO` como unidade principal. Não há oferta da UFPA com Conceito Enade 1 em Pedagogia. O contraste interno é Castanhal, Conceito 5, versus as seis ofertas UFPA Conceito 4, sem interpretar Conceito 4 como insuficiência.

As relações entre temas distintos são exclusivamente ecológicas no nível do curso. Não foram reconstruídos estudantes nem feitas junções individuais entre arquivos temáticos.

## Ofertas UFPA auditadas

|   CO_CURSO | ROTULO_OFERTA           |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   TAXA_PARTICIPACAO_OFICIAL |   taxa_presenca_microdados |   nt_ger_mean |   nt_obj_mean |   nt_dis_mean |
|-----------:|:------------------------|---------------------:|----------------:|--------------------:|----------------------------:|---------------------------:|--------------:|--------------:|--------------:|
|      38276 | Abaetetuba — Presencial |                4.000 |             124 |             111.000 |                       0.895 |                      0.895 |        62.334 |        60.682 |         6.894 |
|      12048 | Altamira — Presencial   |                4.000 |              56 |              51.000 |                       0.911 |                      0.911 |        59.968 |        59.090 |         6.348 |
|      11996 | Belém — Presencial      |                4.000 |             341 |             280.000 |                       0.821 |                      0.821 |        65.261 |        64.197 |         6.952 |
|      12061 | Bragança — Presencial   |                4.000 |              83 |              75.000 |                       0.904 |                      0.904 |        64.559 |        64.373 |         6.530 |
|      12111 | Breves — Presencial     |                4.000 |              51 |              42.000 |                       0.824 |                      0.824 |        65.890 |        65.026 |         6.935 |
|      12069 | Cametá — Presencial     |                4.000 |             148 |             122.000 |                       0.824 |                      0.824 |        62.485 |        61.180 |         6.770 |
|      12085 | Castanhal — Presencial  |                5.000 |              86 |              63.000 |                       0.733 |                      0.733 |        65.463 |        64.438 |         6.956 |

## Auditoria de N e participação

|   CO_CURSO | ROTULO_OFERTA           | GRUPO_CODIGO   |   PARTICIPANTES_NUM |   registros_microdados |   presentes_validos |   nt_ger_count |   nt_obj_count |   nt_dis_count |   reaplicacoes |   diferenca_participantes_oficial_nt_ger | alerta_n_superior_registros   | alerta_diferenca_participantes   |
|-----------:|:------------------------|:---------------|--------------------:|-----------------------:|--------------------:|---------------:|---------------:|---------------:|---------------:|-----------------------------------------:|:------------------------------|:---------------------------------|
|      11996 | Belém — Presencial      | B              |             280.000 |                    341 |                 280 |            280 |            280 |            280 |              0 |                                    0.000 | False                         | False                            |
|      12048 | Altamira — Presencial   | B              |              51.000 |                     56 |                  51 |             51 |             51 |             51 |              0 |                                    0.000 | False                         | False                            |
|      12061 | Bragança — Presencial   | B              |              75.000 |                     83 |                  75 |             75 |             75 |             75 |              0 |                                    0.000 | False                         | False                            |
|      12069 | Cametá — Presencial     | B              |             122.000 |                    148 |                 122 |            122 |            122 |            122 |              0 |                                    0.000 | False                         | False                            |
|      12085 | Castanhal — Presencial  | B              |              63.000 |                     86 |                  63 |             63 |             63 |             63 |              0 |                                    0.000 | False                         | False                            |
|      12111 | Breves — Presencial     | B              |              42.000 |                     51 |                  42 |             42 |             42 |             42 |              0 |                                    0.000 | False                         | False                            |
|      38276 | Abaetetuba — Presencial | B              |             111.000 |                    124 |                 111 |            111 |            111 |            111 |              0 |                                    0.000 | False                         | False                            |

## Contraste interno UFPA

| INDICADOR                |   CASTANHAL |   N_UFPA_CONCEITO_4 |   MEDIA_UFPA_CONCEITO_4 |   MEDIANA_UFPA_CONCEITO_4 |   DP_UFPA_CONCEITO_4 |   DIFERENCA |   Z_DESCRITIVO | INTERPRETACAO                                 |
|:-------------------------|------------:|--------------------:|------------------------:|--------------------------:|---------------------:|------------:|---------------:|:----------------------------------------------|
| nt_ger_mean              |      65.463 |                   6 |                  63.416 |                    63.522 |                2.225 |       2.047 |          0.920 | contraste descritivo entre cursos; não causal |
| nt_obj_mean              |      64.438 |                   6 |                  62.425 |                    62.689 |                2.425 |       2.013 |          0.830 | contraste descritivo entre cursos; não causal |
| nt_dis_mean              |       6.956 |                   6 |                   6.738 |                     6.832 |                0.247 |       0.218 |          0.883 | contraste descritivo entre cursos; não causal |
| taxa_presenca_microdados |       0.733 |                   6 |                   0.863 |                     0.860 |                0.044 |      -0.131 |         -2.953 | contraste descritivo entre cursos; não causal |
| renda_ate_3sm_pct        |       0.923 |                   6 |                   0.906 |                     0.904 |                0.039 |       0.017 |          0.431 | contraste descritivo entre cursos; não causal |
| trabalha_pct             |       0.754 |                   6 |                   0.537 |                     0.560 |                0.167 |       0.217 |          1.297 | contraste descritivo entre cursos; não causal |
| acao_afirmativa_pct      |       0.785 |                   6 |                   0.822 |                     0.821 |                0.076 |      -0.037 |         -0.493 | contraste descritivo entre cursos; não causal |
| auxilio_permanencia_pct  |       0.154 |                   6 |                   0.273 |                     0.239 |                0.105 |      -0.119 |         -1.129 | contraste descritivo entre cursos; não causal |
| bolsa_academica_pct      |       0.127 |                   6 |                   0.315 |                     0.333 |                0.077 |      -0.188 |         -2.430 | contraste descritivo entre cursos; não causal |
| estudo_4h_ou_mais_pct    |       0.508 |                   6 |                   0.563 |                     0.549 |                0.143 |      -0.055 |         -0.384 | contraste descritivo entre cursos; não causal |
| qe_i68_media             |       9.554 |                   6 |                   9.286 |                     9.275 |                0.212 |       0.268 |          1.267 | contraste descritivo entre cursos; não causal |
| qe_i69_media             |       9.600 |                   6 |                   9.365 |                     9.420 |                0.274 |       0.235 |          0.858 | contraste descritivo entre cursos; não causal |

A diferença Castanhal menos média das ofertas Conceito 4 é apresentada como contraste descritivo entre cursos. O grupo Conceito 5 possui apenas uma oferta, portanto não é tratado como população independente para inferência estatística.

## Sensibilidade dos benchmarks

|   CO_CURSO_ALVO | ROTULO_ALVO             |   CONCEITO_ALVO |   N_CURSOS |   nt_ger_mean_ALVO |   nt_ger_mean_MEDIA_BENCHMARK |   nt_ger_mean_DIFERENCA |   nt_ger_mean_Z |   nt_obj_mean_DIFERENCA |   nt_dis_mean_DIFERENCA |
|----------------:|:------------------------|----------------:|-----------:|-------------------:|------------------------------:|------------------------:|----------------:|------------------------:|------------------------:|
|           11996 | Belém — Presencial      |           4.000 |          6 |             65.261 |                        75.027 |                  -9.766 |          -2.387 |                 -11.830 |                  -0.151 |
|           12048 | Altamira — Presencial   |           4.000 |         82 |             59.968 |                        65.424 |                  -5.455 |          -0.631 |                  -6.681 |                  -0.055 |
|           12061 | Bragança — Presencial   |           4.000 |         57 |             64.559 |                        67.659 |                  -3.100 |          -0.327 |                  -3.852 |                  -0.009 |
|           12069 | Cametá — Presencial     |           4.000 |         36 |             62.485 |                        72.410 |                  -9.925 |          -1.392 |                 -11.875 |                  -0.212 |
|           12085 | Castanhal — Presencial  |           5.000 |         70 |             65.463 |                        66.885 |                  -1.422 |          -0.159 |                  -2.894 |                   0.446 |
|           12111 | Breves — Presencial     |           4.000 |         78 |             65.890 |                        64.845 |                   1.045 |           0.123 |                  -0.111 |                   0.567 |
|           38276 | Abaetetuba — Presencial |           4.000 |         40 |             62.334 |                        71.870 |                  -9.536 |          -1.269 |                 -11.850 |                  -0.028 |

Foram avaliados cinco cenários por oferta: modalidade; modalidade e categoria; modalidade, categoria e organização; estrutura com porte 0,5x–2x; e estrutura com porte 0,75x–1,5x. O benchmark reduz heterogeneidade observável, mas não é um desenho causal.

## Processo formativo

QE_I20–QE_I66 são mantidos item a item. Nesta sprint, a comparação identifica os códigos com maiores diferenças entre Castanhal e as ofertas UFPA Conceito 4. A interpretação substantiva exige vinculação ao texto oficial do item; não foi criado índice único.

| ITEM   | REFERENCIA        |   MEDIA_CASTANHAL |   N_VALIDO_CASTANHAL |   N_CURSOS_REFERENCIA |   MEDIA_REFERENCIA |   DP_REFERENCIA |   DIFERENCA_CASTANHAL_REFERENCIA | STATUS_INTERPRETACAO                                             |
|:-------|:------------------|------------------:|---------------------:|----------------------:|-------------------:|----------------:|---------------------------------:|:-----------------------------------------------------------------|
| QE_I34 | UFPA — Conceito 4 |             4.206 |                   63 |                     6 |              4.877 |           0.394 |                           -0.670 | interpretar substantivamente somente com o texto oficial do item |
| QE_I29 | UFPA — Conceito 4 |             4.281 |                   64 |                     6 |              4.920 |           0.312 |                           -0.639 | interpretar substantivamente somente com o texto oficial do item |
| QE_I20 | UFPA — Conceito 4 |             4.271 |                   59 |                     6 |              4.721 |           0.443 |                           -0.449 | interpretar substantivamente somente com o texto oficial do item |
| QE_I39 | UFPA — Conceito 4 |             4.783 |                   60 |                     6 |              5.110 |           0.213 |                           -0.327 | interpretar substantivamente somente com o texto oficial do item |
| QE_I26 | UFPA — Conceito 4 |             5.092 |                   65 |                     6 |              5.418 |           0.169 |                           -0.326 | interpretar substantivamente somente com o texto oficial do item |
| QE_I49 | UFPA — Conceito 4 |             5.048 |                   63 |                     6 |              5.348 |           0.163 |                           -0.300 | interpretar substantivamente somente com o texto oficial do item |
| QE_I45 | UFPA — Conceito 4 |             4.547 |                   64 |                     6 |              4.844 |           0.330 |                           -0.297 | interpretar substantivamente somente com o texto oficial do item |
| QE_I35 | UFPA — Conceito 4 |             4.984 |                   64 |                     6 |              5.271 |           0.290 |                           -0.287 | interpretar substantivamente somente com o texto oficial do item |
| QE_I43 | UFPA — Conceito 4 |             4.556 |                   18 |                     6 |              4.836 |           0.493 |                           -0.281 | interpretar substantivamente somente com o texto oficial do item |
| QE_I23 | UFPA — Conceito 4 |             4.906 |                   64 |                     6 |              5.177 |           0.300 |                           -0.271 | interpretar substantivamente somente com o texto oficial do item |
| QE_I28 | UFPA — Conceito 4 |             5.369 |                   65 |                     6 |              5.631 |           0.096 |                           -0.262 | interpretar substantivamente somente com o texto oficial do item |
| QE_I42 | UFPA — Conceito 4 |             4.281 |                   64 |                     6 |              4.524 |           0.491 |                           -0.243 | interpretar substantivamente somente com o texto oficial do item |

## Associações ecológicas

| INDICADOR_X               | INDICADOR_Y   |   N_CURSOS |   SPEARMAN_RHO |   P_VALOR_EXPLORATORIO | NIVEL_ANALISE     | RESSALVA                                             |
|:--------------------------|:--------------|-----------:|---------------:|-----------------------:|:------------------|:-----------------------------------------------------|
| bolsa_academica_pct       | nt_ger_mean   |       1129 |          0.432 |                  0.000 | curso (ecológico) | não interpretar como associação individual ou causal |
| acao_afirmativa_pct       | nt_ger_mean   |       1129 |          0.345 |                  0.000 | curso (ecológico) | não interpretar como associação individual ou causal |
| renda_ate_3sm_pct         | nt_ger_mean   |       1129 |         -0.321 |                  0.000 | curso (ecológico) | não interpretar como associação individual ou causal |
| auxilio_permanencia_pct   | nt_ger_mean   |       1129 |          0.241 |                  0.000 | curso (ecológico) | não interpretar como associação individual ou causal |
| qe_i69_media              | nt_ger_mean   |       1129 |          0.229 |                  0.000 | curso (ecológico) | não interpretar como associação individual ou causal |
| estudo_4h_ou_mais_pct     | nt_ger_mean   |       1129 |          0.224 |                  0.000 | curso (ecológico) | não interpretar como associação individual ou causal |
| anos_desde_ingresso_media | nt_ger_mean   |       1129 |          0.215 |                  0.000 | curso (ecológico) | não interpretar como associação individual ou causal |
| qe_i68_media              | nt_ger_mean   |       1129 |          0.053 |                  0.073 | curso (ecológico) | não interpretar como associação individual ou causal |
| turno_noturno_pct         | nt_ger_mean   |       1129 |         -0.032 |                  0.279 | curso (ecológico) | não interpretar como associação individual ou causal |
| trabalha_pct              | nt_ger_mean   |       1129 |          0.015 |                  0.618 | curso (ecológico) | não interpretar como associação individual ou causal |

As correlações de Spearman acima usam cursos, não estudantes. Não representam associações individuais e não sustentam causalidade.

## Outliers

|   CO_CURSO | ROTULO_OFERTA               | RECORTE_PEDAGOGIA   | INDICADOR   |   VALOR |     Q1 |     Q3 |   LIMITE_INFERIOR |   LIMITE_SUPERIOR | OUTLIER_IQR   |
|-----------:|:----------------------------|:--------------------|:------------|--------:|-------:|-------:|------------------:|------------------:|:--------------|
|       2898 | São Paulo — Presencial      | Brasil sem Norte    | nt_ger_mean |  88.227 | 51.642 | 64.474 |            32.393 |            83.723 | True          |
|      94363 | Paracatu — EaD              | Brasil sem Norte    | nt_ger_mean |  29.460 | 51.642 | 64.474 |            32.393 |            83.723 | True          |
|    1268503 | Elesbão Veloso — Presencial | Brasil sem Norte    | nt_ger_mean |  32.104 | 51.642 | 64.474 |            32.393 |            83.723 | True          |
|    1386222 | Cuiabá — EaD                | Brasil sem Norte    | nt_ger_mean |  26.980 | 51.642 | 64.474 |            32.393 |            83.723 | True          |
|    1454674 | Santos — EaD                | Brasil sem Norte    | nt_ger_mean |  83.770 | 51.642 | 64.474 |            32.393 |            83.723 | True          |
|       2898 | São Paulo — Presencial      | Brasil sem Norte    | nt_obj_mean |  89.428 | 52.527 | 65.232 |            33.468 |            84.291 | True          |
|      94363 | Paracatu — EaD              | Brasil sem Norte    | nt_obj_mean |  33.075 | 52.527 | 65.232 |            33.468 |            84.291 | True          |
|    1386222 | Cuiabá — EaD                | Brasil sem Norte    | nt_obj_mean |  30.600 | 52.527 | 65.232 |            33.468 |            84.291 | True          |
|    1454674 | Santos — EaD                | Brasil sem Norte    | nt_obj_mean |  86.900 | 52.527 | 65.232 |            33.468 |            84.291 | True          |
|      16214 | Botucatu — Presencial       | Brasil sem Norte    | nt_dis_mean |   1.083 |  4.625 |  6.364 |             2.017 |             8.972 | True          |
|      94363 | Paracatu — EaD              | Brasil sem Norte    | nt_dis_mean |   1.500 |  4.625 |  6.364 |             2.017 |             8.972 | True          |
|    1133262 | Goiânia — Presencial        | Brasil sem Norte    | nt_dis_mean |   1.438 |  4.625 |  6.364 |             2.017 |             8.972 | True          |
|    1386222 | Cuiabá — EaD                | Brasil sem Norte    | nt_dis_mean |   1.250 |  4.625 |  6.364 |             2.017 |             8.972 | True          |
|    1446088 | Caçador — EaD               | Brasil sem Norte    | nt_dis_mean |   1.750 |  4.625 |  6.364 |             2.017 |             8.972 | True          |
|    1457056 | Paracatu — EaD              | Brasil sem Norte    | nt_dis_mean |   1.833 |  4.625 |  6.364 |             2.017 |             8.972 | True          |

## Decisões para o relatório final

- preservar Castanhal como referência interna, não como prova de efeito do Conceito 5;
- apresentar N, dispersão e participação para cada oferta da UFPA;
- usar benchmarks estruturais por oferta e análise de sensibilidade;
- manter comparações territoriais com média simples e ponderada por participantes;
- interpretar processo formativo apenas com rótulos oficiais;
- manter associações entre temas no nível ecológico.