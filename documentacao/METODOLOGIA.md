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

Indicadores principais:

- inscritos;
- participantes;
- taxa de participação/presença;
- `NT_GER`;
- `NT_OBJ`;
- `NT_DIS`;
- `PROFICIENCIA`;
- `QT_ACERTOS`;
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
- itens relevantes de `QE_I01–QE_I19`.

Percentuais usam denominador válido e as ausências permanecem documentadas.

## 8. Trajetória e condições acadêmicas

Indicadores de turno, tempo desde o ingresso, trabalho, bolsas, auxílios e dedicação aos estudos são interpretados no nível do curso quando integrados a outros temas.

## 9. Processo formativo — QE_I20–QE_I66

Os 47 itens devem ser lidos e documentados antes da formação de índices.

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

`QE_I68`, `QE_I69` e, quando pertinente, `QE_I70` devem manter os rótulos oficiais.

Eles não são agrupados automaticamente sob o termo “satisfação”.

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
