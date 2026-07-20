# Diagrama de relacionamento dos microdados

```mermaid
flowchart TD
    A[Arquivo temático] --> B[Tratamento específico de códigos ausentes]
    B --> C[Agregação por CO_CURSO]
    C --> D[Uma linha por curso]
    D --> E[Validação de unicidade]
    E --> F[Junção 1:1 entre tabelas agregadas]
    F --> G[Base analítica por curso]
    H[Planilha Conceito Enade] --> G

    X[Posição da linha] -. proibido .-> Y[Reconstrução individual]
    Z[Join muitos-para-muitos por CO_CURSO] -. produto cartesiano .-> Y
```

## Regras

- Não existe identificador público comum de estudante.
- A posição da linha não é chave.
- `CO_CURSO` é chave de agregação, não identificador individual.
- Toda junção entre temas exige uma linha por `CO_CURSO` em cada lado.
- Associações entre indicadores de temas distintos são ecológicas e não individuais.
