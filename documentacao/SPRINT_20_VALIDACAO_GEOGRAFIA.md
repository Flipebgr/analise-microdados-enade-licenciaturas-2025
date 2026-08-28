# Sprint 20 — Validação analítica de Geografia

## Objetivo

Aprofundar e validar os resultados da Sprint 19, mantendo `CO_CURSO` como unidade principal e o contraste interno entre as duas ofertas UFPA Conceito 3 e as duas ofertas UFPA Conceito 4.

## Escopo

- 254 cursos de Geografia;
- 4 ofertas da UFPA;
- nenhuma oferta UFPA Conceito Enade 1;
- contraste interno Conceito 3 × Conceito 4;
- auditoria de participação, desempenho e Ns;
- cinco cenários de benchmark por oferta;
- 20 combinações oferta-cenário;
- perfil demográfico, socioeconômico e trajetória;
- QE_I20–QE_I66 item a item;
- QE_I68, QE_I69 e QE_I70 separadamente;
- outliers;
- associações ecológicas;
- comparações regionais e nacionais.

## Decisões metodológicas

O Grupo A permanece vazio. Conceito 3 não é tratado como insuficiência. As duas ofertas de cada estrato permitem um contraste interno mais equilibrado que áreas com apenas uma oferta de referência, mas o N institucional continua pequeno e não sustenta inferência causal.

As relações entre temas diferentes permanecem no nível ecológico do curso. Os benchmarks reduzem somente parte da heterogeneidade observável.

## Saídas

A Sprint 20 gera 11 tabelas derivadas, 6 figuras validadas e:

`relatorios/sprint_20_validacao_geografia.md`

## Execução

```powershell
python executar_sprint_20.py
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```
