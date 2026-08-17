from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from src.portugues import PORTUGUES

ORDEM_GRUPOS = ("A", "B", "C", "D", "E")
INDICADORES_PRINCIPAIS = (
    "nt_ger_mean",
    "nt_obj_mean",
    "nt_dis_mean",
    "taxa_presenca_microdados",
    "renda_ate_3sm_pct",
    "trabalha_pct",
    "acao_afirmativa_pct",
    "auxilio_permanencia_pct",
    "bolsa_academica_pct",
    "estudo_4h_ou_mais_pct",
    "qe_i68_media",
    "qe_i69_media",
)


def construir_comparacao_grupos(
    base: pd.DataFrame,
    indicadores: Iterable[str] = INDICADORES_PRINCIPAIS,
) -> pd.DataFrame:
    linhas: list[dict[str, object]] = []
    for grupo in ORDEM_GRUPOS:
        sub = base[base["GRUPO_CODIGO"].eq(grupo)]
        rotulo = sub["GRUPO"].iloc[0] if not sub.empty else grupo
        for indicador in indicadores:
            if indicador not in sub.columns:
                continue
            valores = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append(
                {
                    "GRUPO_CODIGO": grupo,
                    "GRUPO": rotulo,
                    "INDICADOR": indicador,
                    "N_CURSOS": int(valores.size),
                    "MEDIA_CURSOS": valores.mean(),
                    "MEDIANA_CURSOS": valores.median(),
                    "DP_CURSOS": valores.std(ddof=1),
                    "P25": valores.quantile(0.25),
                    "P75": valores.quantile(0.75),
                }
            )
    return pd.DataFrame(linhas)


def construir_contraste_ufpa(base: pd.DataFrame) -> pd.DataFrame:
    ufpa = base[base["CO_IES"].eq(PORTUGUES.co_ies_focal)].copy()
    resumo = construir_comparacao_grupos(
        ufpa,
        indicadores=(
            "nt_ger_mean",
            "nt_obj_mean",
            "nt_dis_mean",
            "taxa_presenca_microdados",
            "renda_ate_3sm_pct",
            "trabalha_pct",
            "acao_afirmativa_pct",
            "auxilio_permanencia_pct",
            "qe_i68_media",
            "qe_i69_media",
        ),
    )
    resumo = resumo[resumo["GRUPO_CODIGO"].isin(["A", "B"])].copy()

    linhas: list[dict[str, object]] = []
    for indicador in resumo["INDICADOR"].drop_duplicates():
        a = resumo[
            resumo["GRUPO_CODIGO"].eq("A") & resumo["INDICADOR"].eq(indicador)
        ]
        b = resumo[
            resumo["GRUPO_CODIGO"].eq("B") & resumo["INDICADOR"].eq(indicador)
        ]
        if a.empty or b.empty:
            continue
        va = a.iloc[0]
        vb = b.iloc[0]
        dp_b = pd.to_numeric(
            pd.Series([vb["DP_CURSOS"]]),
            errors="coerce",
        ).iloc[0]
        diferenca = va["MEDIA_CURSOS"] - vb["MEDIA_CURSOS"]
        linhas.append(
            {
                "INDICADOR": indicador,
                "N_CURSOS_A": int(va["N_CURSOS"]),
                "MEDIA_A": va["MEDIA_CURSOS"],
                "N_CURSOS_B": int(vb["N_CURSOS"]),
                "MEDIA_B": vb["MEDIA_CURSOS"],
                "DIFERENCA_A_MENOS_B": diferenca,
                "Z_DESCRITIVO_VS_B": (
                    diferenca / dp_b
                    if pd.notna(dp_b) and np.isfinite(dp_b) and dp_b > 0
                    else np.nan
                ),
            }
        )
    return pd.DataFrame(linhas)
