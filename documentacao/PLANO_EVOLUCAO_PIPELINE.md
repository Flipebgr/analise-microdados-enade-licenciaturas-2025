# Plano de evolução — pipeline genérico multi-edição

## 1. Objetivo

Reduzir a dependência de código específico por área e da IA para análises mecânicas, sem reescrever o núcleo estatístico já validado.

A primeira implementação multi-edição usará Enade 2017 + Ciências Biológicas — Bacharelado (`CO_GRUPO=1601`) como piloto.

## 2. Princípio de desenho

Separar três níveis:

```text
EDIÇÃO
  define schema oficial, instrumento e capacidades

ÁREA
  define CO_GRUPO, nome, grau e IES focal

NÚCLEO
  agrega, valida, compara e produz evidências
```

O núcleo não deve conhecer números de questões específicos de 2017 ou 2025 quando isso puder ser expresso pelo schema/configuração da edição.

## 3. Estrutura-alvo sugerida

A implementação pode ajustar nomes após inspeção do repositório, mas a separação conceitual deve ser preservada.

Exemplo:

```text
src/
├── core/
├── edicoes/
│   ├── base.py
│   ├── enade_2017.py
│   └── enade_2025_licenciaturas.py
├── instrumento/
│   ├── questionario.py
│   └── dicionario.py
├── agregacao/
├── analise/
├── evidencias/
│   ├── construir.py
│   ├── alertas.py
│   └── validar.py
├── visualizacao/
└── relatorios/
```

Alternativamente, parte do schema pode ser declarativa em YAML. Não criar abstrações apenas por estética; manter a solução pequena e testável.

## 4. Fase 0 — baseline antes de alterar

Antes de implementar:

1. `git status` e branch atual;
2. `python -m pytest -q`;
3. `python -m ruff check .`;
4. registrar comportamento atual de `python executar.py --listar`;
5. identificar testes que protegem 2025;
6. não editar fontes em `dados_brutos/`.

Se a árvore já estiver suja, não apagar alterações do usuário.

## 5. Fase 1 — configuração/contrato da edição

**Implementada no escopo declarativo inicial.** Os contratos de 2017 e 2025 estão separados em `src/edicoes/`, e as áreas são resolvidas pela edição e pelo slug. A implementação também separa capacidade da edição de aplicabilidade da área/grau e define valor original, faixa numérica anulável e situação como campos distintos do Conceito Enade.

Criar uma representação explícita de edição com, no mínimo:

```text
ano
prefixo_arquivos
quantidade_arquivos
separador
decimal
encoding(s)
schema_arq1
schema_arq2
schema_desempenho
mapa_presenca
questionario_geral
processo_formativo
questionario_licenciatura
capacidades
schema_conceito
```

Capacidades são preferíveis a condicionais espalhadas. Exemplo:

```text
supports_proficiencia = false
supports_recomendacao = false
supports_itens_licenciatura = true/false conforme grau
```

Na implementação, `supports_itens_licenciatura` é capacidade da edição. A utilização efetiva é uma propriedade independente da configuração da área/grau. O bacharelado 1601 em 2017, por exemplo, não aplica esse bloco embora a edição o ofereça.

Permanecem para as fases seguintes a leitura dirigida pelo contrato, os adapters dos agregadores, o loader multi-edição do Conceito Enade, a orquestração genérica e o teste end-to-end do piloto.

## 6. Fase 2 — inventário e carregamento

**Implementada como infraestrutura de leitura.** O inventário valida ZIP ou diretório extraído conforme o contrato da edição. A leitura aceita o TXT diretamente do ZIP, valida o schema, lê apenas colunas solicitadas, usa o `chunksize` de `config.yaml` e filtra cada bloco por `CO_GRUPO` no `arq1` ou por `CO_CURSO` nos demais arquivos. O recorte 1601 foi verificado na fonte local de 2017. A integração desse leitor aos agregadores e a agregação nacional em streaming são decisões das fases analíticas seguintes.

Generalizar o inventário que hoje está acoplado ao prefixo 2025.

Implementar leitura filtrada eficiente para arquivos grandes. O `chunksize` já aparece em configuração histórica; a nova implementação deve efetivamente usá-lo quando apropriado.

Fluxo desejado:

