# Relatório regional de Física

## Objetivo

Comparar a nota geral (`NT_GER`) das ofertas de Física da UFPA com a Região Norte, as demais regiões brasileiras e o Brasil geral.

## Unidade de análise

A unidade principal é `CO_CURSO`. A base de desempenho já agregada por curso é relacionada ao cadastro regional somente após a obtenção de uma linha por curso. Não há join individual entre arquivos temáticos.

## Referências

- UFPA agregada;
- Norte sem UFPA;
- Norte completo, como benchmark descritivo;
- Nordeste, Sudeste, Sul e Centro-Oeste;
- Brasil geral;
- Brasil sem UFPA;
- Brasil sem Norte.

## Estatísticas

- média ponderada pelo número de participantes com `NT_GER` válida;
- média e mediana das médias dos cursos;
- dispersão entre cursos;
- intervalo bootstrap por reamostragem de cursos, semente 2025;
- diferença absoluta e tamanho de efeito padronizado;
- posição percentílica das ofertas da UFPA.

## Limitações

As comparações são descritivas e ecológicas. A região e a instituição não são tratadas como causas da nota. A oferta de Tucuruí (`CO_CURSO=1627581`) não integra os cálculos porque não foi localizada nas fontes analíticas utilizadas.
