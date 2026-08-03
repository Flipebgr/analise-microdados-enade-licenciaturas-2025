from __future__ import annotations

import pandas as pd

from src.core.configuracao_area import INGLES
from src.core.validacao import validar_base_area
from src.validacao.validar_grupos import validar_grupos

MUNICIPIOS_ESPERADOS = {"Belém", "Altamira", "Bragança", "Cametá", "Soure"}


def validar_base_ingles(base: pd.DataFrame) -> None:
    validar_base_area(base, INGLES)
    validar_grupos(base)
    ufpa = base[base["CO_IES"].eq(INGLES.co_ies_focal)].copy()
    if len(ufpa) != 5:
        raise ValueError(f"Esperadas 5 ofertas localizadas da UFPA; encontradas {len(ufpa)}.")
    conceitos_1 = ufpa["CONCEITO_ENADE_NUM"].eq(1).sum()
    if conceitos_1 != 4:
        raise ValueError(f"Esperadas 4 ofertas da UFPA com Conceito 1; encontradas {conceitos_1}.")
    municipios = set(ufpa["MUNICIPIO"].dropna().astype(str))
    if municipios != MUNICIPIOS_ESPERADOS:
        raise ValueError(
            "Municípios da UFPA divergentes: "
            f"esperado={sorted(MUNICIPIOS_ESPERADOS)}, encontrado={sorted(municipios)}"
        )
    sem_conceito = ufpa["CONCEITO_ENADE_NUM"].isna()
    if ufpa.loc[sem_conceito, "GRUPO_CODIGO"].eq("A").any():
        raise ValueError("Oferta sem conceito foi classificada indevidamente como Conceito 1.")