```text
ler chunk
→ normalizar apenas colunas necessárias
→ filtrar CO_CURSO/CO_GRUPO
→ acumular subset
→ próximo chunk
```

Não carregar centenas de milhares de linhas inteiras quando o objetivo é uma única área, salvo justificativa de benchmark nacional que exija o universo.

Quando o universo nacional for necessário, ainda preferir agregação streaming/chunked quando possível.

## 7. Fase 3 — desempenho por edição

**Implementada como agregador por curso dirigido pelo contrato.** O novo agregador lê somente o `arq3`, mapeia os componentes disponíveis para nomes canônicos e preserva as variáveis oficiais na tabela individual de auditoria. As estatísticas de notas usam apenas registros com o código de presença válida declarado pela edição; os denominadores, ausências e notas fora dessa situação são explicitados por curso. O agregador legado de 2025 permanece disponível até a migração da orquestração.

Não forçar um schema único que destrua a semântica original.

Criar um contrato canônico capaz de representar componentes opcionais, por exemplo:

```text
geral
formacao_geral.objetiva
formacao_geral.discursiva
formacao_geral.total
componente_especifico.objetiva
componente_especifico.discursiva
componente_especifico.total
proficiencia (opcional)
acertos (opcional)
```

O adapter 2017 mapeia `NT_*_FG` e `NT_*_CE` para esses campos conceituais.

O adapter 2025 mapeia somente o que a edição realmente fornece.

## 8. Fase 4 — questionário e indicadores derivados

**Implementada para os indicadores declarados nos contratos de 2017 e 2025.** O agregador lê cada item geral no seu arquivo oficial, normaliza e classifica as respostas segundo regras da edição, agrega por `CO_CURSO` e entrega percentuais, denominadores e contagens de ausentes, excluídos, não aplicáveis e inválidos. A resposta de múltipla escolha de `QE_I16` em 2025 aceita combinações de bolsas e rejeita combinações contraditórias com `A = nenhuma`. Regras e proveniência são retornadas para auditoria. O cálculo legado de 2025 permanece durante a migração da orquestração.

Separar:

```text
texto/código oficial da pergunta
```

de:

```text
indicador derivado do projeto
```

Exemplo:

```text
2017 QE_I21 = alguém na família concluiu superior
→ indicador derivado: primeira_geracao
```

Cada indicador derivado deve declarar:

- edição;
- item de origem;
- categorias incluídas/excluídas;
- denominador válido;
- tratamento de ausentes/não se aplica;
- rótulo final;
- teste unitário.

Não compartilhar indicador entre edições apenas porque o nome final é igual.

## 9. Fase 5 — processo formativo

**Motor por item implementado; dimensões ainda não definidas.** O agregador multi-edição lê os itens declarados no contrato da edição, classifica códigos 1–6, 7/8, ausências e respostas inválidas, e retorna estatísticas e denominadores por `CO_CURSO` e item. A direção da escala e os códigos de concordância ficam no contrato. O novo caminho não calcula alfa ou média global do bloco. A análise de dimensões depende de leitura e justificativa item a item, além das verificações abaixo.

O diagnóstico legado exploratório de 2025 também exclui 7/8 e respostas fora da escala do alfa e do número de casos completos. Seus agrupamentos candidatos não foram validados e não são índices; a matriz teórica permanece pendente, sem bloquear a Fase 6.

Ressalva da fonte: o questionário 2025 contém `QE_I67`, mas nenhum arquivo temático do ZIP público disponível traz essa coluna. O contrato usa `QE_I20–QE_I66` e não inventa respostas para `QE_I67`.

O motor estatístico deve aceitar lista/configuração de itens e códigos especiais.

Antes de construir dimensões:

1. ler rótulos oficiais;
2. verificar direção da escala;
3. definir teoria da dimensão;
4. avaliar consistência interna;
5. documentar itens excluídos;
6. não criar média global única sem validação.

Dimensões de 2025 não devem ser transplantadas automaticamente para 2017.

## 10. Fase 6 — Conceito Enade

**Implementada no carregamento independente da orquestração.** O schema da edição declara aba e correspondências de colunas. O loader entrega ofertas normalizadas, tabela original e proveniência, valida `CO_CURSO` único e mantém `SC`/ausente fora da faixa numérica. A ligação com a CLI de área permanece para a Fase 7.

Criar loader/adaptador por fonte/edição que normalize para campos canônicos, por exemplo:

