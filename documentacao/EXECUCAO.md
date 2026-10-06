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

## 10. Processo formativo por edição

```python
from src.agregacao.agregar_processo_formativo import agregar_processo_formativo_edicao

processo_cursos, processo_itens, proveniencia = agregar_processo_formativo_edicao(
    fonte, edicao, cursos
)
```

O agregador lê somente o arquivo temático que contém todos os itens declarados pela edição: `QE_I27–QE_I68` em 2017 e `QE_I20–QE_I66` nos microdados disponíveis de 2025. A tabela `processo_itens` apresenta, por curso e item, `n_total`, `n_valido`, `n_ausente`, `n_invalido`, contagens dos códigos especiais, média, mediana, desvio-padrão e concordância. `concordancia_pct` usa `n_valido`; `ausencia_analitica_pct`, `nao_sabe_responder_pct` e `nao_se_aplica_pct` usam `n_total` do item. As taxas são frações entre 0 e 1; denominador zero produz percentual ausente. `processo_cursos` contém uma linha por `CO_CURSO`, e `proveniencia` registra os códigos e a direção da escala.

Este caminho não cria dimensão, índice ou alfa global. O agregador legado de 2025 permanece disponível, mas seu alfa para o bloco completo é apenas diagnóstico histórico e não valida uma escala única. O questionário oficial de 2025 contém a questão 67, porém `QE_I67` não aparece nos arquivos temáticos do ZIP público disponível; por isso não é inventada nesta saída.

## 11. Conceito Enade por edição

```python
from pathlib import Path

from src.edicoes import carregar_conceitos_edicao, obter_edicao

edicao = obter_edicao(2017)
fonte_conceito = Path("dados_brutos/enade_2017/resultados_conceito_enade_2017.xlsx")
conceitos, tabela_original, proveniencia = carregar_conceitos_edicao(fonte_conceito, edicao)
```

O contrato da edição declara a aba, os cabeçalhos oficiais e os campos numéricos. A tabela `conceitos` mantém uma linha por `CO_CURSO`, com códigos oficiais em texto, inscritos e participantes oficiais, valor original do conceito, faixa numérica anulável e situação (`com_conceito`, `sem_conceito`, `ausente` ou `nao_reconhecida`). `SC` nunca vira Conceito 1. A tabela `tabela_original` preserva inclusive notas de rodapé, enquanto `proveniencia` registra fonte, SHA256, aba e quantidades de linhas. Linhas apenas de nota de rodapé são excluídas da tabela de ofertas; registros parcialmente preenchidos sem `CO_CURSO` geram erro.

O conceito contínuo existe na fonte de 2017. Na planilha de 2025, os valores da coluna normalizada correspondente permanecem ausentes; eles não são calculados a partir da faixa. A leitura não altera as planilhas em `dados_brutos/` e ainda não integra a CLI operacional (Fase 7).

## 12. Pipeline genérico de área — primeira implementação da Fase 7

```powershell
python executar.py area --ano 2017 --slug biologia_bacharelado `
  --microdados dados_brutos/enade_2017/microdados_enade_2017_LGPD.zip `
  --conceitos dados_brutos/enade_2017/resultados_conceito_enade_2017.xlsx `
  --etapa tudo
```

`--etapa validacao` confere o `arq1` e a planilha de Conceito, produzindo uma linha por curso e uma auditoria de cobertura. `--etapa analise` ou `tudo` também executa os agregadores de desempenho, questionário e processo formativo. As saídas CSV ficam em `dados_processados/<ano>/<slug>/validacao/` ou `analise/`; `--saida` permite escolher outra pasta-raiz. Nenhuma tabela individual de arquivos temáticos distintos é juntada ou gravada nessa base. O `CO_CURSO` e os demais identificadores oficiais permanecem texto.

Na etapa `analise` ou `tudo`, o comando também produz `evidencias.json` ao lado dos CSVs auditáveis. O pacote versionado reúne edição, área, cobertura, ofertas focais, desempenho, perfil, processo formativo e proveniência. Ele preserva por curso e item `n_total`, `n_valido`, as contagens e os percentuais separados de "não sei responder" e "não se aplica"; estes últimos usam `n_total` como denominador. O JSON não substitui os CSVs e não contém registros individuais.

Benchmarks, efeitos, associações ecológicas, alertas e achados priorizados aparecem explicitamente como indisponíveis/vazios até que seus contratos analíticos sejam implementados e validados. A auditoria registra cursos presentes somente em uma das fontes e, na etapa analítica, a cobertura de desempenho; divergência de ano, grupo, IES ou município entre ofertas correspondentes causa erro. As contagens `INSCRITOS` e `PARTICIPANTES` são as oficiais da planilha de Conceito; `registros_microdados` é uma contagem distinta da fonte temática de desempenho.

## 13. Reproduzir uma entrega antiga

Não reintroduza o código aposentado na `main` apenas para consulta.

Use:

1. a entrega arquivada no Drive;
2. o histórico Git;
3. a tag `archive/pre-aposentadoria-areas` ou snapshot equivalente.

Se for necessário corrigir uma entrega histórica excepcionalmente, crie branch específica a partir do commit/tag correspondente.
