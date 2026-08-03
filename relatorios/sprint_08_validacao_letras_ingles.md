# Sprint 08 — Validação analítica de Letras–Inglês

## Resumo executivo

Foram auditados **138 cursos de Letras–Inglês**, incluindo **5 ofertas da UFPA**. A unidade de análise permanece `CO_CURSO`.

## Participação e desempenho

|   CO_CURSO | ROTULO_OFERTA         | GRUPO_CODIGO   |   PARTICIPANTES_NUM |   registros_microdados |   presentes_validos |   nt_ger_count |   nt_obj_count |   nt_dis_count |   reaplicacoes |   diferenca_participantes_oficial_nt_ger | alerta_n_superior_registros   | alerta_diferenca_participantes   |
|-----------:|:----------------------|:---------------|--------------------:|-----------------------:|--------------------:|---------------:|---------------:|---------------:|---------------:|-----------------------------------------:|:------------------------------|:---------------------------------|
|      23777 | Belém — Presencial    | B              |              85.000 |                    100 |                  85 |             85 |             85 |             85 |              0 |                                    0.000 | False                         | False                            |
|      95652 | Soure — Presencial    | A              |              37.000 |                     44 |                  37 |             37 |             37 |             37 |              0 |                                    0.000 | False                         | False                            |
|     114847 | Cametá — Presencial   | A              |              15.000 |                     17 |                  15 |             15 |             15 |             15 |              0 |                                    0.000 | False                         | False                            |
|     114875 | Bragança — Presencial | A              |              41.000 |                     44 |                  41 |             41 |             41 |             41 |              0 |                                    0.000 | False                         | False                            |
|     114877 | Altamira — Presencial | A              |              21.000 |                     22 |                  21 |             21 |             21 |             21 |              0 |                                    0.000 | False                         | False                            |

## Comparações regionais e nacionais

| RECORTE                      | INDICADOR   |   N_CURSOS |   N_PARTICIPANTES |   MEDIA_CURSOS |   MEDIA_PONDERADA_PARTICIPANTES |   MEDIANA_CURSOS |   DP_CURSOS |    P25 |    P75 |   AMPLITUDE_IQR |   DIF_MEDIA_PONDERADA | ALERTA_IQR_NEGATIVO   |
|:-----------------------------|:------------|-----------:|------------------:|---------------:|--------------------------------:|-----------------:|------------:|-------:|-------:|----------------:|----------------------:|:----------------------|
| UFPA — Altamira — Presencial | nt_ger_mean |          1 |            21.000 |         31.844 |                          31.844 |           31.844 |     nan     | 31.844 | 31.844 |           0.000 |                 0.000 | False                 |
| UFPA — Bragança — Presencial | nt_ger_mean |          1 |            41.000 |         45.193 |                          45.193 |           45.193 |     nan     | 45.193 | 45.193 |           0.000 |                 0.000 | False                 |
| UFPA — Cametá — Presencial   | nt_ger_mean |          1 |            15.000 |         34.617 |                          34.617 |           34.617 |     nan     | 34.617 | 34.617 |           0.000 |                 0.000 | False                 |
| UFPA — Soure — Presencial    | nt_ger_mean |          1 |            37.000 |         31.834 |                          31.834 |           31.834 |     nan     | 31.834 | 31.834 |           0.000 |                 0.000 | False                 |
| UFPA — Belém — Presencial    | nt_ger_mean |          1 |            85.000 |         56.454 |                          56.454 |           56.454 |     nan     | 56.454 | 56.454 |           0.000 |                 0.000 | False                 |
| UFPA agregada                | nt_ger_mean |          5 |           199.000 |         39.988 |                          45.313 |           34.617 |      10.722 | 31.844 | 45.193 |          13.349 |                 5.325 | False                 |
| Região Norte sem UFPA        | nt_ger_mean |          9 |           186.000 |         43.368 |                          43.460 |           39.947 |       7.149 | 38.853 | 47.486 |           8.633 |                 0.092 | False                 |
| Região Norte completa        | nt_ger_mean |         14 |           385.000 |         42.161 |                          44.418 |           39.718 |       8.346 | 35.334 | 47.128 |          11.794 |                 2.257 | False                 |
| Nordeste                     | nt_ger_mean |         49 |          1115.000 |         48.407 |                          50.492 |           47.623 |      10.648 | 41.906 | 54.051 |          12.145 |                 2.085 | False                 |
| Sudeste                      | nt_ger_mean |         28 |           956.000 |         55.447 |                          52.073 |           54.059 |      11.123 | 48.508 | 64.629 |          16.121 |                -3.374 | False                 |
| Sul                          | nt_ger_mean |         29 |          1109.000 |         54.357 |                          48.080 |           51.769 |      13.324 | 44.360 | 66.409 |          22.049 |                -6.277 | False                 |
| Centro-Oeste                 | nt_ger_mean |          7 |           101.000 |         55.856 |                          58.475 |           52.302 |       9.943 | 48.850 | 61.894 |          13.044 |                 2.620 | False                 |
| Brasil geral                 | nt_ger_mean |        127 |          3666.000 |         51.040 |                          49.757 |           49.704 |      11.859 | 42.882 | 59.744 |          16.861 |                -1.283 | False                 |
| Brasil sem UFPA              | nt_ger_mean |        122 |          3467.000 |         51.493 |                          50.012 |           49.981 |      11.722 | 43.164 | 60.325 |          17.161 |                -1.481 | False                 |
| Restante do Brasil sem Norte | nt_ger_mean |        113 |          3281.000 |         52.140 |                          50.383 |           50.789 |      11.792 | 44.110 | 61.470 |          17.360 |                -1.757 | False                 |

