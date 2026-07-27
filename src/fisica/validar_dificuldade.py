from __future__ import annotations

import pandas as pd
from scipy.stats import spearmanr


ITENS = ["co_rs_i1", "co_rs_i2", "co_rs_i7"]


def diagnosticar_dificuldade(base: pd.DataFrame, co_ies: int = 569) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Audita os indicadores e estima associações ecológicas no conjunto de cursos."""
    ufpa = base[base["CO_IES"].eq(co_ies)].copy()
    linhas = []
    for _, row in ufpa.iterrows():
        for item in ITENS:
            n = pd.to_numeric(row.get(f"{item}_n"), errors="coerce")
            pct = pd.to_numeric(row.get(f"{item}_dificuldade_alta_pct"), errors="coerce")
            linhas.append({
                "CO_CURSO": row["CO_CURSO"],
                "ROTULO_OFERTA": row["ROTULO_OFERTA"],
                "CONCEITO_ENADE_NUM": row.get("CONCEITO_ENADE_NUM"),
                "item": item.upper(),
                "n_valido": n,
                "dificuldade_alta_pct": pct,
                "alerta": "OK" if pd.notna(pct) and 0 <= pct <= 100 else "Percentual inválido ou ausente",
            })
    associacoes = []
    for item in ITENS:
        y = pd.to_numeric(base[f"{item}_dificuldade_alta_pct"], errors="coerce")
        for xcol in ["nt_ger_mean", "CONCEITO_ENADE_NUM"]:
            x = pd.to_numeric(base[xcol], errors="coerce")
            validos = x.notna() & y.notna()
            rho, p = spearmanr(x[validos], y[validos]) if validos.sum() >= 10 else (float("nan"), float("nan"))
            associacoes.append({
                "variavel_x": xcol,
                "variavel_y": f"{item}_dificuldade_alta_pct",
                "n_cursos": int(validos.sum()),
                "spearman_rho": rho,
                "p_valor_exploratorio": p,
                "nivel": "curso (ecológico)",
            })
    return pd.DataFrame(linhas), pd.DataFrame(associacoes)
