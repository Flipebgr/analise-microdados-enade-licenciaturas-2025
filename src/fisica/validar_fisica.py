from __future__ import annotations

import pandas as pd

from src.core.configuracao_area import FISICA
from src.core.validacao import validar_base_area

AREA_FISICA = FISICA.co_grupo
CO_IES_UFPA = FISICA.co_ies_focal


def validar_base_fisica(base: pd.DataFrame) -> None:
    resultado = validar_base_area(
        base,
        FISICA,
        colunas_obrigatorias=("ROTULO_OFERTA",),
        ofertas_ies_esperadas=5,
    )
    resultado.exigir_valido()

    ufpa = base[base["CO_IES"].eq(FISICA.co_ies_focal)]
    if ufpa["ROTULO_OFERTA"].duplicated().any():
        raise ValueError("Rótulos de ofertas da UFPA duplicados.")

    taxa = pd.to_numeric(base.get("taxa_presenca_microdados"), errors="coerce")
    if ((taxa.dropna() < 0) | (taxa.dropna() > 1)).any():
        raise ValueError("Taxa de presença fora do intervalo 0–1.")

    for coluna in ["nt_ger_mean", "nt_obj_mean", "nt_dis_mean"]:
        valores = pd.to_numeric(base.get(coluna), errors="coerce").dropna()
        if ((valores < 0) | (valores > 100)).any():
            raise ValueError(f"{coluna} fora da escala 0–100.")
