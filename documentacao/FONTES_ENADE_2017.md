# Organização recomendada das fontes — Enade 2017

## 1. Princípio

As fontes oficiais de 2017 devem permanecer imutáveis e separadas das fontes de 2025.

Estrutura recomendada:

```text
dados_brutos/
├── enade_2017/
│   ├── microdados_enade_2017_LGPD.zip
│   ├── resultados_conceito_enade_2017.xlsx
│   └── referencias/
│       ├── Dicionário_arquivos _ variáveis_microdados do Enade_2017.xlsx
│       ├── Dicionário_arquivos _ variáveis_microdados do Enade_2017.ods
│       ├── Manual do usuário_Enade_2017.pdf
│       ├── Questionário do Estudante_Enade_Edição 2017.pdf
│       └── Questionário Licenciaturas - Enade 2017.pdf
│
└── ... fontes de outras edições ...
```

Os nomes físicos reais podem conter pequenas diferenças de espaços/acentos. O código de produção não deve depender de nomes frágeis de documentos de referência; apenas as fontes de dados operacionais precisam de caminho configurado explicitamente.

## 2. Dados operacionais

As duas fontes que entram diretamente no pipeline 2017 são:

```text
microdados_enade_2017_LGPD.zip
resultados_conceito_enade_2017.xlsx
```

Manual, dicionário e questionários servem para validação semântica e documentação do instrumento.

## 3. Extração

Não editar o ZIP.

O cache extraído deve ser regenerável, por exemplo:

```text
dados_extraidos/enade_2017/
```

A estrutura interna esperada deve ser descoberta pelo extrator a partir do ZIP, não presumida por concatenação de caminhos sem validação.

## 4. Proveniência

Registrar, quando o pipeline 2017 for implementado:

- caminho da fonte;
- SHA256;
- tamanho;
- data da execução;
- edição (`2017`);
- lista/quantidade dos arquivos extraídos;
- schema observado dos arquivos usados.

## 5. Git

Respeitar `.gitignore` e a política atual do projeto para fontes/dados derivados. Não adicionar bases grandes ao Git apenas para facilitar testes.

Testes unitários devem usar dados sintéticos mínimos. Testes de integração com dados oficiais podem ser condicionais à disponibilidade local das fontes.
