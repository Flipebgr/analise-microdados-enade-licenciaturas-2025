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

## 3. Validação inicial

A validação de fontes e estrutura é executada por:

```powershell
python executar_sprint_00.py
```

Ela verifica fontes, cadastro, identificadores, relação da UFPA, tabela-mestra e integridade básica.

## 4. Pipelines por área

Os executores históricos continuam disponíveis enquanto não houver uma CLI unificada.

### Matemática

```powershell
python executar_sprint_01.py
python executar_sprint_02.py
python executar_sprint_03.py
```

### Física

```powershell
python executar_sprint_04.py
python executar_sprint_05.py
python executar_sprint_06.py
python executar_relatorio_regional_fisica.py
```

### Letras–Inglês

```powershell
python executar_sprint_07.py
python executar_sprint_08.py
python executar_sprint_09.py
```

### Ciências Biológicas

```powershell
python executar_sprint_10.py
python executar_sprint_11.py
python executar_sprint_12.py
```

### Pedagogia

```powershell
python executar_sprint_13.py
python executar_sprint_14.py
python executar_sprint_15.py
```

### Letras–Português

```powershell
python executar_sprint_16.py
python executar_sprint_17.py
```

O relatório final de Letras–Português deve ser executado pelo executor da Sprint 18 quando essa etapa estiver presente e sincronizada no branch atual.

### Geografia

```powershell
python executar_sprint_19.py
python executar_sprint_20.py
python executar_sprint_21.py
```

### Química

Química está registrada na configuração (`CO_GRUPO=1502`), mas deve ser retomada com um pipeline novo a partir do núcleo atual antes de qualquer resultado ser considerado validado.

## 5. Ordem típica por área

```text
base analítica
→ validação analítica
→ relatório final
```

O relatório final depende dos produtos agregados e figuras gerados nas etapas anteriores.

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
