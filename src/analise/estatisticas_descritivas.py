from __future__ import annotations

import numpy as np
import pandas as pd


def posicao_percentil(serie: pd.Series) -> pd.Series:
    return serie.rank(method="average", pct=True) * 100


def adicionar_posicoes(base: pd.DataFrame) -> pd.DataFrame:
    out = base.copy()
    if "nt_ger_mean" in out:
        out["nt_ger_percentil_brasil"] = posicao_percentil(out["nt_ger_mean"])
        for regiao_nome, mask in {
            "norte": out["CO_REGIAO_CURSO"].eq(1),
            "para": out["CO_UF_CURSO"].eq(15),
        }.items():
            out.loc[mask, f"nt_ger_percentil_{regiao_nome}"] = posicao_percentil(out.loc[mask, "nt_ger_mean"])
        mediana = out["nt_ger_mean"].median()
        dp = out["nt_ger_mean"].std(ddof=1)
        out["nt_ger_dif_mediana_brasil"] = out["nt_ger_mean"] - mediana
        out["nt_ger_z_curso"] = (out["nt_ger_mean"] - out["nt_ger_mean"].mean()) / dp if np.isfinite(dp) and dp > 0 else np.nan
    return out


def resumo_por_grupo(base: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    linhas: list[dict] = []
    for grupo, sub in base[base["GRUPO_CODIGO"].isin(list("ABCDE"))].groupby(["GRUPO_CODIGO", "GRUPO"], observed=True):
        codigo, rotulo = grupo
        for coluna in colunas:
            if coluna not in sub:
                continue
            s = pd.to_numeric(sub[coluna], errors="coerce").dropna()
            linhas.append({
                "GRUPO_CODIGO": codigo,
                "GRUPO": rotulo,
                "INDICADOR": coluna,
                "N_CURSOS": int(s.size),
                "MEDIA_CURSOS": s.mean(),
                "MEDIANA_CURSOS": s.median(),
                "DP_CURSOS": s.std(ddof=1),
                "MIN": s.min(),
                "MAX": s.max(),
            })
    return pd.DataFrame(linhas)
