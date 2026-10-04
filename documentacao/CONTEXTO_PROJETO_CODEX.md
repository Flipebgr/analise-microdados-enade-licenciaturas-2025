# Contexto do projeto para Codex

## 1. Situação atual

Este repositório nasceu para analisar os Microdados do Enade das Licenciaturas 2025 da UFPA e produzir bases analíticas, figuras e relatórios por área.

Ao longo do projeto foram implementadas e entregues várias áreas. O repositório passou por uma refatoração de núcleo compartilhado e por uma política de aposentadoria: pipelines específicos de áreas concluídas podem ser removidos do branch operacional após preservação em histórico/tag.

No ZIP do repositório auditado antes desta nova fase, o `main` estava no commit:

```text
a5c14e6 Merge pull request #30 from Flipebgr/chore/aposenta-musica
```

O `executar.py` operacional registrava apenas a validação de fontes (`fontes`). Isso é intencional: Música e Educação Física, por exemplo, foram entregues e aposentadas do branch operacional.

Tags relevantes:

```text
archive/educacao-fisica-2025
archive/musica-2025
archive/pre-aposentadoria-areas
pre-refatoracao-arquitetural
```

A última auditoria anterior à frente 2017 reportou a suíte compartilhada passando. O agente deve sempre executar novamente os testes no ambiente atual; não trate um resultado histórico como garantia.

## 2. Estrutura relevante existente

O núcleo compartilhado está organizado principalmente em:

```text
src/core/
src/agregacao/
src/analise/
src/configuracao/
src/extracao/
src/qualidade/
src/relatorios/
src/utilitarios/
src/validacao/
```

Documentação existente:

```text
documentacao/ARQUITETURA.md
documentacao/METODOLOGIA.md
documentacao/EXECUCAO.md
documentacao/POLITICA_APOSENTADORIA_AREAS.md
```

Esses documentos descrevem a arquitetura consolidada para 2025 e continuam sendo referência. Esta nova documentação complementa-os para a evolução multi-edição.

## 3. Núcleo metodológico que deve ser preservado

A unidade principal é `CO_CURSO`.

Os arquivos públicos do Enade pós-LGPD não permitem reconstruir o mesmo estudante entre arquivos temáticos. Portanto:

```text
arquivo temático
→ tratar ausências
→ agregar por CO_CURSO
→ garantir uma linha por curso
→ juntar agregações one-to-one
→ comparar cursos
```

Nunca usar posição de linha como identificador.

Análises individuais só podem combinar variáveis do mesmo arquivo. Relações entre temas provenientes de arquivos diferentes são avaliadas somente depois da agregação por curso, com ressalva de falácia ecológica.

## 4. Grupos comparativos históricos do projeto

Quando havia oferta UFPA com Conceito Enade 1, o projeto utilizava grupos exclusivos:

- A — UFPA com Conceito 1;
- B — demais ofertas UFPA da mesma área com conceito superior;
- C — outras IES do Pará, excluindo UFPA;
- D — restante da Região Norte, excluindo Pará;
- E — restante do Brasil, excluindo Norte.

Pará, Norte e Brasil completos podem existir como benchmarks descritivos, mas não como grupos independentes sobrepostos em testes.

Quando não existe UFPA Conceito 1, não se fabrica um Grupo A. Define-se um contraste focal adequado e explicitamente documentado.

## 5. Benchmarks

O projeto usa dois níveis:

1. **amplo** — todos os cursos válidos da mesma área no recorte;
2. **comparável** — cursos semelhantes em características observáveis, como modalidade, categoria administrativa, organização acadêmica e porte.

Benchmarks não constituem desenho causal.

## 6. O que já está bem automatizado

O código compartilhado já cobre boa parte de:

- leitura e normalização de fontes;
- agregação por curso;
- demografia;
- trajetória;
- parte do perfil socioeconômico;
- processo formativo;
- estatísticas descritivas;
- definição de grupos;
- benchmarks;
- sensibilidade;
- tamanhos de efeito;
- validações estruturais;
- infraestrutura de relatórios.

O problema atual não é ausência de funções estatísticas básicas. É o acoplamento semântico a 2025 e a falta de uma orquestração analítica genérica multi-edição.

## 7. Dependência de IA que queremos reduzir

A evolução do projeto busca mover para código determinístico:

- seleção mecânica de indicadores;
- cálculo de estatísticas e incerteza;
- QA;
- benchmarks;
- efeitos;
- correlações ecológicas pré-especificadas;
- detecção de alertas;
- geração de figuras padronizadas;
- construção de um pacote estruturado de evidências.

A IA deve ficar principalmente com:

- desenvolvimento de novas capacidades;
- decisões metodológicas não resolvidas por regras;
- interpretação substantiva;
- redação científica;
- apresentação.

## 8. Arquitetura-alvo conceitual

O objetivo é separar claramente:

```text
FONTES OFICIAIS
      ↓
ADAPTADOR DA EDIÇÃO
      ↓
SCHEMA CANÔNICO / CONTRATOS
      ↓
AGREGAÇÕES POR CURSO
      ↓
ANÁLISES GENÉRICAS
      ↓
QA + BENCHMARKS + EFEITOS
      ↓
FIGURAS
      ↓
EVIDÊNCIAS ESTRUTURADAS
      ↓
RELATÓRIO / IA EDITORIAL
```

A área deve ser majoritariamente configuração, não um pacote Python novo com milhares de linhas.

## 9. Pacote de evidências desejado

A direção planejada é gerar um artefato semelhante a:

```text
dados_processados/<edicao>/<area>/evidencias.json
```

Com schema versionado e blocos como:

```json
{
  "schema_version": "1.0",
  "edicao": {},
  "area": {},
  "universo": {},
  "ofertas_focais": [],
  "participacao": {},
  "desempenho": {},
  "perfil": {},
  "trajetoria": {},
  "processo_formativo": {},
  "benchmarks": {},
  "efeitos": {},
  "associacoes_ecologicas": {},
  "qualidade": {},
  "alertas": [],
  "achados_priorizados": []
}
```

Esse arquivo não deve substituir CSVs auditáveis. Ele é uma interface resumida e determinística para a camada editorial/IA.

## 10. Regra de promoção ao núcleo

Se uma área exige uma melhoria que também serve a outras áreas/edições, implemente-a no núcleo e teste-a antes de aposentar a área.

Não aposente conhecimento generalizável junto com código específico.
