from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from src.geografia import GEOGRAFIA

RECORTES_GEOGRAFIA = (
    "UFPA — Conceito 4",
    "UFPA — Conceito 3",
    "Outras IES do Pará",
    "Norte sem Pará",
    "Brasil sem Norte",
)

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


def construir_comparacao_recortes(
    base: pd.DataFrame,
    indicadores: Iterable[str] = INDICADORES_PRINCIPAIS,
) -> pd.DataFrame:
    linhas: list[dict[str, object]] = []
    for recorte in RECORTES_GEOGRAFIA:
        sub = base[base["RECORTE_GEOGRAFIA"].eq(recorte)]
        for indicador in indicadores:
            if indicador not in sub.columns:
                continue
            valores = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append(
                {
                    "RECORTE_GEOGRAFIA": recorte,
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


def construir_benchmarks_por_oferta(
    base: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Seleciona benchmark externo estrutural para cada oferta UFPA."""
    ufpa = base[base["CO_IES"].eq(GEOGRAFIA.co_ies_focal)].copy()
    externos = base[~base["CO_IES"].eq(GEOGRAFIA.co_ies_focal)].copy()
    partes: list[pd.DataFrame] = []
    resumos: list[dict[str, object]] = []

    for _, alvo in ufpa.iterrows():
        participantes = pd.to_numeric(
            pd.Series([alvo.get("PARTICIPANTES_NUM")]), errors="coerce"
        ).iloc[0]

        mask = (
            externos["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
            & externos["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
            & externos["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])
        )
        if pd.notna(participantes) and participantes > 0:
            mask &= pd.to_numeric(
                externos["PARTICIPANTES_NUM"], errors="coerce"
            ).between(max(1, participantes * 0.5), participantes * 2.0)

        selecionados = externos.loc[mask].copy()
        selecionados.insert(0, "CO_CURSO_ALVO", int(alvo["CO_CURSO"]))
        selecionados.insert(1, "ROTULO_ALVO", alvo["ROTULO_OFERTA"])
        partes.append(selecionados)

        resumo: dict[str, object] = {
            "CO_CURSO_ALVO": int(alvo["CO_CURSO"]),
            "ROTULO_ALVO": alvo["ROTULO_OFERTA"],
            "CONCEITO_ALVO": alvo["CONCEITO_ENADE_NUM"],
            "PARTICIPANTES_ALVO": participantes,
            "N_CURSOS_COMPARAVEIS": len(selecionados),
            "CRITERIO": (
                "mesma modalidade, categoria administrativa e organização acadêmica; "
                "participantes entre 0,5x e 2x da oferta UFPA"
            ),
        }
        for indicador in ("nt_ger_mean", "nt_obj_mean", "nt_dis_mean"):
            valores = pd.to_numeric(
                selecionados.get(indicador), errors="coerce"
            ).dropna()
            valor_alvo = pd.to_numeric(
                pd.Series([alvo.get(indicador)]), errors="coerce"
            ).iloc[0]
            media = valores.mean()
            dp = valores.std(ddof=1)
            resumo[f"{indicador}_ALVO"] = valor_alvo
            resumo[f"{indicador}_MEDIA_BENCHMARK"] = media
            resumo[f"{indicador}_DIFERENCA"] = (
                valor_alvo - media if pd.notna(valor_alvo) else np.nan
            )
            resumo[f"{indicador}_Z"] = (
                (valor_alvo - media) / dp
                if pd.notna(valor_alvo) and np.isfinite(dp) and dp > 0
                else np.nan
            )
        resumos.append(resumo)

    benchmarks = pd.concat(partes, ignore_index=True) if partes else pd.DataFrame()
    return benchmarks, pd.DataFrame(resumos)


def construir_comparacao_interna_ufpa(base: pd.DataFrame) -> pd.DataFrame:
    ufpa = base[base["CO_IES"].eq(GEOGRAFIA.co_ies_focal)].copy()
    return construir_comparacao_recortes(
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
