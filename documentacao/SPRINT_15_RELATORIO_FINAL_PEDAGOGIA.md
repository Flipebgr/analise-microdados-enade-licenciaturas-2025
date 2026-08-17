# Sprint 15 — Relatório final de Pedagogia

## Objetivo

Produzir o relatório técnico-científico final de Pedagogia no padrão ABNT já consolidado no projeto, utilizando exclusivamente os produtos validados das Sprints 13 e 14.

## Escopo analítico

- universo nacional de 1.200 cursos de Pedagogia identificados por `CO_CURSO`;
- sete ofertas da UFPA;
- ausência de oferta UFPA com Conceito Enade 1;
- contraste interno de Castanhal, Conceito 5, com seis ofertas Conceito 4;
- benchmarks territoriais e estruturais;
- cinco cenários de benchmark por oferta, totalizando 35 combinações;
- desempenho, participação, perfil, trajetória, processo formativo, recomendação, comparações regionais e associações ecológicas.

## Estrutura

1. Introdução
2. Referencial institucional e metodológico
3. Metodologia
4. Panorama da licenciatura
5. Resultados
   - 5.1 Desempenho
   - 5.2 Perfil demográfico e socioeconômico
   - 5.3 Trajetória e condições acadêmicas
   - 5.4 Processo formativo
   - 5.5 Recomendação
   - 5.6 Benchmark comparável
   - 5.7 Associações ecológicas
   - 5.8 Comparações regionais e nacionais
   - 5.9 Contraste interno das ofertas da UFPA
6. Discussão
7. Conclusão
8. Referências
9. Apêndices

## Regras preservadas

- `CO_CURSO` é a unidade principal;
- não há junção individual entre arquivos temáticos;
- ausência de conceito não é Conceito 1;
- Conceito 4 não é tratado como insuficiência;
- Castanhal é referência interna descritiva, não grupo causal;
- associações entre temas distintos permanecem ecológicas;
- QE_I20–QE_I66 permanecem item a item, com textos oficiais;
- QE_I68, QE_I69 e QE_I70 não são chamados automaticamente de satisfação.

## Saídas

- `relatorios/pedagogia/relatorio_pedagogia_enade_2025_ufpa.md`
- `relatorios/pedagogia/relatorio_pedagogia_enade_2025_ufpa.docx`
- PDF somente quando LibreOffice estiver disponível.

## Validação

```cmd
python executar_sprint_15.py
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```
