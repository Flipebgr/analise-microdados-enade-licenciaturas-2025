# Sprint 07 — Letras–Inglês

## Objetivo

Construir o piloto nacional de Letras–Inglês (`CO_GRUPO=6407`) com foco nas ofertas da UFPA, especialmente as ofertas de Conceito Enade 1.

## Unidade e relacionamentos

A unidade final é `CO_CURSO`. Cada arquivo temático é tratado e agregado isoladamente. As junções ocorrem somente após a produção de uma linha por curso e são validadas como `one-to-one`.

## Ofertas informadas da UFPA

- Belém: Conceito 3;
- Altamira: Conceito 1;
- Bragança: Conceito 1;
- Cametá: Conceito 1;
- Soure: Conceito 1.

A relação é validada contra a planilha de Conceito Enade e o cadastro dos microdados. Ausência de conceito permanece distinta de Conceito 1.

## Produtos

- catálogo e base analítica por curso;
- agregados de desempenho, demografia, trajetória, perfil socioeconômico, processo formativo e recomendação;
- benchmarks amplos e comparáveis;
- comparações regionais e nacionais com média simples e média ponderada por participantes;
- oito figuras;
- relatório piloto em Markdown.

## Limitações

Não é realizado join individual entre arquivos. Relações entre desempenho, perfil e percepção somente podem ser interpretadas no nível ecológico do curso. Os benchmarks são descritivos, sem interpretação causal.
