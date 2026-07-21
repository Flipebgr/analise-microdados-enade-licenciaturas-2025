from __future__ import annotations

import pandas as pd


def validar_resultados(auditoria: pd.DataFrame, indicadores: pd.DataFrame, benchmarks: pd.DataFrame, sensibilidade: pd.DataFrame) -> None:
    if auditoria["alerta_n_superior_registros"].any():
        raise ValueError("Há N válido superior ao total de registros do curso.")
    if (indicadores["fora_0_1"] > 0).any():
        ruins = indicadores.loc[indicadores["fora_0_1"].gt(0), "indicador"].tolist()
        raise ValueError(f"Indicadores percentuais fora de 0–1: {ruins}")
    if benchmarks.empty or sensibilidade.empty:
        raise ValueError("As análises de benchmark/sensibilidade não podem ser vazias.")
    if benchmarks["CO_CURSO_ALVO"].nunique() != 7:
        raise ValueError("Esperados sete cursos-alvo da UFPA com Conceito 1.")
