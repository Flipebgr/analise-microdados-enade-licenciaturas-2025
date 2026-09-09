UNIVERSIDADE FEDERAL DO PARÁ

ENADE DAS LICENCIATURAS 2025

MÚSICA

**Desempenho, perfil discente, processo formativo e benchmarks da oferta da UFPA**

Belém  
2026

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# MÚSICA NO ENADE DAS LICENCIATURAS 2025: DESEMPENHO, PERFIL, PROCESSO FORMATIVO E BENCHMARKS DA OFERTA DA UFPA

## RESUMO

Este relatório técnico-científico analisa a Licenciatura em Música da Universidade Federal do Pará (UFPA) no Enade das Licenciaturas 2025. O universo reúne 107 cursos identificados por `CO_CURSO`. A UFPA possui uma única oferta localizada nas fontes analisadas, em Belém, presencial (`CO_CURSO=114950`), com 44 inscritos, 37 participantes, participação oficial de 84,1% e Conceito Enade 1. Não há outra oferta de Música da UFPA nem outra oferta da área no Pará nas fontes oficiais, de modo que os grupos B e C são estruturalmente vazios. A oferta apresenta NT_GER médio de 41,64, situando-se no percentil 19,4 da distribuição nacional das médias de curso. O contraste com cursos estruturalmente comparáveis indica diferença de cerca de 8 pontos abaixo da mediana do benchmark. Em contrapartida, as avaliações do processo formativo e os itens de recomendação são, em geral, favoráveis. Os resultados evidenciam uma configuração multidimensional e não sustentam causalidade individual.

**Palavras-chave:** Enade; Música; UFPA; formação de professores; microdados; Conceito Enade; benchmark.

## ABSTRACT

This technical-scientific report examines the UFPA Music teacher-education program in the 2025 Enade. The analytical universe comprises 107 courses. UFPA has one on-campus offer in Belém (`CO_CURSO=114950`), with 44 enrolled students, 37 participants and Enade Concept 1. There are no other UFPA Music offers and no other Music offers in Pará in the official sources. UFPA's mean NT_GER is 41,64, around the 19,4th national percentile of course means, and roughly eight points below the median of structurally comparable courses. Formative-process perceptions and recommendation indicators, however, are generally favorable. Results are descriptive and non-causal.

**Keywords:** Enade; Music; UFPA; teacher education; microdata; benchmark.

# 1 INTRODUÇÃO

A pergunta central é: **quais características de desempenho, composição discente, trajetória acadêmica e avaliação do processo formativo diferenciam a oferta de Música da UFPA, com Conceito Enade 1, das demais ofertas da mesma área na Região Norte e no Brasil?**

A planilha oficial identifica 107 ofertas nacionais, mas apenas uma oferta da UFPA e nenhuma outra oferta de Música no Pará. Assim, os contrastes principais são com o restante da Região Norte, o restante do Brasil, os cursos nacionais de Conceito 1, os cursos de conceito superior e benchmarks estruturalmente comparáveis.

# 2 REFERENCIAL INSTITUCIONAL E METODOLÓGICO

O Enade integra o Sistema Nacional de Avaliação da Educação Superior (Sinaes) e fornece evidências de desempenho e informações declaradas pelos estudantes sobre trajetória, perfil e experiência formativa. O Conceito Enade é tratado como classificação externa do curso, não como variável causal nem explicação suficiente do desempenho.

Resultados de prova, composição discente, condições acadêmicas, processo formativo e recomendação são dimensões distintas. A coexistência de resultados favoráveis e desfavoráveis entre dimensões é interpretada como heterogeneidade institucional.

# 3 METODOLOGIA

A unidade principal é `CO_CURSO`. Os 28 arquivos temáticos não permitem reconhecer o mesmo estudante entre temas. Não se utiliza posição de linha como chave, não se cria identificador artificial e não se realizam joins individuais entre desempenho, perfil e percepção. O fluxo é: arquivo temático → tratamento de ausências → agregação por `CO_CURSO` → uma linha por curso → junções one-to-one → comparação entre cursos.

`NT_GER`, `NT_OBJ` e `NT_DIS` são examinadas conjuntamente porque pertencem ao mesmo arquivo. Relações entre desempenho e indicadores de questionário ou perfil são apenas ecológicas.

