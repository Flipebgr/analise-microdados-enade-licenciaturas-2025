# Análise de Microdados — ENADE Licenciaturas 2025

Projeto para análise técnico-científica das licenciaturas da UFPA no Enade das Licenciaturas 2025.

## Estado operacional

As áreas já concluídas e entregues foram aposentadas do branch operacional. O código que produziu essas entregas permanece preservado no histórico Git e no snapshot/tag criado antes da aposentadoria.

Áreas encerradas:

- Matemática (`CO_GRUPO=702`);
- Física (`1402`);
- Letras–Inglês (`6407`);
- Ciências Biológicas (`1602`);
- Pedagogia (`2001`);
- Letras–Português (`904`);
- Geografia (`3002`).

Química (`1502`) permanece cadastrada, mas seu novo pipeline ainda não foi implementado. Ela deverá nascer em uma branch própria a partir do núcleo atual.

## Regra metodológica central

Os arquivos temáticos dos microdados **não são unidos no nível individual**:

```text
arquivo temático
→ tratamento de ausências
→ agregação por CO_CURSO
→ uma linha por curso
→ validação de unicidade
→ junção one-to-one das tabelas agregadas
→ comparação entre cursos
```

Não se usa posição de linha como chave, não se cria identificador artificial e não se realizam joins individuais entre temas diferentes.

## Estrutura operacional

```text
src/
├── core/
├── agregacao/
├── analise/
├── configuracao/
├── extracao/
├── qualidade/
├── relatorios/
├── utilitarios/
└── validacao/

scripts/
└── pipelines/
    └── executar_sprint_00.py

tests/
├── unit/
└── integration/

executar.py
```

Pacotes específicos de áreas concluídas não permanecem no branch operacional.

## Requisitos

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Fontes locais esperadas em `dados_brutos/`:

- `microdados_enade_licenciaturas_2025.zip`;
- `conceito_enade_licenciaturas.xlsx`.

## Execução

```powershell
python executar.py --listar
python executar.py fontes
```

Novas áreas são registradas em `executar.py` somente durante seu desenvolvimento operacional.

## Validação

```powershell
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```

## Documentação

- [Arquitetura](documentacao/ARQUITETURA.md)
- [Metodologia](documentacao/METODOLOGIA.md)
- [Execução](documentacao/EXECUCAO.md)
- [Áreas analisadas](documentacao/AREAS_ANALISADAS.md)
- [Qualidade e validação](documentacao/QUALIDADE_E_VALIDACAO.md)
- [Estrutura dos relatórios](documentacao/ESTRUTURA_RELATORIOS.md)
- [Histórico](documentacao/HISTORICO.md)
- [Política de aposentadoria](documentacao/POLITICA_APOSENTADORIA_AREAS.md)

## Histórico e entregas

As entregas finais (relatório/PDF/DOCX/PPTX) são arquivadas externamente. O estado exato do código anterior à aposentadoria das áreas é preservado pela tag/snapshot de arquivamento e pelo histórico do Git.
