from __future__ import annotations

import pandas as pd
from scipy.stats import spearmanr


PREDITORES = [
    "taxa_presenca_microdados", "renda_ate_3sm_pct", "trabalha_pct",
    "acao_afirmativa_pct", "auxilio_permanencia_pct", "primeira_geracao_pct",
    "qe_i68_nota_9_10_pct", "qe_i69_nota_9_10_pct",
    "co_rs_i1_dificuldade_alta_pct", "co_rs_i7_dificuldade_alta_pct",
]


def calcular_associacoes(base: pd.DataFrame, desfecho: str = "nt_ger_mean") -> pd.DataFrame:
    linhas = []
    y = pd.to_numeric(base[desfecho], errors="coerce")
    for col in PREDITORES:
        if col not in base.columns:
            continue
        x = pd.to_numeric(base[col], errors="coerce")
        validos = x.notna() & y.notna()
        if validos.sum() < 30:
            rho = p = float("nan")
        else:
            rho, p = spearmanr(x[validos], y[validos])
        linhas.append({
            "desfecho": desfecho,
            "preditor": col,
            "n_cursos": int(validos.sum()),
            "spearman_rho": rho,
            "p_valor_exploratorio": p,
            "interpretacao": "Associação ecológica; não representa relação individual",
        })
    return pd.DataFrame(linhas)
