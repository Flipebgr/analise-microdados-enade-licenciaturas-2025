# Execução e reprodução

## 1. Estado atual

O branch operacional contém apenas a infraestrutura compartilhada e a validação das fontes. Pipelines de áreas já concluídas foram aposentados depois da entrega.

A reprodução histórica de uma área encerrada deve usar o snapshot/tag criado antes da aposentadoria, e não o branch operacional atual.

## 2. Ambiente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 3. Fontes locais

Em `dados_brutos/`:

```text
microdados_enade_licenciaturas_2025.zip
conceito_enade_licenciaturas.xlsx
```

Para validar os contratos de 2017, as fontes opcionais ficam em:

```text
dados_brutos/enade_2017/microdados_enade_2017_LGPD.zip
dados_brutos/enade_2017/resultados_conceito_enade_2017.xlsx
```

Ausência dessas fontes produz `skip` explícito somente nos testes de integração. Testes unitários não dependem de `dados_brutos/`.

## 4. Executor operacional

```powershell
python executar.py --listar
```

No estado atual:

```powershell
python executar.py fontes
```

Esse comando despacha para:

```text
scripts/pipelines/executar_sprint_00.py
```

## 5. Novas áreas

Uma nova área deve nascer em branch própria a partir de `main`.

Fluxo:

```text
main
→ feature/<area>-base
→ implementação
→ validação
→ relatório
→ apresentação/entrega
→ merge em main
→ arquivamento da entrega
→ aposentadoria do código específico quando a área estiver encerrada
```

O núcleo compartilhado deve ser reutilizado; módulos específicos só devem existir enquanto necessários para o trabalho da área.

## 6. Testes

```powershell
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```

Os contratos declarativos são selecionados pelo ano em `src/edicoes/`. As áreas são resolvidas por `(edição, slug)`; exemplos: `(2017, biologia_bacharelado)` e `(2025, biologia)`.

A CLI operacional continua limitada à validação legada de fontes nesta fase. A seleção de edição pela CLI e a leitura efetiva dos novos contratos pertencem à Fase 2.

## 7. Reproduzir uma entrega antiga

Não reintroduza o código aposentado na `main` apenas para consulta.

Use:

1. a entrega arquivada no Drive;
2. o histórico Git;
3. a tag `archive/pre-aposentadoria-areas` ou snapshot equivalente.

Se for necessário corrigir uma entrega histórica excepcionalmente, crie branch específica a partir do commit/tag correspondente.
