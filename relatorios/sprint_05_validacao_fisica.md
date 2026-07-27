# Sprint 5 — Validação analítica de Física

## Resumo executivo

Foram auditados **257 cursos de Física**, incluindo **5 ofertas da UFPA**. A validação preserva `CO_CURSO` como unidade principal e mantém separadas as análises individuais disponíveis no mesmo arquivo e as associações ecológicas entre cursos.

## Auditoria da presença

|   CO_CURSO | ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   registros_microdados |   presentes_validos |   ausentes |   eliminados |   resultado_desconsiderado |   reaplicacoes |   nt_ger_count |   taxa_presenca_microdados |   taxa_presenca_pct |   diferenca_participantes |   cobertura_nt_ger_pct | alerta   |
|-----------:|:-------------------------|---------------------:|----------------:|--------------------:|-----------------------:|--------------------:|-----------:|-------------:|---------------------------:|---------------:|---------------:|---------------------------:|--------------------:|--------------------------:|-----------------------:|:---------|
|      12022 | Belém — Presencial       |                 3.00 |              53 |               34.00 |                     53 |                  34 |         18 |            0 |                          0 |              0 |             34 |                       0.64 |               64.15 |                      0.00 |                 100.00 | OK       |
|    1364837 | Salinópolis — Presencial |                 1.00 |              20 |               14.00 |                     20 |                  14 |          6 |            0 |                          0 |              0 |             14 |                       0.70 |               70.00 |                      0.00 |                 100.00 | OK       |
|      92851 | Abaetetuba — Presencial  |                 1.00 |              58 |               42.00 |                     58 |                  42 |         16 |            0 |                          0 |              0 |             42 |                       0.72 |               72.41 |                      0.00 |                 100.00 | OK       |
|    1202639 | Belém — EaD              |                 1.00 |              32 |               24.00 |                     32 |                  24 |          6 |            0 |                          0 |              0 |             24 |                       0.75 |               75.00 |                      0.00 |                 100.00 | OK       |
|    1330339 | Ananindeua — Presencial  |                 1.00 |              22 |               17.00 |                     22 |                  17 |          4 |            0 |                          0 |              0 |             17 |                       0.77 |               77.27 |                      0.00 |                 100.00 | OK       |

As taxas ficaram no domínio esperado. Participantes oficiais, presentes e cobertura de NT_GER foram mantidos em colunas distintas.

## Comparação territorial de NT_GER

| referencia            |   n_cursos |   media_cursos |   mediana_cursos |   media_ponderada_participantes |   p25 |   p75 |
|:----------------------|-----------:|---------------:|-----------------:|--------------------------------:|------:|------:|
| UFPA agregada         |          5 |          41.72 |            42.33 |                           42.15 | 38.45 | 42.47 |
| Outras IES do Pará    |          3 |          41.52 |            41.42 |                           41.52 | 40.26 | 42.73 |
| Região Norte completa |         25 |          43.97 |            44.05 |                           42.96 | 39.10 | 49.11 |
| Brasil completo       |        237 |          52.96 |            53.04 |                           52.45 | 46.15 | 59.48 |

Os agregados Norte e Brasil são referências descritivas sobrepostas; não são tratados como grupos independentes em testes.

## Sensibilidade dos benchmarks

