# Desempenho dos cursos de Física da UFPA no contexto regional e nacional

## Resumo

O relatório compara a nota geral (NT_GER) de 131 participantes válidos distribuídos em 5 ofertas de Física da UFPA com os cursos da Região Norte, das demais regiões e do Brasil. A análise combina médias ponderadas pelos participantes e estatísticas entre cursos. A unidade principal permanece CO_CURSO; não há reconstrução de vínculos individuais entre arquivos temáticos.

**Palavras-chave:** Enade; Física; UFPA; Região Norte; comparação regional; NT_GER.

# 1 Introdução

O objetivo é posicionar o desempenho agregado das ofertas de Física da UFPA diante da Região Norte, das demais regiões brasileiras e do Brasil geral. A pergunta central é: como a NT_GER das ofertas da UFPA se posiciona nesses referenciais, considerando a heterogeneidade de modalidade, organização acadêmica, categoria administrativa e porte?

# 2 Metodologia

A base foi construída previamente por curso. O desempenho foi agregado no arquivo temático de notas por CO_CURSO e relacionado ao cadastro regional somente após a obtenção de uma linha por curso. A média ponderada usa nt_ger_count como peso. A média e a mediana entre cursos atribuem o mesmo peso a cada oferta. Os intervalos de 95% foram estimados por reamostragem de cursos com semente fixa 2025. Esses intervalos descrevem a incerteza entre cursos e não corrigem integralmente a dependência institucional.

# 3 Cobertura e resultados gerais

| grupo            |   n_cursos |   n_participantes |   media_ponderada |   ic95_inf |   ic95_sup |   media_cursos |   mediana_cursos |   dp_cursos |
|:-----------------|-----------:|------------------:|------------------:|-----------:|-----------:|---------------:|-----------------:|------------:|
| UFPA             |          5 |               131 |             42.15 |      34.81 |      49.66 |          41.72 |            42.33 |        8.52 |
| Norte sem UFPA   |         20 |               232 |             43.41 |      40.93 |      46.26 |          44.53 |            46.07 |        7.24 |
| Norte            |         25 |               363 |             42.96 |      40.07 |      46.46 |          43.97 |            44.05 |        7.41 |
| Nordeste         |         79 |              1059 |             50.73 |      48.80 |      52.70 |          50.84 |            51.48 |        7.92 |
| Sudeste          |         74 |               835 |             57.41 |      55.19 |      59.80 |          56.50 |            56.98 |        8.69 |
| Sul              |         41 |               734 |             53.87 |      51.94 |      59.59 |          56.16 |            56.24 |       10.20 |
| Centro-Oeste     |         18 |               173 |             53.05 |      47.91 |      57.85 |          52.87 |            53.62 |        9.57 |
| Brasil geral     |        237 |              3164 |             52.45 |      51.11 |      53.84 |          52.96 |            53.04 |        9.47 |
| Brasil sem UFPA  |        232 |              3033 |             52.90 |      51.66 |      54.33 |          53.20 |            53.28 |        9.36 |
| Brasil sem Norte |        212 |              2801 |             53.68 |      52.40 |      55.16 |          54.02 |            54.20 |        9.13 |

# 4 Ofertas da UFPA

A média ponderada da UFPA foi 42,2. Entre as ofertas, Belém — Presencial apresentou a maior média (54,4; N=34), enquanto Belém — EaD apresentou a menor (30,9; N=24). A amplitude interna mostra que uma média institucional isolada não representa adequadamente a heterogeneidade das ofertas.

|   CO_CURSO | ROTULO_OFERTA            |   CONCEITO_ENADE_NUM |   nt_ger_count |   nt_ger_mean |   nt_ger_median |   dif_norte_sem_ufpa |   dif_brasil_sem_ufpa |   percentil_norte_sem_ufpa |   percentil_brasil_sem_ufpa |
|-----------:|:-------------------------|---------------------:|---------------:|--------------:|----------------:|---------------------:|----------------------:|---------------------------:|----------------------------:|
|      12022 | Belém — Presencial       |                 3.00 |             34 |         54.45 |           58.25 |                11.04 |                  1.55 |                      95.00 |                       56.03 |
|    1364837 | Salinópolis — Presencial |                 1.00 |             14 |         42.47 |           43.45 |                -0.94 |                -10.43 |                      40.00 |                       11.21 |
|    1330339 | Ananindeua — Presencial  |                 1.00 |             17 |         42.33 |           40.84 |                -1.08 |                -10.57 |                      40.00 |                       11.21 |
|      92851 | Abaetetuba — Presencial  |                 1.00 |             42 |         38.45 |           38.74 |                -4.96 |                -14.45 |                      20.00 |                        5.60 |
|    1202639 | Belém — EaD              |                 1.00 |             24 |         30.91 |           28.60 |               -12.50 |                -21.99 |                       5.00 |                        1.29 |

