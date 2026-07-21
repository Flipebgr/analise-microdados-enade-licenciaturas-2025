# Sprint 2 — Validação analítica de Matemática

## Resumo executivo

Esta sprint auditou indicadores, grupos, benchmarks e estabilidade dos resultados do piloto de Matemática.

Foram auditadas **482 ofertas** e **21 combinações curso-alvo × critério de benchmark**.

## Auditoria de participação — UFPA

|   CO_CURSO | ROTULO_OFERTA            |   PARTICIPANTES_NUM |   registros_microdados |   nt_ger_count |   diferenca_participantes_oficial_nt_ger | alerta_diferenca_participantes   |
|-----------:|:-------------------------|--------------------:|-----------------------:|---------------:|-----------------------------------------:|:---------------------------------|
|      11999 | Belém - Presencial       |                  61 |                     68 |             61 |                                        0 | False                            |
|      12033 | Bragança - Presencial    |                  34 |                     49 |             34 |                                        0 | False                            |
|      12035 | Castanhal - Presencial   |                  52 |                     68 |             52 |                                        0 | False                            |
|      12044 | Breves - Presencial      |                  31 |                     45 |             31 |                                        0 | False                            |
|      12074 | Cametá - Presencial      |                  72 |                     86 |             72 |                                        0 | False                            |
|      86396 | Belém - EaD              |                  16 |                     34 |             16 |                                        0 | False                            |
|     114853 | Abaetetuba - Presencial  |                  86 |                    135 |             86 |                                        0 | False                            |
|    1300375 | Salinópolis - Presencial |                  26 |                     35 |             26 |                                        0 | False                            |

## Indicadores percentuais

Foram verificados **67 indicadores**. Indicadores fora do domínio 0–1: **0**.

## Sensibilidade dos benchmarks

|   CO_CURSO_ALVO | ROTULO_ALVO              | criterio    |   n_comparaveis |   nt_ger_alvo |   media_benchmark |   mediana_benchmark |   diferenca_media |   diferenca_mediana |
|----------------:|:-------------------------|:------------|----------------:|--------------:|------------------:|--------------------:|------------------:|--------------------:|
|           12033 | Bragança - Presencial    | porte_25pct |              12 |        41.753 |            54.192 |              55.421 |           -12.439 |             -13.668 |
|           12033 | Bragança - Presencial    | porte_50pct |              31 |        41.753 |            54.388 |              54.935 |           -12.635 |             -13.182 |
|           12033 | Bragança - Presencial    | porte_2x    |              37 |        41.753 |            54.750 |              54.935 |           -12.998 |             -13.182 |
|           12035 | Castanhal - Presencial   | porte_25pct |               9 |        44.827 |            55.665 |              54.914 |           -10.838 |             -10.087 |
|           12035 | Castanhal - Presencial   | porte_50pct |              20 |        44.827 |            55.151 |              55.421 |           -10.324 |             -10.594 |
|           12035 | Castanhal - Presencial   | porte_2x    |              21 |        44.827 |            55.500 |              55.906 |           -10.673 |             -11.079 |
|           12044 | Breves - Presencial      | porte_25pct |              16 |        44.831 |            53.155 |              53.068 |            -8.324 |              -8.237 |
|           12044 | Breves - Presencial      | porte_50pct |              32 |        44.831 |            54.556 |              55.211 |            -9.725 |             -10.380 |
|           12044 | Breves - Presencial      | porte_2x    |              38 |        44.831 |            54.996 |              55.211 |           -10.165 |             -10.380 |
|           12074 | Cametá - Presencial      | porte_25pct |               4 |        43.896 |            55.762 |              56.027 |           -11.865 |             -12.130 |
|           12074 | Cametá - Presencial      | porte_50pct |              12 |        43.896 |            55.932 |              56.027 |           -12.035 |             -12.130 |
|           12074 | Cametá - Presencial      | porte_2x    |              12 |        43.896 |            55.932 |              56.027 |           -12.035 |             -12.130 |
|           86396 | Belém - EaD              | porte_25pct |               6 |        34.739 |            44.892 |              45.154 |           -10.153 |             -10.416 |
|           86396 | Belém - EaD              | porte_50pct |               6 |        34.739 |            44.892 |              45.154 |           -10.153 |             -10.416 |
|           86396 | Belém - EaD              | porte_2x    |              10 |        34.739 |            46.217 |              45.699 |           -11.478 |             -10.960 |
|          114853 | Abaetetuba - Presencial  | porte_25pct |               1 |        44.201 |            62.485 |              62.485 |           -18.283 |             -18.283 |
|          114853 | Abaetetuba - Presencial  | porte_50pct |               9 |        44.201 |            57.246 |              57.139 |           -13.044 |             -12.938 |
|          114853 | Abaetetuba - Presencial  | porte_2x    |               9 |        44.201 |            57.246 |              57.139 |           -13.044 |             -12.938 |
|         1300375 | Salinópolis - Presencial | porte_25pct |              15 |        41.364 |            51.547 |              52.085 |           -10.183 |             -10.721 |
|         1300375 | Salinópolis - Presencial | porte_50pct |              42 |        41.364 |            54.831 |              55.378 |           -13.467 |             -14.014 |
|         1300375 | Salinópolis - Presencial | porte_2x    |              47 |        41.364 |            54.862 |              55.357 |           -13.498 |             -13.993 |

