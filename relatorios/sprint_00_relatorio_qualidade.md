# Sprint 0 - Relatório de qualidade e validação inicial

## Resumo executivo
- Arquivos temáticos encontrados: **28**.
- Ofertas selecionadas da UFPA na tabela-mestra: **29**.
- Divergências de cruzamento: **0**.
- Erros estruturais: **0**.

## Regra de relacionamento
Os arquivos não possuem identificador público individual comum. A posição da linha não é uma chave. O fluxo permitido é: tratamento por arquivo, agregação por CO_CURSO, uma linha por curso e somente então junção das tabelas agregadas.

## Volumetria
| arquivo                  |   numero_linhas |   numero_colunas |   tamanho_bytes | encoding_detectado   |
|:-------------------------|----------------:|-----------------:|----------------:|:---------------------|
| microdados2025_arq1.txt  |          293082 |               10 |        13312075 | ascii                |
| microdados2025_arq2.txt  |          293082 |                5 |         7361853 | ascii                |
| microdados2025_arq3.txt  |          293082 |               23 |        93756019 | ascii                |
| microdados2025_arq4.txt  |          293082 |               49 |        31394979 | ascii                |
| microdados2025_arq5.txt  |          293082 |                3 |         5017186 | ascii                |
| microdados2025_arq6.txt  |          293082 |                3 |         4724104 | ascii                |
| microdados2025_arq7.txt  |          293082 |                3 |         5014095 | ascii                |
| microdados2025_arq8.txt  |          293082 |                3 |         5014085 | ascii                |
| microdados2025_arq9.txt  |          293082 |                3 |         5014091 | ascii                |
| microdados2025_arq10.txt |          293082 |                3 |         5020849 | ascii                |
| microdados2025_arq11.txt |          293082 |                3 |         5014081 | ascii                |
| microdados2025_arq12.txt |          293082 |                3 |         5014089 | ascii                |
| microdados2025_arq13.txt |          293082 |                3 |         5014099 | ascii                |
| microdados2025_arq14.txt |          293082 |                3 |         5014093 | ascii                |
| microdados2025_arq15.txt |          293082 |                3 |         5014093 | ascii                |
| microdados2025_arq16.txt |          293082 |                3 |         5014087 | ascii                |
| microdados2025_arq17.txt |          293082 |                3 |         5014093 | ascii                |
| microdados2025_arq18.txt |          293082 |                3 |         5014095 | ascii                |
| microdados2025_arq19.txt |          293082 |                3 |         5014095 | ascii                |
| microdados2025_arq20.txt |          293082 |                3 |         5014099 | ascii                |
| microdados2025_arq21.txt |          293082 |                3 |         5014083 | ascii                |
| microdados2025_arq22.txt |          293082 |                3 |         5063147 | ascii                |
| microdados2025_arq23.txt |          293082 |                3 |         5014085 | ascii                |
| microdados2025_arq24.txt |          293082 |                3 |         5014085 | ascii                |
| microdados2025_arq25.txt |          293082 |                3 |         5014087 | ascii                |
| microdados2025_arq26.txt |          293082 |                3 |         4557902 | ascii                |
| microdados2025_arq27.txt |          293082 |                3 |         4554591 | ascii                |
| microdados2025_arq28.txt |          293082 |                3 |         5014321 | ascii                |

