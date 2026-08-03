from __future__ import annotations

from pathlib import Path

import pandas as pd


def validar_resultados_sprint08(
    base: pd.DataFrame,
    auditoria_desempenho: pd.DataFrame,
    auditoria_indicadores: pd.DataFrame,
    comparacoes: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    benchmarks: pd.DataFrame,
    figuras: list[Path],
) -> None:
    if len(base) != 138:
        raise ValueError(f"Esperados 138 cursos de Letras–Inglês; encontrados {len(base)}.")
    if not base["CO_CURSO"].is_unique:
        raise ValueError("A base analítica não possui uma linha única por CO_CURSO.")
    ufpa = base[base["CO_IES"].eq(569)]
    if len(ufpa) != 5:
        raise ValueError(f"Esperadas 5 ofertas da UFPA; encontradas {len(ufpa)}.")
    if int(ufpa["CONCEITO_ENADE_NUM"].eq(1).sum()) != 4:
        raise ValueError("Esperadas 4 ofertas da UFPA com Conceito Enade 1.")
    if auditoria_desempenho["alerta_n_superior_registros"].any():
        raise ValueError("Há N válido superior ao número de registros do curso.")
    if (auditoria_indicadores["fora_0_1"] > 0).any():
        ruins = auditoria_indicadores.loc[
            auditoria_indicadores["fora_0_1"].gt(0), "indicador"
        ].tolist()
        raise ValueError(f"Indicadores percentuais fora de 0–1: {ruins}")
    if comparacoes.empty or sensibilidade.empty or benchmarks.empty:
        raise ValueError("Comparações e análises de sensibilidade não podem ser vazias.")
    if benchmarks["CO_CURSO_ALVO"].nunique() != 4:
        raise ValueError("Esperados quatro cursos-alvo da UFPA com Conceito Enade 1.")
    ausentes = [str(path) for path in figuras if not path.exists() or path.stat().st_size == 0]
    if ausentes:
        raise ValueError(f"Figuras de validação ausentes ou vazias: {ausentes}")
