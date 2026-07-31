# Refactor 05 — migração de Física para o núcleo compartilhado

## Objetivo

Migrar os contratos estruturais do pipeline de Física para `src/core`, sem alterar resultados, produtos ou regras específicas da licenciatura.

## Componentes migrados

- configuração da área por `FISICA`;
- filtro e preparação do catálogo por `preparar_catalogo_area`;
- junções agregadas por `juntar_por_curso`;
- validação estrutural por `validar_base_area`;
- classificação comparativa parametrizada por área;
- validação de uma linha por `CO_CURSO`.

## Componentes específicos preservados

Permanecem em `src/fisica` as agregações temáticas, análise de dificuldade, presença, desempenho, benchmarks, figuras, relatórios e a regra documental de Tucuruí (`CO_CURSO=1627581`) não localizado nas fontes utilizadas.

## Contratos metodológicos

- unidade principal: `CO_CURSO`;
- nenhuma junção individual entre arquivos temáticos;
- junções somente após agregação por curso;
- duplicidades são rejeitadas antes da junção;
- conceito ausente permanece ausente e não integra o grupo de Conceito Enade 1;
- grupos comparativos independentes permanecem exclusivos.

## Regressão esperada

- 257 cursos de Física;
- 5 ofertas localizadas da UFPA;
- 4 ofertas da UFPA com Conceito Enade 1;
- Tucuruí não inserido artificialmente;
- 13 figuras na Sprint 4;
- 20 benchmarks e 4 figuras validadas na Sprint 5;
- 6 figuras e 4 tabelas no relatório regional.

## Comandos

```powershell
python executar_refactor_05.py
pytest -q -m "not integration"
pytest -q -m integration
pytest -q
ruff check .
python executar_sprint_04.py
python executar_sprint_05.py
python executar_sprint_06.py
python executar_relatorio_regional_fisica.py
```
