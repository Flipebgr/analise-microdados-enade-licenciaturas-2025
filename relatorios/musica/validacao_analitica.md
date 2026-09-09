# Validação analítica — Música — Enade 2025

## Escopo

A análise cobre 107 cursos de Música. A UFPA possui uma única oferta localizada nas fontes Enade 2025: Belém, presencial, Conceito Enade 1.

Os grupos B (outras ofertas UFPA com conceito superior) e C (outras IES do Pará) são estruturalmente vazios. Os contrastes externos principais são o restante da Região Norte e o restante do Brasil.

## Oferta UFPA

| CO_CURSO | Oferta | Inscritos | Participantes | Participação | Proficiência | Conceito | NT_GER |
|---:|---|---:|---:|---:|---:|---:|---:|
| 114950 | Belém — Presencial | 44 | 37 | 84,09% | 0,24% | 1 | 41,64 |

## Processo formativo

QE_I20–QE_I66 usam escala analítica 1–6. Respostas 7 (Não sei) e 8 (Não se aplica) são tratadas como ausentes analíticas. Os itens QE_I31, QE_I32 e QE_I43 são específicos de EaD e ficam fora das dimensões comuns para a oferta presencial da UFPA.

| Recorte | Dimensão | Itens | N completos | Alfa de Cronbach |
|---|---|---:|---:|---:|
| Brasil — Música | Oportunidades de formação | 4 | 1965 | 0,805 |
| Brasil — Música | Atuação docente | 8 | 2466 | 0,928 |
| Brasil — Música | Organização e integração teoria-prática | 6 | 2420 | 0,904 |
| Brasil — Música | Infraestrutura e recursos | 5 | 1156 | 0,877 |
| Brasil — Música | Preparação para planejamento e ensino | 6 | 2566 | 0,943 |
| Brasil — Música | Inclusão e diversidade | 4 | 2448 | 0,869 |
| Brasil — Música | Gestão da sala e avaliação | 7 | 2489 | 0,955 |
| Brasil — Música | Colaboração, escola e famílias | 4 | 2577 | 0,922 |
| UFPA — Música | Oportunidades de formação | 4 | 36 | 0,748 |
| UFPA — Música | Atuação docente | 8 | 37 | 0,939 |
| UFPA — Música | Organização e integração teoria-prática | 6 | 36 | 0,930 |
| UFPA — Música | Infraestrutura e recursos | 5 | 9 | NA |
| UFPA — Música | Preparação para planejamento e ensino | 6 | 38 | 0,946 |
| UFPA — Música | Inclusão e diversidade | 4 | 32 | 0,892 |
| UFPA — Música | Gestão da sala e avaliação | 7 | 38 | 0,956 |
| UFPA — Música | Colaboração, escola e famílias | 4 | 39 | 0,898 |

Alfa de Cronbach avalia consistência interna, mas não comprova unidimensionalidade. Os escores são exploratórios e descritivos.

## Benchmark comparável — sensibilidade

O benchmark mantém modalidade, categoria administrativa e organização acadêmica e varia apenas a janela de porte.

| Critério | N | NT_GER UFPA | Mediana benchmark | Diferença |
|---|---:|---:|---:|---:|
| porte_25pct | 5 | 41,64 | 49,30 | -7,66 |
| porte_50pct | 10 | 41,64 | 49,95 | -8,30 |
| porte_2x | 11 | 41,64 | 49,68 | -8,03 |

## Associações ecológicas

As correlações são calculadas entre indicadores agregados por curso. Não representam relações individuais e não permitem inferência causal.

| X | Y | N cursos | Spearman rho | p |
|---|---|---:|---:|---:|
| renda_ate_3sm_pct | nt_ger_mean | 103 | -0,293 | 0,0027 |
| trabalha_pct | nt_ger_mean | 103 | -0,021 | 0,8345 |
| auxilio_permanencia_pct | nt_ger_mean | 103 | 0,455 | 0,0000 |
| qe_i68_media | nt_ger_mean | 103 | -0,261 | 0,0078 |
| qe_i69_media | nt_ger_mean | 103 | 0,009 | 0,9299 |
| dim_atuacao_docente_media | nt_ger_mean | 103 | -0,169 | 0,0885 |
| dim_infraestrutura_recursos_media | nt_ger_mean | 103 | -0,333 | 0,0006 |
| dim_organizacao_integracao_media | nt_ger_mean | 103 | -0,263 | 0,0073 |

