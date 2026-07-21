from __future__ import annotations

import numpy as np
import pandas as pd


def auditar_desempenho(base: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "CO_CURSO", "ROTULO_OFERTA", "GRUPO_CODIGO", "PARTICIPANTES_NUM",
        "registros_microdados", "presentes_validos", "nt_ger_count",
        "nt_obj_count", "nt_dis_count", "reaplicacoes",
    ]
    out = base[cols].copy()
    out["diferenca_participantes_oficial_nt_ger"] = out["PARTICIPANTES_NUM"] - out["nt_ger_count"]
    out["alerta_n_superior_registros"] = (
        out[["presentes_validos", "nt_ger_count", "nt_obj_count", "nt_dis_count"]]
        .max(axis=1) > out["registros_microdados"]
    )
    out["alerta_diferenca_participantes"] = out["diferenca_participantes_oficial_nt_ger"].abs() > 1
    return out


def auditar_indicadores(base: pd.DataFrame) -> pd.DataFrame:
    linhas: list[dict] = []
    pct_cols = [c for c in base.columns if c.endswith("_pct") or c.startswith("taxa_")]
    for col in pct_cols:
        s = pd.to_numeric(base[col], errors="coerce")
        linhas.append({
            "indicador": col,
            "n_cursos": int(s.notna().sum()),
            "ausencia_pct": float(s.isna().mean() * 100),
            "minimo": float(s.min()) if s.notna().any() else np.nan,
            "maximo": float(s.max()) if s.notna().any() else np.nan,
            "fora_0_1": int(((s < 0) | (s > 1)).sum()),
        })
    return pd.DataFrame(linhas)
