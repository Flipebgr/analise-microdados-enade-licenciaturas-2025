from __future__ import annotations

import pandas as pd

from src.core.validacao import validar_base_area
from src.geografia import GEOGRAFIA
from src.validacao.validar_grupos import validar_grupos

CURSOS_UFPA_ESPERADOS = {
    11991: ("Belém", 4),
    12052: ("Altamira", 3),
    1194057: ("Cametá", 3),
    1330343: ("Ananindeua", 4),
}


def validar_base_geografia(base: pd.DataFrame) -> None:
    validar_base_area(base, GEOGRAFIA).exigir_valido()
    validar_grupos(base)

    if len(base) != 254:
        raise ValueError(
            f"Esperados 254 cursos únicos de Geografia; encontrados {len(base)}."
        )

    ufpa = base[base["CO_IES"].eq(GEOGRAFIA.co_ies_focal)].copy()
    if len(ufpa) != len(CURSOS_UFPA_ESPERADOS):
        raise ValueError(
            f"Esperadas {len(CURSOS_UFPA_ESPERADOS)} ofertas da UFPA; "
            f"encontradas {len(ufpa)}."
        )

    if ufpa["CONCEITO_ENADE_NUM"].eq(1).any() or ufpa["GRUPO_CODIGO"].eq("A").any():
        raise ValueError("Geografia da UFPA não possui oferta com Conceito Enade 1.")

    encontrados: dict[int, tuple[str, int]] = {}
    for _, linha in ufpa.iterrows():
        codigo = int(pd.to_numeric(linha["CO_CURSO"], errors="raise"))
        conceito = int(pd.to_numeric(linha["CONCEITO_ENADE_NUM"], errors="raise"))
        encontrados[codigo] = (str(linha["MUNICIPIO"]), conceito)

    if encontrados != CURSOS_UFPA_ESPERADOS:
        raise ValueError(
            f"Relação UFPA divergente: esperado={CURSOS_UFPA_ESPERADOS}, "
            f"encontrado={encontrados}"
        )

    if set(ufpa["RECORTE_GEOGRAFIA"]) != {
        "UFPA — Conceito 3",
        "UFPA — Conceito 4",
    }:
        raise ValueError("Recortes internos da UFPA em Geografia estão divergentes.")


def validar_auditoria_fontes(auditoria: pd.DataFrame) -> None:
    if len(auditoria) != 4:
        raise ValueError(
            f"Esperadas 4 ofertas UFPA na auditoria; encontradas {len(auditoria)}."
        )
    if not auditoria["STATUS_FONTES"].eq("Localizada nas duas fontes").all():
        divergentes = auditoria.loc[
            ~auditoria["STATUS_FONTES"].eq("Localizada nas duas fontes")
        ]
        raise ValueError(
            "Há divergência entre cadastro dos microdados e planilha de conceito: "
            f"{divergentes.to_dict(orient='records')}"
        )