Grupos exclusivos: A) UFPA Conceito 1, N=1; B) demais ofertas UFPA com conceito superior, N=0; C) outras IES do Pará, N=0; D) restante da Região Norte, N=8; E) restante do Brasil, N=98. B e C permanecem vazios.

O benchmark mantém modalidade, categoria administrativa e organização acadêmica e varia a janela de porte em 0,75–1,25x, 0,50–1,50x e 0,50–2,00x o número de participantes da oferta UFPA.

No processo formativo, `QE_I20–QE_I66` usam respostas 1–6; 7 e 8 são ausências analíticas. `QE_I31`, `QE_I32` e `QE_I43` são específicos de EaD e não entram nas dimensões comuns da oferta presencial. Não há itens invertidos. As oito dimensões são exploratórias e não formam índice global.

No desempenho, reportam-se média, mediana, dispersão, IC95%, diferença padronizada de Hedges e comparação com os recortes externos usando somente o arquivo de desempenho.

# 4 PANORAMA DA LICENCIATURA EM MÚSICA

O universo contém **107 cursos** de Música. A distribuição dos conceitos é: Conceito 1 = 44; Conceito 2 = 36; Conceito 3 = 14; Conceito 4 = 8; Conceito 5 = 1; sem conceito numérico = 4. A concentração nacional em Conceito 1 torna indispensável observar também a nota contínua.

## Tabela 1 – Oferta de Música da UFPA

| CO_CURSO | Oferta | Inscritos | Participantes | Participação | Padrão de proficiência | Conceito | NT_GER | NT_OBJ | NT_DIS | Percentil Brasil |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 114950 | Belém — Presencial | 44 | 37 | 84,1% | 24,3% | 1 | 41,64 | 39,27 | 5,11 | 19,4 |

A taxa de presença no arquivo de desempenho coincide com a participação oficial: 84,1%. Não houve reaplicações.

# 5 RESULTADOS

## 5.1 Desempenho

A UFPA apresenta `NT_GER` médio de **41,64**, mediana de 40,68, DP de 10,92 e IC95% de 38,12 a 45,16. O `NT_OBJ` médio é 39,27 e o `NT_DIS` médio é 5,11.

Entre os 103 cursos nacionais com `NT_GER` calculável, a UFPA está no percentil **19,4**.

### Tabela 2 – Referências territoriais de desempenho

| Recorte | Cursos | Cursos com NT_GER | Média NT_GER | Mediana NT_GER | Média NT_OBJ | Média NT_DIS |
|---|---:|---:|---:|---:|---:|---:|
| UFPA — Belém | 1 | 1 | 41,64 | 41,64 | 39,27 | 5,11 |
| Norte sem Pará | 8 | 7 | 41,67 | 43,68 | 41,11 | 4,39 |
| Brasil sem Norte | 98 | 95 | 47,98 | 47,98 | 45,69 | 5,71 |

No arquivo de desempenho, a diferença de `NT_GER` entre UFPA e Norte sem Pará é -2,06 pontos (IC95% -6,97 a 2,86; Hedges g=-0,158). Frente ao Brasil sem Norte, a diferença é -4,54 pontos (IC95% -8,22 a -0,85; g=-0,331). O contraste é mais forte em `NT_OBJ`; em `NT_DIS` o efeito é pequeno.

O percentual no padrão de proficiência é **24,3%** (9 de 37 participantes).

## 5.2 Perfil demográfico e socioeconômico

Entre 44 registros válidos de sexo, 36,4% são do sexo feminino. A idade média é 31,77 anos e a mediana, 28,50.

Em raça/cor (`QE_I03`, N=40), a distribuição válida é: Parda 70,0% (n=28), Preta 17,5% (n=7), Branca 7,5% (n=3), Não quer declarar 5,0% (n=2). Quatro registros não tiveram resposta analítica válida.

### Tabela 3 – Perfil selecionado da oferta UFPA

