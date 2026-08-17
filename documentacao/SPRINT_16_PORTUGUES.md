# Sprint 16 — Base analítica de Letras–Português

## Objetivo

Construir a base analítica nacional de Letras–Português (`CO_GRUPO=904`), validar as ofertas da UFPA e produzir o panorama inicial com grupos comparativos exclusivos e benchmark estrutural.

## Validação da relação UFPA

A validação direta das fontes de 2025 encontrou oito ofertas da UFPA:

| CO_CURSO | Município | Modalidade | Conceito |
|---:|---|---|---:|
| 27645 | Belém | Presencial | 4 |
| 114846 | Cametá | Presencial | 3 |
| 114850 | Abaetetuba | Presencial | 3 |
| 114857 | Castanhal | Presencial | 3 |
| 114874 | Bragança | Presencial | 3 |
| 114876 | Altamira | Presencial | 2 |
| 115013 | Breves | Presencial | 3 |
| 115161 | Belém | EaD | 1 |

A oferta inicialmente informada de Soure não foi localizada no `microdados2025_arq1.txt` para `CO_GRUPO=904` nem na planilha oficial `conceito_enade_licenciaturas.xlsx`. Ela é preservada em `auditoria_relacao_ufpa.csv`, mas sem criação artificial de `CO_CURSO`, inscritos, participantes, desempenho ou conceito e fora dos grupos comparativos.

## Universo

O cadastro `microdados2025_arq1.txt` contém 340 `CO_CURSO` únicos de Letras–Português:
- Norte: 36
- Nordeste: 125
- Sudeste: 88
- Sul: 59
- Centro-Oeste: 32
- Presencial: 222
- EaD: 118

## Grupos exclusivos

A. UFPA — Conceito 1  
B. UFPA — conceito superior  
C. Outras IES do Pará  
D. Restante da Região Norte, excluindo Pará  
E. Restante do Brasil, excluindo Norte

Belém EaD (`CO_CURSO=115161`) é a única oferta UFPA do Grupo A. As sete demais ofertas localizadas pertencem ao Grupo B.

## Regras metodológicas

- unidade principal: `CO_CURSO`;
- não há join individual entre arquivos temáticos;
- cada arquivo é agregado por curso antes das junções;
- relações entre temas distintos são ecológicas;
- ausência de fonte não equivale a Conceito 1;
- Soure não é fabricada no catálogo;
- benchmark comparável usa mesma modalidade, categoria administrativa, organização acadêmica e porte entre 0,5x e 2x participantes;
- QE_I20–QE_I66 permanecem item a item nesta sprint.

## Saídas

A Sprint produz bases agregadas e analíticas em `dados_processados/portugues/`, 13 figuras em `figuras/portugues/` e `relatorios/sprint_16_piloto_letras_portugues.md`.

## Validação local

```cmd
python executar_sprint_16.py
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```