```text
NU_ANO
CO_GRUPO
CO_IES
CO_CURSO
CO_MUNIC_CURSO
modalidade
inscritos_oficiais
participantes_oficiais
conceito_continuo
conceito_faixa
situacao_conceito
observacao_conceito
```

Manter a fonte original disponível para auditoria.

`SC`/ausente nunca vira 1.

## 11. Fase 7 — pipeline genérico de área

**Em implementação.** A primeira fatia oferece CLI por edição/slug e fontes explícitas, caracteriza cursos pelo `arq1`, reconcilia a planilha de Conceito e combina somente agregados one-to-one de desempenho, indicadores gerais e processo formativo. Os CSVs de validação e análise ficam separados. Ainda faltam contratos de comparações e benchmarks para a área focal; a saída atual não deve ser confundida com relatório ou pacote de evidências.

Depois que os adapters estiverem estáveis, criar uma orquestração genérica.

Exemplo conceitual de CLI:

```powershell
python executar.py area --ano 2017 --grupo 1601 --etapa validacao
python executar.py area --ano 2017 --grupo 1601 --etapa analise
python executar.py area --ano 2017 --grupo 1601 --etapa tudo
```

A sintaxe final deve respeitar o estilo atual do repositório; não é obrigatório usar exatamente esses argumentos.

## 12. Fase 8 — pacote de evidências

**Implementada para as saídas já validadas.** A etapa analítica da CLI gera `evidencias.json` versionado, ao lado dos CSVs auditáveis. O pacote contém proveniência, cobertura, ofertas focais, desempenho, perfil e processo formativo, incluindo denominadores e percentuais separados dos códigos 7/8. Benchmark, efeitos, associações ecológicas e alertas permanecem explicitamente indisponíveis até receberem contratos e validação próprios.

Gerar `evidencias.json` a partir de produtos já validados.

O pacote deve registrar também proveniência:

```text
fonte
edição
arquivo/variável de origem
N válido
ausências
regra de cálculo
versão do schema
```

No bloco de processo formativo, preservar por curso e item `n_total`, `n_valido`, as contagens e os percentuais separados de "não sei responder" e "não se aplica", com denominador `n_total`. O relatório final deve exibir esses percentuais junto aos respectivos N; não apresentar concordância sem seu denominador válido.

Não permitir números hardcoded em geradores de relatório quando eles já existem no pacote/CSV validado.

## 13. Fase 9 — motor de alertas

O código pode automatizar triagem mecânica, não conclusões substantivas.

Exemplos adequados:

```text
N benchmark pequeno
alta taxa de ausência
mudança de sinal entre benchmarks
IC inclui zero
consistência interna limitada
resultado sensível a outliers
```

Exemplos inadequados para regra automática:

```text
"infraestrutura explica o conceito"
"EaD causou baixo desempenho"
"o curso tem fragilidade pedagógica"
```

## 14. Fase 10 — teste end-to-end permanente

A política de aposentadoria remove testes específicos de áreas. Para o pipeline genérico, criar pelo menos um teste end-to-end que permaneça no núcleo.

Usar Ciências Biológicas — Bacharelado 2017 como smoke/regressão quando as fontes reais estiverem disponíveis localmente.

Expectativas preliminares do piloto UFPA:

```text
CO_CURSO=12027
inscritos=23
participantes=13
conceito=3
```

Esses valores não entram na lógica de produção.

Para 2025, snapshots/tags de Música e Educação Física podem servir como referência de regressão ao promover funcionalidades compartilhadas.

## 15. Definition of Done da primeira entrega multi-edição

A primeira entrega técnica não é o relatório de Biologia. É a infraestrutura mínima confiável.

Considerar pronta quando:

- 2017 e 2025 possuem schemas/adapters explicitamente separados;
- nenhum mapeamento socioeconômico 2025 é aplicado silenciosamente a 2017;
- o desempenho 2017 preserva FG/CE;
- o processo formativo 2017 usa o instrumento correto;
- conceito 2017 é carregado e `SC` preservado;
- o piloto 1601 produz base agregada por curso sem joins individuais;
- as reconciliações oficiais do curso UFPA passam;
- testes novos protegem os contratos;
- testes existentes permanecem verdes;
- Ruff permanece verde;
- documentação é atualizada junto com o código.
