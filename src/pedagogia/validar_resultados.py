from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.pedagogia import CO_CURSO_CASTANHAL


def validar_resultados_sprint14(
    base: pd.DataFrame,
    auditoria_desempenho: pd.DataFrame,
    auditoria_indicadores: pd.DataFrame,
    comparacoes: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    contraste_interno: pd.DataFrame,
    comparacao_itens: pd.DataFrame,
    figuras: list[Path],
) -> None:
    if len(base) != 1200:
        raise ValueError(f"Esperados 1200 cursos de Pedagogia; encontrados {len(base)}.")
    if not base["CO_CURSO"].is_unique:
        raise ValueError("A base analítica não possui uma linha única por CO_CURSO.")

    ufpa = base.loc[base["CO_IES"].eq(569)]
    if len(ufpa) != 7:
        raise ValueError(f"Esperadas 7 ofertas da UFPA; encontradas {len(ufpa)}.")
    if ufpa["CONCEITO_ENADE_NUM"].eq(1).any():
        raise ValueError("Pedagogia da UFPA não deve conter oferta tratada como Conceito 1.")
    if set(pd.to_numeric(ufpa["CONCEITO_ENADE_NUM"], errors="coerce").dropna().astype(int)) != {4, 5}:
        raise ValueError("Os conceitos da UFPA em Pedagogia devem ser somente 4 e 5.")

    castanhal = ufpa.loc[
        pd.to_numeric(ufpa["CO_CURSO"], errors="coerce").eq(CO_CURSO_CASTANHAL)
    ]
    if len(castanhal) != 1 or int(castanhal.iloc[0]["CONCEITO_ENADE_NUM"]) != 5:
        raise ValueError("Castanhal não foi preservada como única oferta UFPA Conceito 5.")

    if auditoria_desempenho["alerta_n_superior_registros"].any():
        raise ValueError("Há N válido superior ao número de registros do curso.")
    if (auditoria_indicadores["fora_0_1"] > 0).any():
        ruins = auditoria_indicadores.loc[
            auditoria_indicadores["fora_0_1"].gt(0), "indicador"
        ].tolist()
        raise ValueError(f"Indicadores percentuais fora de 0–1: {ruins}")

    if comparacoes["ALERTA_IQR_NEGATIVO"].any():
        raise ValueError("Há amplitude interquartil negativa nas comparações regionais.")

    esperadas = 7 * 5
    if len(sensibilidade) != esperadas:
        raise ValueError(
            f"Esperadas {esperadas} linhas na sensibilidade dos benchmarks; "
            f"encontradas {len(sensibilidade)}."
        )
    principal = sensibilidade.loc[
        sensibilidade["CENARIO"].eq("estrutura_porte_0_5_2_0")
    ]
    if len(principal) != 7 or (principal["N_CURSOS"] <= 0).any():
        raise ValueError("O benchmark estrutural principal deve existir para as 7 ofertas da UFPA.")

    if contraste_interno.empty or contraste_interno["INDICADOR"].nunique() < 4:
        raise ValueError("O contraste interno da UFPA está incompleto.")

    if comparacao_itens.empty or comparacao_itens["ITEM"].nunique() != 47:
        raise ValueError("Esperados 47 itens QE_I20–QE_I66 na validação do processo formativo.")

    ausentes = [str(path) for path in figuras if not path.exists() or path.stat().st_size == 0]
    if ausentes:
        raise ValueError(f"Figuras de validação ausentes ou vazias: {ausentes}")
