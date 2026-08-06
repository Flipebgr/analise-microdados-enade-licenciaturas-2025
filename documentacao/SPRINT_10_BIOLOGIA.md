# Sprint 10 — Ciências Biológicas com estudo focal de Soure

## Objetivo

Construir a base analítica nacional de Ciências Biológicas (`CO_GRUPO=1602`),
preservando o padrão metodológico do projeto e acrescentando um estudo focal da
oferta da UFPA em Soure (`CO_CURSO=104640`).

## Mudança do desenho comparativo

As cinco ofertas da UFPA possuem Conceito Enade 3 ou 4. Não existe oferta UFPA
com Conceito 1. Assim, o Grupo A permanece vazio e não é artificialmente
preenchido. O panorama geral mantém os grupos territoriais do projeto, enquanto
o estudo focal usa recortes exclusivos: Soure, UFPA sem Soure, outras IES do
Pará, Norte sem Pará e Brasil sem Norte.

## Unidade de análise

A unidade principal permanece `CO_CURSO`. Cada arquivo temático é tratado e
agregado separadamente antes da junção `one-to-one`. Não se usa posição da linha,
identificador artificial ou join individual entre arquivos temáticos.

## Produtos principais

- catálogo nacional e base analítica por curso;
- agregados de desempenho, demografia, trajetória, perfil socioeconômico,
  processo formativo e recomendação;
- comparações regionais e nacionais;
- benchmark estruturalmente comparável específico para Soure;
- comparação focal e perfil diferencial de Soure;
- percentis de desempenho de Soure no Brasil, Norte e Pará;
- desempenho individual de Soure somente com variáveis do arquivo de desempenho;
- 13 figuras iniciais;
- relatório piloto em Markdown.

## Benchmark de Soure

O benchmark inicial exclui a UFPA e seleciona cursos com a mesma modalidade,
categoria administrativa e organização acadêmica, além de porte entre 0,5 e 2
vezes o número de participantes de Soure. A Sprint 11 deverá executar análise de
sensibilidade do benchmark.

## Limitações

As comparações são descritivas. Relações entre indicadores provenientes de
arquivos diferentes são ecológicas. Nenhuma associação é interpretada como
causalidade individual.