| Indicador | Valor | N válido |
|---|---:|---:|
| Sexo feminino | 36,4% | 44 |
| Idade média (anos) | 31,77 | 44 |
| Primeira geração no ensino superior | 38,9% | 36 |
| Mãe com ensino superior | 25,6% | 39 |
| Pai com ensino superior | 20,6% | 34 |
| Renda até 3 SM | 75,0% | 40 |
| Trabalha | 52,5% | 40 |
| Trabalha 40h | 7,5% | 40 |
| Ação afirmativa | 42,5% | 40 |
| Auxílio permanência | 12,5% | 40 |
| Bolsa acadêmica | 74,4% | 39 |
| Estudo ≥4h/semana | 55,0% | 40 |
| Pretende magistério | 80,0% | 40 |

A renda até três salários mínimos alcança 75,0%, acima das medianas do Norte sem Pará (64,9%) e do Brasil sem Norte (59,5%). A bolsa acadêmica aparece em 74,4% e o auxílio permanência em 12,5% das respostas válidas.
Essas diferenças são descritivas; não podem explicar individualmente o desempenho porque os indicadores vêm de arquivos distintos.

## 5.3 Trajetória e condições acadêmicas

O tempo médio desde o ingresso é 5,07 anos. O turno noturno não aparece entre os 44 registros válidos. A proporção que estuda quatro horas ou mais por semana é 55,0%. A intenção de exercer o magistério é 80,0%.
No `QE_I70`, 37 dos 40 respondentes válidos escolheram “Quero ser professor da rede pública”, indicando forte interesse declarado pela docência pública.

## 5.4 Processo formativo

As médias UFPA nas oito dimensões variam entre 5,09 e 5,46, em escala de 1 a 6.

### Tabela 4 – Dimensões do processo formativo

| Dimensão | UFPA | N UFPA | Mediana Norte sem Pará | Mediana Brasil sem Norte |
|---|---:|---:|---:|---:|
| Oportunidades | 5,12 | 39 | 5,34 | 4,93 |
| Atuação docente | 5,44 | 40 | 5,16 | 5,18 |
| Organização / teoria-prática | 5,43 | 40 | 5,16 | 5,12 |
| Infraestrutura | 5,09 | 38 | 4,80 | 4,79 |
| Planejamento / ensino | 5,40 | 40 | 5,36 | 5,21 |
| Inclusão / diversidade | 5,12 | 38 | 4,92 | 4,84 |
| Gestão / avaliação | 5,28 | 40 | 5,17 | 5,04 |
| Colaboração / famílias | 5,46 | 39 | 5,26 | 5,23 |

Na UFPA, os alfas calculáveis variam de 0,748 a 0,956. Em infraestrutura e recursos há apenas 9 casos completos, abaixo do mínimo de 10 adotado, e por isso o alfa UFPA não é reportado. Alfa elevado não comprova unidimensionalidade.
A oferta apresenta avaliações formativas favoráveis apesar do baixo posicionamento relativo em desempenho, o que impede uma leitura monocausal do Conceito 1.

## 5.5 Recomendação
No `QE_I68`, recomendação do curso, a média é **8,88** (N=40). No `QE_I69`, recomendação da IES, a média é **9,55** (N=40). As medianas Norte sem Pará são 8,48 e 9,27; no Brasil sem Norte, 8,56 e 8,88.
Os itens são tratados como recomendação, conforme o instrumento oficial, e não como satisfação.

## 5.6 Benchmark comparável
A análise produz entre 5 e 11 cursos comparáveis, dependendo da janela de porte.

### Tabela 5 – Sensibilidade do benchmark comparável em NT_GER

| Critério de porte | N comparáveis | NT_GER UFPA | Média benchmark | Mediana benchmark | Diferença para mediana |
|---|---:|---:|---:|---:|---:|
| ±25% | 5 | 41,64 | 48,30 | 49,30 | -7,66 |
| 0,5–1,5x | 10 | 41,64 | 49,22 | 49,95 | -8,30 |
| 0,5–2x | 11 | 41,64 | 49,13 | 49,68 | -8,03 |

A diferença para a mediana permanece entre aproximadamente -7,7 e -8,3 pontos. A estabilidade torna o contraste mais informativo que a comparação territorial ampla, embora o pareamento observacional não controle todas as diferenças institucionais.

## 5.7 Associações ecológicas

### Tabela 6 – Associações ecológicas com NT_GER médio

