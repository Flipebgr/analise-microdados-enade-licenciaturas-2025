# Sprint 21 — Relatório técnico-científico final de Geografia

## Objetivo

Consolidar os produtos validados das Sprints 19 e 20 em relatório final de Geografia, em Markdown e DOCX, seguindo a estrutura técnico-científica e a formatação ABNT já adotadas no projeto.

## Escopo consolidado

- `CO_GRUPO=3002`;
- 254 cursos de Geografia no universo analítico;
- 4 ofertas da UFPA;
- Belém e Ananindeua: Conceito Enade 4;
- Altamira e Cametá: Conceito Enade 3;
- nenhuma oferta UFPA Conceito Enade 1;
- Grupo A vazio;
- contraste interno: duas ofertas Conceito 3 × duas ofertas Conceito 4;
- 20 combinações oferta-cenário nos benchmarks;
- 19 figuras;
- desempenho, perfil, trajetória, processo formativo, recomendação, benchmark, associações ecológicas e comparação regional/nacional.

## Estrutura

O relatório contém:

- capa;
- resumo e palavras-chave;
- abstract e keywords;
- sumário;
- 1 Introdução;
- 2 Referencial institucional e metodológico;
- 3 Metodologia;
- 4 Panorama;
- 5 Resultados;
- 5.1 Desempenho;
- 5.2 Perfil demográfico e socioeconômico;
- 5.3 Trajetória e condições acadêmicas;
- 5.4 Processo formativo;
- 5.5 Recomendação;
- 5.6 Benchmark comparável;
- 5.7 Associações ecológicas;
- 5.8 Comparações regionais e nacionais;
- 5.9 Contraste interno das ofertas da UFPA;
- 6 Discussão;
- 7 Conclusão;
- Referências;
- Apêndices A, B e C.

## Regras preservadas

Não se cria Grupo A artificial. Conceito 3 não é chamado de insuficiência. Relações entre arquivos temáticos permanecem no nível ecológico do curso. QE_I20–QE_I66 são apresentados com rótulos oficiais e não são condensados em índice único. QE_I68, QE_I69 e QE_I70 permanecem conceitualmente separados. O texto apresenta padrões e hipóteses, não causalidade.

## Execução

```powershell
python executar_sprint_21.py
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```

## Saídas

- `relatorios/geografia/relatorio_geografia_enade_2025_ufpa.md`
- `relatorios/geografia/relatorio_geografia_enade_2025_ufpa.docx`
- PDF opcional, quando LibreOffice estiver disponível.
