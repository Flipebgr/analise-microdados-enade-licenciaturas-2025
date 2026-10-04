# Especificação inicial — adaptação dos Microdados Enade 2017

## 1. Escopo

A fonte `microdados_enade_2017_LGPD` contém a **edição completa do Enade 2017**, não apenas Ciências Biológicas.

A primeira área usada para validar a nova arquitetura será:

```text
Área: Ciências Biológicas — Bacharelado
CO_GRUPO: 1601
IES focal: UFPA
CO_IES: 569
```

O objetivo não é criar um pipeline específico dessa área, e sim usar a área como primeiro teste end-to-end do suporte multi-edição.

## 2. Fontes oficiais disponíveis para 2017

Documentos recebidos/a serem mantidos junto às fontes do projeto:

```text
microdados_enade_2017_LGPD.zip
resultados_conceito_enade_2017.xlsx
Dicionário_arquivos _ variáveis_microdados do Enade_2017.xlsx
Dicionário_arquivos _ variáveis_microdados do Enade_2017.ods
Manual do usuário_Enade_2017.pdf
Questionário do Estudante_Enade_Edição 2017.pdf
Questionário Licenciaturas - Enade 2017.pdf
```

Não inferir semântica de variável apenas pelo nome. Quando houver conflito, o dicionário/manual/questionário oficial da edição é a referência.

## 3. Estrutura real da edição 2017

A edição possui:

```text
microdados2017_arq1.txt
...
microdados2017_arq42.txt
```

Total: 42 arquivos temáticos.

Regras de importação documentadas para a edição:

- separador `;`;
- primeira linha é cabeçalho;
- decimais em ponto (`.`);
- faltantes representados conforme a codificação oficial do arquivo;
- vetores como `DS_VT_ACE_OFG` e `DS_VT_ACE_OCE` devem permanecer string.

O agente deve validar essas propriedades no arquivo real antes de fixar contratos.

## 4. LGPD e unidade de análise

Os arquivos são ordenados por variáveis diferentes. Mesmo quando têm o mesmo número de linhas, a linha `i` de arquivos diferentes não representa o mesmo estudante.

Portanto:

```text
NUNCA juntar registros individuais entre arq*.txt distintos.
```

A integração entre temas acontece após agregação por `CO_CURSO`.

## 5. Mapa estrutural dos arquivos 2017

### arq1 — caracterização do curso

Variáveis principais:

```text
NU_ANO
CO_CURSO
CO_IES
CO_CATEGAD
CO_ORGACAD
CO_GRUPO
CO_MODALIDADE
CO_MUNIC_CURSO
CO_UF_CURSO
CO_REGIAO_CURSO
```

### arq2 — trajetória acadêmica

```text
NU_ANO
CO_CURSO
ANO_FIM_EM
ANO_IN_GRAD
CO_TURNO_GRADUACAO
```

O ano de referência deve vir da edição/`NU_ANO`. Não usar default 2025.

### arq3 — desempenho e presença

A estrutura de 2017 é diferente da estrutura 2025 usada pelo pipeline atual.

Variáveis de desempenho relevantes:

```text
NT_GER
NT_FG
NT_OBJ_FG
NT_DIS_FG
NT_CE
NT_OBJ_CE
NT_DIS_CE
```

Além de notas por questão discursiva e vetores da prova.

Presença/situação inclui, entre outras:

```text
TP_PRES
TP_PR_GER
TP_PR_OB_FG
TP_PR_DI_FG
TP_PR_OB_CE
TP_PR_DI_CE
```

Não renomear `NT_OBJ_CE` para `NT_OBJ` apenas para encaixar no schema de 2025. Formação Geral e Componente Específico devem permanecer semanticamente separados.

### arq4 — avaliação do processo formativo

Em 2017, o bloco geral de processo formativo está em:

```text
QE_I27 ... QE_I68
```

Escala do questionário geral:

```text
1–6 = grau de concordância
7   = Não sei responder
8   = Não se aplica
```

O motor estatístico pode ser compartilhado, mas os itens, rótulos e dimensões devem ser configurados para 2017.

### arq5 — sexo

```text
TP_SEXO
```

### arq6 — idade

```text
NU_IDADE
```

### arq7 a arq32 — Questionário do Estudante geral

Correspondem a:

```text
QE_I01 ... QE_I26
```

O pipeline 2025 usa semântica diferente para vários números de questão. Portanto, regras socioeconômicas devem ser específicas do instrumento 2017.

### arq33 a arq42 — itens específicos de licenciaturas

Incluem:

```text
QE_I69 ... QE_I81
```

São específicos de licenciaturas e não devem entrar em Ciências Biológicas — Bacharelado.

Para bacharelados, a inexistência de respostas nesses itens deve ser tratada como **não aplicabilidade do instrumento**, não como não resposta discente.

## 6. Mapa mínimo do Questionário 2017

Alguns itens relevantes confirmados no instrumento oficial:

```text
QE_I04 = escolaridade do pai
QE_I05 = escolaridade da mãe
QE_I08 = renda familiar
QE_I10 = situação de trabalho
QE_I12 = auxílio permanência
QE_I13 = bolsa acadêmica
QE_I15 = ação afirmativa
QE_I21 = alguém na família concluiu curso superior
QE_I23 = horas semanais dedicadas aos estudos
```

`QE_I21` permite construir um indicador de primeira geração de forma mais direta:

```text
A = Sim, alguém na família concluiu superior
B = Não
```

