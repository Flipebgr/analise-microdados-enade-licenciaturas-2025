from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.portugues import CO_CURSO_BELEM_EAD, PORTUGUES


def validar_resultados_sprint17(
    base: pd.DataFrame,
    auditoria_desempenho: pd.DataFrame,
    auditoria_indicadores: pd.DataFrame,
    comparacoes: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    benchmarks: pd.DataFrame,
    processo: pd.DataFrame,
    figuras: list[Path],
) -> None:
    if base["CO_CURSO"].duplicated().any():
        raise ValueError("Base de Português deixou de ser única por CO_CURSO.")
    if len(base) != 340:
        raise ValueError(f"Esperados 340 cursos de Português; encontrados {len(base)}.")

    ufpa = base.loc[base["CO_IES"].eq(PORTUGUES.co_ies_focal)]
    if len(ufpa) != 8:
        raise ValueError(f"Esperadas 8 ofertas localizadas da UFPA; encontradas {len(ufpa)}.")

    conceito1 = ufpa.loc[ufpa["CONCEITO_ENADE_NUM"].eq(1)]
    if len(conceito1) != 1:
        raise ValueError("Deve existir exatamente uma oferta UFPA Conceito Enade 1.")
    if int(conceito1.iloc[0]["CO_CURSO"]) != CO_CURSO_BELEM_EAD:
        raise ValueError("A oferta UFPA Conceito 1 não é Belém EaD CO_CURSO 115161.")

    if set(base["GRUPO_CODIGO"].dropna().astype(str)) - set("ABCDE"):
        raise ValueError("Foram encontrados grupos comparativos fora de A-E.")

    if auditoria_desempenho.empty or auditoria_indicadores.empty:
        raise ValueError("Auditorias da Sprint 17 estão vazias.")

    if comparacoes["ALERTA_IQR_NEGATIVO"].fillna(False).any():
        raise ValueError("Há IQR negativo nas comparações regionais.")

    cenarios_esperados = {"todos", "n_minimo_10", "presencial", "universidades_federais"}
    if not cenarios_esperados.issubset(set(sensibilidade["cenario"].astype(str))):
        raise ValueError("Cenários de sensibilidade de desempenho incompletos.")

    criterios = {"porte_25pct", "porte_50pct", "porte_2x"}
    if set(benchmarks["criterio"].astype(str)) != criterios:
        raise ValueError("Critérios de benchmark da oferta Conceito 1 incompletos.")

    if set(processo["REFERENCIA"].dropna().astype(str)) != {
        "UFPA — conceitos superiores",
        "Benchmark comparável",
        "Norte sem UFPA",
        "Brasil sem UFPA",
    }:
        raise ValueError("Referências do processo formativo incompletas.")

    if processo["ITEM"].nunique() != 47:
        raise ValueError("Esperados 47 itens QE_I20-QE_I66 na validação.")

    ausentes = [str(path) for path in figuras if not path.exists() or path.stat().st_size == 0]
    if ausentes:
        raise ValueError(f"Figuras de validação ausentes ou vazias: {ausentes}")
