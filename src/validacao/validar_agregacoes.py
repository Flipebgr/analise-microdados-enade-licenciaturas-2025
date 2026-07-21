from __future__ import annotations

import numpy as np
import pandas as pd


def validar_tabela_agregada(df: pd.DataFrame, nome: str) -> None:
    if "CO_CURSO" not in df:
        raise AssertionError(f"{nome}: CO_CURSO ausente")
    if not df["CO_CURSO"].is_unique:
        raise AssertionError(f"{nome}: CO_CURSO duplicado")


def validar_percentuais(df: pd.DataFrame) -> None:
    cols = [c for c in df.columns if c.endswith("_pct") or c.startswith("taxa_")]
    for c in cols:
        valores = pd.to_numeric(df[c], errors="coerce").astype("float64").to_numpy()
        valores = valores[np.isfinite(valores)]
        if valores.size and not ((valores >= 0) & (valores <= 1)).all():
            raise AssertionError(f"Percentual fora de [0,1] em {c}")