A definição operacional exata deve ser documentada e testada antes de ser promovida ao pacote de evidências.

## 7. Incompatibilidades conhecidas com o código 2025

### 7.1 Inventário de arquivos

O código atual procura padrões de 2025, como:

```text
microdados2025_arq*.txt
```

Deve ser parametrizado pela edição.

### 7.2 Desempenho

O agregador 2025 espera variáveis como:

```text
NT_OBJ
NT_DIS
PROFICIENCIA
QT_ACERTOS
IN_REAPLICACAO
TP_SIT_DISC
```

Esse schema não corresponde ao `arq3` de 2017.

### 7.3 Trajetória

Existe risco de default de ano fixo em 2025. Qualquer cálculo temporal deve usar o ano da edição/registro.

### 7.4 Perfil socioeconômico

As regras atuais associam números `QE_*` a significados de 2025. Não podem ser reutilizadas em 2017.

Este é um erro silencioso de alta gravidade: o código pode produzir números válidos sobre a variável errada.

### 7.5 Processo formativo

O pipeline 2025 usa um intervalo diferente de itens. Em 2017 o bloco correto é `QE_I27–QE_I68`.

### 7.6 Recomendação

O módulo 2025 baseado em `QE_I68`, `QE_I69` e `QE_I70` não é aplicável a 2017.

Em 2017, `QE_I68` ainda é um item do processo formativo. `QE_I69+` inicia o bloco específico de licenciaturas.

Para Ciências Biológicas — Bacharelado 2017:

```yaml
recomendacao:
  disponivel: false
```

salvo definição posterior baseada em outra fonte/variável oficial.

### 7.7 Proficiência

Não transportar automaticamente para 2017 os indicadores 2025:

```text
PROFICIENCIA
QT_ACERTOS
Padrão 1 de Proficiência
```

Se não existirem no schema oficial 2017 com a mesma definição, marque a capacidade como indisponível.

### 7.8 Modalidade

A edição 2017 usa:

```text
0 = EaD
1 = Presencial
```

Foi identificado drift em constante histórica do código que mapeava `2` para EaD. Corrigir de modo testável, preferencialmente no schema da edição.

## 8. Planilha de Conceito Enade 2017

Fonte:

```text
resultados_conceito_enade_2017.xlsx
```

Aba esperada:

```text
Conceito Enade 2017
```

Campos relevantes observados:

```text
Ano
Código da Área
Área de Avaliação
Código da IES
Nome/Sigla da IES
Organização Acadêmica
Categoria Administrativa
Código do Curso
Modalidade de Ensino
Código do Município
Município
UF
Nº de Concluintes Inscritos
Nº de Concluintes Participantes
Nota Bruta - FG
Nota Padronizada - FG
Nota Bruta - CE
Nota Padronizada - CE
Conceito Enade (Contínuo)
Conceito Enade (Faixa)
Observação
```

O loader 2017 deve normalizar esses campos para um schema interno sem destruir os nomes/fonte originais.

`Conceito Enade (Faixa)` pode assumir:

```text
1, 2, 3, 4, 5, SC
```

`SC` deve permanecer categoria de situação do conceito e nunca ser recodificado como 1 ou 0.

## 9. Caso piloto — Ciências Biológicas Bacharelado

Identificadores validados na auditoria preliminar:

```text
CO_GRUPO = 1601
CO_IES   = 569
CO_CURSO = 12027
Município = Belém
Modalidade = Presencial
```

Referências de regressão preliminares para o curso UFPA:

```text
Inscritos oficiais: 23
Participantes oficiais: 13
Conceito Enade: 3
```

Esses valores devem ser confirmados diretamente pelas fontes durante os testes. Não hardcode esses números em lógica de produção; use-os apenas como expectativa de teste/regressão para o snapshot de 2017 disponível.

## 10. Consequência para grupos comparativos

O piloto UFPA possui Conceito Enade 3, não Conceito 1.

Logo, não construir artificialmente:

```text
A = UFPA Conceito 1
```

Para essa análise, definir um contraste focal documentado, por exemplo:

- oferta UFPA focal;
- outras IES do Pará;
- restante da Região Norte;
- restante do Brasil;
- benchmarks comparáveis.

A pergunta substantiva final deve ser definida antes do relatório. A infraestrutura de grupos precisa aceitar cenários sem Grupo A.

## 11. Critérios de aceite mínimos para o adapter 2017

A primeira implementação só deve ser considerada pronta quando:

1. a edição 2017 é reconhecida sem alterar manualmente nomes de arquivos;
2. o inventário identifica os 42 arquivos esperados;
3. `CO_GRUPO=1601` pode ser filtrado a partir de `arq1`;
4. os agregadores nunca juntam indivíduos entre arquivos;
5. desempenho preserva FG e CE separadamente;
6. trajetória usa `NU_ANO`/ano configurado, não 2025 hardcoded;
7. itens socioeconômicos usam mapa semântico 2017;
8. processo formativo usa `QE_I27–QE_I68`;
9. itens `QE_I69–QE_I81` são desativados para bacharelado;
10. recomendação/proficiência 2025 não são fabricadas para 2017;
11. o loader de Conceito preserva `SC`;
12. o smoke test da UFPA reconcilia inscritos/participantes/conceito com a fonte oficial;
13. 2025 continua funcionando ou, no mínimo, seus contratos existentes continuam cobertos pelos testes;
14. `pytest` e `ruff` passam.
