from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.biologia import BIOLOGIA, CO_CURSO_SOURE
from src.core.catalogo import preparar_catalogo_area
from src.core.grupos import aplicar_grupos_area
from src.core.juncoes import juntar_por_curso, validar_unicidade_por_curso
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.normalizacao import normalizar_codigo
from src.validacao.validar_grupos import validar_grupos
from src.validacao.validar_planilha_conceito import carregar_conceitos

COLUNAS_CADASTRO = [
    "NU_ANO", "CO_CURSO", "CO_IES", "CO_CATEGAD", "CO_ORGACAD",
    "CO_GRUPO", "CO_MODALIDADE", "CO_MUNIC_CURSO", "CO_UF_CURSO",
    "CO_REGIAO_CURSO",
]
COLUNAS_CONCEITO = [
    "CO_CURSO", "NO_IES", "SG_IES", "AREA", "MODALIDADE", "MUNICIPIO",
    "UF", "INSCRITOS", "PARTICIPANTES", "TOTAL_PADRAO_PROFICIENCIA",
    "PCT_PADRAO_PROFICIENCIA", "CONCEITO_ENADE", "SITUACAO_CONCEITO",
]


def numerico(serie: pd.Series) -> pd.Series:
    return pd.to_numeric(
        serie.astype("string").str.replace(",", ".", regex=False),
        errors="coerce",
    )


def aplicar_recorte_focal(cursos: pd.DataFrame) -> pd.DataFrame:
    """Cria recortes exclusivos para a análise focal de Soure."""
    out = cursos.copy()
    curso = pd.to_numeric(out["CO_CURSO"], errors="coerce")
    ies = pd.to_numeric(out["CO_IES"], errors="coerce")
    uf = pd.to_numeric(out["CO_UF_CURSO"], errors="coerce")
    regiao = pd.to_numeric(out["CO_REGIAO_CURSO"], errors="coerce")
    out["FOCO_SOURE"] = curso.eq(CO_CURSO_SOURE)
    out["RECORTE_FOCAL"] = pd.Series(
        np.select(
            [
                curso.eq(CO_CURSO_SOURE),
                ies.eq(BIOLOGIA.co_ies_focal),
                uf.eq(15),
                regiao.eq(1),
            ],
            [
                "Soure",
                "UFPA sem Soure",
                "Outras IES do Pará",
                "Norte sem Pará",
            ],
            default="Brasil sem Norte",
        ),
        index=out.index,
        dtype="string",
    )
    return out


def preparar_catalogo_biologia(extraida: Path, conceito_path: Path) -> pd.DataFrame:
    arq1 = encontrar_arquivo(extraida, "microdados2025_arq1.txt")
    cadastro = pd.read_csv(arq1, sep=";", dtype="string", low_memory=False)
    cadastro = cadastro.loc[:, COLUNAS_CADASTRO].copy()
    for coluna in COLUNAS_CADASTRO:
        cadastro[coluna] = normalizar_codigo(cadastro[coluna])
    cadastro = cadastro[cadastro["CO_GRUPO"].eq(BIOLOGIA.co_grupo)].drop_duplicates("CO_CURSO")
    adicionais = tuple(
        coluna for coluna in COLUNAS_CADASTRO
        if coluna not in {"CO_CURSO", "CO_IES", "CO_GRUPO"}
    )
    cadastro = preparar_catalogo_area(
        cadastro, BIOLOGIA, colunas_adicionais=adicionais
    ).drop(columns=["IES_FOCAL", "AREA_SLUG", "AREA_NOME"])

    conceitos = carregar_conceitos(conceito_path)
    conceitos = conceitos[conceitos["CO_GRUPO"].eq(BIOLOGIA.co_grupo)].copy()
    conceitos = conceitos.loc[:, COLUNAS_CONCEITO]
    conceitos["CO_CURSO"] = normalizar_codigo(conceitos["CO_CURSO"])
    conceitos = conceitos.drop_duplicates("CO_CURSO")
    validar_unicidade_por_curso(conceitos, nome="conceitos de Ciências Biológicas")

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
    cursos["TAXA_PARTICIPACAO_OFICIAL"] = (
        cursos["PARTICIPANTES_NUM"] / cursos["INSCRITOS_NUM"]
    ).where(cursos["INSCRITOS_NUM"].gt(0))
    cursos = aplicar_grupos_area(cursos, BIOLOGIA)
    cursos = aplicar_recorte_focal(cursos)
    validar_grupos(cursos)
    return cursos
