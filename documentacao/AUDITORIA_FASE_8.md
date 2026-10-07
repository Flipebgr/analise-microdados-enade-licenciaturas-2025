# Auditoria corretiva da Fase 8

## A. Estado inicial

- Branch real: `feature/pipeline-multiedicao`, acompanhando `origin/feature/pipeline-multiedicao`.
- Branch citada no pedido: `recursos/pipeline-multieditavel`. Divergência registrada; o checkout real coincide com o histórico e o estado operacional, por isso foi mantido.
- Commit inicial: `e75142f feat(fase-8): gera pacote de evidencias versionado`.
- Git inicial: árvore limpa; nenhuma alteração preexistente a preservar.
- Baseline: 136 testes não integrados; 19 de integração; 155 no total; Ruff passou. Nenhum skip.
- Ambiente: Python do runtime local com dependências de `.venv/Lib/site-packages`. A tentativa inicial no sandbox gerou 29 erros de setup por impossibilidade de criar diretórios temporários (107 testes não integrados passaram; na suíte completa, 126 passaram). Repetição autorizada fora do sandbox: todos aprovados. Na verificação final, `--basetemp` apontou para área gravável e o cache pytest foi desativado. Nenhum teste foi enfraquecido para contornar o ambiente.

## B. Auditoria independente dos achados

As linhas abaixo referem-se ao commit inicial `e75142f`, antes da reorganização do validador. Reproduções usaram cópias em memória dos pacotes, fontes sintéticas e diretórios temporários. O código inicial também foi recuperado com `git show` para conferir contagens compensadas, sem alterar o checkout.

| Achado/status | Arquivo, função, linhas iniciais | Esperado × observado e reprodução | Causa, impacto e gravidade |
|---|---|---|---|
| 1A — parcialmente confirmado | `src/evidencias/construir.py`, `validar_evidencias`, ~171–220 | Alterar concordância/ausência analítica para -0,1, 2, NaN ou ±inf deveria falhar; todos passavam. Percentuais 7/8 já rejeitavam esses cinco valores nos casos testados. | Só 7/8 eram recalculados; concordância era verificada apenas para N válido zero. Evidências inválidas poderiam chegar ao consumidor. Alta. |
| 1B — confirmado | Mesmo arquivo/função, ~187 | Substituir `CO_CURSO` de um item por `99999` deveria falhar; passava. | Ausência de integridade referencial contra o universo. Alta. |
| 1C — confirmado | Mesmo arquivo/função, ~187 | Duplicar um registro curso/item deveria falhar; passava. | Ausência de unicidade da chave composta. Dupla contagem possível na camada consumidora. Alta. |
| 1D — confirmado | Mesmo arquivo/função, ~186 | `itens_por_curso=[]` em processo aplicável deveria falhar; passava. | O laço vazio dispensava todas as verificações, sem contrato de aplicabilidade. Alta. |
| 1E — parcialmente confirmado | Mesmo arquivo/função, ~191–214 | A soma simples já era conferida. Contudo, `n_ausente=-1` compensado em `n_invalido` passava; `n_valido=n_total+1` compensado com ausência negativa também passava. | Reconciliar soma não garantia contagens não negativas nem relações subconjunto/total. Alta. |
| 2 — confirmado | Mesmo arquivo/função, ~174–179 | Remover separadamente trajetória, benchmarks, efeitos, associações, qualidade, alertas ou achados deveria falhar; passava. | Lista parcial de blocos obrigatórios. Consumidores não distinguiam indisponibilidade explícita de perda de conteúdo. Alta. |
| 3 — confirmado | `construir_evidencias`, ~147–158 | União das origens de produtos deveria constar do manifesto. Comparação com as regras mostrou nove arquivos de perfil omitidos em 2017; a mesma construção fixa omitia dez em 2025. | Lista `(1,3,4)` independente das regras dos indicadores. Rastreabilidade incompleta, embora as regras individuais preservassem origem. Média. |
| 4 — confirmado | `construir_evidencias`, ~71–72 | Diretório existente aceito pelo leitor deveria concluir a análise; recebia `FileNotFoundError`. | `is_file()` e hash de arquivo único. Regressão funcional do caminho extraído. Alta. |
| 5 — confirmado | `executar.py`, `executar_area_cli`, ~129–132 | Uma falha da nova execução deveria preservar a anterior. Com arquivos antigos e `construir_evidencias` lançando erro, retorno foi 2, CSV antigo foi substituído e JSON antigo permaneceu. | Escrita definitiva dos CSVs precedia construção/validação do pacote. Mistura de gerações. Alta. |
| 6 — confirmado | `construir_evidencias`, ~118 | Participação por curso deveria distinguir oficiais e microdados. Inspeção mostrou só curso, registros, presentes e taxa; oficiais existiam apenas no recorte focal. | Seleção das primeiras quatro colunas de desempenho perdia informações oficiais dos outros cursos. Média. |
| 10 — confirmado | `ESTADO_ATUAL_PROJETO.md`, ~37; `PLANO_EVOLUCAO_PIPELINE.md`, ~268 | Próximo passo deveria ter dependências coerentes. Estado mencionava contrastes/benchmarks/efeitos; plano só nomeava alertas. | Dependências analíticas implícitas; risco de ampliar escopo sem contrato. Média. |

