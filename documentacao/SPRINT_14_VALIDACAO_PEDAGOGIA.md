# Sprint 14 — Validação analítica de Pedagogia

## Objetivo

Validar os produtos da Sprint 13 e aprofundar o contraste interno entre a oferta de Castanhal, Conceito Enade 5, e as seis ofertas da UFPA com Conceito Enade 4, mantendo comparações territoriais e benchmarks estruturais.

## Princípios

- `CO_CURSO` continua sendo a unidade principal.
- Não existe oferta UFPA com Conceito Enade 1 em Pedagogia.
- Conceito 4 não é tratado como insuficiência.
- Castanhal é referência interna descritiva, não grupo causal.
- Não são realizadas junções individuais entre arquivos temáticos.
- Relações entre desempenho e indicadores de outros arquivos são apenas ecológicas.
- QE_I20–QE_I66 permanecem item a item até vinculação ao texto oficial e validação teórica.

## Produtos

A Sprint 14 gera auditorias de participação e indicadores, comparação regional validada, cinco cenários de benchmark para cada uma das sete ofertas da UFPA, contraste interno validado, perfil por recorte, comparação do processo formativo de Castanhal, outliers e associações ecológicas.

## Sensibilidade do benchmark

Para cada oferta UFPA são testados:

1. mesma modalidade;
2. modalidade + categoria administrativa;
3. modalidade + categoria + organização acadêmica;
4. estrutura + porte entre 0,5x e 2,0x participantes;
5. estrutura + porte entre 0,75x e 1,5x participantes.

O cenário 4 é o benchmark estrutural principal. Cenários mais restritivos são usados apenas como análise de sensibilidade.

## Figuras validadas

- participação das ofertas da UFPA;
- contraste interno Castanhal versus média UFPA Conceito 4;
- benchmark estrutural por oferta;
- itens QE_I20–QE_I66 com maiores diferenças internas;
- perfil agregado interno;
- comparação regional e nacional.

## Validação

```cmd
python executar_sprint_14.py
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```
