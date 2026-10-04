# Prompt inicial sugerido para o Codex

Copie o texto abaixo na primeira sessão do Codex aberta na raiz do repositório.

---

Leia integralmente `AGENTS.md` e, antes de modificar qualquer arquivo, leia também:

- `documentacao/CONTEXTO_PROJETO_CODEX.md`
- `documentacao/ADAPTACAO_ENADE_2017.md`
- `documentacao/PLANO_EVOLUCAO_PIPELINE.md`
- `documentacao/FONTES_ENADE_2017.md`
- `documentacao/ARQUITETURA.md`
- `documentacao/METODOLOGIA.md`

Objetivo desta sessão: iniciar a adaptação multi-edição do projeto para processar o Enade 2017 sem quebrar os contratos existentes de 2025. A primeira área de validação será Ciências Biológicas — Bacharelado (`CO_GRUPO=1601`), mas não crie um pipeline específico da área como solução principal.

Antes de codificar:

1. inspecione a árvore atual, `config.yaml`, `executar.py`, `src/` e `tests/`;
2. execute a baseline de testes e Ruff;
3. identifique todos os pontos hardcoded em 2025 que afetam a edição 2017;
4. proponha um plano incremental e liste exatamente os arquivos que pretende criar/alterar;
5. espere minha aprovação do plano antes de realizar uma refatoração ampla.

Regras essenciais:

- unidade principal `CO_CURSO`;
- não reconstruir estudante entre arquivos temáticos;
- não usar posição de linha como chave;
- agregar por curso antes de joins entre arquivos;
- não reutilizar semântica de `QE_*` de 2025 em 2017;
- não inventar `PROFICIENCIA`, recomendação ou outros indicadores ausentes em 2017;
- preservar `SC` como sem conceito;
- não editar arquivos em `dados_brutos/`;
- manter compatibilidade com o pipeline/núcleo 2025;
- preferir adapters/configuração por edição a condicionais espalhadas.

Nesta primeira resposta, não implemente ainda. Entregue a auditoria do código atual e o plano da Fase 1, com riscos e critérios de aceite.

---
