# Qualidade e validação

## 1. Objetivo

A validação do projeto protege tanto a integridade computacional quanto as restrições metodológicas do desenho.

## 2. Validação das fontes

Antes das análises:

- localizar os arquivos oficiais;
- validar estrutura e encoding;
- localizar a UFPA por código oficial;
- validar `CO_GRUPO`;
- confrontar cadastro dos microdados e planilha de Conceito Enade;
- documentar divergências;
- manter ofertas sem conceito separadas de Conceito 1.

Divergências devem ser registradas, não corrigidas silenciosamente.

## 3. Encoding

O padrão textual do projeto é UTF-8.

A auditoria histórica de encoding levou à adoção de:

- `.editorconfig`;
- leitura com encodings conhecidos quando necessário;
- saída CSV preferencialmente em `utf-8-sig`.

A auditoria ignora arquivos derivados e também o próprio `tests/unit/test_encoding.py`, pois esse teste contém sequências de mojibake deliberadas usadas como fixtures. Essas ocorrências não representam defeitos de encoding do repositório.

## 4. Contratos estruturais

Devem ser validados:

- área correta;
- uma linha por `CO_CURSO` após agregação;
- ausência de duplicidade antes de junções;
- joins one-to-one;
- conceito ausente diferente de Conceito 1;
- exclusividade dos grupos comparativos;
- contagens esperadas quando usadas como contrato de regressão.

## 5. Participação e desempenho

A auditoria deve comparar, quando disponíveis:

- inscritos;
- participantes oficiais;
- registros no arquivo;
- presença válida;
- N válido de `NT_GER`;
- cobertura das notas.

Nenhum N válido pode exceder o número de registros elegíveis do curso.

## 6. Indicadores percentuais

Indicadores normalizados como proporção devem respeitar o intervalo `0–1`, salvo quando o produto estiver explicitamente expresso em percentual de `0–100`.

Ausências e denominadores válidos devem permanecer rastreáveis.

## 7. Benchmarks

Benchmarks devem registrar:

- critérios de seleção;
- N de cursos comparáveis;
- curso-alvo;
- modalidade;
- categoria administrativa;
- organização acadêmica;
- porte;
- diferenças de desempenho;
- sensibilidade a critérios alternativos.

Mudança de sinal ou forte alteração de magnitude entre cenários é evidência de instabilidade descritiva.

## 8. Processo formativo

`QE_I20–QE_I66` não deve gerar índice único automaticamente.

Validação de dimensão exige:

- texto oficial;
- direção de escala;
- itens invertidos;
- coerência teórica;
- N válido;
- consistência interna;
- correlação item-total.

Alfa elevado, isoladamente, não valida um construto.

## 9. Outliers

Outliers são sinalizados e preservados por padrão. A exclusão exige justificativa.

## 10. Testes

### Unitários

Localizados em `tests/unit/`.

Devem preferir:

- DataFrames sintéticos;
- funções puras;
- `tmp_path` para arquivos temporários;
- ausência de dependência de produtos reais.

### Integração

Localizados em `tests/integration/`.

Podem depender de:

- bases processadas;
- figuras;
- relatórios reais.

São marcados como `integration`.

Comandos:

```powershell
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```

## 11. Contratos históricos aposentados

O arquivo `baseline_pre_refatoracao.json` e seu teste de integração foram úteis durante a criação do núcleo compartilhado, mas seus contratos passaram a ser cobertos por testes operacionais atuais:

- contagens e ofertas reais de Matemática e Física são verificadas pelos testes de regressão dessas áreas;
- unicidade por `CO_CURSO` e joins one-to-one são cobertos pelos testes do núcleo;
- ausência de conceito diferente de Conceito 1 é protegida por testes de integridade e grupos comparativos;
- a não inserção artificial de Tucuruí em Física é coberta por teste de regressão específico.

Por isso, o baseline pré-refatoração não integra mais o estado operacional do projeto.

A auditoria de encoding continua disponível, mas seu relatório JSON é produto regenerável e passa a ser salvo localmente em:

```text
dados_processados/qualidade/resultado_auditoria_encoding.json
```

## 12. Critério de merge

Uma etapa só deve ser integrada depois de:

1. executor concluído;
2. produtos esperados gerados;
3. testes unitários aprovados;
4. testes de integração aplicáveis aprovados;
5. suíte completa aprovada;
6. Ruff aprovado;
7. divergências e exceções metodológicas documentadas.
