# Sprint 11 — Validação analítica de Ciências Biológicas com foco em Soure

## Objetivo

Validar os produtos da Sprint 10 e aprofundar a análise da oferta de Ciências Biológicas da UFPA em Soure (`CO_CURSO=104640`) sem transformar diferenças descritivas em explicações causais.

## Desenho analítico

A unidade principal permanece `CO_CURSO`. Não existe oferta UFPA de Ciências Biológicas com Conceito Enade 1, portanto não se cria artificialmente um grupo de Conceito 1. Soure é o caso focal e é contrastada com:

- demais ofertas da UFPA;
- outras IES do Pará;
- Norte sem Pará;
- Brasil sem Norte;
- benchmark estruturalmente comparável.

## Validações

1. auditoria de participantes, presença e Ns válidos;
2. sensibilidade do benchmark de Soure por modalidade, categoria administrativa, organização acadêmica e porte;
3. descritivas e correlações individuais apenas dentro do arquivo de desempenho;
4. perfil demográfico, socioeconômico e de trajetória no nível agregado do curso;
5. comparação item a item de `QE_I20–QE_I66`;
6. dimensões do processo formativo somente como diagnóstico exploratório;
7. recomendação (`QE_I68`, `QE_I69`, `QE_I70`) usando os indicadores já agregados;
8. outliers por 1,5×IQR, sem exclusão automática;
9. associações ecológicas de Spearman entre indicadores agregados por curso.

## Sensibilidade do benchmark

São produzidos cinco cenários progressivos:

1. mesma modalidade;
2. modalidade + categoria administrativa;
3. modalidade + categoria + organização acadêmica;
4. estrutura completa + participantes entre 0,5× e 2,0× Soure;
5. estrutura completa + participantes entre 0,75× e 1,5× Soure.

A estabilidade das diferenças de `NT_GER`, `NT_OBJ`, `NT_DIS` e presença é usada como diagnóstico de robustez.

## Processo formativo

Os 47 itens `QE_I20–QE_I66` são preservados individualmente. A Sprint 11 não atribui rótulos substantivos automaticamente aos códigos e não cria índice único. Antes do relatório final é obrigatório vincular os códigos ao texto oficial, conferir direção da escala e possíveis itens invertidos, e justificar teoricamente qualquer agrupamento dimensional.

## Restrições metodológicas

- não usar posição da linha como chave;
- não reconstruir estudante entre arquivos;
- não correlacionar individualmente variáveis de arquivos temáticos distintos;
- correlações entre perfil/processo e desempenho são ecológicas;
- não tratar interiorização, porte, perfil socioeconômico ou modalidade como causas sem desenho causal;
- informar N, dispersão e ausências;
- não interpretar ausência de conceito como Conceito 1.

## Produtos

A sprint gera CSVs de auditoria, sensibilidade, análise individual de desempenho, perfil focal, processo formativo, dimensões exploratórias, outliers e associações ecológicas, além de seis figuras validadas e o relatório `relatorios/sprint_11_validacao_biologia_soure.md`.