|   CO_CURSO_ALVO | ROTULO_ALVO              | criterio               |   n_cursos_comparaveis |   nt_ger_alvo |   media_comparaveis |   mediana_comparaveis |   diferenca_media |   percentil_alvo |
|----------------:|:-------------------------|:-----------------------|-----------------------:|--------------:|--------------------:|----------------------:|------------------:|-----------------:|
|           92851 | Abaetetuba — Presencial  | porte_25pct            |                      4 |         38.45 |               57.33 |                 56.29 |            -18.88 |             0.00 |
|           92851 | Abaetetuba — Presencial  | porte_50pct            |                     10 |         38.45 |               54.36 |                 54.67 |            -15.91 |             0.00 |
|           92851 | Abaetetuba — Presencial  | porte_2x               |                     10 |         38.45 |               54.36 |                 54.67 |            -15.91 |             0.00 |
|           92851 | Abaetetuba — Presencial  | mesmo_quartil_porte    |                     19 |         38.45 |               56.14 |                 57.10 |            -17.69 |             0.00 |
|           92851 | Abaetetuba — Presencial  | universidades_federais |                     10 |         38.45 |               54.36 |                 54.67 |            -15.91 |             0.00 |
|         1202639 | Belém — EaD              | porte_25pct            |                      0 |         30.91 |              nan    |                nan    |            nan    |           nan    |
|         1202639 | Belém — EaD              | porte_50pct            |                      1 |         30.91 |               32.89 |                 32.89 |             -1.98 |             0.00 |
|         1202639 | Belém — EaD              | porte_2x               |                      1 |         30.91 |               32.89 |                 32.89 |             -1.98 |             0.00 |
|         1202639 | Belém — EaD              | mesmo_quartil_porte    |                      4 |         30.91 |               43.44 |                 41.55 |            -12.53 |             0.00 |
|         1202639 | Belém — EaD              | universidades_federais |                      1 |         30.91 |               32.89 |                 32.89 |             -1.98 |             0.00 |
|         1330339 | Ananindeua — Presencial  | porte_25pct            |                     21 |         42.33 |               59.09 |                 59.66 |            -16.76 |             0.00 |
|         1330339 | Ananindeua — Presencial  | porte_50pct            |                     35 |         42.33 |               56.89 |                 56.54 |            -14.56 |             5.71 |
|         1330339 | Ananindeua — Presencial  | porte_2x               |                     36 |         42.33 |               57.07 |                 56.82 |            -14.74 |             5.56 |
|         1330339 | Ananindeua — Presencial  | mesmo_quartil_porte    |                     19 |         42.33 |               56.14 |                 57.10 |            -13.80 |             5.26 |
|         1330339 | Ananindeua — Presencial  | universidades_federais |                     36 |         42.33 |               57.07 |                 56.82 |            -14.74 |             5.56 |
|         1364837 | Salinópolis — Presencial | porte_25pct            |                     18 |         42.47 |               58.49 |                 58.29 |            -16.02 |             5.56 |
|         1364837 | Salinópolis — Presencial | porte_50pct            |                     41 |         42.47 |               57.79 |                 57.10 |            -15.31 |             2.44 |
|         1364837 | Salinópolis — Presencial | porte_2x               |                     45 |         42.47 |               57.14 |                 56.54 |            -14.67 |             4.44 |
|         1364837 | Salinópolis — Presencial | mesmo_quartil_porte    |                     17 |         42.47 |               58.73 |                 58.31 |            -16.26 |             5.88 |
|         1364837 | Salinópolis — Presencial | universidades_federais |                     45 |         42.47 |               57.14 |                 56.54 |            -14.67 |             4.44 |

A estabilidade deve ser julgada pela direção e magnitude das diferenças em critérios alternativos, não pela seleção do resultado mais favorável.

## Percepção de dificuldade

|   CO_CURSO | ROTULO_OFERTA            |   CONCEITO_ENADE_NUM | item     |   n_valido |   dificuldade_alta_pct | alerta   |
|-----------:|:-------------------------|---------------------:|:---------|-----------:|-----------------------:|:---------|
|      12022 | Belém — Presencial       |                 3.00 | CO_RS_I1 |         30 |                  80.00 | OK       |
|      12022 | Belém — Presencial       |                 3.00 | CO_RS_I2 |         32 |                  15.62 | OK       |
|      12022 | Belém — Presencial       |                 3.00 | CO_RS_I7 |         32 |                  96.88 | OK       |
|      92851 | Abaetetuba — Presencial  |                 1.00 | CO_RS_I1 |         40 |                  75.00 | OK       |
|      92851 | Abaetetuba — Presencial  |                 1.00 | CO_RS_I2 |         41 |                   4.88 | OK       |
|      92851 | Abaetetuba — Presencial  |                 1.00 | CO_RS_I7 |         41 |                  97.56 | OK       |
|    1202639 | Belém — EaD              |                 1.00 | CO_RS_I1 |         22 |                  86.36 | OK       |
|    1202639 | Belém — EaD              |                 1.00 | CO_RS_I2 |         22 |                   0.00 | OK       |
|    1202639 | Belém — EaD              |                 1.00 | CO_RS_I7 |         22 |                 100.00 | OK       |
|    1330339 | Ananindeua — Presencial  |                 1.00 | CO_RS_I1 |         17 |                  82.35 | OK       |
|    1330339 | Ananindeua — Presencial  |                 1.00 | CO_RS_I2 |         17 |                   5.88 | OK       |
|    1330339 | Ananindeua — Presencial  |                 1.00 | CO_RS_I7 |         17 |                 100.00 | OK       |
|    1364837 | Salinópolis — Presencial |                 1.00 | CO_RS_I1 |         13 |                  92.31 | OK       |
|    1364837 | Salinópolis — Presencial |                 1.00 | CO_RS_I2 |         13 |                   0.00 | OK       |
|    1364837 | Salinópolis — Presencial |                 1.00 | CO_RS_I7 |         13 |                 100.00 | OK       |