| Indicador agregado | N cursos | Spearman ρ | p |
|---|---:|---:|---:|
| Renda até 3 SM | 103 | -0,293 | 0,0027 |
| Trabalha | 103 | -0,021 | 0,8345 |
| Auxílio permanência | 103 | 0,455 | 0,0000 |
| Recomendação do curso (QE_I68) | 103 | -0,261 | 0,0078 |
| Recomendação da IES (QE_I69) | 103 | 0,009 | 0,9299 |
| Atuação docente | 103 | -0,169 | 0,0885 |
| Infraestrutura e recursos | 103 | -0,333 | 0,0006 |
| Organização e integração | 103 | -0,263 | 0,0073 |

As maiores magnitudes aparecem em auxílio permanência, infraestrutura e recursos e renda até três salários mínimos. Essas associações são ecológicas e podem refletir composição, políticas institucionais, padrões de resposta e variáveis não modeladas; não autorizam interpretação individual ou causal.

## 5.8 Narrativa gráfica

### Figura 1 – Oferta UFPA: participação e proficiência

![Figura 1 – Oferta UFPA: participação e proficiência](/mnt/data/musica_report_figures/01_painel_oferta_ufpa.png)

Nota: N=44 inscritos; N=37 participantes; oferta presencial UFPA; ausências não são recodificadas.

Participação oficial de 84,1% e 24,3% no padrão de proficiência. A presença elevada indica que o baixo resultado não pode ser atribuído simplesmente à baixa adesão. Limitação: participação não explica desempenho.

### Figura 2 – Posição relativa de NT_GER

![Figura 2 – Posição relativa de NT_GER](/mnt/data/musica_report_figures/02_posicao_relativa_nt_ger.png)

Nota: N=103 cursos com NT_GER calculável; mesma área de Música; a UFPA é destacada.

A UFPA está no percentil 19,4 nacional das médias de curso. Hipótese: a faixa 1 corresponde também a posição baixa na nota contínua. Limitação: média do curso não descreve toda a dispersão individual.

### Figuras 3 a 5 – NT_GER, NT_OBJ e NT_DIS

![Figuras 3 a 5 – NT_GER, NT_OBJ e NT_DIS](/mnt/data/musica_report_figures/03a_distribuicao_nt_ger.png)

Nota: N válido indicado no próprio gráfico; variáveis do mesmo arquivo de desempenho.

![Figura 4 – Distribuição individual de NT_OBJ](/mnt/data/musica_report_figures/03b_distribuicao_nt_obj.png)

Nota: N válido indicado no gráfico; mesma fonte temática de desempenho.

![Figura 5 – Distribuição individual de NT_DIS](/mnt/data/musica_report_figures/03c_distribuicao_nt_dis.png)

Nota: N válido indicado no gráfico; mesma fonte temática de desempenho.

Os boxplots usam apenas o arquivo de desempenho. O distanciamento é mais visível em NT_OBJ; em NT_DIS é pequeno. Limitação: NT_OBJ e NT_DIS têm relação mecânica com NT_GER.

### Figura 6 – Perfil socioeconômico

![Figura 6 – Perfil socioeconômico](/mnt/data/musica_report_figures/04_perfil_socioeconomico.png)

Nota: percentuais entre respostas válidas; benchmarks são medianas de cursos dos recortes.

A UFPA apresenta maior renda baixa e menor trabalho que as medianas externas, além de ação afirmativa e bolsa acadêmica elevadas. Limitação: esses indicadores não podem ser ligados individualmente às notas.

### Figura 7 – Processo formativo

![Figura 7 – Processo formativo](/mnt/data/musica_report_figures/05_processo_formativo_dimensoes.png)

Nota: escala 1–6; respostas 7 e 8 tratadas como ausências; QE_I31, QE_I32 e QE_I43 excluídos das dimensões comuns.

As médias UFPA são altas e em geral superiores às medianas externas. Isso evidencia que percepção formativa favorável e baixo resultado na prova podem coexistir. Limitação: dimensões exploratórias e autorrelato.

### Figura 8 – Benchmark comparável

![Figura 8 – Benchmark comparável](/mnt/data/musica_report_figures/06_benchmark_sensibilidade.png)

