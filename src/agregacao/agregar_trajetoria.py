from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.agregacao.comum import carregar_filtrado, converter_numerico, validar_unicidade


def agregar_trajetoria(path: Path, cursos: list[int], ano_referencia: int = 2025) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = carregar_filtrado(path, cursos, usecols=["CO_CURSO", "ANO_FIM_EM", "ANO_IN_GRAD", "CO_TURNO_GRADUACAO"])
    for c in ["ANO_FIM_EM", "ANO_IN_GRAD", "CO_TURNO_GRADUACAO"]:
        df[c] = converter_numerico(df[c])
    df.loc[~df["ANO_FIM_EM"].between(1950, ano_referencia), "ANO_FIM_EM"] = pd.NA
    df.loc[~df["ANO_IN_GRAD"].between(1950, ano_referencia), "ANO_IN_GRAD"] = pd.NA
    df["anos_desde_ingresso"] = ano_referencia - df["ANO_IN_GRAD"]
    agregado = df.groupby("CO_CURSO", observed=True).agg(
        ano_fim_em_n=("ANO_FIM_EM", "count"),
        ano_fim_em_mediana=("ANO_FIM_EM", "median"),
        ano_ingresso_n=("ANO_IN_GRAD", "count"),
        ano_ingresso_mediana=("ANO_IN_GRAD", "median"),
        anos_desde_ingresso_media=("anos_desde_ingresso", "mean"),
        anos_desde_ingresso_mediana=("anos_desde_ingresso", "median"),
        turno_n_valido=("CO_TURNO_GRADUACAO", lambda s: int(s.isin([1, 2, 3, 4]).sum())),
        turno_noturno_n=("CO_TURNO_GRADUACAO", lambda s: int((s == 4).sum())),
    ).reset_index()
    agregado["turno_noturno_pct"] = agregado["turno_noturno_n"] / agregado["turno_n_valido"]
    validar_unicidade(agregado, "agregado_trajetoria")
    distribuicao = df.groupby(["CO_CURSO", "CO_TURNO_GRADUACAO"], dropna=False).size().rename("n").reset_index()
    return agregado, distribuicao