A auditoria não encontrou evidência de cálculo errado nos produtos reais examinados: os 11.256 registros curso/item do snapshot 2017 reconciliaram as quatro proporções e contagens; o perfil também reconciliou. As falhas eram principalmente de garantia do contrato, rastreabilidade e publicação, não prova de alteração dos resultados existentes.

## C. Correções realizadas por arquivo

- `src/evidencias/construir.py` → schema `2.0`, universo/focais explícitos, participação oficial em todos os cursos, aplicabilidade e manifesto derivado → preservar campos e impedir perda silenciosa; infinito não é convertido em ausência.
- `src/evidencias/validar.py` → contrato completo, finitude, contagens, razões, grade curso/item, chaves, cobertura, perfil/distribuições, desempenho, SC e coerência entre blocos → pacote rejeita contradições metodológicas.
- `src/evidencias/proveniencia.py` → união das origens dos produtos, resolução pelo schema, hashes/tamanhos de TXT usados → nenhuma lista de arquivos por ano no núcleo; ZIP e diretório auditáveis.
- `src/evidencias/publicar.py` → staging no mesmo volume, comparação JSON/agregados/CSVs, lock exclusivo, troca do conjunto e rollback → falha tratável preserva a geração anterior.
- `executar.py` → construir antes da publicação e usar o publicador para `analise`/`tudo`; reportar erros de I/O → nenhum CSV novo é publicado antes da validação integral.
- `src/edicoes/base.py` → capacidade explícita de processo formativo, com padrão compatível → declarar oferta da edição.
- `src/core/configuracao_area.py` → aplicabilidade explícita do processo e validação de compatibilidade → separar edição de área/grau.
- `src/orquestracao/area.py` → respeitar aplicabilidade antes de executar o processo → recurso não aplicável não é fabricado nem listado como consumido.
- `tests/suporte_evidencias.py` → fontes sintéticas completas para ambas as edições → testes independentes de fontes locais.
- `tests/unit/test_evidencias.py` → preservar os três testes anteriores com fixture completa e ampliar testes negativos → proteger contrato `2.0`.
- `tests/unit/test_publicacao_evidencias.py` → testes de armazenamento, proveniência e transação → proteger publicação e equivalência.
- `tests/unit/test_executar_cli.py` → adaptar o teste de despacho ao publicador → manter garantia de saída pela CLI.
- `tests/integration/test_evidencias.py` → ampliar verificações 2017/2025 → proteger manifesto, piloto, capacidades e SC reais.

## D. Testes novos e falhas impedidas

Em `tests/unit/test_evidencias.py`:

