from __future__ import annotations

import numpy as np
import pandas as pd


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = pd.to_numeric(a, errors="coerce").dropna().to_numpy()
    b = pd.to_numeric(b, errors="coerce").dropna().to_numpy()
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    sp2 = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if not np.isfinite(sp2) or sp2 <= 0:
        return float("nan")
    d = (a.mean() - b.mean()) / np.sqrt(sp2)
    correcao = 1 - 3 / (4 * (len(a) + len(b)) - 9)
    return float(d * correcao)


def contrastes_desempenho(individual: pd.DataFrame, cadastro: pd.DataFrame, variavel: str = "NT_GER") -> pd.DataFrame:
    dados = individual.merge(cadastro[["CO_CURSO", "GRUPO_CODIGO", "GRUPO"]], on="CO_CURSO", how="left", validate="many_to_one")
    linhas: list[dict] = []
    foco = dados.loc[dados["GRUPO_CODIGO"].eq("A"), variavel]
    for grupo in list("BCDE"):
        comparacao = dados.loc[dados["GRUPO_CODIGO"].eq(grupo), variavel]
        linhas.append({
            "CONTRASTE": f"A vs {grupo}",
            "VARIAVEL": variavel,
            "N_A": int(pd.to_numeric(foco, errors="coerce").notna().sum()),
            "N_COMPARACAO": int(pd.to_numeric(comparacao, errors="coerce").notna().sum()),
            "DIF_MEDIA": pd.to_numeric(foco, errors="coerce").mean() - pd.to_numeric(comparacao, errors="coerce").mean(),
            "HEDGES_G": hedges_g(foco, comparacao),
        })
    return pd.DataFrame(linhas)
