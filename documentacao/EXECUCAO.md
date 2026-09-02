# Execução e reprodução

## 1. Ambiente

Requisitos:

- Python 3.11 ou superior;
- Git;
- ambiente virtual;
- dependências de `requirements.txt`.

No Windows/PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Fontes locais

Copie para `dados_brutos/`:

```text
microdados_enade_licenciaturas_2025.zip
conceito_enade_licenciaturas.xlsx
```

O arquivo `config.yaml` aponta para esses caminhos.

As fontes brutas não devem ser versionadas.

## 3. Executor unificado

A interface operacional preferencial é:

```powershell
python executar.py --listar
```

Exemplos:

```powershell
python executar.py fontes
python executar.py matematica base
python executar.py matematica validacao
python executar.py matematica relatorio
python executar.py fisica regional
python executar.py geografia tudo
```

As etapas padronizadas são:

```text
base
validacao
relatorio
tudo
```

Física possui adicionalmente:

```text
regional
```

`tudo` executa base → validação → relatório e interrompe imediatamente se uma etapa retornar erro.

## 4. Compatibilidade com executores históricos

Os executores históricos ficam em `scripts/pipelines/` porque ainda contêm a orquestração concreta de cada etapa. `executar.py` funciona como uma interface única sobre esses executores.

Eles não devem ser removidos até que a lógica de orquestração seja migrada para módulos reutilizáveis sob `src/`.

O antigo `executar_sprint_07_validacao.py` foi removido; a validação efetiva de Letras–Inglês é executada pela Sprint 08.

## 5. Pipelines registrados

| Área | Base | Validação | Relatório | Extra |
|---|---:|---:|---:|---|
| Fontes | — | Sprint 00 | — | — |
| Matemática | 01 | 02 | 03 | — |
| Física | 04 | 05 | 06 | regional |
| Letras–Inglês | 07 | 08 | 09 | — |
| Ciências Biológicas | 10 | 11 | 12 | — |
| Pedagogia | 13 | 14 | 15 | — |
| Letras–Português | 16 | 17 | 18 | — |
| Geografia | 19 | 20 | 21 | — |

Se o arquivo executor de uma etapa ainda não estiver integrado na branch atual, `executar.py` informa o problema e retorna código 2.

Química permanece fora desse registro operacional até que seu pipeline seja reconstruído e validado a partir do núcleo compartilhado.

## 6. Testes

Rodada rápida:

```powershell
python -m pytest -q -m "not integration"
```

Integração:

```powershell
python -m pytest -q -m integration
```

Suíte completa:

```powershell
python -m pytest -q
```

Lint:

```powershell
python -m ruff check .
```

No Windows, prefira `python -m pytest` e `python -m ruff`.

## 7. Testes ignorados

Um teste de integração pode aparecer como `skipped` quando a base processada ou o artefato real necessário não existe naquele computador.

Isso não equivale automaticamente a falha. Antes do merge de uma área, os produtos da área em desenvolvimento devem estar disponíveis e seus testes de integração devem executar.

## 8. Conversão para PDF

DOCX e Markdown são produtos válidos mesmo sem LibreOffice.

Quando o LibreOffice estiver disponível, o módulo compartilhado de conversão pode produzir PDF. Ausência do conversor não deve transformar automaticamente o pipeline analítico em falha.

## 9. Git

Fluxo recomendado:

```text
refactor/nucleo-compartilhado
↓
branch de sprint/refatoração
↓
execução
↓
pytest + ruff
↓
commit
↓
push
↓
Pull Request
↓
merge na branch de integração
```

Não misturar limpeza estrutural extensa com desenvolvimento analítico de uma área no mesmo commit.
