# Refactor 03 — testes unitários e de integração

## Objetivo

Separar verificações isoladas da lógica analítica dos testes que dependem das bases processadas, figuras e relatórios reais do projeto.

## Categorias

### Testes unitários

Localizados em `tests/unit/`. Devem utilizar DataFrames sintéticos, `tmp_path` e funções puras ou de escopo restrito. Não podem depender de `dados_processados`, figuras ou relatórios previamente gerados.

### Testes de integração

Localizados em `tests/integration/`. Verificam produtos reais de Matemática e Física e recebem o marcador `integration` por localização.

## Comandos

```powershell
pytest -q -m "not integration"
pytest -q -m integration
pytest -q
ruff check .
```

O comando padrão continua executando toda a suíte. O marcador permite uma rodada rápida durante o desenvolvimento sem eliminar a validação integral antes do merge.

## Contratos metodológicos testados

- uma linha por `CO_CURSO` após agregação;
- bloqueio de duplicidade em junções agregadas;
- ausência de conceito distinta de Conceito Enade 1;
- exclusividade dos grupos A–E;
- distinção entre média simples de cursos e média ponderada por participantes;
- preservação dos produtos de Matemática e Física.

## Artefatos antigos

Testes de integração não devem considerar apenas a existência de um arquivo. Sempre que viável, também validam tamanho, conteúdo, contagens e unicidade. Geradores que aceitam destino parametrizado devem usar `tmp_path`.