| Teste | Contrato protegido |
|---|---|
| `test_processo_rejeita_proporcao_invalida` | Quatro taxas × valores negativos, superiores a 1, NaN e ±inf. |
| `test_processo_rejeita_contagens_e_razoes_incoerentes` | Negativos, contagens fracionárias/booleanas, N válido excedente e razões incorretas. |
| `test_todos_blocos_sao_obrigatorios` | Remoção individual de cada bloco obrigatório. |
| `test_referencia_a_curso_inexistente_rejeitada` | Referências fora do universo em processo, perfil, distribuições, participação e desempenho. |
| `test_processo_duplicado_ou_incompleto_rejeitado` | Duplicidade, desaparecimento de uma célula e bloco aplicável vazio. |
| `test_denominador_zero_exige_nulos` | N zero conserva taxas/estatísticas nulas; zero numérico não substitui ausência. |
| `test_perfil_e_participacao_reconciliam_denominadores` | Taxas aritmeticamente inconsistentes em outros blocos. |
| `test_participacao_preserva_medidas_distintas_e_sc` | Oficiais 23/13 e microdados 10/10 coexistem; SC não vira 1. |
| `test_manifesto_rejeita_omissao_ou_fonte_nao_usada` | Proveniência incompleta ou artificialmente ampliada. |
| `test_processo_nao_aplicavel_e_explicito` | Processo vazio é válido somente com aplicabilidade compatível. |
| `test_capacidade_ausente_exige_aplicabilidade_compativel` | Área não solicita capacidade inexistente; indisponibilidade explícita. |
| `test_schema_interno_e_produtos_obrigatorios` | Omissão de ofertas focais, tabelas, mapa, estatísticas, denominadores, distribuições e proveniência. |

Em `tests/unit/test_publicacao_evidencias.py`:

| Teste | Contrato protegido |
|---|---|
| `test_zip_diretorio_equivalentes_ate_publicacao` | Leitura → análise → pacote → publicação nas duas formas, para 2017 e 2025; igualdade analítica e de hashes. |
| `test_novo_indicador_inclui_automaticamente_sua_fonte` | Nova regra em outro arquivo inclui origem automaticamente; arquivos sem uso continuam excluídos. |
| `test_falha_preserva_toda_geracao_anterior` | Falhas no schema, CSV, JSON, validação do staging e promoção não alteram nenhum byte publicado; temporários limpos. |
| `test_publicacao_sucesso_substitui_conjunto_completo` | Nova geração válida substitui o conjunto e remove temporários. |
| `test_cli_erro_preserva_saida_e_sucesso_publica` | CLI `analise` e `tudo`: sucesso real sintético e erro antes da publicação. |
| `test_lock_rejeita_escritor_concorrente` | Segunda publicação não interfere com escritor já ativo. |
| `test_json_valido_mas_divergente_do_csv_nao_publica` | JSON isoladamente válido, mas de outra geração, não pode acompanhar os CSVs. |

Nenhum teste anterior foi removido. O crescimento de 155 para 237 casos decorre de 82 casos novos, incluindo parametrizações; fixtures mínimas incompletas foram substituídas por fontes sintéticas completas, preservando expectativas válidas.

## E. Regressões finais

| Comando lógico | Resultado |
|---|---|
| `python -m pytest -q -m "not integration"` | 218 aprovados; 19 não selecionados |
| `python -m pytest -q -m integration` | 19 aprovados; 218 não selecionados |
| `python -m pytest -q` | 237 aprovados |
| `python -m ruff check .` | All checks passed |

Nenhum skip. `git diff --check` passou. Os comandos finais receberam somente opções operacionais de cache/diretório temporário, sem exclusão de testes além dos marcadores solicitados.

## F. Piloto 2017

Execução real da CLI com `--ano 2017 --slug biologia_bacharelado --etapa tudo`: 268 cursos e 11.256 registros curso/item. Oferta `CO_CURSO=12027`, `CO_IES=569`, `CO_GRUPO=1601`: 23 inscritos oficiais, 13 participantes oficiais, Conceito 3. Nenhuma divergência. FG/CE permanecem separados, processo `QE_I27–QE_I68`, licenciatura não aplicável, proficiência/recomendação indisponíveis. Os números aparecem somente em expectativas de regressão, nunca em decisões de produção.

