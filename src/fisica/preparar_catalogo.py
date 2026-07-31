from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.core.catalogo import preparar_catalogo_area
from src.core.configuracao_area import FISICA
from src.core.grupos import aplicar_grupos_area
from src.core.juncoes import juntar_por_curso, validar_unicidade_por_curso
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.normalizacao import normalizar_codigo
from src.validacao.validar_grupos import validar_grupos
from src.validacao.validar_planilha_conceito import carregar_conceitos

AREA_FISICA = FISICA.co_grupo
CO_IES_UFPA = FISICA.co_ies_focal


COLUNAS_CADASTRO = [
    "NU_ANO",
    "CO_CURSO",
    "CO_IES",
    "CO_CATEGAD",
    "CO_ORGACAD",
    "CO_GRUPO",
    "CO_MODALIDADE",
    "CO_MUNIC_CURSO",
    "CO_UF_CURSO",
    "CO_REGIAO_CURSO",
]

COLUNAS_CONCEITO = [
    "CO_CURSO",
    "NO_IES",
    "SG_IES",
    "AREA",
    "MODALIDADE",
    "MUNICIPIO",
    "UF",
    "INSCRITOS",
    "PARTICIPANTES",
    "TOTAL_PADRAO_PROFICIENCIA",
    "PCT_PADRAO_PROFICIENCIA",
    "CONCEITO_ENADE",
    "SITUACAO_CONCEITO",
]


def numerico(serie: pd.Series) -> pd.Series:
    return pd.to_numeric(
        serie.astype("string").str.replace(",", ".", regex=False),
        errors="coerce",
    )


def _preparar_cadastro(cadastro: pd.DataFrame) -> pd.DataFrame:
    trabalho = cadastro.loc[:, COLUNAS_CADASTRO].copy()
    for coluna in COLUNAS_CADASTRO:
        trabalho[coluna] = normalizar_codigo(trabalho[coluna])

    trabalho = trabalho[trabalho["CO_GRUPO"].eq(FISICA.co_grupo)].copy()
    trabalho = trabalho.drop_duplicates("CO_CURSO")
    return preparar_catalogo_area(
        trabalho,
        FISICA,
        colunas_adicionais=tuple(
            coluna
            for coluna in COLUNAS_CADASTRO
            if coluna not in {"CO_CURSO", "CO_IES", "CO_GRUPO"}
        ),
    ).drop(columns=["IES_FOCAL", "AREA_SLUG", "AREA_NOME"])


def _preparar_conceitos(conceitos: pd.DataFrame) -> pd.DataFrame:
    trabalho = conceitos[conceitos["CO_GRUPO"].eq(FISICA.co_grupo)].copy()
    trabalho = trabalho.loc[:, COLUNAS_CONCEITO]
    trabalho["CO_CURSO"] = normalizar_codigo(trabalho["CO_CURSO"])
    trabalho = trabalho.drop_duplicates("CO_CURSO")
    validar_unicidade_por_curso(trabalho, nome="conceitos de Física")
    return trabalho


def preparar_catalogo_fisica(extraida: Path, conceito_path: Path) -> pd.DataFrame:
    arq1 = encontrar_arquivo(extraida, "microdados2025_arq1.txt")
    cadastro_bruto = pd.read_csv(arq1, sep=";", dtype="string", low_memory=False)
    cadastro = _preparar_cadastro(cadastro_bruto)

    conceitos = _preparar_conceitos(carregar_conceitos(conceito_path))
    cursos = juntar_por_curso(cadastro, conceitos)
    cursos["MODALIDADE"] = cursos["MODALIDADE"].fillna(
        cursos["CO_MODALIDADE"].map({0: "EaD", 1: "Presencial"})
    )
    cursos["ROTULO_OFERTA"] = cursos.apply(
        lambda linha: (
            f"{linha.get('MUNICIPIO') or linha.get('CO_MUNIC_CURSO')}"
            f" — {linha.get('MODALIDADE')}"
        ),
        axis=1,
    )
    cursos["CONCEITO_ENADE_NUM"] = numerico(cursos["CONCEITO_ENADE"])
    cursos["INSCRITOS_NUM"] = numerico(cursos["INSCRITOS"])
    cursos["PARTICIPANTES_NUM"] = numerico(cursos["PARTICIPANTES"])
    cursos["PCT_PADRAO_PROFICIENCIA_NUM"] = numerico(
        cursos["PCT_PADRAO_PROFICIENCIA"]
    )
    cursos = aplicar_grupos_area(cursos, FISICA)
    validar_grupos(cursos)
    return cursos
