# AGENTS.md — Projeto ENADE

Este arquivo contém regras obrigatórias para qualquer agente que trabalhe neste repositório.
Leia também, antes de alterar código relacionado à nova frente multi-edição:

- `documentacao/CONTEXTO_PROJETO_CODEX.md`
- `documentacao/ADAPTACAO_ENADE_2017.md`
- `documentacao/PLANO_EVOLUCAO_PIPELINE.md`
- `documentacao/FONTES_ENADE_2017.md`

## 1. Objetivo do projeto

O projeto processa microdados do Enade, agrega evidências por curso (`CO_CURSO`), constrói comparações institucionais/territoriais/estruturais e produz insumos reprodutíveis para relatórios técnico-científicos.

A arquitetura deve evoluir para suportar múltiplas edições do Enade sem copiar pipelines inteiros por área ou por ano.

## 2. Unidade de análise e regra de junção

A unidade principal é `CO_CURSO`.

Fluxo obrigatório entre arquivos temáticos distintos:

```text
arquivo temático
→ tratamento de ausências
→ agregação por CO_CURSO
→ uma linha por curso
→ validação de unicidade
→ junção one-to-one entre agregados
→ análise entre cursos
```

É proibido:

- usar posição de linha como chave de estudante;
- assumir que a linha `i` de dois arquivos corresponde ao mesmo estudante;
- criar identificador artificial para reconstruir registros individuais entre arquivos;
- fazer join individual entre arquivos temáticos distintos;
- fazer join muitos-para-muitos por `CO_CURSO`;
- inferir associações individuais a partir de indicadores agregados por curso;
- correlacionar individualmente variáveis vindas de arquivos diferentes.

Análises individuais são permitidas apenas quando as variáveis estão no mesmo arquivo oficial.

## 3. Regras de integridade científica

- Conceito ausente, `SC` ou sem conceito nunca pode ser tratado como Conceito Enade 1.
- Não criar equivalência entre variáveis de edições diferentes apenas por terem nomes ou posições semelhantes.
- Não reutilizar regras semânticas de itens `QE_*` de uma edição em outra sem validação no instrumento oficial.
- Não inventar indicadores que não existam na edição analisada.
- Não transformar automaticamente associação em causalidade.
- Não remover outliers automaticamente sem regra explícita e registro da decisão.
- Sempre informar denominadores válidos e tratamento de ausências nas saídas analíticas.
- Notas brutas de áreas diferentes não devem ser comparadas diretamente.

## 4. Fontes oficiais são imutáveis

Arquivos em `dados_brutos/` são fontes. Não os edite, sobrescreva ou normalize in place.

Derivações devem ir para pastas de saída apropriadas, como:

```text
dados_extraidos/
dados_intermediarios/
dados_processados/
figuras/
relatorios/
```

## 5. Multi-edição: regra arquitetural

Não espalhe condicionais como `if ano == 2017` por módulos estatísticos genéricos.

Prefira separar:

1. **contratos estatísticos compartilhados**;
2. **schema/adaptador da edição**;
3. **configuração da área**.

A semântica de cada edição deve ficar declarada em um ponto central e testável.

Exemplos de propriedades específicas da edição:

- prefixo e quantidade de arquivos;
- separador e formato decimal;
- variáveis de desempenho;
- códigos de presença/situação;
- intervalo e significado dos itens `QE_*`;
- disponibilidade de proficiência, recomendação ou itens de licenciatura;
- schema da planilha de Conceito Enade.

## 6. Reuso e aposentadoria

Antes de aposentar código específico de uma área, qualquer melhoria generalizável deve ser promovida ao núcleo compartilhado e coberta por testes.

Não reintroduza pipelines aposentados na `main` apenas para copiar código. Use histórico/tags como referência quando necessário.

Snapshots históricos conhecidos incluem:

- `archive/educacao-fisica-2025`
- `archive/musica-2025`
- `archive/pre-aposentadoria-areas`
- `pre-refatoracao-arquitetural`

## 7. Processo de alteração

Antes de modificar código em uma tarefa substancial:

1. leia os documentos citados no topo deste arquivo;
2. inspecione o código atual e os testes relacionados;
3. apresente um plano curto com os arquivos que pretende alterar;
4. implemente em passos pequenos;
5. mantenha compatibilidade com 2025, salvo mudança explicitamente aprovada;
6. adicione ou atualize testes para cada contrato novo;
7. não altere dados brutos para fazer um teste passar.

## 8. Validação obrigatória

Ao final de alterações Python, execute, quando o ambiente permitir:

```powershell
python -m pytest -q
python -m ruff check .
```

Se houver testes de integração dependentes de dados reais, também registre separadamente o resultado deles.

Falhas não devem ser ocultadas. Se uma dependência ou fonte estiver ausente, descreva a limitação.

## 9. Estilo do código

- Python legível e modular.
- Nomes e comentários podem permanecer em português, seguindo o padrão do repositório.
- Evitar duplicação de lógica por área.
- Funções devem receber parâmetros/configuração em vez de depender de constantes ocultas quando a propriedade varia por edição.
- Preservar identificadores oficiais (`CO_CURSO`, `CO_GRUPO`, `CO_IES`) sem coerções destrutivas.
- Prefira validações explícitas e falhas rápidas quando um schema não corresponde ao esperado.

## 10. Escopo imediato

A próxima frente é tornar o núcleo capaz de processar a edição completa do Enade 2017 e usar **Ciências Biológicas — Bacharelado (`CO_GRUPO=1601`)** como primeiro teste end-to-end.

Não criar `src/biologia_bacharelado_2017/` ou equivalente como solução principal. A meta é um pipeline genérico dirigido por edição + área.


## 11.  Continuidade entre sessões

Antes de iniciar trabalho substancial neste repositório:

1. Leia `documentacao/ESTADO_ATUAL_PROJETO.md`.
2. Confirme o estado real com:
   - `git status`
   - `git branch --show-current`
   - `git log -1 --oneline`
3. Caso haja divergência entre a documentação e o repositório, o estado do Git e do código é a fonte primária.

Ao concluir uma tarefa que altere significativamente o projeto:

1. Atualize `documentacao/ESTADO_ATUAL_PROJETO.md`.
2. Registre:
   - trabalho concluído;
   - estado dos testes;
   - decisões técnicas novas;
   - pendências;
   - próximo passo recomendado.
3. Não use esse arquivo como diário detalhado.
4. Mantenha apenas o contexto necessário para que outra sessão consiga continuar o trabalho.
