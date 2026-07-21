from __future__ import annotations

import numpy as np
import pandas as pd

CRITERIOS = {
    "porte_25pct": (0.75, 1.25),
    "porte_50pct": (0.50, 1.50),
    "porte_2x": (0.50, 2.00),
}


def _selecionar(candidatos: pd.DataFrame, alvo: pd.Series, faixa: tuple[float, float]) -> pd.DataFrame:
    mask = (
        candidatos["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
        & candidatos["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
        & candidatos["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])
    )
    n = pd.to_numeric(pd.Series([alvo.get("PARTICIPANTES_NUM")]), errors="coerce").iloc[0]
    if pd.notna(n) and n > 0:
        mask &= candidatos["PARTICIPANTES_NUM"].between(max(1, n * faixa[0]), n * faixa[1])
    return candidatos.loc[mask].copy()


def sensibilidade_benchmarks(base: pd.DataFrame, co_ies_ufpa: int = 569) -> tuple[pd.DataFrame, pd.DataFrame]:
    alvos = base[base["CO_IES"].eq(co_ies_ufpa) & base["CONCEITO_ENADE_NUM"].eq(1)].copy()
    candidatos = base[~base["CO_IES"].eq(co_ies_ufpa)].copy()
    resumo: list[dict] = []
    membros: list[pd.DataFrame] = []
    for _, alvo in alvos.iterrows():
        for criterio, faixa in CRITERIOS.items():
            sel = _selecionar(candidatos, alvo, faixa)
            if not sel.empty:
                tmp = sel[["CO_CURSO", "nt_ger_mean", "nt_ger_median", "PARTICIPANTES_NUM"]].copy()
                tmp.insert(0, "criterio", criterio)
                tmp.insert(0, "CO_CURSO_ALVO", alvo["CO_CURSO"])
                membros.append(tmp)
            media = pd.to_numeric(sel.get("nt_ger_mean"), errors="coerce").mean() if len(sel) else np.nan
            mediana = pd.to_numeric(sel.get("nt_ger_mean"), errors="coerce").median() if len(sel) else np.nan
            alvo_media = pd.to_numeric(pd.Series([alvo.get("nt_ger_mean")]), errors="coerce").iloc[0]
            resumo.append({
                "CO_CURSO_ALVO": alvo["CO_CURSO"],
                "ROTULO_ALVO": alvo["ROTULO_OFERTA"],
                "criterio": criterio,
                "n_comparaveis": len(sel),
                "nt_ger_alvo": alvo_media,
                "media_benchmark": media,
                "mediana_benchmark": mediana,
                "diferenca_media": alvo_media - media if pd.notna(media) else np.nan,
                "diferenca_mediana": alvo_media - mediana if pd.notna(mediana) else np.nan,
            })
    return pd.DataFrame(resumo), (pd.concat(membros, ignore_index=True) if membros else pd.DataFrame())