As referências Norte e Brasil são benchmarks descritivos sobrepostos e não são tratadas como grupos independentes em testes.

## Sensibilidade do desempenho

| cenario                | grupo   |   n_cursos |   media_cursos |   mediana_cursos |   media_ponderada_participantes |
|:-----------------------|:--------|-----------:|---------------:|-----------------:|--------------------------------:|
| todos                  | A       |          4 |         35.872 |           33.231 |                          37.006 |
| todos                  | B       |          1 |         56.454 |           56.454 |                          56.454 |
| todos                  | C       |          2 |         36.979 |           36.979 |                          36.775 |
| todos                  | D       |          7 |         45.193 |           46.053 |                          46.489 |
| todos                  | E       |        113 |         52.140 |           50.789 |                          50.383 |
| n_minimo_10            | A       |          4 |         35.872 |           33.231 |                          37.006 |
| n_minimo_10            | B       |          1 |         56.454 |           56.454 |                          56.454 |
| n_minimo_10            | C       |          2 |         36.979 |           36.979 |                          36.775 |
| n_minimo_10            | D       |          6 |         46.250 |           46.769 |                          46.864 |
| n_minimo_10            | E       |         77 |         51.480 |           50.078 |                          50.245 |
| presencial             | A       |          4 |         35.872 |           33.231 |                          37.006 |
| presencial             | B       |          1 |         56.454 |           56.454 |                          56.454 |
| presencial             | C       |          1 |         39.947 |           39.947 |                          39.947 |
| presencial             | D       |          6 |         46.250 |           46.769 |                          46.864 |
| presencial             | E       |         85 |         53.446 |           52.116 |                          55.346 |
| universidades_federais | A       |          4 |         35.872 |           33.231 |                          37.006 |
| universidades_federais | B       |          1 |         56.454 |           56.454 |                          56.454 |
| universidades_federais | C       |          1 |         39.947 |           39.947 |                          39.947 |
| universidades_federais | D       |          5 |         47.602 |           47.486 |                          48.311 |
| universidades_federais | E       |         30 |         59.271 |           61.227 |                          60.104 |

## Sensibilidade do benchmark comparável

