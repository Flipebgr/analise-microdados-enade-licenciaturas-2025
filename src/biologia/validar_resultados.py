from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.biologia import CO_CURSO_SOURE


def validar_resultados_sprint11(
    base: pd.DataFrame,
    auditoria_desempenho: pd.DataFrame,
    auditoria_indicadores: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    comparacao_itens: pd.DataFrame,
    figuras: list[Path],
) -> None:
    if len(base) != 428:
        raise ValueError(f"Esperados 428 cursos de Ciências Biológicas; encontrados {len(base)}.")
    if not base["CO_CURSO"].is_unique:
        raise ValueError("A base analítica não possui uma linha única por CO_CURSO.")
    ufpa = base.loc[base["CO_IES"].eq(569)]
    if len(ufpa) != 5:
        raise ValueError(f"Esperadas 5 ofertas da UFPA; encontradas {len(ufpa)}.")
    if int(pd.to_numeric(ufpa["CONCEITO_ENADE_NUM"], errors="coerce").eq(1).sum()) != 0:
        raise ValueError("Biologia não deve conter oferta UFPA tratada como Conceito Enade 1.")
    soure = base.loc[pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)]
    if len(soure) != 1 or soure.iloc[0]["RECORTE_FOCAL"] != "Soure":
        raise ValueError("A oferta focal de Soure não foi preservada corretamente.")
    if auditoria_desempenho["alerta_n_superior_registros"].any():
        raise ValueError("Há N válido superior ao número de registros do curso.")
    if (auditoria_indicadores["fora_0_1"] > 0).any():
        ruins = auditoria_indicadores.loc[
            auditoria_indicadores["fora_0_1"].gt(0), "indicador"
        ].tolist()
        raise ValueError(f"Indicadores percentuais fora de 0–1: {ruins}")
    if len(sensibilidade) < 5 or (sensibilidade["N_CURSOS"] <= 0).any():
        raise ValueError("A sensibilidade do benchmark de Soure está incompleta.")
    if comparacao_itens.empty or comparacao_itens["ITEM"].nunique() != 47:
        raise ValueError("Esperados 47 itens QE_I20–QE_I66 na validação do processo formativo.")
    ausentes = [str(path) for path in figuras if not path.exists() or path.stat().st_size == 0]
    if ausentes:
        raise ValueError(f"Figuras de validação ausentes ou vazias: {ausentes}")
