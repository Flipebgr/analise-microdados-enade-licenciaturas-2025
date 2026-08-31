# Histórico técnico do projeto

Este arquivo mantém a visão resumida da evolução do projeto. A documentação detalhada de sprints e refatorações pode ser arquivada fora do branch operacional porque permanece recuperável pelo histórico do Git.

## Fase inicial

### Sprint 0 — validação das fontes

Objetivos centrais:

- identificar os arquivos temáticos;
- localizar a UFPA;
- validar áreas e tabela-mestra;
- separar ausência de conceito de Conceito 1;
- documentar divergências;
- impedir junções individuais/posicionais.

## Matemática

Matemática (`CO_GRUPO=702`) foi a área piloto.

Etapas históricas:

- Sprint 1 — bases agregadas e piloto;
- Sprint 2 — validação analítica;
- Sprint 3 — relatório final.

A área estabeleceu critérios iniciais de benchmark, visualização, dimensões diagnósticas do processo formativo e estrutura de relatório.

## Física

Etapas históricas:

- Sprint 4 — base/piloto;
- Sprint 5 — validação;
- Sprint 6 — relatório;
- relatório regional complementar.

Física introduziu auditorias ampliadas de presença, desempenho e comparação regional. A oferta inicialmente informada de Tucuruí não foi localizada nas fontes analíticas e permaneceu fora dos cálculos.

## Refatoração arquitetural

A refatoração criou e consolidou o núcleo compartilhado.

### Refactor 01

- auditoria da estrutura;
- padronização de encoding;
- baseline de regressão.

### Refactor 02

- `ConfiguracaoArea`;
- catálogo compartilhado;
- unicidade por curso;
- junções one-to-one;
- validação estrutural.

### Refactor 03

- separação entre testes unitários e de integração;
- marcador `integration`;
- contratos metodológicos testados.

### Refactor 04

- contrato compartilhado de geração de relatórios;
- conversão DOCX→PDF não fatal;
- preservação de Markdown e DOCX quando LibreOffice não está disponível.

### Refactor 05

Migração dos contratos estruturais de Física para o núcleo.

### Refactor 06

Migração dos contratos estruturais de Matemática para o núcleo.

## Letras–Inglês

- Sprint 7 — base analítica;
- Sprint 8 — validação;
- Sprint 9 — relatório final.

Foi a primeira nova área estruturada diretamente sobre o núcleo compartilhado.

## Ciências Biológicas

- Sprint 10 — base;
- Sprint 11 — validação;
- Sprint 12 — relatório final.

Não há oferta UFPA Conceito 1. Soure foi definida como estudo focal, sem recodificação artificial.

## Pedagogia

- Sprint 13 — base;
- Sprint 14 — validação;
- Sprint 15 — relatório final.

Não há oferta UFPA Conceito 1. O contraste interno usa Castanhal Conceito 5 versus as seis ofertas Conceito 4.

## Letras–Português

- Sprint 16 — base;
- Sprint 17 — validação;
- Sprint 18 — relatório final no fluxo planejado.

Belém EaD é a única oferta localizada Conceito 1. Soure, informada inicialmente, não foi localizada nas fontes e não é fabricada no catálogo.

## Geografia

- Sprint 19 — base;
- Sprint 20 — validação;
- Sprint 21 — relatório final.

Não há oferta UFPA Conceito 1. O contraste interno usa duas ofertas Conceito 3 versus duas Conceito 4.

## Química

Química está configurada no núcleo, mas uma tentativa anterior foi abandonada antes da validação. A área deve ser retomada a partir da arquitetura compartilhada atual.

## Política de histórico

Detalhes de sprints concluídas não precisam permanecer como dezenas de arquivos na raiz de `documentacao/`.

Após a consolidação:

- manter este `HISTORICO.md` no Git;
- arquivar os documentos detalhados em backup externo;
- confiar no histórico Git para recuperação de versões antigas;
- manter artefatos JSON ainda usados por testes ou auditorias automáticas.

## Contratos históricos aposentados

Após a estabilização do núcleo compartilhado, o baseline pré-refatoração deixou de ser necessário como artefato operacional. Seus contratos permaneceram protegidos por testes correntes de núcleo e regressão por área.

O relatório JSON de encoding também deixou de ser documentação versionada: a auditoria permanece no código, mas seu resultado é regenerável e local.
