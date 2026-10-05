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

Os contratos são selecionados pelo ano em `src/edicoes/`. As áreas são resolvidas por `(edição, slug)`; exemplos: `(2017, biologia_bacharelado)` e `(2025, biologia)`.

A CLI operacional continua limitada à validação legada de fontes. A orquestração genérica de área está prevista para a Fase 7.

## 7. Inventário e leitura multi-edição

`inventariar_arquivos` valida a quantidade e os nomes oficiais dos arquivos temáticos em um ZIP ou diretório extraído. Falha se houver arquivo esperado ausente, duplicado ou fora da sequência. O leitor pode abrir um membro do ZIP diretamente, sem extrair as fontes.

Para obter apenas os cursos de Ciências Biológicas — Bacharelado 2017 e algumas colunas de trajetória:

```python
from pathlib import Path

from src.edicoes import obter_edicao
from src.utilitarios.leitura import carregar_filtrado_edicao, obter_cursos_area

edicao = obter_edicao(2017)
fonte = Path("dados_brutos/enade_2017/microdados_enade_2017_LGPD.zip")
cursos = obter_cursos_area(fonte, edicao, co_grupo=1601)
trajetoria = carregar_filtrado_edicao(
    fonte, edicao, 2, usecols=["ANO_FIM_EM", "ANO_IN_GRAD"], cursos=cursos
)
```

O leitor usa `chunksize` de `config.yaml`, seleciona somente as colunas necessárias e filtra cada bloco antes de acumular o subconjunto. `CO_CURSO` permanece como texto para preservar o código oficial. O filtro por `CO_GRUPO` só é aceito no `arq1`; os demais arquivos usam o conjunto de `CO_CURSO` obtido dele. Não há associação de registros individuais entre arquivos. Para análises nacionais que retenham quase todas as linhas, a agregação em streaming deve ser implementada no adaptador da etapa analítica, evitando acumular o universo completo.

## 8. Desempenho por edição

O agregador usa apenas o `arq3` da edição e produz uma linha por `CO_CURSO`:

```python
from src.agregacao.agregar_desempenho import agregar_desempenho_edicao

agregado, auditoria_arq3 = agregar_desempenho_edicao(fonte, edicao, cursos)
```

O mapa `edicao.desempenho.mapa_canonico` documenta a origem de cada componente. Em 2017, `formacao_geral_total` vem de `NT_FG` e `componente_especifico_total` de `NT_CE`. Em 2025, `objetiva` e `discursiva` correspondem a `NT_OBJ` e `NT_DIS`; não são renomeadas como FG ou CE. O `n_valido` de cada nota conta somente resultados com presença válida. A tabela `auditoria_arq3` mantém os nomes das colunas oficiais e não deve ser juntada por linha a outros arquivos temáticos.

## 9. Indicadores do Questionário do Estudante

```python
from src.agregacao.agregar_socioeconomico import agregar_indicadores_questionario

indicadores, distribuicoes, regras = agregar_indicadores_questionario(
    fonte, edicao, cursos
)
```

Cada item é lido no arquivo temático declarado pela edição e agregado por `CO_CURSO` antes de ser combinado com outros indicadores. `regras` informa edição, arquivo, item, rótulo, categorias, tratamento de ausências e denominador. Cada percentual usa `n_valido` da própria pergunta; a saída também informa ausências, respostas excluídas, não aplicáveis e inválidas. Em 2025, `QE_I16` permite combinações como `B,F`; `A,B` é inválida porque `A` significa nenhuma bolsa. O agregador legado de 2025 permanece disponível até a migração da orquestração e usa a mesma classificação do contrato 2025 para esse item, preservando suas colunas de saída anteriores.

## 10. Reproduzir uma entrega antiga

Não reintroduza o código aposentado na `main` apenas para consulta.

Use:

1. a entrega arquivada no Drive;
2. o histórico Git;
3. a tag `archive/pre-aposentadoria-areas` ou snapshot equivalente.

Se for necessário corrigir uma entrega histórica excepcionalmente, crie branch específica a partir do commit/tag correspondente.