## Tabela-mestra da UFPA
|   CO_GRUPO | AREA             |   CO_CURSO | MUNICIPIO   | MODALIDADE   |   PARTICIPANTES |   PCT_PADRAO_PROFICIENCIA |   CONCEITO_ENADE | SITUACAO_CONCEITO     | SITUACAO_CRUZAMENTO      |
|-----------:|:-----------------|-----------:|:------------|:-------------|----------------:|--------------------------:|-----------------:|:----------------------|:-------------------------|
|        702 | MATEMÁTICA       |     114853 | Abaetetuba  | Presencial   |              86 |                     0.209 |                1 | Conceito 1            | Correspondência validada |
|        702 | MATEMÁTICA       |      86396 | Belém       | EaD          |              16 |                     0.063 |                1 | Conceito 1            | Correspondência validada |
|        702 | MATEMÁTICA       |      11999 | Belém       | Presencial   |              61 |                     0.607 |                3 | Conceito superior a 1 | Correspondência validada |
|        702 | MATEMÁTICA       |      12033 | Bragança    | Presencial   |              34 |                     0.294 |                1 | Conceito 1            | Correspondência validada |
|        702 | MATEMÁTICA       |      12044 | Breves      | Presencial   |              31 |                     0.258 |                1 | Conceito 1            | Correspondência validada |
|        702 | MATEMÁTICA       |      12074 | Cametá      | Presencial   |              72 |                     0.25  |                1 | Conceito 1            | Correspondência validada |
|        702 | MATEMÁTICA       |      12035 | Castanhal   | Presencial   |              52 |                     0.327 |                1 | Conceito 1            | Correspondência validada |
|        702 | MATEMÁTICA       |    1300375 | Salinópolis | Presencial   |              26 |                     0.115 |                1 | Conceito 1            | Correspondência validada |
|        904 | LETRAS-PORTUGUÊS |     114850 | Abaetetuba  | Presencial   |              82 |                     0.695 |                3 | Conceito superior a 1 | Correspondência validada |
|        904 | LETRAS-PORTUGUÊS |     114876 | Altamira    | Presencial   |              47 |                     0.404 |                2 | Conceito superior a 1 | Correspondência validada |
|        904 | LETRAS-PORTUGUÊS |     115161 | Belém       | EaD          |              56 |                     0.375 |                1 | Conceito 1            | Correspondência validada |
|        904 | LETRAS-PORTUGUÊS |      27645 | Belém       | Presencial   |             150 |                     0.867 |                4 | Conceito superior a 1 | Correspondência validada |
|        904 | LETRAS-PORTUGUÊS |     114874 | Bragança    | Presencial   |              49 |                     0.714 |                3 | Conceito superior a 1 | Correspondência validada |
|        904 | LETRAS-PORTUGUÊS |     115013 | Breves      | Presencial   |              25 |                     0.64  |                3 | Conceito superior a 1 | Correspondência validada |
|        904 | LETRAS-PORTUGUÊS |     114846 | Cametá      | Presencial   |              69 |                     0.638 |                3 | Conceito superior a 1 | Correspondência validada |
|        904 | LETRAS-PORTUGUÊS |     114857 | Castanhal   | Presencial   |              38 |                     0.632 |                3 | Conceito superior a 1 | Correspondência validada |
|       1402 | FÍSICA           |      92851 | Abaetetuba  | Presencial   |              42 |                     0.19  |                1 | Conceito 1            | Correspondência validada |
|       1402 | FÍSICA           |    1330339 | Ananindeua  | Presencial   |              17 |                     0.176 |                1 | Conceito 1            | Correspondência validada |
|       1402 | FÍSICA           |    1202639 | Belém       | EaD          |              24 |                     0.042 |                1 | Conceito 1            | Correspondência validada |
|       1402 | FÍSICA           |      12022 | Belém       | Presencial   |              34 |                     0.618 |                3 | Conceito superior a 1 | Correspondência validada |
|       1402 | FÍSICA           |    1364837 | Salinópolis | Presencial   |              14 |                     0.214 |                1 | Conceito 1            | Correspondência validada |
|       1502 | QUÍMICA          |    1330344 | Ananindeua  | Presencial   |              20 |                     0.9   |                5 | Conceito superior a 1 | Correspondência validada |
|       1502 | QUÍMICA          |     114892 | Belém       | EaD          |               6 |                     0     |                1 | Conceito 1            | Correspondência validada |
|       1502 | QUÍMICA          |      12026 | Belém       | Presencial   |              27 |                     0.815 |                4 | Conceito superior a 1 | Correspondência validada |
|       6407 | Letras - Inglês  |     114877 | Altamira    | Presencial   |              21 |                     0.143 |                1 | Conceito 1            | Correspondência validada |
|       6407 | Letras - Inglês  |      23777 | Belém       | Presencial   |              85 |                     0.694 |                3 | Conceito superior a 1 | Correspondência validada |
|       6407 | Letras - Inglês  |     114875 | Bragança    | Presencial   |              41 |                     0.341 |                1 | Conceito 1            | Correspondência validada |
|       6407 | Letras - Inglês  |     114847 | Cametá      | Presencial   |              15 |                     0.133 |                1 | Conceito 1            | Correspondência validada |
|       6407 | Letras - Inglês  |      95652 | Soure       | Presencial   |              37 |                     0.054 |                1 | Conceito 1            | Correspondência validada |

## Divergências
Nenhuma divergência de existência entre as duas fontes.

## Erros estruturais
Nenhum erro estrutural detectado.

## Limitações obrigatórias
- Não realizar junções individuais entre os 28 arquivos.
- Não tratar curso sem conceito como Conceito 1.
- Não interpretar associações agregadas como relações individuais.
- Não comparar notas brutas entre áreas distintas sem padronização.