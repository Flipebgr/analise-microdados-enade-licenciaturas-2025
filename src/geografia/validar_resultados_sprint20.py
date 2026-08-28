from __future__ import annotations

from pathlib import Path

import pandas as pd


CURSOS_UFPA = {11991: 4, 12052: 3, 1194057: 3, 1330343: 4}


def validar_resultados_sprint20(
    base: pd.DataFrame,
    auditoria_desempenho: pd.DataFrame,
    auditoria_indicadores: pd.DataFrame,
    comparacoes: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    contraste: pd.DataFrame,
    processo: pd.DataFrame,
    figuras: list[Path],
) -> None:
    if len(base) != 254:
        raise ValueError(
            f"Esperados 254 cursos de Geografia; encontrados {len(base)}."
        )
    if not base["CO_CURSO"].is_unique:
        raise ValueError("A base analítica não é única por CO_CURSO.")

    ufpa = base.loc[base["CO_IES"].eq(569)].copy()
    if len(ufpa) != 4:
        raise ValueError(
            f"Esperadas 4 ofertas da UFPA; encontradas {len(ufpa)}."
        )
    if ufpa["CONCEITO_ENADE_NUM"].eq(1).any():
        raise ValueError(
            "Geografia da UFPA não deve conter oferta tratada como Conceito 1."
        )

    encontrados = {
        int(r.CO_CURSO): int(r.CONCEITO_ENADE_NUM)
        for r in ufpa.itertuples()
    }
    if encontrados != CURSOS_UFPA:
        raise ValueError(
            f"Relação UFPA divergente: {encontrados}"
        )

    if auditoria_desempenho["alerta_n_superior_registros"].any():
        raise ValueError(
            "Há N válido superior ao número de registros do curso."
        )
    if (auditoria_indicadores["fora_0_1"] > 0).any():
        ruins = auditoria_indicadores.loc[
            auditoria_indicadores["fora_0_1"].gt(0),
            "indicador",
        ].tolist()
        raise ValueError(
            f"Indicadores percentuais fora de 0–1: {ruins}"
        )

    if comparacoes["ALERTA_IQR_NEGATIVO"].any():
        raise ValueError(
            "Há amplitude interquartil negativa nas comparações regionais."
        )

    if len(sensibilidade) != 20:
        raise ValueError(
            "Esperadas 20 combinações oferta-cenário "
            f"(4 ofertas × 5 cenários); encontradas {len(sensibilidade)}."
        )
    principal = sensibilidade.loc[
        sensibilidade["CENARIO"].eq("estrutura_porte_0_5_2_0")
    ]
    if len(principal) != 4:
        raise ValueError(
            "O cenário estrutural principal deve conter as quatro ofertas UFPA."
        )

    if contraste.empty or contraste["INDICADOR"].nunique() < 4:
        raise ValueError("O contraste Conceito 3 × Conceito 4 está incompleto.")
    if not (
        contraste["N_CONCEITO_3"].dropna().eq(2).all()
        and contraste["N_CONCEITO_4"].dropna().eq(2).all()
    ):
        raise ValueError(
            "O contraste interno deve preservar duas ofertas em cada conceito."
        )

    if processo.empty or processo["ITEM"].nunique() != 47:
        raise ValueError(
            "Esperados 47 itens QE_I20–QE_I66 na validação."
        )

    ausentes = [
        str(path)
        for path in figuras
        if not path.exists() or path.stat().st_size == 0
    ]
    if ausentes:
        raise ValueError(
            f"Figuras de validação ausentes ou vazias: {ausentes}"
        )