As diferenças variam com o critério de porte. Resultados estáveis em direção entre critérios recebem maior confiança descritiva; mudanças de sinal devem ser tratadas como sensibilidade relevante.

## Sensibilidade do desempenho

| cenario                | grupo   |   n_cursos |   media_cursos |   mediana_cursos |   media_ponderada_participantes |
|:-----------------------|:--------|-----------:|---------------:|-----------------:|--------------------------------:|
| todos                  | A       |          7 |         42.230 |           43.896 |                          43.323 |
| todos                  | B       |          1 |         54.141 |           54.141 |                          54.141 |
| todos                  | C       |          5 |         45.563 |           49.455 |                          47.889 |
| todos                  | D       |         27 |         44.826 |           43.582 |                          44.117 |
| todos                  | E       |        401 |         50.399 |           50.208 |                          48.757 |
| n_minimo_10            | A       |          7 |         42.230 |           43.896 |                          43.323 |
| n_minimo_10            | B       |          1 |         54.141 |           54.141 |                          54.141 |
| n_minimo_10            | C       |          3 |         49.371 |           49.455 |                          48.734 |
| n_minimo_10            | D       |         16 |         43.485 |           43.132 |                          43.634 |
| n_minimo_10            | E       |        233 |         50.786 |           50.445 |                          48.608 |
| presencial             | A       |          6 |         43.479 |           44.049 |                          43.780 |
| presencial             | B       |          1 |         54.141 |           54.141 |                          54.141 |
| presencial             | C       |          4 |         49.393 |           49.458 |                          48.760 |
| presencial             | D       |         23 |         45.560 |           44.984 |                          44.836 |
| presencial             | E       |        301 |         51.967 |           52.085 |                          52.616 |
| universidades_federais | A       |          7 |         42.230 |           43.896 |                          43.323 |
| universidades_federais | B       |          1 |         54.141 |           54.141 |                          54.141 |
| universidades_federais | C       |          4 |         49.393 |           49.458 |                          48.760 |
| universidades_federais | D       |         21 |         45.707 |           45.650 |                          44.481 |
| universidades_federais | E       |        206 |         52.280 |           52.387 |                          53.203 |

## Dimensões do processo formativo

| dimensao                        | itens                                                                                                          |   n_itens |   n_casos_completos |   alpha_cronbach | decisao                                                   |
|:--------------------------------|:---------------------------------------------------------------------------------------------------------------|----------:|--------------------:|-----------------:|:----------------------------------------------------------|
| organizacao_didatico_pedagogica | QE_I20, QE_I21, QE_I22, QE_I23, QE_I24, QE_I25, QE_I26, QE_I27, QE_I28, QE_I29, QE_I30, QE_I31, QE_I32, QE_I33 |        14 |                6531 |            0.954 | diagnóstico preliminar; exige validação teórica dos itens |
| atuacao_docente                 | QE_I34, QE_I35, QE_I36, QE_I37, QE_I38, QE_I39, QE_I40, QE_I41                                                 |         8 |               10141 |            0.932 | diagnóstico preliminar; exige validação teórica dos itens |
| infraestrutura_recursos         | QE_I42, QE_I43, QE_I44, QE_I45, QE_I46, QE_I47, QE_I48, QE_I49                                                 |         8 |                5339 |            0.943 | diagnóstico preliminar; exige validação teórica dos itens |
| oportunidades_formacao          | QE_I50, QE_I51, QE_I52, QE_I53, QE_I54, QE_I55, QE_I56, QE_I57, QE_I58                                         |         9 |               11161 |            0.951 | diagnóstico preliminar; exige validação teórica dos itens |
| integracao_teoria_pratica       | QE_I59, QE_I60, QE_I61, QE_I62, QE_I63, QE_I64, QE_I65, QE_I66                                                 |         8 |               11589 |            0.962 | diagnóstico preliminar; exige validação teórica dos itens |

Os agrupamentos são diagnósticos preliminares. Nenhuma dimensão deve ser incorporada ao relatório final sem conferência textual dos itens no questionário oficial.

## Decisões metodológicas

- manter média e mediana em paralelo;
- apresentar análises ponderadas e não ponderadas;
- informar cursos excluídos por N mínimo;
- usar benchmark amplo para contexto e benchmark comparável para contraste;
- não interpretar associações agregadas como relações individuais;
- não criar índice único de QE_I20–QE_I66.

## Limitações

- grupos A e B contêm poucos cursos da UFPA;
- critérios determinísticos de comparabilidade não equivalem a desenho causal;
- consistência interna não substitui validade de conteúdo;
- diferenças entre participantes oficiais e notas válidas precisam aparecer nas figuras e tabelas.