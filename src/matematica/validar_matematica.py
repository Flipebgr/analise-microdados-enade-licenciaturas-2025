from __future__ import annotations

import pandas as pd

from src.core.configuracao_area import MATEMATICA
from src.core.validacao import validar_base_area
from src.validacao.validar_agregacoes import validar_percentuais


def validar_base_matematica(base: pd.DataFrame) -> None:
    resultado = validar_base_area(
        base,
        MATEMATICA,
        colunas_obrigatorias=("ROTULO_OFERTA", "GRUPO_CODIGO"),
        ofertas_ies_esperadas=8,
    )
    resultado.exigir_valido()

    validar_percentuais(base)
    if "nt_ger_count" in base and "registros_microdados" in base:
        excedentes = base["nt_ger_count"].fillna(0) > base["registros_microdados"].fillna(0)
        if excedentes.any():
            raise AssertionError("N válido de NT_GER supera registros do curso")

    ufpa = base[base["CO_IES"].eq(MATEMATICA.co_ies_focal)].copy()
    conceito = pd.to_numeric(ufpa.get("CONCEITO_ENADE_NUM"), errors="coerce")
    if int(conceito.eq(1).sum()) != 7:
        raise ValueError("Esperadas 7 ofertas da UFPA com Conceito Enade 1 em Matemática")
    if not ufpa.loc[conceito.isna(), "GRUPO_CODIGO"].eq("SEM_GRUPO").all():
        raise ValueError("Oferta sem conceito foi classificada em grupo comparativo")