|   CO_CURSO_ALVO | ROTULO_ALVO           | criterio    |   n_comparaveis |   nt_ger_alvo |   media_benchmark |   mediana_benchmark |   diferenca_media |   diferenca_mediana |
|----------------:|:----------------------|:------------|----------------:|--------------:|------------------:|--------------------:|------------------:|--------------------:|
|           95652 | Soure — Presencial    | porte_25pct |               5 |        31.834 |            62.882 |              63.315 |           -31.048 |             -31.482 |
|           95652 | Soure — Presencial    | porte_50pct |              19 |        31.834 |            57.076 |              57.571 |           -25.242 |             -25.737 |
|           95652 | Soure — Presencial    | porte_2x    |              21 |        31.834 |            57.922 |              59.608 |           -26.088 |             -27.775 |
|          114847 | Cametá — Presencial   | porte_25pct |               5 |        34.617 |            66.904 |              68.574 |           -32.287 |             -33.957 |
|          114847 | Cametá — Presencial   | porte_50pct |              11 |        34.617 |            61.770 |              68.352 |           -27.152 |             -33.735 |
|          114847 | Cametá — Presencial   | porte_2x    |              20 |        34.617 |            57.488 |              58.172 |           -22.871 |             -23.555 |
|          114875 | Bragança — Presencial | porte_25pct |               6 |        45.193 |            60.811 |              58.725 |           -15.617 |             -13.532 |
|          114875 | Bragança — Presencial | porte_50pct |              15 |        45.193 |            55.678 |              56.735 |           -10.484 |             -11.542 |
|          114875 | Bragança — Presencial | porte_2x    |              17 |        45.193 |            56.887 |              57.571 |           -11.694 |             -12.377 |
|          114877 | Altamira — Presencial | porte_25pct |              15 |        31.844 |            58.307 |              59.608 |           -26.463 |             -27.765 |
|          114877 | Altamira — Presencial | porte_50pct |              18 |        31.844 |            58.561 |              62.506 |           -26.717 |             -30.662 |
|          114877 | Altamira — Presencial | porte_2x    |              22 |        31.844 |            59.160 |              61.462 |           -27.316 |             -29.618 |

## Perfil socioeconômico das ofertas da UFPA

|   CO_CURSO | ROTULO_OFERTA         |   CONCEITO_ENADE_NUM |   nt_ger_mean |   renda_ate_3sm_pct |   trabalha_pct |   acao_afirmativa_pct |   auxilio_permanencia_pct |
|-----------:|:----------------------|---------------------:|--------------:|--------------------:|---------------:|----------------------:|--------------------------:|
|      23777 | Belém — Presencial    |                3.000 |        56.454 |               0.678 |          0.782 |                 0.506 |                     0.080 |
|      95652 | Soure — Presencial    |                1.000 |        31.834 |               0.895 |          0.368 |                 0.789 |                     0.289 |
|     114847 | Cametá — Presencial   |                1.000 |        34.617 |               1.000 |          0.312 |                 0.750 |                     0.250 |
|     114875 | Bragança — Presencial |                1.000 |        45.193 |               0.864 |          0.455 |                 0.682 |                     0.182 |
|     114877 | Altamira — Presencial |                1.000 |        31.844 |               0.762 |          0.810 |                 0.714 |                     0.095 |

## Diagnóstico de outliers

Nenhum outlier de NT_GER pela regra exploratória de 1,5×IQR.

Os outliers não são excluídos automaticamente; são apenas sinalizados para análise de sensibilidade.

## Associações ecológicas

| INDICADOR_X             | INDICADOR_Y   |   N_CURSOS |   SPEARMAN_RHO |   P_VALOR_EXPLORATORIO | NIVEL_ANALISE     |
|:------------------------|:--------------|-----------:|---------------:|-----------------------:|:------------------|
| renda_ate_3sm_pct       | nt_ger_mean   |        127 |        -0.3912 |                 0.0000 | curso (ecológico) |
| trabalha_pct            | nt_ger_mean   |        127 |         0.0768 |                 0.3909 | curso (ecológico) |
| acao_afirmativa_pct     | nt_ger_mean   |        127 |        -0.1597 |                 0.0730 | curso (ecológico) |
| auxilio_permanencia_pct | nt_ger_mean   |        127 |        -0.0840 |                 0.3476 | curso (ecológico) |
| qe_i68_media            | nt_ger_mean   |        127 |         0.0352 |                 0.6943 | curso (ecológico) |
| qe_i69_media            | nt_ger_mean   |        127 |         0.2889 |                 0.0010 | curso (ecológico) |

As correlações são ecológicas, calculadas entre indicadores agregados por curso. Não representam associações individuais e não sustentam inferência causal.

## Processo formativo

A Sprint 07 preservou `QE_I20–QE_I66` em nível agregado por curso e item e não formou índice único. A validação mantém essa decisão até confirmação teórica dos itens e da escala.

## Decisões para o relatório final

- manter N válido, dispersão e ausências junto aos indicadores;
- apresentar média simples e média ponderada por participantes nas comparações territoriais;
- manter grupos A–E exclusivos para comparações independentes;
- apresentar benchmarks comparáveis com análise de sensibilidade de porte;
- tratar relações entre perfil, processo formativo e desempenho apenas no nível ecológico do curso;
- não interpretar modalidade, interiorização ou baixo N como explicação causal sem desenho apropriado.