# 5 UFPA e Região Norte

A comparação exclusiva entre UFPA e Norte sem UFPA resultou em diferença de -1,3 ponto(s) na NT_GER e tamanho de efeito d=-0,09. A Região Norte completa inclui a própria UFPA e, por isso, é apresentada apenas como benchmark descritivo sobreposto.

# 6 UFPA, demais regiões e Brasil

Frente ao Brasil sem UFPA, a diferença da média ponderada da UFPA foi -10,7 ponto(s), com d=-0,65. O Brasil geral é mantido como referência descritiva; os contrastes inferenciais usam grupos exclusivos.

| referencia   | comparador       |   media_referencia |   media_comparador |   diferenca |   cohen_d |   n_cursos_referencia |   n_cursos_comparador |   n_participantes_referencia |   n_participantes_comparador |
|:-------------|:-----------------|-------------------:|-------------------:|------------:|----------:|----------------------:|----------------------:|-----------------------------:|-----------------------------:|
| UFPA         | Norte sem UFPA   |             42.154 |             43.410 |      -1.256 |    -0.087 |                     5 |                    20 |                          131 |                          232 |
| UFPA         | Nordeste         |             42.154 |             50.726 |      -8.572 |    -0.550 |                     5 |                    79 |                          131 |                         1059 |
| UFPA         | Sudeste          |             42.154 |             57.407 |     -15.253 |    -0.905 |                     5 |                    74 |                          131 |                          835 |
| UFPA         | Sul              |             42.154 |             53.867 |     -11.713 |    -0.706 |                     5 |                    41 |                          131 |                          734 |
| UFPA         | Centro-Oeste     |             42.154 |             53.047 |     -10.893 |    -0.668 |                     5 |                    18 |                          131 |                          173 |
| UFPA         | Brasil sem UFPA  |             42.154 |             52.898 |     -10.744 |    -0.647 |                     5 |                   232 |                          131 |                         3033 |
| Norte        | Brasil sem Norte |             42.957 |             53.684 |     -10.728 |    -0.654 |                    25 |                   212 |                          363 |                         2801 |

# 7 Análise de sensibilidade

