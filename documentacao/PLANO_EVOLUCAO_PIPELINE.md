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

## 6. Fase 2 — inventário e carregamento

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

Depois que os adapters estiverem estáveis, criar uma orquestração genérica.

Exemplo conceitual de CLI:

```powershell
python executar.py area --ano 2017 --grupo 1601 --etapa validacao
python executar.py area --ano 2017 --grupo 1601 --etapa analise
python executar.py area --ano 2017 --grupo 1601 --etapa tudo
```

A sintaxe final deve respeitar o estilo atual do repositório; não é obrigatório usar exatamente esses argumentos.

## 12. Fase 8 — pacote de evidências

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
