from __future__ import annotations

import pandas as pd

from src.biologia import BIOLOGIA, CO_CURSO_SOURE
from src.core.validacao import validar_base_area
from src.validacao.validar_grupos import validar_grupos

MUNICIPIOS_ESPERADOS = {"Belém", "Bragança", "Altamira", "Soure"}
CONCEITOS_ESPERADOS = {3, 4}


def validar_base_biologia(base: pd.DataFrame) -> None:
    validar_base_area(base, BIOLOGIA).exigir_valido()
    validar_grupos(base)
    ufpa = base[base["CO_IES"].eq(BIOLOGIA.co_ies_focal)].copy()
    if len(ufpa) != 5:
        raise ValueError(f"Esperadas 5 ofertas localizadas da UFPA; encontradas {len(ufpa)}.")
    if int(ufpa["CONCEITO_ENADE_NUM"].eq(1).sum()) != 0:
        raise ValueError("Ciências Biológicas da UFPA não deve possuir oferta com Conceito Enade 1.")
    conceitos = set(pd.to_numeric(ufpa["CONCEITO_ENADE_NUM"], errors="coerce").dropna().astype(int))
    if conceitos != CONCEITOS_ESPERADOS:
        raise ValueError(
            f"Conceitos da UFPA divergentes: esperado={sorted(CONCEITOS_ESPERADOS)}, "
            f"encontrado={sorted(conceitos)}"
        )
    municipios = set(ufpa["MUNICIPIO"].dropna().astype(str))
    if municipios != MUNICIPIOS_ESPERADOS:
        raise ValueError(
            "Municípios da UFPA divergentes: "
            f"esperado={sorted(MUNICIPIOS_ESPERADOS)}, encontrado={sorted(municipios)}"
        )
    soure = ufpa[pd.to_numeric(ufpa["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)]
    if len(soure) != 1:
        raise ValueError(f"Oferta focal de Soure ({CO_CURSO_SOURE}) não localizada de forma única.")
    if int(pd.to_numeric(soure.iloc[0]["CONCEITO_ENADE_NUM"], errors="coerce")) != 3:
        raise ValueError("A oferta focal de Soure deve possuir Conceito Enade 3 na fonte oficial.")
    if not bool(soure.iloc[0].get("FOCO_SOURE", False)):
        raise ValueError("A oferta de Soure não foi marcada como foco analítico.")
    if soure.iloc[0].get("RECORTE_FOCAL") != "Soure":
        raise ValueError("A oferta focal não recebeu o recorte 'Soure'.")
    if ufpa["GRUPO_CODIGO"].eq("A").any():
        raise ValueError("Grupo A deve permanecer vazio: não há UFPA Conceito 1 em Biologia.")
