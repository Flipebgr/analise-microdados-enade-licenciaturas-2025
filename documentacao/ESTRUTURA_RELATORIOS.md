# Estrutura dos relatórios técnico-científicos

## 1. Princípio geral

Os relatórios são gerados a partir de produtos agregados e validados por `CO_CURSO`. O gerador de relatório não deve criar vínculos individuais entre arquivos temáticos.

## 2. Estrutura-base

Os relatórios finais seguem, em geral:

1. elementos pré-textuais;
2. Introdução;
3. Referencial institucional e metodológico;
4. Metodologia;
5. Panorama da licenciatura;
6. Resultados;
7. Discussão;
8. Conclusão;
9. Referências;
10. Apêndices e, quando necessário, Anexos.

Em Resultados:

- 5.1 Desempenho;
- 5.2 Perfil demográfico e socioeconômico;
- 5.3 Trajetória e condições acadêmicas;
- 5.4 Processo formativo;
- 5.5 Recomendação;
- 5.6 Benchmark comparável;
- 5.7 Associações ecológicas;
- 5.8 Comparações regionais e nacionais, quando implementadas;
- 5.9 estudo focal ou contraste interno, quando o desenho da área exigir.

## 3. Formatação

O modelo técnico adotado usa:

- margens superior e esquerda: 3 cm;
- margens inferior e direita: 2 cm;
- fonte Arial 12 no corpo;
- texto justificado;
- espaçamento 1,5;
- corpo menor e espaçamento simples para fontes, notas e elementos auxiliares.

A instituição deve conferir requisitos locais de capa, folha de rosto, ficha catalográfica e demais elementos obrigatórios.

## 4. Redação dos resultados

Cada resultado deve distinguir:

- **descrição** — o que os dados mostram;
- **interpretação** — leitura substantiva compatível com o desenho;
- **hipótese** — explicação possível que exige investigação;
- **limitação** — restrição de dados, N, desenho ou comparabilidade.

Formulações causais são proibidas sem desenho causal.

## 5. Tabelas

Tabelas devem informar, quando aplicável:

- indicador;
- unidade;
- N válido;
- grupo/recorte;
- dispersão;
- ausências;
- fonte.

Cursos sem conceito não podem ser apresentados como Conceito 1.

## 6. Figuras

Figuras devem informar ou permitir recuperar:

- variável;
- nível de análise;
- grupo/recorte;
- modalidade quando pertinente;
- N válido;
- exclusões;
- tratamento de ausências;
- fonte.

Recursos recomendados:

- boxplots;
- ECDF;
- dotplots;
- barras percentuais;
- heatmaps;
- gráficos Likert.

Histogramas e violin plots devem ser usados somente quando o N for adequado.

## 7. Comparação regional

Quando implementada, a narrativa pode incluir:

- oferta individual da UFPA;
- UFPA agregada;
- Norte sem UFPA;
- Norte completo como benchmark descritivo;
- demais regiões;
- Brasil geral;
- Brasil sem UFPA;
- restante do Brasil sem Norte.

Média simples de cursos e média ponderada por participantes respondem a perguntas diferentes e devem ser identificadas explicitamente.

## 8. Processo formativo

`QE_I20–QE_I66` deve manter o vínculo com os textos oficiais.

Não criar média global ou índice dimensional sem validação específica.

## 9. Recomendação

`QE_I68`, `QE_I69` e `QE_I70`, quando usados, devem manter os rótulos oficiais e permanecer conceitualmente separados.

Não utilizar automaticamente “satisfação” como sinônimo.

## 10. Referências

Não inventar referências.

Incluir somente fontes efetivamente utilizadas/citadas, priorizando:

- legislação e documentos oficiais do SINAES/Enade;
- microdados e documentação do Inep;
- Questionário do Estudante;
- notas técnicas pertinentes;
- normas efetivamente aplicadas;
- referências metodológicas citadas no texto.

## 11. Formatos de saída

Produto textual auditável:

```text
Markdown
```

Produto de entrega:

```text
DOCX
```

Produto opcional:

```text
PDF
```

A ausência de LibreOffice não invalida DOCX ou Markdown.

## 12. Aprofundamentos

Ao final de cada área, sugerir de 3 a 5 aprofundamentos com:

- justificativa;
- pergunta;
- variáveis;
- método;
- limitações.

Eles não devem ser executados automaticamente sem nova prioridade.
