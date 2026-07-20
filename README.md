# Análise de Microdados - ENADE Licenciaturas 2025

Projeto para análise das ofertas da UFPA em Matemática, Letras-Português, Física, Letras-Inglês e Química, com foco nas ofertas de Conceito Enade 1.

## Sprint atual

**Sprint 0 - Preparação, auditoria e validação das fontes.**

A sprint inventaria o pacote, valida os 28 arquivos, identifica a UFPA, cruza os cursos selecionados com a planilha de Conceito Enade e gera a tabela-mestra.

## Requisitos

- Python 3.11 ou superior;
- VS Code;
- Git;
- aproximadamente 1 GB livre para ambiente, extração e produtos intermediários.

## Configuração no Windows/PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copie para `dados_brutos/`:

- `microdados_enade_licenciaturas_2025.zip`;
- `conceito_enade_licenciaturas.xlsx`.

Execute:

```powershell
python executar_sprint_00.py
```

Testes:

```powershell
pytest -q
```

Qualidade:

```powershell
ruff check .
```

## Principais saídas

- `dados_processados/manifesto_arquivos.csv`;
- `dados_processados/inventario_microdados.csv`;
- `dados_processados/ausencias_amostra.csv`;
- `dados_processados/tabela_mestra_ufpa.csv`;
- `dados_processados/divergencias_ufpa.csv`;
- `relatorios/sprint_00_relatorio_qualidade.md`;
- `logs/sprint_00.log`.

## Regra metodológica central

Os 28 arquivos não podem ser unidos no nível individual. A posição da linha não identifica a mesma pessoa entre temas. O fluxo permitido é: tratamento separado, agregação por `CO_CURSO`, uma linha por curso e junção 1:1 entre tabelas agregadas.

## Git/GitHub

Branch sugerida:

```text
sprint/00-validacao-fontes
```

Após validação local:

```powershell
git add .
git commit -m "feat(sprint-00): implementa auditoria inicial dos microdados"
git push -u origin sprint/00-validacao-fontes
```

Os dados brutos não são enviados ao GitHub.
