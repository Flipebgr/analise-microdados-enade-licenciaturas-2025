from __future__ import annotations

import numpy as np
import pandas as pd


def _media_ponderada(valores: pd.Series, pesos: pd.Series) -> float:
    v = pd.to_numeric(valores, errors="coerce")
    w = pd.to_numeric(pesos, errors="coerce")
    mask = v.notna() & w.notna() & (w > 0)
    return float(np.average(v[mask], weights=w[mask])) if mask.any() else np.nan


def sensibilidade_desempenho(base: pd.DataFrame) -> pd.DataFrame:
    cenarios = {
        "todos": pd.Series(True, index=base.index),
        "n_minimo_10": base["nt_ger_count"].fillna(0).ge(10),
        "presencial": base["CO_MODALIDADE"].eq(1),
        "universidades_federais": base["CO_CATEGAD"].eq(1),
    }
    linhas: list[dict] = []
    for cenario, mask in cenarios.items():
        df = base.loc[mask & base["GRUPO_CODIGO"].isin(list("ABCDE"))]
        for grupo, g in df.groupby("GRUPO_CODIGO", observed=True):
            s = pd.to_numeric(g["nt_ger_mean"], errors="coerce")
            linhas.append({
                "cenario": cenario,
                "grupo": grupo,
                "n_cursos": int(s.notna().sum()),
                "media_cursos": float(s.mean()),
                "mediana_cursos": float(s.median()),
                "media_ponderada_participantes": _media_ponderada(s, g["nt_ger_count"]),
            })
    return pd.DataFrame(linhas)