O arquivo `associacoes_ecologicas_diagnostico.csv` registra dispersão e quantidade de outliers pelo critério de Tukey para cada par analisado.

## Narrativa gráfica

### 01 — Painel da oferta UFPA

Descrição: apresenta participação oficial e percentual no padrão de proficiência da oferta de Belém. Interpretação: contextualiza adesão e proficiência sem inferir qualidade causal. Hipótese: a combinação entre participação e desempenho pode ajudar a interpretar a posição da oferta. Limitação: ambos são indicadores agregados. Relação: define o universo observado da UFPA.

### 02 — Posição relativa em NT_GER

Descrição: posiciona a média da UFPA na distribuição nacional dos cursos de Música. Interpretação: mostra posição relativa dentro da mesma área. Hipótese: o Conceito 1 pode corresponder a uma posição inferior também na nota contínua. Limitação: média do curso não descreve toda a distribuição individual. Relação: desempenho.

### 03 — Distribuições NT_GER, NT_OBJ e NT_DIS

Descrição: compara os estudantes da UFPA, do Norte sem Pará e do Brasil sem Norte usando apenas variáveis do mesmo arquivo de desempenho. Interpretação: permite observar centro e dispersão. Hipótese: o contraste pode ser mais forte em algum componente da nota. Limitação: não relacionar individualmente essas notas a questionários de outros arquivos. Relação: desempenho.

### 04 — Perfil socioeconômico

Descrição: compara a oferta UFPA com medianas de cursos nos recortes externos. Interpretação: caracteriza composição discente. Hipótese: diferenças de condições materiais podem acompanhar diferenças acadêmicas. Limitação: associação com nota apenas no nível ecológico. Relação: composição discente.

### 05 — Processo formativo

Descrição: contrasta dimensões exploratórias da UFPA com medianas regionais/nacionais. Interpretação: identifica dimensões relativamente mais ou menos favoráveis. Hipótese: fragilidades percebidas podem coexistir com o baixo desempenho. Limitação: alfa não comprova unidimensionalidade. Relação: avaliação do processo formativo.

### 06 — Benchmark comparável

Descrição: mostra a sensibilidade da mediana de NT_GER a três janelas de porte. Interpretação: diferenças persistentes são mais robustas ao critério. Hipótese: parte do contraste amplo pode refletir composição institucional. Limitação: pareamento observacional não elimina diferenças não medidas. Relação: benchmark comparável.

### 07 — Recomendação

Descrição: compara QE_I68 e QE_I69 com seus rótulos oficiais. Interpretação: recomendação do curso e da IES podem divergir. Hipótese: avaliação institucional e avaliação do curso não são intercambiáveis. Limitação: não chamar automaticamente de satisfação. Relação: recomendação.

### 08 — Associação ecológica

Descrição: mostra o par com maior |rho| entre os pares pré-definidos. Interpretação: auxilia a inspeção de dispersão e outliers. Hipótese: associações de curso podem refletir composição institucional. Limitação: não é associação individual nem causal. Relação: associações ecológicas.

### 09 — Síntese UFPA

Descrição: reúne indicadores em escala percentual/percentil sem compor índice único. Interpretação: evidencia dimensões distintas da oferta. Hipótese: fragilidades e fortalezas podem coexistir. Limitação: os indicadores não são aditivos. Relação: síntese da pergunta central.

## Arquivos gráficos

- `01_painel_oferta_ufpa.png`
- `02_posicao_relativa_nt_ger.png`
- `03a_distribuicao_nt_ger.png`
- `03b_distribuicao_nt_obj.png`
- `03c_distribuicao_nt_dis.png`
- `04_perfil_socioeconomico.png`
- `05_processo_formativo_dimensoes.png`
- `06_benchmark_sensibilidade.png`
- `07_recomendacao.png`
- `08_associacao_ecologica.png`
- `09_sintese_ufpa.png`

## Diagnóstico de associações

Pares avaliados: 8.