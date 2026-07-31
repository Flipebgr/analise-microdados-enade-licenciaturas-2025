# Refactor 02 — núcleo compartilhado

## Objetivo

Introduzir contratos reutilizáveis para as próximas áreas do Enade sem migrar ou reescrever os pipelines consolidados de Matemática e Física.

## Componentes

- `ConfiguracaoArea`: identifica slug, nome, `CO_GRUPO` e IES focal;
- `preparar_catalogo_area`: filtra e normaliza um cadastro já carregado;
- `validar_unicidade_por_curso`: exige uma linha por `CO_CURSO`;
- `juntar_por_curso`: executa somente junções um-para-um;
- `validar_base_area`: verifica domínio da área, contagens esperadas e colunas obrigatórias.

## Limites desta etapa

O núcleo não lê arquivos, não define grupos comparativos, não associa questionários no nível individual, não infere Conceito Enade e não altera os módulos existentes de Matemática e Física.

## Decisões metodológicas

1. `CO_CURSO` permanece a unidade principal.
2. Duplicidade em qualquer lado de uma junção é erro impeditivo.
3. Ausência de conceito é preservada e nunca convertida em Conceito Enade 1.
4. Contagens esperadas são parâmetros de regressão, não constantes embutidas no validador.
5. O DataFrame recebido não é alterado pelas funções do núcleo.

## Uso previsto

Letras–Inglês será a primeira área nova a consumir diretamente esse núcleo. Matemática e Física poderão ser migradas gradualmente após a validação da terceira área.
