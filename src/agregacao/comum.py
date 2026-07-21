from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from src.utilitarios.leitura import ler_txt
from src.utilitarios.normalizacao import normalizar_codigo


def converter_numerico(serie: pd.Series) -> pd.Series:
    return pd.to_numeric(
        serie.astype("string").str.replace(",", ".", regex=False).replace({".": pd.NA, "": pd.NA}),
        errors="coerce",
    )


def carregar_filtrado(path: Path, cursos: Iterable[int], usecols: list[str] | None = None) -> pd.DataFrame:
    df = ler_txt(path, usecols=usecols)
    df["CO_CURSO"] = normalizar_codigo(df["CO_CURSO"])
    return df[df["CO_CURSO"].isin(set(int(x) for x in cursos))].copy()


def resumo_numerico(df: pd.DataFrame, variaveis: list[str]) -> pd.DataFrame:
    partes: list[pd.DataFrame] = []
    for variavel in variaveis:
        tmp = df[["CO_CURSO", variavel]].copy()
        tmp[variavel] = converter_numerico(tmp[variavel])
        g = tmp.groupby("CO_CURSO", observed=True)[variavel]
        out = g.agg(["count", "mean", "median", "std", "min", "max"]).reset_index()
        quantis = g.quantile([0.10, 0.25, 0.75, 0.90]).unstack().reset_index()
        quantis.columns = ["CO_CURSO", "p10", "p25", "p75", "p90"]
        out = out.merge(quantis, on="CO_CURSO", how="left", validate="one_to_one")
        out["iqr"] = out["p75"] - out["p25"]
        out["erro_padrao"] = out["std"] / np.sqrt(out["count"].where(out["count"] > 0))
        out["ic95_inf"] = out["mean"] - 1.96 * out["erro_padrao"]
        out["ic95_sup"] = out["mean"] + 1.96 * out["erro_padrao"]
        out = out.rename(columns={c: f"{variavel.lower()}_{c}" for c in out.columns if c != "CO_CURSO"})
        partes.append(out)
    resultado = partes[0]
    for parte in partes[1:]:
        resultado = resultado.merge(parte, on="CO_CURSO", how="outer", validate="one_to_one")
    return resultado


def validar_unicidade(df: pd.DataFrame, nome: str) -> None:
    if not df["CO_CURSO"].is_unique:
        duplicados = df.loc[df["CO_CURSO"].duplicated(keep=False), "CO_CURSO"].tolist()[:10]
        raise ValueError(f"{nome} não possui uma linha por CO_CURSO. Exemplos: {duplicados}")
