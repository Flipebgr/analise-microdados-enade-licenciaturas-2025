# Análise de Microdados — ENADE Licenciaturas 2025

Projeto reproduzível para análise das licenciaturas da UFPA no Enade das Licenciaturas 2025, com comparação por curso (`CO_CURSO`) e benchmarks territoriais e estruturais.

## Regra metodológica central

Os arquivos temáticos dos microdados **não são unidos no nível individual**. O fluxo obrigatório é:

```text
arquivo temático
→ tratamento de ausências
→ agregação por CO_CURSO
→ uma linha por curso
→ validação de unicidade
→ junção one-to-one das tabelas agregadas
→ comparação entre cursos
```

A posição da linha não é chave e não é criado identificador artificial de estudante.

## Áreas configuradas

| Área | CO_GRUPO |
|---|---:|
| Matemática | 702 |
| Letras–Português | 904 |
| Física | 1402 |
| Química | 1502 |
| Ciências Biológicas | 1602 |
| Pedagogia | 2001 |
| Geografia | 3002 |
| Letras–Inglês | 6407 |

A configuração de uma área no núcleo não significa que todo o pipeline analítico esteja concluído. Química deve ser retomada a partir do núcleo compartilhado e validada antes de uso analítico.

## Requisitos

- Python 3.11 ou superior;
- Git;
- ambiente virtual Python;
- fontes oficiais em `dados_brutos/`.

### Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Coloque localmente em `dados_brutos/`:

- `microdados_enade_licenciaturas_2025.zip`;
- `conceito_enade_licenciaturas.xlsx`.

Essas fontes não são versionadas no Git.

## Execução recomendada

O ponto de entrada preferencial é o executor unificado:

```powershell
python executar.py --listar
python executar.py matematica base
python executar.py fisica validacao
python executar.py geografia relatorio
python executar.py geografia tudo
```

` tudo ` executa, em sequência, base → validação → relatório da área. O relatório regional de Física permanece uma etapa explícita:

```powershell
python executar.py fisica regional
```

Os executores históricos ficam em `scripts/pipelines/` como implementações de compatibilidade. Novos fluxos devem preferir `executar.py`.


## Validação

Antes de qualquer merge:

```powershell
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```

Testes de integração podem ser ignorados (`skipped`) quando produtos processados locais de uma área não estão disponíveis.

## Documentação

- [Arquitetura](documentacao/ARQUITETURA.md)
- [Metodologia](documentacao/METODOLOGIA.md)
- [Execução](documentacao/EXECUCAO.md)
- [Áreas analisadas](documentacao/AREAS_ANALISADAS.md)
- [Qualidade e validação](documentacao/QUALIDADE_E_VALIDACAO.md)
- [Estrutura dos relatórios](documentacao/ESTRUTURA_RELATORIOS.md)
- [Histórico](documentacao/HISTORICO.md)

## Política de artefatos

O Git deve priorizar código, testes, configuração, documentação operacional e relatórios finais em Markdown. Fontes brutas, ambientes virtuais, caches e bases processadas por área permanecem locais. DOCX, PDF, apresentações e snapshots históricos podem ser arquivados externamente.
