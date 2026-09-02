from __future__ import annotations

import pandas as pd
import pytest

from src.core.configuracao_area import QUIMICA
from src.core.grupos import aplicar_grupos_area
from src.validacao.validar_grupos import validar_grupos


def _cursos() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [1, 2, 3, 4, 5, 6],
            "CO_IES": [569, 569, 999, 998, 997, 569],
            "UF": ["PA", "PA", "PA", "AM", "SP", "PA"],
            "CO_UF_CURSO": [15, 15, 15, 13, 35, 15],
            "CO_REGIAO_CURSO": [1, 1, 1, 1, 3, 1],
            "CONCEITO_ENADE": [1, 3, 1, 1, 1, pd.NA],
        }
    )


def test_grupos_comparativos_sao_exclusivos_no_core():
    resultado = aplicar_grupos_area(_cursos(), QUIMICA)

    assert resultado["CO_CURSO"].is_unique
    assert resultado["GRUPO_CODIGO"].tolist() == [
        "A",
        "B",
        "C",
        "D",
        "E",
        "SEM_GRUPO",
    ]
    assert (
        resultado.loc[
            resultado["CO_CURSO"].eq(6),
            "GRUPO_CODIGO",
        ].item()
        == "SEM_GRUPO"
    )

    validar_grupos(
        resultado,
        co_ies_focal=QUIMICA.co_ies_focal,
    )


def test_validacao_de_grupos_rejeita_grupo_a_sem_conceito_1():
    resultado = aplicar_grupos_area(_cursos(), QUIMICA)
    resultado.loc[resultado["CO_CURSO"].eq(2), "GRUPO_CODIGO"] = "A"

    with pytest.raises(AssertionError, match="Grupo A"):
        validar_grupos(
            resultado,
            co_ies_focal=QUIMICA.co_ies_focal,
        )


def test_validacao_aceita_coluna_conceito_enade_num():
    resultado = aplicar_grupos_area(_cursos(), QUIMICA)
    resultado["CONCEITO_ENADE_NUM"] = pd.to_numeric(
        resultado.pop("CONCEITO_ENADE"),
        errors="coerce",
    )

    validar_grupos(
        resultado,
        co_ies_focal=QUIMICA.co_ies_focal,
    )
