# Metodologia analítica

## 1. Pergunta geral

O projeto investiga quais características de desempenho, composição discente, trajetória acadêmica e avaliação do processo formativo diferenciam ofertas da UFPA e como essas ofertas se posicionam diante de referências institucionais, territoriais e estruturais da mesma área.

Os resultados descrevem padrões e formulam hipóteses. Não constituem desenho causal.

## 2. Unidade de análise e junções

A unidade principal é `CO_CURSO`.

Fluxo obrigatório:

```text
arquivo temático
→ tratamento de ausências
→ agregação por CO_CURSO
→ uma linha por curso
→ junção das tabelas agregadas
→ comparação entre cursos
```

Na orquestração multi-edição, a caracterização do `arq1` é reduzida a uma linha por `CO_CURSO` somente após verificar que os atributos estruturais são constantes dentro do curso. O Conceito é reconciliado pela mesma chave e as diferenças de cobertura são registradas. Desempenho, indicadores do questionário e processo formativo entram na base apenas depois de agregados e validados como one-to-one.

O pacote `evidencias.json` é uma interface estruturada derivada dessas tabelas agregadas e não substitui seus CSVs auditáveis. Ele preserva as regras, fontes, variáveis, denominadores e ausências de cada indicador. No processo formativo, a validação exige que `n_total` corresponda à soma das categorias e que os percentuais de "não sei responder" e "não se aplica" usem `n_total`. Campos sem contrato analítico validado são declarados indisponíveis, sem conclusão automática.

No schema `2.0`, todos os blocos conceituais são obrigatórios, inclusive os indisponíveis. O universo explicita os identificadores oficiais em texto e o subconjunto focal. Tabelas por curso devem referenciar esse universo; a auditoria de cobertura pode incluir também cursos somente da planilha, identificados como tal. Chaves de curso, curso/item e curso/item/resposta são únicas nos respectivos produtos. Processo aplicável exige a grade completa curso × itens declarados; cursos sem respostas têm contagens zero e estatísticas nulas, não são omitidos. A disponibilidade depende da capacidade da edição e da aplicabilidade da área; processo não aplicável é explicitado como `disponivel=false`, `status=nao_aplicavel`, sem resultados fabricados.

Contagens devem ser finitas, não negativas e integrais (inclusive representação `10.0` decorrente de coluna anulável; nunca há arredondamento). As categorias do processo e do perfil reconciliam `n_total`; concordância/positivos não excedem `n_valido`. As quatro proporções do processo, indicadores do perfil, distribuições e taxa de presença são frações em `[0,1]`. Denominador zero exige `null`. `NaN` e infinitos são rejeitados no pacote; ausências pandas legítimas são serializadas como `null`. A conferência das razões tolera apenas precisão de serialização (15 casas no JSON, tolerâncias relativa `1e-12` e absoluta `1e-14`). Médias/medianas de processo respeitam a escala declarada; desvio-padrão amostral exige ao menos duas respostas válidas.

`participacao.por_curso` conserva `INSCRITOS` e `PARTICIPANTES` oficiais, separados de `registros_microdados`, `presentes_validos` e `taxa_presenca_microdados = presentes_validos / registros_microdados`. Não se exige igualdade entre as fontes nem se preenche ausência oficial com contagem temática. O Conceito original, a faixa e a situação são reconciliados em todos os cursos; `SC` permanece fora da faixa numérica. A mesma evidência repetida em oferta focal deve corresponder aos blocos por curso.

O manifesto de microdados é a união das origens da caracterização, desempenho, regras de perfil e processo efetivamente integrado. Origem estrutural é resolvida pelo schema da edição; origem de indicadores vem das regras retornadas pelos agregadores. Arquivos apenas inventariados não são rotulados como utilizados. Cada TXT usado possui nome, caminho relativo, tamanho e SHA256 dos bytes descomprimidos (ZIP) ou bytes do arquivo (diretório); o hash é comparável entre formas de armazenamento. A planilha de Conceito conserva sua proveniência própria. A publicação verifica a concordância entre os CSVs e o JSON da mesma geração.

São proibidos:

- uso da posição da linha como chave;
- criação de identificador artificial de estudante;
- join individual entre arquivos temáticos;
- join muitos-para-muitos por `CO_CURSO`;
- inferência de que registros na mesma posição pertencem ao mesmo estudante.

Análises individuais podem combinar somente variáveis que estejam no mesmo arquivo. Por exemplo, `NT_GER`, `NT_OBJ` e `NT_DIS` podem ser analisadas conjuntamente quando pertencem ao mesmo arquivo de desempenho.

