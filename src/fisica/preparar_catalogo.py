from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.analise.definir_grupos import aplicar_grupos
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.normalizacao import normalizar_codigo
from src.validacao.validar_grupos import validar_grupos
from src.validacao.validar_planilha_conceito import carregar_conceitos

AREA_FISICA = 1402
CO_IES_UFPA = 569


def numerico(serie: pd.Series) -> pd.Series:
    return pd.to_numeric(serie.astype("string").str.replace(",", ".", regex=False), errors="coerce")


def preparar_catalogo_fisica(extraida: Path, conceito_path: Path) -> pd.DataFrame:
    arq1 = encontrar_arquivo(extraida, "microdados2025_arq1.txt")
    cadastro = pd.read_csv(arq1, sep=";", dtype="string", low_memory=False)
    for coluna in cadastro.columns:
        cadastro[coluna] = normalizar_codigo(cadastro[coluna])
    cadastro = cadastro[cadastro["CO_GRUPO"].eq(AREA_FISICA)].copy()
    chaves = [
        "NU_ANO", "CO_CURSO", "CO_IES", "CO_CATEGAD", "CO_ORGACAD", "CO_GRUPO",
        "CO_MODALIDADE", "CO_MUNIC_CURSO", "CO_UF_CURSO", "CO_REGIAO_CURSO",
    ]
    cadastro = cadastro[chaves].drop_duplicates("CO_CURSO")

    conceitos = carregar_conceitos(conceito_path)
    conceitos = conceitos[conceitos["CO_GRUPO"].eq(AREA_FISICA)].copy()
    manter = [
        "CO_CURSO", "NO_IES", "SG_IES", "AREA", "MODALIDADE", "MUNICIPIO", "UF",
        "INSCRITOS", "PARTICIPANTES", "TOTAL_PADRAO_PROFICIENCIA",
        "PCT_PADRAO_PROFICIENCIA", "CONCEITO_ENADE", "SITUACAO_CONCEITO",
    ]
    conceitos = conceitos[manter].drop_duplicates("CO_CURSO")
    cursos = cadastro.merge(conceitos, on="CO_CURSO", how="left", validate="one_to_one")
    cursos["MODALIDADE"] = cursos["MODALIDADE"].fillna(
        cursos["CO_MODALIDADE"].map({0: "EaD", 1: "Presencial"})
    )
    cursos["ROTULO_OFERTA"] = cursos.apply(
        lambda r: f"{r.get('MUNICIPIO') or r.get('CO_MUNIC_CURSO')} — {r.get('MODALIDADE')}", axis=1
    )
    cursos["CONCEITO_ENADE_NUM"] = numerico(cursos["CONCEITO_ENADE"])
    cursos["INSCRITOS_NUM"] = numerico(cursos["INSCRITOS"])
    cursos["PARTICIPANTES_NUM"] = numerico(cursos["PARTICIPANTES"])
    cursos["PCT_PADRAO_PROFICIENCIA_NUM"] = numerico(cursos["PCT_PADRAO_PROFICIENCIA"])
    cursos = aplicar_grupos(cursos, CO_IES_UFPA)
    validar_grupos(cursos)
    return cursos
