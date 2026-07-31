# Refactor 06 — Migração de Matemática para o núcleo compartilhado

## Objetivo

Migrar o pipeline de Matemática para os contratos centrais de configuração por área, catálogo, grupos comparativos, junções por `CO_CURSO` e validação estrutural, sem alterar resultados analíticos, figuras ou relatórios já validados.

## Componentes centralizados

- configuração `MATEMATICA` (`CO_GRUPO=702`, `CO_IES=569`);
- filtro e normalização do catálogo;
- junções agregadas com validação `one_to_one`;
- grupos comparativos exclusivos;
- unicidade por `CO_CURSO`;
- validação da área e do número de ofertas da UFPA.

## Componentes específicos preservados

As agregações temáticas, os indicadores, os benchmarks, as figuras e a redação dos relatórios continuam nos módulos existentes. A migração não cria ligação individual entre arquivos temáticos.

## Contrato de regressão

- 482 cursos de Matemática;
- 8 ofertas da UFPA;
- 7 ofertas da UFPA com Conceito Enade 1;
- 7 figuras principais;
- uma linha por `CO_CURSO`;
- conceito ausente distinto de Conceito Enade 1.

## Execução

```powershell
python executar_refactor_06.py
pytest -q -m "not integration"
pytest -q -m integration
pytest -q
ruff check .
python executar_sprint_01.py
python executar_sprint_02.py
python executar_sprint_03.py
```
