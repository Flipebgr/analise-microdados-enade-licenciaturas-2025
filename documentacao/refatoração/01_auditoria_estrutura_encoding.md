# Refactor 01 — Auditoria da estrutura consolidada e do encoding

## Objetivo

Registrar o estado real do repositório consolidado antes da criação do núcleo compartilhado, separar limitações dos pacotes incrementais de problemas do código principal e padronizar arquivos textuais em UTF-8.

## Conclusões arquiteturais

1. Os pacotes ZIP usados no projeto são incrementais. Eles não são distribuições autossuficientes e devem ser aplicados sobre a versão consolidada indicada no `INSTRUCOES.md`.
2. O repositório consolidado possui módulos compartilhados em `src/agregacao`, `src/analise`, `src/configuracao`, `src/extracao`, `src/utilitarios`, `src/validacao` e `src/visualizacao`.
3. A estrutura de Física em `src/fisica` é funcional, mas assimétrica em relação à estrutura de Matemática. Essa assimetria será reduzida progressivamente, sem reescrever retrospectivamente todas as sprints.
4. O `requirements.txt` da raiz é a fonte única de dependências. Pacotes incrementais não devem criar arquivos de dependências paralelos.
5. A tag `pre-refatoracao-arquitetural` é o ponto de recuperação anterior à refatoração.

## Encoding

A codificação padrão passa a ser UTF-8, com finais de linha LF para arquivos textuais versionados. O arquivo `.editorconfig` registra essas regras.

A auditoria é executada por:

```powershell
python executar_refactor_01.py
```

Para aplicar apenas substituições conservadoras conhecidas:

```powershell
python executar_refactor_01.py --corrigir
```

O resultado é gravado em:

```text
documentacao/refatoracao/resultado_auditoria_encoding.json
```

O modo de correção não tenta adivinhar a codificação integral de um arquivo. Sequências não reconhecidas permanecem no relatório para revisão manual.

## Baseline

`baseline_pre_refatoracao.json` registra contagens e restrições metodológicas que não podem mudar silenciosamente durante a refatoração. Ele não substitui os testes analíticos existentes; funciona como contrato de regressão de alto nível.

## Critério de conclusão

A etapa pode ser integrada em `refactor/nucleo-compartilhado` quando:

- `python executar_refactor_01.py --corrigir` terminar sem ocorrências pendentes, ou as pendências forem justificadas e registradas;
- `pytest -q` passar;
- `ruff check .` passar;
- nenhuma contagem do baseline tiver sido alterada;
- nenhuma saída de Matemática ou Física tiver sido removida.