A relação entre conceito, dificuldade e desempenho é ecológica no nível do curso.

## Processo formativo

| dimensao                        |   n_itens_previstos |   n_itens_encontrados |   n_cursos_com_score |   media_nacional_exploratoria |   media_ufpa_exploratoria | decisao                                                                        |
|:--------------------------------|--------------------:|----------------------:|---------------------:|------------------------------:|--------------------------:|:-------------------------------------------------------------------------------|
| organizacao_didatico_pedagogica |                   8 |                     8 |                  242 |                         0.868 |                     0.870 | Uso exploratório; validar redação e coerência teórica antes do relatório final |
| atuacao_docente                 |                   7 |                     7 |                  242 |                         0.817 |                     0.825 | Uso exploratório; validar redação e coerência teórica antes do relatório final |
| infraestrutura                  |                   8 |                     8 |                  242 |                         0.882 |                     0.886 | Uso exploratório; validar redação e coerência teórica antes do relatório final |
| oportunidades_formacao          |                  10 |                    10 |                  242 |                         0.874 |                     0.850 | Uso exploratório; validar redação e coerência teórica antes do relatório final |
| integracao_teoria_pratica       |                   8 |                     8 |                  242 |                         0.839 |                     0.776 | Uso exploratório; validar redação e coerência teórica antes do relatório final |
| apoio_academico                 |                   6 |                     6 |                  242 |                         0.876 |                     0.853 | Uso exploratório; validar redação e coerência teórica antes do relatório final |

As dimensões são candidatas exploratórias. A redação oficial dos itens e a coerência teórica deverão ser confirmadas antes de qualquer uso como índice no relatório final.

## Síntese socioeconômica por oferta

|   CO_CURSO | ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   nt_ger_mean |   nt_ger_median |   taxa_presenca_microdados |   primeira_geracao_pct |   mae_superior_pct |   pai_superior_pct |   renda_ate_3sm_pct |   trabalha_pct |   trabalha_40h_pct |   acao_afirmativa_pct |   auxilio_permanencia_pct |   bolsa_academica_pct |   estudo_4h_ou_mais_pct |   pretende_magisterio_pct |
|-----------:|:-------------------------|---------------------:|--------------:|----------------:|---------------------------:|-----------------------:|-------------------:|-------------------:|--------------------:|---------------:|-------------------:|----------------------:|--------------------------:|----------------------:|------------------------:|--------------------------:|
|      12022 | Belém — Presencial       |                3.000 |        54.448 |          58.250 |                      0.642 |                  0.342 |              0.216 |              0.125 |               0.775 |          0.550 |              0.100 |                 0.575 |                     0.075 |                 0.621 |                   0.750 |                     0.825 |
|      92851 | Abaetetuba — Presencial  |                1.000 |        38.451 |          38.740 |                      0.724 |                  0.462 |              0.116 |              0.059 |               0.955 |          0.477 |              0.114 |                 0.750 |                     0.409 |                 0.238 |                   0.591 |                     0.818 |
|    1202639 | Belém — EaD              |                1.000 |        30.905 |          28.600 |                      0.750 |                  0.160 |              0.077 |              0.043 |               0.926 |          0.704 |              0.407 |                 0.741 |                     0.000 |                 0.000 |                   0.370 |                     0.889 |
|    1330339 | Ananindeua — Presencial  |                1.000 |        42.333 |          40.840 |                      0.773 |                  0.476 |              0.190 |              0.100 |               0.810 |          0.476 |              0.095 |                 0.571 |                     0.190 |                 0.562 |                   0.619 |                     0.619 |
|    1364837 | Salinópolis — Presencial |                1.000 |        42.473 |          43.450 |                      0.700 |                  0.667 |              0.000 |              0.111 |               1.000 |          0.467 |              0.067 |                 0.733 |                     0.533 |                 0.500 |                   0.533 |                     0.867 |

