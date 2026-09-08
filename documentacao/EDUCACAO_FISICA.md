# Educação Física — ENADE Licenciaturas 2025 / UFPA

## Estado

Área ativa na branch `feature/educacao-fisica`.

- `CO_GRUPO = 3502`;
- universo nacional identificado nas fontes 2025: 406 cursos;
- UFPA: 2 ofertas;
- Castanhal (`CO_CURSO=21849`): Presencial, Conceito Enade 4;
- Belém (`CO_CURSO=104598`): Presencial, Conceito Enade 4;
- não há oferta UFPA Conceito Enade 1 localizada nas fontes oficiais.

## Pergunta central adaptada

> Quais são as características de desempenho, composição discente,
> trajetória acadêmica e avaliação do processo formativo das ofertas de
> Educação Física da UFPA, e como elas se posicionam em relação às demais
> ofertas da mesma área no Pará, na Região Norte e no Brasil?

O contraste interno da UFPA será Belém versus Castanhal. O contraste não
pressupõe problema em qualquer campus e não substitui os benchmarks externos.

## Grupos comparativos

Os grupos territoriais exclusivos permanecem:

- B — ofertas da UFPA com conceito superior a 1;
- C — outras IES do Pará;
- D — restante da Região Norte, excluindo Pará;
- E — restante do Brasil, excluindo Norte.

O Grupo A é vazio nesta área porque não existe oferta UFPA Conceito 1.

## Unidade de análise

`CO_CURSO`.

Arquivos temáticos são agregados separadamente antes de qualquer junção.
Não há reconstrução de identificadores individuais nem join individual
entre arquivos diferentes.

## Entrega 01 — base analítica

A primeira entrega gera:

- catálogo nacional;
- tabela-mestra UFPA;
- auditoria das duas fontes;
- agregados de desempenho;
- demografia;
- trajetória;
- perfil socioeconômico;
- processo formativo item a item;
- recomendação;
- base analítica uma linha por curso;
- benchmarks amplos;
- benchmark comparável para cada oferta UFPA;
- comparação Belém × Castanhal;
- distribuições auxiliares para as etapas seguintes.

A validação fixa a edição 2025 em 406 cursos e as duas ofertas UFPA
`21849` e `104598`.
