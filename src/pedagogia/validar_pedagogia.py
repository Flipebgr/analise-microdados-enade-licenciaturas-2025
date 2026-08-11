from __future__ import annotations

import pandas as pd

from src.core.validacao import validar_base_area
from src.pedagogia import CO_CURSO_CASTANHAL, PEDAGOGIA
from src.validacao.validar_grupos import validar_grupos

CURSOS_UFPA_ESPERADOS = {
    11996: ("Belém", 4),
    12048: ("Altamira", 4),
    12061: ("Bragança", 4),
    12069: ("Cametá", 4),
    12085: ("Castanhal", 5),
    12111: ("Breves", 4),
    38276: ("Abaetetuba", 4),
}


def validar_base_pedagogia(base: pd.DataFrame) -> None:
    validar_base_area(base, PEDAGOGIA).exigir_valido()
    validar_grupos(base)
    ufpa = base[base["CO_IES"].eq(PEDAGOGIA.co_ies_focal)].copy()

    if len(ufpa) != len(CURSOS_UFPA_ESPERADOS):
        raise ValueError(
            f"Esperadas {len(CURSOS_UFPA_ESPERADOS)} ofertas localizadas da UFPA; "
            f"encontradas {len(ufpa)}."
        )
    if ufpa["CONCEITO_ENADE_NUM"].eq(1).any() or ufpa["GRUPO_CODIGO"].eq("A").any():
        raise ValueError("Pedagogia da UFPA não possui oferta com Conceito Enade 1.")

    encontrados = {}
    for _, linha in ufpa.iterrows():
        codigo = int(pd.to_numeric(linha["CO_CURSO"], errors="raise"))
        conceito = int(pd.to_numeric(linha["CONCEITO_ENADE_NUM"], errors="raise"))
        encontrados[codigo] = (str(linha["MUNICIPIO"]), conceito)
    if encontrados != CURSOS_UFPA_ESPERADOS:
        raise ValueError(
            f"Relação UFPA divergente: esperado={CURSOS_UFPA_ESPERADOS}, "
            f"encontrado={encontrados}"
        )

    castanhal = ufpa[pd.to_numeric(ufpa["CO_CURSO"], errors="coerce").eq(CO_CURSO_CASTANHAL)]
    if len(castanhal) != 1:
        raise ValueError("Oferta de Castanhal não localizada de forma única.")
    if int(castanhal.iloc[0]["CONCEITO_ENADE_NUM"]) != 5:
        raise ValueError("Castanhal deve possuir Conceito Enade 5 na fonte oficial.")
    if not bool(castanhal.iloc[0].get("REFERENCIA_INTERNA_CASTANHAL", False)):
        raise ValueError("Castanhal não foi marcado como referência interna.")
    if set(ufpa["RECORTE_PEDAGOGIA"]) != {"UFPA — Conceito 4", "UFPA — Conceito 5"}:
        raise ValueError("Recortes internos da UFPA em Pedagogia estão divergentes.")
