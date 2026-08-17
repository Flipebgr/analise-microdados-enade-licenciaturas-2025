# Sprint 17 — Validação analítica de Letras–Português

## Objetivo

Aprofundar e validar os resultados da Sprint 16, mantendo `CO_CURSO` como unidade principal e Belém EaD (`CO_CURSO=115161`) como a única oferta da UFPA com Conceito Enade 1.

## Escopo

- 340 cursos de Letras–Português;
- 8 ofertas localizadas da UFPA;
- Grupo A com uma única oferta: Belém EaD, Conceito 1;
- Grupo B com as sete ofertas UFPA de conceito superior;
- grupos C, D e E exclusivos;
- Soure preservada como oferta inicialmente informada, porém não localizada nas fontes de 2025;
- auditoria de participação, desempenho e Ns;
- sensibilidade dos grupos A–E;
- sensibilidade do benchmark estrutural da oferta Conceito 1;
- perfil demográfico, socioeconômico e trajetória;
- QE_I20–QE_I66 item a item;
- QE_I68, QE_I69 e QE_I70 separadamente;
- outliers;
- associações ecológicas;
- comparações regionais e nacionais.

## Decisões metodológicas

A oferta Conceito 1 é uma única unidade institucional; portanto, não é tratada como população independente para inferência. Os benchmarks são descritivos e reduzem apenas parte da heterogeneidade observável. Relações entre temas distintos permanecem ecológicas. Não há reconstrução individual entre arquivos temáticos.

## Saídas

A Sprint 17 gera 11 tabelas derivadas, 6 figuras validadas e o relatório:

`relatorios/sprint_17_validacao_letras_portugues.md`

## Execução

```cmd
python executar_sprint_17.py
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```
