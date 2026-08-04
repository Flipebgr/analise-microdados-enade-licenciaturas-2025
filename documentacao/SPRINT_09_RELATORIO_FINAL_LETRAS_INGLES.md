# Sprint 09 — Relatório técnico-científico final de Letras–Inglês

## Objetivo

Consolidar os produtos validados das Sprints 07 e 08 em relatório técnico-científico final de Letras–Inglês (`CO_GRUPO=6407`), em estrutura compatível com o modelo ABNT adotado no projeto.

## Fontes analíticas

O relatório lê exclusivamente produtos agregados por `CO_CURSO` já produzidos e validados nas Sprints 07 e 08. Não reabre os 28 arquivos temáticos para criar vínculos individuais e não realiza junções entre registros de estudantes.

## Estrutura

- elementos pré-textuais;
- Introdução;
- Referencial institucional e metodológico;
- Metodologia;
- Panorama da licenciatura;
- 5.1 Desempenho;
- 5.2 Perfil demográfico e socioeconômico;
- 5.3 Trajetória e condições acadêmicas;
- 5.4 Processo formativo;
- 5.5 Recomendação;
- 5.6 Benchmark comparável;
- 5.7 Associações ecológicas;
- 5.8 Comparação regional e nacional;
- Discussão;
- Conclusão;
- Referências;
- Apêndices.

## Regras metodológicas preservadas

- unidade principal: `CO_CURSO`;
- nenhuma identificação artificial de estudante;
- nenhuma junção individual entre arquivos temáticos;
- junções analíticas somente após agregação por curso e com validação one-to-one;
- ausência de Conceito Enade não equivale a Conceito 1;
- grupos A–E exclusivos nas comparações independentes;
- Norte e Brasil completos usados como benchmarks descritivos sobrepostos;
- médias ponderadas de desempenho usam participantes válidos;
- correlações entre temas distintos são ecológicas e não causais;
- `QE_I20–QE_I66` não são reduzidos a índice único sem validação teórica.

## Produtos

- `relatorios/ingles/relatorio_letras_ingles_enade_2025.docx`;
- `relatorios/ingles/relatorio_letras_ingles_enade_2025.md`;
- PDF quando LibreOffice estiver disponível.

## Validação

O relatório possui validador estrutural próprio, testes unitários para as sínteses e tabelas principais e testes de integração que exigem os produtos locais das Sprints 07 e 08.
