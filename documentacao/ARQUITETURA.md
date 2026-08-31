# Arquitetura do projeto

## 1. Objetivo arquitetural

O projeto transforma os microdados do Enade das Licenciaturas 2025 em bases analíticas por curso, comparações institucionais e territoriais, figuras e relatórios técnico-científicos.

A arquitetura foi desenhada para impedir relações indevidas entre registros individuais de arquivos temáticos distintos.

## 2. Unidade principal

A unidade principal é:

```text
CO_CURSO
```

`CO_CURSO` identifica o curso/oferta para fins de agregação. Ele **não identifica estudante**.

## 3. Fluxo de dados

```mermaid
flowchart TD
    A[Arquivo temático] --> B[Tratamento específico de ausências]
    B --> C[Agregação por CO_CURSO]
    C --> D[Uma linha por curso]
    D --> E[Validação de unicidade]
    E --> F[Junção one-to-one entre tabelas agregadas]
    F --> G[Base analítica por curso]
    H[Planilha Conceito Enade] --> G

    X[Posição da linha] -. proibido .-> Y[Reconstrução individual]
    Z[Join muitos-para-muitos por CO_CURSO] -. proibido .-> Y
```

Regras:

- não existe identificador público comum de estudante entre os arquivos temáticos;
- posição da linha não é chave;
- não se cria identificador artificial;
- cada lado de uma junção temática deve possuir uma linha por `CO_CURSO`;
- duplicidade em junção agregada é erro impeditivo;
- associações entre temas distintos são ecológicas.

## 4. Núcleo compartilhado

### `src/core/`

Contratos estruturais reutilizados pelas áreas:

- `ConfiguracaoArea`: slug, nome, `CO_GRUPO` e IES focal;
- preparação e normalização do catálogo;
- validação de unicidade por curso;
- junções one-to-one;
- validação estrutural da base;
- aplicação dos grupos comparativos.

A IES focal é a UFPA (`CO_IES=569`).

### `src/agregacao/`

Agregações temáticas compartilhadas:

- desempenho;
- demografia;
- trajetória;
- perfil socioeconômico;
- processo formativo;
- recomendação.

### `src/analise/`

Funções analíticas compartilhadas:

- estatísticas descritivas;
- benchmarks;
- sensibilidade;
- tamanhos de efeito;
- consistência de dimensões;
- validação de indicadores.

### `src/validacao/`

Contratos de integridade e validações de catálogo, grupos, agregações, relacionamentos e resultados.

### `src/relatorios/`

Infraestrutura compartilhada para:

- formatação;
- tabelas e figuras;
- referências;
- geração de DOCX;
- conversão opcional para PDF;
- contratos de resultado e validação de relatório.

### Outros componentes

- `src/configuracao/`: caminhos e leitura de configuração;
- `src/extracao/`: extração do ZIP oficial;
- `src/qualidade/`: inspeção e auditorias;
- `src/utilitarios/`: leitura, normalização e logs.

## 5. Módulos por área

As áreas possuem pacotes próprios quando há regras específicas:

```text
src/matematica/
src/fisica/
src/ingles/
src/biologia/
src/pedagogia/
src/portugues/
src/geografia/
```

Esses pacotes preservam diferenças de desenho analítico, oferta focal, benchmark, validações e figuras.

A repetição entre módulos de área deve ser reduzida somente por refatoração testada. Arquivos específicos não devem ser removidos apenas por semelhança estrutural.

## 6. Camadas de produto

```text
fontes oficiais
↓
dados_extraidos/
↓
dados_processados/<area>/
↓
figuras/<area>/
↓
relatorios/<area>/
```

### Fontes oficiais

Localizadas em `dados_brutos/` e não versionadas.

### Dados extraídos

Cache regenerável do ZIP oficial.

### Dados processados

Produtos derivados, normalmente locais e regeneráveis.

### Figuras

Produtos derivados dos pipelines analíticos.

### Relatórios

Os geradores consomem produtos agregados e validados. Não reconstroem vínculos individuais entre arquivos.

## 7. Testes

```text
tests/unit/
tests/integration/
```

Testes unitários usam dados sintéticos ou funções isoladas. Testes de integração podem depender de produtos reais locais e são marcados com `integration`.

## 8. Configuração das áreas

O registro central fica em `src/core/configuracao_area.py` e a configuração de arquivos e parâmetros de leitura fica em `config.yaml`.

A presença de uma área no registro central apenas permite parametrização; não equivale à conclusão de seu pipeline analítico.
