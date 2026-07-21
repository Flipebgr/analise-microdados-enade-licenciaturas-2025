from __future__ import annotations

import pandas as pd
from src.validacao.validar_agregacoes import validar_percentuais


def validar_base_analitica(df: pd.DataFrame) -> None:
    if not df["CO_CURSO"].is_unique:
        raise AssertionError("Base analítica não é única por CO_CURSO")
    if not df["CO_GRUPO"].eq(702).all():
        raise AssertionError("Base contém área diferente de Matemática")
    validar_percentuais(df)
    if "nt_ger_count" in df and "registros_microdados" in df:
        if (df["nt_ger_count"].fillna(0) > df["registros_microdados"].fillna(0)).any():
            raise AssertionError("N válido de NT_GER supera registros do curso")
