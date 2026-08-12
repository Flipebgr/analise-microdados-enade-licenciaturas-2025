# Sprint 13 — Pedagogia: base analítica e panorama inicial

## Objetivo

Incorporar Pedagogia (`CO_GRUPO=2001`) ao núcleo compartilhado e produzir a base analítica nacional por `CO_CURSO`, com panorama das ofertas da UFPA e comparações territoriais e estruturais.

## Relação validada na planilha oficial

A planilha `conceito_enade_licenciaturas.xlsx` contém sete ofertas da UFPA:

| CO_CURSO | Município | Modalidade | Inscritos | Participantes | Proficiência | Conceito |
|---:|---|---|---:|---:|---:|---:|
| 11996 | Belém | Presencial | 341 | 280 | 84,6% | 4 |
| 12048 | Altamira | Presencial | 56 | 51 | 80,4% | 4 |
| 12061 | Bragança | Presencial | 83 | 75 | 84,0% | 4 |
| 12069 | Cametá | Presencial | 148 | 122 | 83,6% | 4 |
| 12085 | Castanhal | Presencial | 86 | 63 | 90,5% | 5 |
| 12111 | Breves | Presencial | 51 | 42 | 85,7% | 4 |
| 38276 | Abaetetuba | Presencial | 124 | 111 | 78,4% | 4 |

Não há oferta UFPA com Conceito Enade 1. O Grupo A permanece vazio e nenhum curso é recodificado como Conceito 1.

## Desenho analítico

A pergunta orientadora é:

> Quais características de desempenho, participação, composição discente, trajetória acadêmica, condições socioeconômicas e avaliação do processo formativo diferenciam as ofertas de Pedagogia da UFPA entre si e em relação a cursos comparáveis no Pará, Região Norte e Brasil?

O contraste interno usa:

- UFPA — Conceito 5: Castanhal;
- UFPA — Conceito 4: seis demais ofertas;
- outras IES do Pará;
- Norte sem Pará;
- Brasil sem Norte.

Castanhal é uma referência interna para contraste, não um caso causal e não uma medida normativa de excelência.

## Integridade

- unidade principal: `CO_CURSO`;
- arquivos temáticos tratados separadamente;
- tratamento de ausentes antes da agregação;
- uma linha por curso antes das junções;
- junções agregadas one-to-one;
- nenhuma reconstrução de estudante;
- nenhuma associação individual entre arquivos temáticos;
- relações entre temas distintos somente em nível ecológico;
- nenhuma média única de `QE_I20–QE_I66` sem validação.

## Benchmarks

Cada oferta UFPA recebe benchmark externo próprio com:

- mesma modalidade;
- mesma categoria administrativa;
- mesma organização acadêmica;
- participantes entre 0,5x e 2x da oferta-alvo;
- exclusão da própria UFPA.

A Sprint 14 deverá testar a sensibilidade desses critérios.

## Produtos principais

- `dados_processados/pedagogia/base_analitica_cursos.csv`;
- agregados temáticos por curso;
- `benchmark_comparavel_cursos.csv`;
- `benchmark_comparavel_resumo.csv`;
- `comparacoes_regionais_nacionais.csv`;
- `comparacao_recortes.csv`;
- `comparacao_interna_ufpa.csv`;
- 13 figuras;
- `relatorios/sprint_13_piloto_pedagogia.md`.

## Próxima etapa

A Sprint 14 aprofundará:

- auditoria de presença e desempenho;
- sensibilidade dos benchmarks;
- diferença interna entre Castanhal e ofertas Conceito 4;
- processo formativo item a item e dimensões teoricamente validadas;
- perfil diferencial por oferta;
- recomendação;
- associações ecológicas e outliers.