## 3. Conceito Enade

- Conceito ausente permanece ausente.
- Ausência de conceito nunca é recodificada como Conceito Enade 1.
- A representação normalizada mantém três campos separados: valor original, conceito numérico anulável e situação do conceito. `SC` aparece na situação e no valor original, nunca na coluna numérica 1–5.
- O loader dirigido pelo contrato da edição mantém os identificadores oficiais como texto, valida unicidade por `CO_CURSO` e conserva a planilha original para auditoria. Remove da tabela analítica somente linhas de rodapé sem oferta; inconsistências de schema, ano, código ou contagem falham explicitamente.
- Inscritos e participantes da planilha são contagens oficiais por curso, não registros individuais reconstruídos. O conceito contínuo de 2017 é preservado; não é inferido para 2025, cuja fonte não o fornece.
- Ofertas informadas mas não localizadas nas fontes permanecem documentadas sem fabricação de `CO_CURSO`, inscritos, participantes ou desempenho.
- Conceitos superiores podem servir de contraste interno, mas não são tratados automaticamente como categorias normativas de suficiência ou excelência.

## 4. Grupos comparativos exclusivos

Quando existe oferta UFPA com Conceito Enade 1, os grupos independentes são:

- **A** — UFPA com Conceito 1;
- **B** — demais ofertas da UFPA da mesma área com conceito superior;
- **C** — outras IES do Pará, excluindo UFPA;
- **D** — restante da Região Norte, excluindo Pará;
- **E** — restante do Brasil, excluindo Norte.

Pará, Norte e Brasil completos podem ser apresentados como referências descritivas, mas não como grupos independentes em testes quando se sobrepõem.

Quando não existe oferta UFPA Conceito 1, o Grupo A permanece vazio. O projeto usa então um contraste focal ou interno explicitamente documentado, sem criar Conceito 1 artificial.

## 5. Benchmarks

São utilizados dois níveis:

### Amplo

Todos os cursos válidos da mesma área no território ou recorte de referência.

### Comparável

Cursos semelhantes em características observáveis, como:

- modalidade;
- categoria administrativa;
- organização acadêmica;
- porte medido por participantes.

Um critério recorrente usa participantes entre `0,5x` e `2,0x` do curso-alvo. Análises de sensibilidade podem usar faixas mais estreitas.

Os benchmarks reduzem parte da heterogeneidade observável, mas não constituem pareamento causal.

## 6. Participação e desempenho

Indicadores principais, quando definidos pela edição:

- inscritos;
- participantes;
- taxa de participação/presença;
- `NT_GER`;
- componentes objetivos e discursivos declarados no contrato da edição;
- Formação Geral e Componente Específico separados quando a fonte os fornece;
- proficiência e acertos somente quando a edição os oferece e a área os aplica;
- presença;
- situação da prova;
- reaplicação.

São reportados, quando disponíveis:

- N válido;
- média;
- mediana;
- dispersão;
- quartis/percentis;
- posição relativa;
- diferenças;
- tamanho de efeito;
- incerteza.

No agregador multi-edição, as estatísticas de notas usam apenas registros com a situação de presença válida definida no contrato da edição. `registros_microdados` é o total de linhas do `arq3` no curso; `presentes_validos` é o subconjunto com presença válida; cada componente apresenta `n_valido`, `n_ausente` em relação a todos os registros, `n_presente_sem_nota` e `n_nota_fora_presenca_valida`. Notas fora da presença válida ficam na tabela individual de auditoria, mas não entram nas estatísticas agregadas. A tabela agregada contém uma linha por `CO_CURSO`.

Ofertas com N pequeno são interpretadas com cautela.

## 7. Perfil demográfico e socioeconômico

Indicadores são agregados por curso, incluindo:

- sexo;
- idade;
- raça/cor;
- escolaridade dos pais;
- renda;
- trabalho;
- ação afirmativa;
- bolsas;
- auxílios;
- moradia;
- horas de estudo;
- itens relevantes declarados pelo instrumento da edição.

O número de um item `QE_*` não transfere sua semântica entre anos. Cada indicador derivado declara edição, item de origem, respostas válidas, respostas positivas e denominador.