A leitura conjunta com desempenho é contextual e não permite inferência individual.

## Associações ecológicas

| desfecho    | preditor                      |   n_cursos |   spearman_rho |   p_valor_exploratorio | interpretacao                                           | variavel_x         | variavel_y                    | nivel             |
|:------------|:------------------------------|-----------:|---------------:|-----------------------:|:--------------------------------------------------------|:-------------------|:------------------------------|:------------------|
| nt_ger_mean | taxa_presenca_microdados      |        237 |         0.0594 |                 0.3624 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | renda_ate_3sm_pct             |        237 |        -0.3875 |                 0.0000 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | trabalha_pct                  |        237 |        -0.0397 |                 0.5432 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | acao_afirmativa_pct           |        237 |         0.0557 |                 0.3932 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | auxilio_permanencia_pct       |        237 |        -0.0626 |                 0.3376 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | primeira_geracao_pct          |        237 |        -0.2037 |                 0.0016 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | qe_i68_nota_9_10_pct          |        237 |        -0.2017 |                 0.0018 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | qe_i69_nota_9_10_pct          |        237 |         0.0252 |                 0.6995 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | co_rs_i1_dificuldade_alta_pct |        235 |        -0.0043 |                 0.9473 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nt_ger_mean | co_rs_i7_dificuldade_alta_pct |        235 |         0.0026 |                 0.9688 | Associação ecológica; não representa relação individual | nan                | nan                           | nan               |
| nan         | nan                           |        235 |        -0.0043 |                 0.9473 | nan                                                     | nt_ger_mean        | co_rs_i1_dificuldade_alta_pct | curso (ecológico) |
| nan         | nan                           |        235 |        -0.0338 |                 0.6063 | nan                                                     | CONCEITO_ENADE_NUM | co_rs_i1_dificuldade_alta_pct | curso (ecológico) |
| nan         | nan                           |        235 |        -0.0475 |                 0.4689 | nan                                                     | nt_ger_mean        | co_rs_i2_dificuldade_alta_pct | curso (ecológico) |
| nan         | nan                           |        235 |        -0.0743 |                 0.2566 | nan                                                     | CONCEITO_ENADE_NUM | co_rs_i2_dificuldade_alta_pct | curso (ecológico) |
| nan         | nan                           |        235 |         0.0026 |                 0.9688 | nan                                                     | nt_ger_mean        | co_rs_i7_dificuldade_alta_pct | curso (ecológico) |
| nan         | nan                           |        235 |         0.0107 |                 0.8699 | nan                                                     | CONCEITO_ENADE_NUM | co_rs_i7_dificuldade_alta_pct | curso (ecológico) |

Os valores de p são apenas exploratórios. A interpretação prioriza magnitude, direção, N de cursos, dispersão e possibilidade de outliers.

## Decisões para o relatório final

- manter taxa de presença, NT_GER, NT_OBJ e NT_DIS por oferta;
- manter comparação territorial com distinção entre ofertas da UFPA e referências agregadas;
- apresentar dificuldade no nível do curso e sem causalidade;
- manter itens ou dimensões de processo formativo somente após validação teórica;
- apresentar perfil socioeconômico por oferta com N e ausências;
- documentar sensibilidade dos benchmarks e instabilidade associada a N pequeno.