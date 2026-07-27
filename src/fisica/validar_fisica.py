from __future__ import annotations

import pandas as pd

AREA_FISICA = 1402
CO_IES_UFPA = 569


def validar_base_fisica(base: pd.DataFrame) -> None:
    if not base["CO_GRUPO"].eq(AREA_FISICA).all():
        raise ValueError("A base contém cursos fora de Física.")
    if base["CO_CURSO"].duplicated().any():
        raise ValueError("CO_CURSO duplicado na base de Física.")
    ufpa = base[base["CO_IES"].eq(CO_IES_UFPA)]
    if len(ufpa) != 5:
        raise ValueError(f"Esperadas 5 ofertas validadas da UFPA; encontradas {len(ufpa)}.")
    if ufpa["ROTULO_OFERTA"].duplicated().any():
        raise ValueError("Rótulos de ofertas da UFPA duplicados.")
    taxa = pd.to_numeric(base.get("taxa_presenca_microdados"), errors="coerce")
    if ((taxa.dropna() < 0) | (taxa.dropna() > 1)).any():
        raise ValueError("Taxa de presença fora do intervalo 0–1.")
    for coluna in ["nt_ger_mean", "nt_obj_mean", "nt_dis_mean"]:
        s = pd.to_numeric(base.get(coluna), errors="coerce").dropna()
        if ((s < 0) | (s > 100)).any():
            raise ValueError(f"{coluna} fora da escala 0–100.")
