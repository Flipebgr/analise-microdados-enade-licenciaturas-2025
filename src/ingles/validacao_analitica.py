from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.analise.analise_sensibilidade import sensibilidade_desempenho
from src.analise.validar_benchmarks import sensibilidade_benchmarks
from src.analise.validar_indicadores import auditar_desempenho, auditar_indicadores

RECORTES_OBRIGATORIOS = {
    "UFPA agregada",
    "Região Norte sem UFPA",
    "Região Norte completa",
    "Nordeste",
    "Sudeste",
    "Sul",
    "Centro-Oeste",
    "Brasil geral",
    "Brasil sem UFPA",
    "Restante do Brasil sem Norte",
}

INDICADORES_ECOLOGICOS = (
    "renda_ate_3sm_pct",
    "trabalha_pct",
    "acao_afirmativa_pct",
    "auxilio_permanencia_pct",
    "qe_i68_media",
    "qe_i69_media",
)


def auditar_participacao_desempenho(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Audita Ns de desempenho e indicadores percentuais no nível do curso."""
    return auditar_desempenho(base), auditar_indicadores(base)


def validar_comparacoes_regionais(comparacoes: pd.DataFrame) -> pd.DataFrame:
    """Produz diagnóstico estrutural dos recortes regional/nacional da Sprint 07."""
    faltantes = RECORTES_OBRIGATORIOS - set(comparacoes["RECORTE"].dropna().astype(str))
    if faltantes:
        raise ValueError(f"Recortes regionais ausentes: {sorted(faltantes)}")

    trabalho = comparacoes.copy()
    colunas_numericas = [
        "N_CURSOS",
        "N_PARTICIPANTES",
        "MEDIA_CURSOS",
        "MEDIA_PONDERADA_PARTICIPANTES",
        "MEDIANA_CURSOS",
        "DP_CURSOS",
        "P25",
        "P75",
    ]
    for coluna in colunas_numericas:
        trabalho[coluna] = pd.to_numeric(trabalho[coluna], errors="coerce")

    if (trabalho["N_CURSOS"].dropna() < 0).any():
        raise ValueError("Há N_CURSOS negativo nas comparações regionais.")
    if (trabalho["N_PARTICIPANTES"].dropna() < 0).any():
        raise ValueError("Há N_PARTICIPANTES negativo nas comparações regionais.")

    trabalho["AMPLITUDE_IQR"] = trabalho["P75"] - trabalho["P25"]
    trabalho["DIF_MEDIA_PONDERADA"] = (
        trabalho["MEDIA_PONDERADA_PARTICIPANTES"] - trabalho["MEDIA_CURSOS"]
    )
    trabalho["ALERTA_IQR_NEGATIVO"] = trabalho["AMPLITUDE_IQR"].lt(0)
    return trabalho


def construir_sensibilidades(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Executa sensibilidade de desempenho e benchmark comparável para Conceito 1."""
    desempenho = sensibilidade_desempenho(base)
    benchmarks, membros = sensibilidade_benchmarks(base)
    return desempenho, benchmarks, membros


def diagnosticar_outliers(base: pd.DataFrame, indicadores: Iterable[str] = ("nt_ger_mean",)) -> pd.DataFrame:
    """Marca outliers por regra 1,5×IQR sem excluir cursos da análise."""
    linhas: list[dict[str, object]] = []
    for indicador in indicadores:
        valores = pd.to_numeric(base[indicador], errors="coerce")
        validos = valores.dropna()
        q1 = validos.quantile(0.25)
        q3 = validos.quantile(0.75)
        iqr = q3 - q1
        inferior = q1 - 1.5 * iqr
        superior = q3 + 1.5 * iqr
        for idx, valor in valores.items():
            if pd.isna(valor):
                continue
            linhas.append(
                {
                    "CO_CURSO": base.loc[idx, "CO_CURSO"],
                    "ROTULO_OFERTA": base.loc[idx, "ROTULO_OFERTA"],
                    "GRUPO_CODIGO": base.loc[idx, "GRUPO_CODIGO"],
                    "INDICADOR": indicador,
                    "VALOR": float(valor),
                    "Q1": float(q1),
                    "Q3": float(q3),
                    "LIMITE_INFERIOR": float(inferior),
                    "LIMITE_SUPERIOR": float(superior),
                    "OUTLIER_IQR": bool(valor < inferior or valor > superior),
                }
            )
    return pd.DataFrame(linhas)


def associacoes_ecologicas(base: pd.DataFrame) -> pd.DataFrame:
    """Calcula Spearman entre desempenho médio e indicadores agregados por curso."""
    linhas: list[dict[str, object]] = []
    y = pd.to_numeric(base["nt_ger_mean"], errors="coerce")
    for indicador in INDICADORES_ECOLOGICOS:
        if indicador not in base.columns:
            continue
        x = pd.to_numeric(base[indicador], errors="coerce")
        mask = x.notna() & y.notna()
        n = int(mask.sum())
        rho = np.nan
        pvalor = np.nan
        if n >= 3 and x[mask].nunique() > 1 and y[mask].nunique() > 1:
            resultado = spearmanr(x[mask], y[mask], nan_policy="omit")
            rho = float(resultado.statistic)
            pvalor = float(resultado.pvalue)
        linhas.append(
            {
                "INDICADOR_X": indicador,
                "INDICADOR_Y": "nt_ger_mean",
                "N_CURSOS": n,
                "SPEARMAN_RHO": rho,
                "P_VALOR_EXPLORATORIO": pvalor,
                "NIVEL_ANALISE": "curso (ecológico)",
            }
        )
    return pd.DataFrame(linhas)


def sintetizar_socioeconomico_ufpa(base: pd.DataFrame, co_ies: int = 569) -> pd.DataFrame:
    colunas = [
        "CO_CURSO",
        "ROTULO_OFERTA",
        "CONCEITO_ENADE_NUM",
        "nt_ger_mean",
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
    ]
    presentes = [c for c in colunas if c in base.columns]
    return base.loc[base["CO_IES"].eq(co_ies), presentes].copy()
