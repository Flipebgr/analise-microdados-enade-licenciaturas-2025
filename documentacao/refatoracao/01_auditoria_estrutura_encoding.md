# Refactor 01 ÔÇö Auditoria da estrutura consolidada e do encoding

## Objetivo

Registrar o estado real do reposit├│rio consolidado antes da cria├º├úo do n├║cleo compartilhado, separar limita├º├Áes dos pacotes incrementais de problemas do c├│digo principal e padronizar arquivos textuais em UTF-8.

## Conclus├Áes arquiteturais

1. Os pacotes ZIP usados no projeto s├úo incrementais. Eles n├úo s├úo distribui├º├Áes autossuficientes e devem ser aplicados sobre a vers├úo consolidada indicada no `INSTRUCOES.md`.
2. O reposit├│rio consolidado possui m├│dulos compartilhados em `src/agregacao`, `src/analise`, `src/configuracao`, `src/extracao`, `src/utilitarios`, `src/validacao` e `src/visualizacao`.
3. A estrutura de F├¡sica em `src/fisica` ├® funcional, mas assim├®trica em rela├º├úo ├á estrutura de Matem├ítica. Essa assimetria ser├í reduzida progressivamente, sem reescrever retrospectivamente todas as sprints.
4. O `requirements.txt` da raiz ├® a fonte ├║nica de depend├¬ncias. Pacotes incrementais n├úo devem criar arquivos de depend├¬ncias paralelos.
5. A tag `pre-refatoracao-arquitetural` ├® o ponto de recupera├º├úo anterior ├á refatora├º├úo.

## Encoding

A codifica├º├úo padr├úo passa a ser UTF-8, com finais de linha LF para arquivos textuais versionados. O arquivo `.editorconfig` registra essas regras.

A auditoria ├® executada por:

```powershell
python executar_refactor_01.py
```

Para aplicar apenas substitui├º├Áes conservadoras conhecidas:

```powershell
python executar_refactor_01.py --corrigir
```

O resultado ├® gravado em:

```text
documentacao/refatoracao/resultado_auditoria_encoding.json
```

O modo de corre├º├úo n├úo tenta adivinhar a codifica├º├úo integral de um arquivo. Sequ├¬ncias n├úo reconhecidas permanecem no relat├│rio para revis├úo manual.

## Baseline

`baseline_pre_refatoracao.json` registra contagens e restri├º├Áes metodol├│gicas que n├úo podem mudar silenciosamente durante a refatora├º├úo. Ele n├úo substitui os testes anal├¡ticos existentes; funciona como contrato de regress├úo de alto n├¡vel.

## Crit├®rio de conclus├úo

A etapa pode ser integrada em `refactor/nucleo-compartilhado` quando:

- `python executar_refactor_01.py --corrigir` terminar sem ocorr├¬ncias pendentes, ou as pend├¬ncias forem justificadas e registradas;
- `pytest -q` passar;
- `ruff check .` passar;
- nenhuma contagem do baseline tiver sido alterada;
- nenhuma sa├¡da de Matem├ítica ou F├¡sica tiver sido removida.
