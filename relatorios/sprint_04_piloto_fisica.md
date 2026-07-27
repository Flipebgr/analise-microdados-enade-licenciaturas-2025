# Sprint 4 — Piloto de Física

## Resumo executivo

A base analítica contém **257 cursos de Física**, incluindo **5 ofertas validadas da UFPA**. A análise preserva cada oferta por `CO_CURSO`, município e modalidade.

Tucuruí não foi incluído nas análises porque não foi localizado com `CO_CURSO` validado nas fontes atuais.

## Ofertas da UFPA

|   CO_CURSO | ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   PCT_PADRAO_PROFICIENCIA_NUM |
|-----------:|:-------------------------|---------------------:|----------------:|--------------------:|------------------------------:|
|      12022 | Belém — Presencial       |                    3 |              53 |                  34 |                          0.62 |
|      92851 | Abaetetuba — Presencial  |                    1 |              58 |                  42 |                          0.19 |
|    1202639 | Belém — EaD              |                    1 |              32 |                  24 |                          0.04 |
|    1330339 | Ananindeua — Presencial  |                    1 |              22 |                  17 |                          0.18 |
|    1364837 | Salinópolis — Presencial |                    1 |              20 |                  14 |                          0.21 |

## Taxa de presença

|   CO_CURSO | ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   INSCRITOS_NUM |   PARTICIPANTES_NUM |   registros_microdados |   presentes_validos |   ausentes |   eliminados |   resultado_desconsiderado |   nt_ger_count |   taxa_presenca_pct |   diferenca_participantes_microdados |
|-----------:|:-------------------------|---------------------:|----------------:|--------------------:|-----------------------:|--------------------:|-----------:|-------------:|---------------------------:|---------------:|--------------------:|-------------------------------------:|
|      12022 | Belém — Presencial       |                    3 |              53 |                  34 |                     53 |                  34 |         18 |            0 |                          0 |             34 |               64.15 |                                    0 |
|    1364837 | Salinópolis — Presencial |                    1 |              20 |                  14 |                     20 |                  14 |          6 |            0 |                          0 |             14 |               70.00 |                                    0 |
|      92851 | Abaetetuba — Presencial  |                    1 |              58 |                  42 |                     58 |                  42 |         16 |            0 |                          0 |             42 |               72.41 |                                    0 |
|    1202639 | Belém — EaD              |                    1 |              32 |                  24 |                     32 |                  24 |          6 |            0 |                          0 |             24 |               75.00 |                                    0 |
|    1330339 | Ananindeua — Presencial  |                    1 |              22 |                  17 |                     22 |                  17 |          4 |            0 |                          0 |             17 |               77.27 |                                    0 |

A taxa utiliza `TP_PRES=555` sobre os registros elegíveis localizados no arquivo de desempenho. Participantes oficiais e registros válidos permanecem documentados separadamente.

## NT_GER, NT_OBJ e NT_DIS por oferta

| ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   nt_ger_count |   nt_ger_mean |   nt_ger_median |   nt_obj_count |   nt_obj_mean |   nt_obj_median |   nt_dis_count |   nt_dis_mean |   nt_dis_median |
|:-------------------------|---------------------:|---------------:|--------------:|----------------:|---------------:|--------------:|----------------:|---------------:|--------------:|----------------:|
| Belém — EaD              |                    1 |             24 |         30.91 |           28.60 |             24 |         26.29 |           23.60 |             24 |          4.94 |            5.25 |
| Abaetetuba — Presencial  |                    1 |             42 |         38.45 |           38.74 |             42 |         33.91 |           32.30 |             42 |          5.66 |            6.25 |
| Ananindeua — Presencial  |                    1 |             17 |         42.33 |           40.84 |             17 |         39.13 |           37.90 |             17 |          5.51 |            6.00 |
| Salinópolis — Presencial |                    1 |             14 |         42.47 |           43.45 |             14 |         37.96 |           36.50 |             14 |          6.05 |            6.50 |
| Belém — Presencial       |                    3 |             34 |         54.45 |           58.25 |             34 |         52.97 |           54.25 |             34 |          6.04 |            6.75 |

## Nota geral comparativa

| REFERENCIA         |   N_CURSOS |   MEDIA_DAS_MEDIAS |   MEDIANA_DAS_MEDIAS |   DP_DAS_MEDIAS |
|:-------------------|-----------:|-------------------:|---------------------:|----------------:|
| UFPA agregada      |          5 |              41.72 |                42.33 |            8.52 |
| Outras IES do Pará |          3 |              41.52 |                41.42 |            2.48 |
| Região Norte       |         25 |              43.97 |                44.05 |            7.41 |
| Brasil             |        237 |              52.96 |                53.04 |            9.47 |

As referências territoriais são calculadas no nível do curso. O agregado UFPA complementa, mas não substitui, a apresentação individual das ofertas.

## Conceito e percepção de dificuldade

| ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   co_rs_i1_dificuldade_alta_pct |   co_rs_i2_dificuldade_alta_pct |   co_rs_i7_dificuldade_alta_pct |
|:-------------------------|---------------------:|--------------------------------:|--------------------------------:|--------------------------------:|
| Belém — Presencial       |                    3 |                           80.00 |                           15.62 |                           96.88 |
| Abaetetuba — Presencial  |                    1 |                           75.00 |                            4.88 |                           97.56 |
| Belém — EaD              |                    1 |                           86.36 |                            0.00 |                          100.00 |
| Ananindeua — Presencial  |                    1 |                           82.35 |                            5.88 |                          100.00 |
| Salinópolis — Presencial |                    1 |                           92.31 |                            0.00 |                          100.00 |

A percepção de dificuldade foi agregada por curso a partir de `CO_RS_I1`, `CO_RS_I2` e `CO_RS_I7`, todos presentes no arquivo de desempenho. A relação com o Conceito Enade é ecológica e não implica causalidade individual.

## Perfil socioeconômico geral por oferta

| ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   nt_ger_mean |   primeira_geracao_pct |   mae_superior_pct |   pai_superior_pct |   renda_ate_3sm_pct |   trabalha_pct |   trabalha_40h_pct |   acao_afirmativa_pct |   auxilio_permanencia_pct |   bolsa_academica_pct |   estudo_4h_ou_mais_pct |   pretende_magisterio_pct |
|:-------------------------|---------------------:|--------------:|-----------------------:|-------------------:|-------------------:|--------------------:|---------------:|-------------------:|----------------------:|--------------------------:|----------------------:|------------------------:|--------------------------:|
| Belém — Presencial       |                    3 |        54.448 |                  0.342 |              0.216 |              0.125 |               0.775 |          0.550 |              0.100 |                 0.575 |                     0.075 |                 0.621 |                   0.750 |                     0.825 |
| Abaetetuba — Presencial  |                    1 |        38.451 |                  0.462 |              0.116 |              0.059 |               0.955 |          0.477 |              0.114 |                 0.750 |                     0.409 |                 0.238 |                   0.591 |                     0.818 |
| Belém — EaD              |                    1 |        30.905 |                  0.160 |              0.077 |              0.043 |               0.926 |          0.704 |              0.407 |                 0.741 |                     0.000 |                 0.000 |                   0.370 |                     0.889 |
| Ananindeua — Presencial  |                    1 |        42.333 |                  0.476 |              0.190 |              0.100 |               0.810 |          0.476 |              0.095 |                 0.571 |                     0.190 |                 0.562 |                   0.619 |                     0.619 |
| Salinópolis — Presencial |                    1 |        42.473 |                  0.667 |              0.000 |              0.111 |               1.000 |          0.467 |              0.067 |                 0.733 |                     0.533 |                 0.500 |                   0.533 |                     0.867 |

A tabela apresenta uma visão geral da composição socioeconômica de cada oferta. A leitura conjunta com NT_GER é descritiva e ecológica; não permite concluir que características individuais produziram as diferenças de nota.

## Recomendação do curso e da instituição

| ROTULO_OFERTA            |   qe_i68_n |   qe_i68_nota_9_10_pct |   qe_i69_n |   qe_i69_nota_9_10_pct |
|:-------------------------|-----------:|-----------------------:|-----------:|-----------------------:|
| Belém — Presencial       |         40 |                  0.375 |         40 |                  0.800 |
| Abaetetuba — Presencial  |         44 |                  0.568 |         44 |                  0.727 |
| Belém — EaD              |         27 |                  0.630 |         27 |                  0.852 |
| Ananindeua — Presencial  |         21 |                  0.714 |         21 |                  0.857 |
| Salinópolis — Presencial |         15 |                  0.600 |         15 |                  0.867 |

Os títulos e interpretações deverão seguir os rótulos oficiais de `QE_I68` e `QE_I69`; os percentuais acima correspondem às avaliações 9 ou 10 entre respostas válidas.

## Benchmark comparável

|   CO_CURSO_ALVO | ROTULO_ALVO              | modalidade   |   participantes_alvo |   n_cursos_comparaveis | criterio                                                                                                 |
|----------------:|:-------------------------|:-------------|---------------------:|-----------------------:|:---------------------------------------------------------------------------------------------------------|
|           92851 | Abaetetuba — Presencial  | Presencial   |                   42 |                     10 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|         1202639 | Belém — EaD              | EaD          |                   24 |                      1 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|         1330339 | Ananindeua — Presencial  | Presencial   |                   17 |                     36 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |
|         1364837 | Salinópolis — Presencial | Presencial   |                   14 |                     45 | mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo |

## Figuras produzidas

1. ofertas da UFPA;
2. taxa de presença por oferta;
3. nota geral por oferta;
4. nota geral comparativa;
5. prova objetiva por oferta;
6. prova discursiva por oferta;
7. Conceito Enade × percepção de dificuldade;
8. percepção do processo formativo;
9. recomendação do curso;
10. recomendação da instituição;
11. perfil socioeconômico;
12. benchmark comparável;
13. síntese socioeconômica e desempenho.

## Limitações

- não existe chave individual entre arquivos temáticos;
- associações entre desempenho, perfil e processo formativo são ecológicas;
- cursos com N pequeno produzem estimativas mais instáveis;
- os itens de processo formativo são apresentados separadamente, sem índice único não validado;
- a comparação ampla não substitui o benchmark comparável.

## Próxima etapa

Auditar os indicadores, testar sensibilidade dos benchmarks e validar a narrativa gráfica antes da elaboração do relatório ABNT de Física.