# Sprint 12 — Relatório final de Ciências Biológicas com estudo focal de Soure

## Objetivo

Consolidar os produtos validados das Sprints 10 e 11 em relatório técnico-científico final, preservando o padrão adotado nas áreas anteriores e acrescentando um estudo focal aprofundado da oferta de Ciências Biológicas da UFPA em Soure (`CO_CURSO=104640`).

## Estrutura

O relatório contém:

- elementos pré-textuais;
- Introdução;
- Referencial institucional e metodológico;
- Metodologia;
- Panorama de Ciências Biológicas;
- Resultados:
  - 5.1 Desempenho;
  - 5.2 Perfil demográfico e socioeconômico;
  - 5.3 Trajetória e condições acadêmicas;
  - 5.4 Processo formativo;
  - 5.5 Recomendação;
  - 5.6 Benchmark comparável;
  - 5.7 Associações ecológicas;
  - 5.8 Comparação regional e nacional;
  - 5.9 Estudo focal da oferta de Soure;
- Discussão;
- Conclusão;
- Referências;
- Apêndices.

## Particularidade metodológica da área

Não existe oferta da UFPA com Conceito Enade 1 em Ciências Biológicas. Portanto, a Sprint 12 não cria artificialmente um grupo de Conceito 1. O contraste principal é Soure versus:

- demais ofertas da UFPA;
- outras IES do Pará;
- Norte sem Pará;
- Brasil sem Norte;
- benchmark estruturalmente comparável.

## Processo formativo

Os códigos `QE_I20–QE_I66` são vinculados aos textos oficiais do Dicionário de Variáveis do Enade das Licenciaturas 2025. A escala válida de concordância é preservada e nenhum índice único é criado automaticamente.

O relatório inclui um apêndice com os 47 rótulos oficiais, além de apresentar os itens com maiores diferenças absolutas entre Soure e seu benchmark.

## Recomendação

Os itens são tratados pelos rótulos oficiais:

- `QE_I68`: recomendação do curso;
- `QE_I69`: recomendação da IES;
- `QE_I70`: interesse em participar da Prova Nacional Docente 2025.

Não são agrupados automaticamente sob o rótulo genérico de satisfação.

## Produtos

- `relatorios/biologia/relatorio_ciencias_biologicas_enade_2025_soure.docx`
- `relatorios/biologia/relatorio_ciencias_biologicas_enade_2025_soure.md`
- PDF quando LibreOffice estiver disponível.

## Validação

```powershell
python executar_sprint_12.py
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```

## Restrições preservadas

- unidade principal `CO_CURSO`;
- nenhuma junção individual entre arquivos temáticos;
- nenhuma reconstrução de estudante;
- ausência de conceito não equivale a Conceito 1;
- análises individuais somente dentro do mesmo arquivo;
- associações entre arquivos distintos apenas no nível ecológico;
- benchmark não é interpretado como desenho causal.
