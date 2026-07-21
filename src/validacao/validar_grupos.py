from __future__ import annotations

import pandas as pd


def validar_grupos(df: pd.DataFrame) -> None:
    if df["GRUPO_CODIGO"].isna().any():
        raise AssertionError("Há cursos sem classificação de grupo")
    if ((df["GRUPO_CODIGO"] == "A") & (df["CONCEITO_ENADE_NUM"] != 1)).any():
        raise AssertionError("Grupo A contém curso que não é Conceito 1")
    if ((df["GRUPO_CODIGO"] == "B") & ~df["CO_IES"].eq(569)).any():
        raise AssertionError("Grupo B contém curso externo à UFPA")
    if ((df["GRUPO_CODIGO"] == "C") & df["CO_IES"].eq(569)).any():
        raise AssertionError("Grupo C contém UFPA")
