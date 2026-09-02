# Política de aposentadoria de áreas concluídas

## Contexto

O fluxo operacional do projeto é de entrega única por licenciatura:

```text
análise
→ relatório técnico-científico
→ apresentação PPTX
→ envio para a equipe responsável pela reunião
→ encerramento da área
```

Depois da entrega, o pipeline específico da área tem baixa probabilidade de ser executado novamente.

## Princípio

O branch operacional não precisa manter indefinidamente código, testes e executores específicos de áreas concluídas.

Antes da aposentadoria, preservar:

1. entrega final (relatório e apresentação);
2. fontes oficiais;
3. histórico Git;
4. snapshot do código antes da remoção.

## O que permanece

Devem continuar no branch operacional os componentes reutilizáveis:

```text
src/core/
src/agregacao/
src/analise/
src/configuracao/
src/extracao/
src/qualidade/
src/relatorios/  # somente infraestrutura genérica após aposentadoria
src/utilitarios/
src/validacao/
```

Também permanecem testes de contratos metodológicos gerais.

## O que pode ser aposentado

Para uma área formalmente encerrada:

- `src/<area>/`;
- geradores/validadores de relatório exclusivos da área;
- testes exclusivos da área;
- executores de Sprints exclusivos da área;
- relatório Markdown final, caso a entrega já esteja arquivada externamente;
- demais produtos específicos já preservados no histórico/Drive.

## Segurança

A remoção só deve ocorrer depois de:

- snapshot do `HEAD`;
- confirmação do backup das entregas finais;
- auditoria de imports/dependências;
- suíte de testes antes e depois da remoção;
- Ruff sem erros.

## Áreas tratadas como concluídas nesta auditoria

- Matemática;
- Física;
- Letras–Inglês;
- Ciências Biológicas;
- Pedagogia;
- Letras–Português;
- Geografia.

Química não entra porque seu pipeline ainda será retomado.