## G. Regressão 2025

Execução real da CLI com `--ano 2025 --slug biologia --etapa analise`: 428 cursos e 20.116 registros curso/item. Processo `QE_I20–QE_I66`, proficiência preservada e FG não fabricada. Os 19 testes reais abrangem schemas/fontes, Conceito, indicadores, processo, orquestração e evidências das duas edições. `test_evidencias_2025_usam_contrato_proprio_da_edicao` também verifica o manifesto esperado e cursos SC com faixa nula.

## H. Proveniência

- 2017: `microdados2017_arq{N}.txt`, N = **1, 3, 4, 10, 11, 14, 16, 18, 19, 21, 27, 29**.
- 2025: `microdados2025_arq{N}.txt`, N = **1, 3, 4, 11, 12, 13, 15, 16, 17, 21, 22, 23, 24**.

Essas listas são resultados observados e expectativas de testes de regressão, não constantes de produção. Caracterização/desempenho resolvem a origem pelo schema; indicadores/processo fornecem suas regras/proveniência. O manifesto usa a união dessas origens, ordenada lexicalmente, com caminho relativo, tamanho e SHA256 por TXT. Inventariar o ZIP completo não torna todos os arquivos fontes de resultados. A planilha conserva fonte, aba, hash e contagens de linhas.

## I. Publicação transacional

Experimento anterior à correção: arquivos antigos com conteúdo sentinela → erro proposital na construção → CSV substituído e JSON antigo preservado (falha confirmada).

Experimentos após a correção: geração válida completa → falha em cada uma das cinco etapas parametrizadas → dicionário `{nome: bytes}` de **todos** os arquivos idêntico ao anterior; somente `analise/` permanece, sem staging/lock. A falha na promoção ocorre após mover a geração antiga para backup e comprova o rollback. Um teste adicional recusa JSON válido porém incompatível com os CSVs. Caminho de sucesso e ambas as etapas CLI passaram.

Limite explícito: a troca usa duas renomeações no mesmo volume, com lock de escritor. Não é uma primitiva de troca atômica de diretórios para leitores simultâneos nem garantia contra queda de energia. Interrupção abrupta pode deixar lock/backup para recuperação; falha da própria restauração preserva o backup e informa seu caminho. Procedimento em `EXECUCAO.md`. Falha de limpeza é avisada, não ocultada nem tratada como invalidação de uma geração já publicada.

## J. Documentação

Atualizados `ESTADO_ATUAL_PROJETO.md`, `PLANO_EVOLUCAO_PIPELINE.md`, `EXECUCAO.md`, `METODOLOGIA.md`, `ARQUITETURA.md` e este relatório. O plano agora distingue Fase 9A (contraste → benchmarks → efeitos/incerteza) de Fase 9B (alertas), mantendo a Fase 10.

## K. Estado final

Branch mantida: `feature/pipeline-multiedicao`. Commit mantido: `e75142f`. Árvore com correções locais para revisão; nenhum commit ou push. Fontes em `dados_brutos/` intactas. Temporários sintéticos criados na raiz durante os testes foram removidos; os produtos reais da auditoria foram gravados fora do repositório. Consultar `git status --short` para a relação atual dos arquivos modificados/novos.

## L. Veredito

**FASE 8 APROVADA**, no escopo dos contratos implementados e das garantias de publicação documentadas. Os 23 critérios de aceite foram cobertos pela implementação, pelos testes e pela revisão documental. Não há bloqueador analítico ou funcional identificado nesta rodada. O pacote é uma entrega de evidências, ainda não o relatório final do curso.

## M. Próximo passo

Revisar o diff e decidir o commit; mensagem sugerida: `fix(fase-8): valida evidencias e publica artefatos com rollback`.

Após essa revisão, o próximo trabalho poderá ser a definição formal da Fase 9A. Fases 9A e 9B não foram implementadas.
