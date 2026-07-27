from __future__ import annotations

import numpy as np
import pandas as pd


CRITERIOS = {
    "porte_25pct": (0.75, 1.25),
    "porte_50pct": (0.50, 1.50),
    "porte_2x": (0.50, 2.00),
}


def _resumo(alvo: pd.Series, candidatos: pd.DataFrame, criterio: str) -> dict[str, object]:
    valores = pd.to_numeric(candidatos["nt_ger_mean"], errors="coerce").dropna()
    alvo_media = pd.to_numeric(alvo.get("nt_ger_mean"), errors="coerce")
    return {
        "CO_CURSO_ALVO": alvo["CO_CURSO"],
        "ROTULO_ALVO": alvo["ROTULO_OFERTA"],
        "criterio": criterio,
        "n_cursos_comparaveis": len(valores),
        "nt_ger_alvo": alvo_media,
        "media_comparaveis": valores.mean(),
        "mediana_comparaveis": valores.median(),
        "diferenca_media": alvo_media - valores.mean() if len(valores) else np.nan,
        "percentil_alvo": (valores.le(alvo_media).mean() * 100) if len(valores) else np.nan,
    }


def sensibilidade_benchmarks(base: pd.DataFrame, co_ies: int = 569) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Testa benchmarks alternativos para ofertas UFPA com conceito 1."""
    alvos = base[base["CO_IES"].eq(co_ies) & base["CONCEITO_ENADE_NUM"].eq(1)].copy()
    universo = base[~base["CO_IES"].eq(co_ies)].copy()
    resumos: list[dict[str, object]] = []
    membros: list[pd.DataFrame] = []
    for _, alvo in alvos.iterrows():
        n_alvo = float(alvo["PARTICIPANTES_NUM"])
        estrutural = universo[
            universo["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
            & universo["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
            & universo["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])
        ]
        for nome, (lim_inf, lim_sup) in CRITERIOS.items():
            cand = estrutural[
                pd.to_numeric(estrutural["PARTICIPANTES_NUM"], errors="coerce").between(n_alvo * lim_inf, n_alvo * lim_sup)
            ].copy()
            resumos.append(_resumo(alvo, cand, nome))
            if not cand.empty:
                cand = cand.assign(CO_CURSO_ALVO=alvo["CO_CURSO"], ROTULO_ALVO=alvo["ROTULO_OFERTA"], criterio=nome)
                membros.append(cand[["CO_CURSO_ALVO", "ROTULO_ALVO", "criterio", "CO_CURSO", "ROTULO_OFERTA", "nt_ger_mean", "PARTICIPANTES_NUM"]])
        for nome, cand in {
            "mesmo_quartil_porte": estrutural[estrutural["PARTICIPANTES_NUM"].pipe(pd.qcut, q=4, duplicates="drop").eq(pd.qcut(estrutural["PARTICIPANTES_NUM"], q=4, duplicates="drop").iloc[(estrutural["PARTICIPANTES_NUM"] - n_alvo).abs().argmin()])] if len(estrutural) >= 4 else estrutural.iloc[0:0],
            "universidades_federais": universo[
                universo["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
                & universo["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
                & universo["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])
                & pd.to_numeric(universo["PARTICIPANTES_NUM"], errors="coerce").between(n_alvo * .5, n_alvo * 2)
            ],
        }.items():
            resumos.append(_resumo(alvo, cand, nome))
            if not cand.empty:
                cand = cand.assign(CO_CURSO_ALVO=alvo["CO_CURSO"], ROTULO_ALVO=alvo["ROTULO_OFERTA"], criterio=nome)
                membros.append(cand[["CO_CURSO_ALVO", "ROTULO_ALVO", "criterio", "CO_CURSO", "ROTULO_OFERTA", "nt_ger_mean", "PARTICIPANTES_NUM"]])
    return pd.DataFrame(resumos), pd.concat(membros, ignore_index=True) if membros else pd.DataFrame()
