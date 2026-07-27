# Análise de Microdados — ENADE Licenciaturas 2025

Projeto reproduzível para analisar as ofertas da UFPA em Matemática, Letras–Português, Física, Letras–Inglês e Química, com foco nas ofertas de Conceito Enade 1.

## Sprint atual

**Sprint 1 — Bases agregadas e piloto de Matemática.**

A Sprint 0 validou as fontes, identificou a UFPA (`CO_IES=569`) e produziu a tabela-mestra. A Sprint 1 constrói bases agregadas por `CO_CURSO`, grupos comparativos exclusivos, benchmarks e o primeiro conjunto de gráficos para Matemática (`CO_GRUPO=702`).

## Requisitos

- Python 3.11 ou superior;
- VS Code;
- Git;
- aproximadamente 1 GB livre.

## Instalação no Windows/PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Coloque em `dados_brutos/`:

- `microdados_enade_licenciaturas_2025.zip`;
- `conceito_enade_licenciaturas.xlsx`.

## Execução

A Sprint 0 pode ser reproduzida com:

```powershell
python executar_sprint_00.py
```

Execute o piloto de Matemática:

```powershell
python executar_sprint_01.py
pytest -q
ruff check .
```

## Principais saídas da Sprint 1

- `dados_processados/matematica/base_analitica_cursos.csv`;
- agregados temáticos em `dados_processados/matematica/`;
- benchmarks amplo e comparável;
- `figuras/matematica/*.png`;
- `relatorios/sprint_01_piloto_matematica.md`.

## Regra metodológica central

Os arquivos não podem ser unidos no nível individual. Cada tema é tratado e agregado separadamente por `CO_CURSO`; somente tabelas com uma linha por curso são unidas com validação `one_to_one`.

## Git/GitHub

Branch da sprint:

```text
sprint/01-bases-agregadas-matematica
```

Após execução e validação local:

```powershell
git add .
git commit -m "feat(sprint-01): implementa bases agregadas e piloto de matemática"
git push -u origin sprint/01-bases-agregadas-matematica
```

Os dados brutos e os arquivos extraídos não são enviados ao GitHub.

## Sprint 2 — validação analítica de Matemática

Execute após a Sprint 1:

```powershell
python executar_sprint_02.py
pytest -q
ruff check .
```

A sprint audita participação, indicadores percentuais, critérios alternativos de benchmark, sensibilidade do desempenho e dimensões preliminares do processo formativo.

## Sprint 3 - Relatório ABNT de Matemática

Execute `python executar_sprint_03.py` após as Sprints 0, 1 e 2. O script gera DOCX, Markdown e, quando o LibreOffice está disponível, PDF em `relatorios/matematica/`.

## Sprint 4 — Piloto de Física

A Sprint 4 adapta o pipeline para Física (`CO_GRUPO=1402`) e gera bases agregadas, benchmarks e 12 figuras. As análises preservam individualmente as cinco ofertas validadas da UFPA e incluem presença, `NT_GER`, `NT_OBJ`, `NT_DIS`, dificuldade percebida, processo formativo e recomendação do curso e da instituição.

Execução:

```powershell
python executar_sprint_04.py
pytest -q
ruff check .
```

Saídas processadas locais: `dados_processados/fisica/`.
Figuras versionáveis: `figuras/fisica/`.
Relatório técnico: `relatorios/sprint_04_piloto_fisica.md`.

## Sprint 5 — Validação analítica de Física

A Sprint 5 audita presença e desempenho, testa critérios alternativos de benchmark, valida a leitura ecológica de dificuldade e perfil socioeconômico e produz quatro figuras revisadas.

Execução:

```powershell
python executar_sprint_04.py
python executar_sprint_05.py
pytest -q
ruff check .
```

Saídas principais:

- `relatorios/sprint_05_validacao_fisica.md`;
- `figuras/fisica/validada_*.png`;
- produtos locais em `dados_processados/fisica/`.