Nota: mesma modalidade, categoria administrativa e organização acadêmica; janelas de porte explicitadas no eixo.

A mediana dos pares permanece acima da UFPA nas três janelas. A estabilidade reforça o diagnóstico de diferença de desempenho, sem causalidade.

### Figura 9 – Recomendação

![Figura 9 – Recomendação](/mnt/data/musica_report_figures/07_recomendacao.png)

Nota: QE_I68 e QE_I69 em escala 0–10; não interpretados automaticamente como satisfação.

Curso e IES têm médias altas, sobretudo a recomendação da instituição. Recomendação e desempenho são construtos distintos.

### Figura 10 – Associação ecológica

![Figura 10 – Associação ecológica](/mnt/data/musica_report_figures/08_associacao_ecologica.png)

Nota: unidade = curso; associação de Spearman; interpretação ecológica, não individual.

A dispersão entre cursos e a posição da UFPA mostram que o coeficiente não deve ser lido isoladamente. Limitação: falácia ecológica e outliers.

### Figura 11 – Síntese

![Figura 11 – Síntese](/mnt/data/musica_report_figures/09_sintese_ufpa.png)

Nota: indicadores em escalas percentuais/percentis; não constituem índice único.

Reúne percentil de desempenho, participação, proficiência e indicadores socioeconômicos sem criar índice global.

# 6 DISCUSSÃO

A oferta de Música da UFPA combina participação elevada, desempenho contínuo baixo e percepções formativas favoráveis. Dos 44 inscritos, 37 participaram. O `NT_GER` médio de 41,64 situa a oferta aproximadamente no percentil 19,4 nacional e cerca de oito pontos abaixo da mediana de cursos comparáveis.

O processo formativo apresenta médias acima de 5 nas oito dimensões exploratórias, e as recomendações do curso e da IES são altas. Portanto, a evidência não sustenta uma narrativa simples em que Conceito 1 corresponda a percepção generalizadamente negativa de docentes, infraestrutura ou organização.

O perfil discente é marcado por 75,0% de renda até três salários mínimos, 42,5% de ação afirmativa e 74,4% de bolsa acadêmica entre respostas válidas. Ao mesmo tempo, 52,5% declaram trabalhar. Esses padrões podem orientar investigação institucional, mas não podem ser ligados individualmente à nota.
Música apresenta forte concentração nacional em Conceito 1: 44 de 107 cursos. A média de `NT_GER` dos cursos Conceito 1 é 42,12, próxima da UFPA, enquanto cursos com conceito superior têm média 51,49. Isso mostra que a faixa sintetiza uma diferença relevante, mas não elimina a heterogeneidade dentro de cada faixa.

O benchmark comparável é o achado de desempenho mais consistente e sugere prioridade para investigação dos componentes da prova, conteúdos específicos, estrutura curricular e preparação dos concluintes. A análise atual não identifica o mecanismo responsável.

# 7 CONCLUSÃO

A Licenciatura em Música da UFPA em Belém obteve Conceito Enade 1, com 44 inscritos e 37 participantes. A participação de 84,1% é elevada, enquanto 24,3% dos participantes atingiram o padrão de proficiência.

O `NT_GER` médio de 41,64 coloca a oferta aproximadamente no percentil 19,4 nacional. Frente a pares comparáveis, a oferta permanece cerca de oito pontos abaixo da mediana. O distanciamento é mais forte no componente objetivo que no discursivo.

O perfil discente apresenta renda baixa elevada, presença de ação afirmativa e bolsa acadêmica e forte intenção de atuar no magistério. As avaliações do processo formativo e de recomendação são favoráveis.

O principal resultado é uma configuração multidimensional: **baixo desempenho relativo na prova não coincide com avaliação formativa ou recomendação generalizadamente baixas**. O aprofundamento institucional deve buscar explicar esse descompasso sem atribuir causalidade a características individuais ou a um único componente.

# REFERÊNCIAS

BRASIL. Lei nº 10.861, de 14 de abril de 2004. Institui o Sistema Nacional de Avaliação da Educação Superior - SINAES. Brasília, DF: Presidência da República, 2004.

INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Dicionário de arquivos e variáveis: microdados do Enade das Licenciaturas 2025. Brasília, DF: Inep, 2026.

INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Enade das Licenciaturas: microdados 2025. Brasília, DF: Inep, 2026.

INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Manual do usuário: Enade das Licenciaturas 2025. Brasília, DF: Inep, 2026.

INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Questionário do Estudante - Enade das Licenciaturas 2025. Brasília, DF: Inep, 2025.

# APÊNDICES

## APÊNDICE A – Regras de integridade metodológica
- Unidade principal: `CO_CURSO`.
- Nenhum join individual entre arquivos temáticos.
- Junções somente após agregação por curso e validação one-to-one.
- Ausência de conceito não é Conceito 1.
- `NT_GER`, `NT_OBJ` e `NT_DIS` podem ser analisadas conjuntamente porque pertencem ao mesmo arquivo.
- Relações entre desempenho e perfil/questionário são exclusivamente ecológicas.
- `QE_I20–QE_I66` não são condensados em índice único.
- `QE_I68` e `QE_I69` são recomendação, não satisfação.
- Grupos B e C permanecem vazios por inexistência de ofertas correspondentes.

## APÊNDICE B – Consistência interna das dimensões

| Dimensão | Itens | N completos Brasil | Alfa Brasil | N completos UFPA | Alfa UFPA |
|---|---:|---:|---:|---:|---:|
| Oportunidades | 4 | 1965 | 0,805 | 36 | 0,748 |
| Atuação docente | 8 | 2466 | 0,928 | 37 | 0,939 |
| Organização / teoria-prática | 6 | 2420 | 0,904 | 36 | 0,930 |
| Infraestrutura | 5 | 1156 | 0,877 | 9 | — |
| Planejamento / ensino | 6 | 2566 | 0,943 | 38 | 0,946 |
| Inclusão / diversidade | 4 | 2448 | 0,869 | 32 | 0,892 |
| Gestão / avaliação | 7 | 2489 | 0,955 | 38 | 0,956 |
| Colaboração / famílias | 4 | 2577 | 0,922 | 39 | 0,898 |

## APÊNDICE C – Aprofundamentos sugeridos

1. **Desempenho por item e componente.** Justificativa: o distanciamento aparece sobretudo em `NT_OBJ`. Pergunta: quais itens, objetos de conhecimento ou faixas de acerto concentram a diferença? Variáveis: `QT_ACERTOS`, respostas objetivas, caderno, proficiência, `NT_OBJ`, `NT_DIS`. Método: dificuldade por item, ECDF, quantis e análise por caderno. Limitação: relações mecânicas entre acertos, nota e proficiência.

2. **Currículo e aderência aos objetos avaliados.** Justificativa: o benchmark comparável permanece acima da UFPA. Pergunta: há desalinhamento entre conteúdos cursados e objetos avaliados? Variáveis: PPC, matriz curricular, conteúdos e matriz de referência do exame. Método: análise documental e mapeamento de cobertura. Limitação: requer fontes institucionais externas aos microdados.

3. **Processo formativo item a item.** Justificativa: as médias das dimensões são altas apesar do Conceito 1. Pergunta: existem itens específicos com fragilidade ocultada pelas médias? Variáveis: `QE_I20–QE_I66`. Método: distribuição ordinal, N válido, concordância e comparação com cursos federais comparáveis. Limitação: autorrelato e múltiplas comparações.

4. **Perfil de trabalho, renda e permanência.** Justificativa: a UFPA apresenta composição socioeconômica específica. Pergunta: como o perfil se compara a licenciaturas de Música em universidades federais de porte semelhante? Variáveis: renda, trabalho, ação afirmativa, auxílios, bolsas, horas de estudo. Método: comparação agregada por curso. Limitação: falácia ecológica.

5. **Trajetória docente e interesse na PND.** Justificativa: 80% pretendem o magistério e a maioria dos respondentes do `QE_I70` quer ser professor da rede pública. Pergunta: quais padrões de intenção profissional distinguem a UFPA? Variáveis: `QE_I18`, `QE_I19`, `QE_I70`. Método: frequências válidas e contrastes por curso. Limitação: intenção declarada não equivale a inserção profissional futura.