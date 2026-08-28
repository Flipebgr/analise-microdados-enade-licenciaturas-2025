from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.core.catalogo import preparar_catalogo_area
from src.core.grupos import aplicar_grupos_area
from src.core.juncoes import juntar_por_curso, validar_unicidade_por_curso
from src.geografia import GEOGRAFIA
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.normalizacao import normalizar_codigo
from src.validacao.validar_grupos import validar_grupos
from src.validacao.validar_planilha_conceito import carregar_conceitos

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


def aplicar_recorte_geografia(cursos: pd.DataFrame) -> pd.DataFrame:
    """Cria recortes exclusivos para Geografia sem inventar Grupo A."""
    out = cursos.copy()
    ies = pd.to_numeric(out["CO_IES"], errors="coerce")
    uf = pd.to_numeric(out["CO_UF_CURSO"], errors="coerce")
    regiao = pd.to_numeric(out["CO_REGIAO_CURSO"], errors="coerce")
    conceito = pd.to_numeric(out["CONCEITO_ENADE_NUM"], errors="coerce")

    out["RECORTE_GEOGRAFIA"] = pd.Series(
        np.select(
            [
                ies.eq(GEOGRAFIA.co_ies_focal) & conceito.eq(4),
                ies.eq(GEOGRAFIA.co_ies_focal) & conceito.eq(3),
                ~ies.eq(GEOGRAFIA.co_ies_focal) & uf.eq(15),
                ~uf.eq(15) & regiao.eq(1),
            ],
            [
                "UFPA — Conceito 4",
                "UFPA — Conceito 3",
                "Outras IES do Pará",
                "Norte sem Pará",
            ],
            default="Brasil sem Norte",
        ),
        index=out.index,
        dtype="string",
    )
    return out


def preparar_catalogo_geografia(
    extraida: Path,
    conceito_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    arq1 = encontrar_arquivo(extraida, "microdados2025_arq1.txt")
    cadastro = pd.read_csv(arq1, sep=";", dtype="string", low_memory=False)
    cadastro = cadastro.loc[:, COLUNAS_CADASTRO].copy()

    for coluna in COLUNAS_CADASTRO:
        cadastro[coluna] = normalizar_codigo(cadastro[coluna])

    cadastro = cadastro[
        cadastro["CO_GRUPO"].eq(GEOGRAFIA.co_grupo)
    ].drop_duplicates("CO_CURSO")

    adicionais = tuple(
        coluna
        for coluna in COLUNAS_CADASTRO
        if coluna not in {"CO_CURSO", "CO_IES", "CO_GRUPO"}
    )
    cadastro = preparar_catalogo_area(
        cadastro,
        GEOGRAFIA,
        colunas_adicionais=adicionais,
    ).drop(columns=["IES_FOCAL", "AREA_SLUG", "AREA_NOME"])

    conceitos = carregar_conceitos(conceito_path)
    conceitos = conceitos[conceitos["CO_GRUPO"].eq(GEOGRAFIA.co_grupo)].copy()
    conceitos = conceitos.loc[:, COLUNAS_CONCEITO]
    conceitos["CO_CURSO"] = normalizar_codigo(conceitos["CO_CURSO"])
    conceitos = conceitos.drop_duplicates("CO_CURSO")
    validar_unicidade_por_curso(conceitos, nome="conceitos de Geografia")

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

    cursos = aplicar_grupos_area(cursos, GEOGRAFIA)
    cursos = aplicar_recorte_geografia(cursos)
    validar_grupos(cursos)

    auditoria = construir_auditoria_fontes_ufpa(cadastro, conceitos)
    return cursos, auditoria


def construir_auditoria_fontes_ufpa(
    cadastro: pd.DataFrame,
    conceitos: pd.DataFrame,
) -> pd.DataFrame:
    """Compara presença das ofertas UFPA no cadastro e na planilha de conceito."""
    cad = cadastro.loc[
        cadastro["CO_IES"].eq(GEOGRAFIA.co_ies_focal),
        ["CO_CURSO", "CO_MUNIC_CURSO", "CO_MODALIDADE"],
    ].copy()
    cad["NO_CADASTRO_MICRODADOS"] = True

    con = conceitos.copy()
    if "CO_IES" in con.columns:
        con = con[con["CO_IES"].eq(GEOGRAFIA.co_ies_focal)]
    else:
        con = con[con["SG_IES"].astype("string").str.upper().eq("UFPA")]
    con = con[
        [
            "CO_CURSO",
            "MUNICIPIO",
            "MODALIDADE",
            "INSCRITOS",
            "PARTICIPANTES",
            "PCT_PADRAO_PROFICIENCIA",
            "CONCEITO_ENADE",
            "SITUACAO_CONCEITO",
        ]
    ].copy()
    con["NA_PLANILHA_CONCEITO"] = True

    audit = cad.merge(con, on="CO_CURSO", how="outer", validate="one_to_one")
    audit["NO_CADASTRO_MICRODADOS"] = audit["NO_CADASTRO_MICRODADOS"].fillna(False)
    audit["NA_PLANILHA_CONCEITO"] = audit["NA_PLANILHA_CONCEITO"].fillna(False)
    audit["STATUS_FONTES"] = np.select(
        [
            audit["NO_CADASTRO_MICRODADOS"] & audit["NA_PLANILHA_CONCEITO"],
            audit["NO_CADASTRO_MICRODADOS"] & ~audit["NA_PLANILHA_CONCEITO"],
            ~audit["NO_CADASTRO_MICRODADOS"] & audit["NA_PLANILHA_CONCEITO"],
        ],
        [
            "Localizada nas duas fontes",
            "Somente no cadastro dos microdados",
            "Somente na planilha de conceito",
        ],
        default="Não localizada",
    )
    return audit.sort_values("CO_CURSO").reset_index(drop=True)


def tabela_mestra_ufpa(cursos: pd.DataFrame) -> pd.DataFrame:
    colunas = [
        "NU_ANO",
        "CO_IES",
        "CO_GRUPO",
        "CO_CURSO",
        "AREA",
        "MUNICIPIO",
        "MODALIDADE",
        "INSCRITOS_NUM",
        "PARTICIPANTES_NUM",
        "PCT_PADRAO_PROFICIENCIA_NUM",
        "CONCEITO_ENADE_NUM",
        "SITUACAO_CONCEITO",
        "ROTULO_OFERTA",
    ]
    ufpa = cursos[cursos["CO_IES"].eq(GEOGRAFIA.co_ies_focal)].copy()
    return ufpa[[c for c in colunas if c in ufpa.columns]].sort_values(
        ["MUNICIPIO", "MODALIDADE"]
    ).reset_index(drop=True)
