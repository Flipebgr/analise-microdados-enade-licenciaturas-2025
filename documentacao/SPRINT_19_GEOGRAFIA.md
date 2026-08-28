# Sprint 19 — Base analítica de Geografia

## Objetivo

Construir a base analítica nacional de Geografia (`CO_GRUPO=3002`) e validar as ofertas da UFPA diretamente nas fontes oficiais de 2025.

## Validação das fontes

O cadastro `microdados2025_arq1.txt` contém:

- 254 cursos únicos de Geografia;
- 170 IES;
- 4 ofertas da UFPA.

A planilha `conceito_enade_licenciaturas.xlsx` também contém 254 cursos de Geografia e as mesmas quatro ofertas da UFPA.

### Ofertas UFPA

| CO_CURSO | Município | Modalidade | Inscritos | Participantes | Proficiência | Conceito |
|---:|---|---|---:|---:|---:|---:|
| 11991 | Belém | Presencial | 71 | 57 | 87,7% | 4 |
| 12052 | Altamira | Presencial | 27 | 23 | 73,9% | 3 |
| 1194057 | Cametá | Presencial | 92 | 68 | 63,2% | 3 |
| 1330343 | Ananindeua | Presencial | 77 | 63 | 77,8% | 4 |

Não existe oferta UFPA com Conceito Enade 1 em Geografia.

O Grupo A permanece vazio. O contraste interno principal passa a ser:

- UFPA Conceito 3;
- UFPA Conceito 4.

Isso não implica tratar Conceito 3 como insuficiência.

## Produtos

A Sprint 19 gera:

- catálogo nacional;
- tabela-mestra UFPA;
- auditoria entre cadastro e planilha;
- seis agregações temáticas;
- base analítica uma linha por `CO_CURSO`;
- benchmarks amplos e comparáveis;
- comparação interna UFPA;
- comparações regionais/nacionais;
- 13 figuras;
- relatório piloto.

## Metodologia

Mantêm-se as regras gerais do projeto:

- `CO_CURSO` é a unidade principal;
- arquivos temáticos são agregados separadamente;
- não há join individual entre temas;
- relações entre temas distintos são ecológicas;
- ausência de conceito não é Conceito 1;
- benchmark não é desenho causal;
- QE_I20–QE_I66 não são condensados em índice único sem validação.

## Execução

```cmd
python executar_sprint_19.py
python -m pytest -q -m "not integration"
python -m pytest -q -m integration
python -m pytest -q
python -m ruff check .
```