| recorte                | grupo           |   n_cursos |   n_participantes |   media_ponderada |   media_cursos |   mediana_cursos |   ic95_inf |   ic95_sup |
|:-----------------------|:----------------|-----------:|------------------:|------------------:|---------------:|-----------------:|-----------:|-----------:|
| Todos                  | UFPA            |          5 |               131 |             42.15 |          41.72 |            42.33 |      34.81 |      49.66 |
| Todos                  | Norte sem UFPA  |         20 |               232 |             43.41 |          44.53 |            46.07 |      40.93 |      46.26 |
| Todos                  | Brasil sem UFPA |        232 |              3033 |             52.90 |          53.20 |            53.28 |      51.66 |      54.33 |
| Presencial             | UFPA            |          4 |               107 |             44.68 |          44.43 |            42.40 |      38.91 |      52.72 |
| Presencial             | Norte sem UFPA  |         18 |               210 |             43.99 |          44.80 |            46.07 |      41.63 |      46.71 |
| Presencial             | Brasil sem UFPA |        196 |              2292 |             53.86 |          54.02 |            54.27 |      52.30 |      55.44 |
| EaD                    | UFPA            |          1 |                24 |             30.91 |          30.91 |            30.91 |      30.91 |      30.91 |
| EaD                    | Norte sem UFPA  |          2 |                22 |             37.90 |          42.07 |            42.07 |      32.89 |      51.25 |
| EaD                    | Brasil sem UFPA |         36 |               741 |             49.93 |          48.72 |            48.88 |      47.33 |      51.08 |
| N válido >= 10         | UFPA            |          5 |               131 |             42.15 |          41.72 |            42.33 |      34.81 |      49.66 |
| N válido >= 10         | Norte sem UFPA  |         11 |               181 |             42.01 |          42.41 |            41.42 |      39.13 |      44.79 |
| N válido >= 10         | Brasil sem UFPA |        115 |              2435 |             52.72 |          53.22 |            52.58 |      51.29 |      54.39 |
| N válido >= 20         | UFPA            |          3 |               100 |             42.08 |          41.27 |            38.45 |      30.90 |      54.45 |
| N válido >= 20         | Norte sem UFPA  |          4 |                91 |             42.57 |          42.66 |            42.73 |      40.34 |      45.03 |
| N válido >= 20         | Brasil sem UFPA |         31 |              1270 |             51.57 |          51.54 |            50.15 |      49.36 |      53.98 |
| Universidades federais | UFPA            |          5 |               131 |             42.15 |          41.72 |            42.33 |      34.81 |      49.66 |
| Universidades federais | Norte sem UFPA  |         19 |               216 |             43.87 |          44.91 |            46.09 |      41.18 |      46.79 |
| Universidades federais | Brasil sem UFPA |        160 |              1861 |             53.50 |          53.55 |            53.76 |      51.81 |      55.15 |

# 8 Discussão

A posição da UFPA deve ser interpretada em conjunto com a forte heterogeneidade entre suas ofertas. Diferenças regionais podem refletir simultaneamente composição institucional, modalidade, porte, perfil discente e condições territoriais. O desenho é descritivo e ecológico; não identifica efeito causal da região ou da instituição sobre a nota individual.

# 9 Conclusão

O relatório fornece três perspectivas complementares: desempenho de cada oferta da UFPA, média institucional da UFPA e referências regionais e nacionais exclusivas. A comparação com Norte sem UFPA e Brasil sem UFPA evita que a própria instituição componha o benchmark usado para avaliá-la. As conclusões devem priorizar a heterogeneidade entre ofertas e a estabilidade dos resultados nos recortes de sensibilidade.

# Figuras

Figura 1 - 01 Nt Ger Ufpa Referencias

`C:/Users/Filipe Menezes/Desktop/PROJETO - Análise de microdados - ENAD/figuras/fisica/regional/01_nt_ger_ufpa_referencias.png`

Figura 2 - 02 Ufpa Regioes Brasil

`C:/Users/Filipe Menezes/Desktop/PROJETO - Análise de microdados - ENAD/figuras/fisica/regional/02_ufpa_regioes_brasil.png`

Figura 3 - 03 Distribuicao Cursos Regiao

`C:/Users/Filipe Menezes/Desktop/PROJETO - Análise de microdados - ENAD/figuras/fisica/regional/03_distribuicao_cursos_regiao.png`

Figura 4 - 04 Diferencas Para Ufpa

`C:/Users/Filipe Menezes/Desktop/PROJETO - Análise de microdados - ENAD/figuras/fisica/regional/04_diferencas_para_ufpa.png`

Figura 5 - 05 Percentis Ofertas Ufpa

`C:/Users/Filipe Menezes/Desktop/PROJETO - Análise de microdados - ENAD/figuras/fisica/regional/05_percentis_ofertas_ufpa.png`

Figura 6 - 06 Sensibilidade Recortes

`C:/Users/Filipe Menezes/Desktop/PROJETO - Análise de microdados - ENAD/figuras/fisica/regional/06_sensibilidade_recortes.png`

# Limitações

- O relatório usa estatísticas agregadas por curso; não há vinculação individual entre região e nota entre arquivos.
- A média ponderada é reproduzida a partir de médias e N por curso; a mediana regional individual não é estimada.
- Os intervalos bootstrap reamostram cursos e são descritivos.
- Comparações amplas não substituem benchmark comparável por modalidade, categoria, organização e porte.
- Tucuruí, CO_CURSO 1627581, não entra nos cálculos por não ter sido localizado nas fontes analíticas usadas.