Percentuais usam o número de respostas válidas para a regra da edição como denominador. A saída informa `n_total`, `n_valido`, `n_positivo`, `n_ausente`, `n_excluida`, `n_nao_aplicavel` e `n_invalida` por curso e indicador; denominador zero produz percentual ausente. Em 2025, `QE_I05=C` e `QE_I06/QE_I07=H` significam desconhecimento e não entram no denominador. `QE_I16` de 2025 aceita respostas múltiplas separadas por vírgula; `A` (nenhuma) junto com outra categoria é incoerente e conta como inválida. Em 2017, `QE_I21=B` indica que ninguém na família concluiu curso superior; esse indicador não utiliza `QE_I05` de 2025.

## 8. Trajetória e condições acadêmicas

Indicadores de turno, tempo desde o ingresso, trabalho, bolsas, auxílios e dedicação aos estudos são interpretados no nível do curso quando integrados a outros temas.

## 9. Processo formativo

Os itens são definidos pelo instrumento oficial e pela disponibilidade nos microdados de cada edição. Em 2025, o contrato usa `QE_I20–QE_I66`; em 2017, o bloco geral é `QE_I27–QE_I68`. A questão 67 consta do questionário oficial de 2025, mas não dos arquivos temáticos do ZIP disponível e, portanto, não é calculada. Ambas as edições declaram 1 = discordância total, 6 = concordância total, 4–6 = concordância para fins descritivos, 7 = não sei responder e 8 = não se aplica.

O agregador multi-edição resume cada item separadamente por `CO_CURSO`, informa o denominador válido, os códigos especiais, ausências e respostas inválidas, e não calcula um índice ou alfa global. As porcentagens de "não sei responder" e "não se aplica" são calculadas separadamente com `n_total` do item como denominador, não com o total oficial de inscritos nem com `n_valido`; as contagens e os denominadores devem acompanhar os percentuais no relatório final. O alfa para o bloco inteiro no agregador legado de 2025 é apenas um diagnóstico histórico; não constitui validação de unidimensionalidade. No diagnóstico exploratório de dimensões de 2025, os códigos 7/8 e respostas fora da escala 1–6 são excluídos tanto do alfa quanto da contagem de casos completos. Seus agrupamentos de itens continuam preliminares e não devem ser usados como índices até a validação teórica.

Antes de criar dimensão composta é necessário:

1. conferir o texto oficial;
2. verificar direção da escala e itens invertidos;
3. justificar teoricamente o agrupamento;
4. avaliar casos válidos;
5. avaliar consistência interna;
6. examinar correlações item-total;
7. rejeitar agrupamentos sem coerência substantiva, mesmo quando a consistência estatística for elevada.

Dimensões candidatas incluem:

- organização didático-pedagógica;
- atuação docente;
- infraestrutura;
- estágio;
- oportunidades de formação;
- integração teoria-prática;
- apoio acadêmico.

Agrupamentos exploratórios não equivalem a índices validados.

## 10. Recomendação

Em 2025, `QE_I68`, `QE_I69` e, quando pertinente, `QE_I70` devem manter os rótulos oficiais.

Eles não são agrupados automaticamente sob o termo “satisfação”.

Essa capacidade não existe no contrato de 2017. Nessa edição, `QE_I68` pertence ao processo formativo e `QE_I69+` inicia o questionário específico de licenciaturas. Para o bacharelado 1601, esse último bloco é não aplicável.

## 11. Correlações

### Individuais

Permitidas apenas entre variáveis presentes no mesmo arquivo.

Relações mecânicas, como nota, acertos e proficiência, devem ser explicitadas.

### Ecológicas

Indicadores agregados por curso podem ser relacionados por Spearman, com:

- N de cursos;
- dispersão;
- inspeção de outliers;
- ponderação por participantes quando metodologicamente pertinente.

Correlação ecológica não representa correlação entre estudantes e não sustenta causalidade.

## 12. Outliers

Outliers podem ser sinalizados por critérios exploratórios, como `1,5 × IQR`, mas não são removidos automaticamente. Exclusões exigem justificativa documentada.

## 13. Comparação entre áreas

Notas brutas não devem ser comparadas diretamente entre `CO_GRUPO` diferentes.

Comparações transversais devem usar medidas padronizadas dentro da área, como:

- percentis;
- escores padronizados;
- posição relativa;
- diferença para a mediana da área.

## 14. Interpretação

Toda análise deve separar:

- descrição;
- interpretação;
- hipótese;
- limitação.

Não concluir previamente que modalidade EaD, interiorização, baixo N, perfil socioeconômico ou infraestrutura explicam os resultados. Essas características devem ser verificadas empiricamente e tratadas como hipóteses quando o desenho não for causal.
