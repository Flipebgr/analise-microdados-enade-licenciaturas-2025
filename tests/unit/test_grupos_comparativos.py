from __future__ import annotations

import pandas as pd
import pytest

from src.core.configuracao_area import BIOLOGIA_BACHARELADO_2017, QUIMICA
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
    assert resultado["eh_focal"].tolist() == [True, True, False, False, False, True]

    validar_grupos(
        resultado,
        co_ies_focal=QUIMICA.co_ies_focal,
    )


def test_piloto_2017_marca_foco_sem_alterar_grupo_b():
    cursos = pd.DataFrame(
        {
            "CO_CURSO": ["12027", "12028", "12029"],
            "CO_IES": ["569", "569", "999"],
            "CO_UF_CURSO": ["15", "15", "15"],
            "CO_REGIAO_CURSO": ["1", "1", "1"],
            "CONCEITO_ENADE_NUM": [3, pd.NA, pd.NA],
        }
    )

    resultado = aplicar_grupos_area(cursos, BIOLOGIA_BACHARELADO_2017)

    assert resultado["GRUPO_CODIGO"].tolist() == ["B", "SEM_GRUPO", "C"]
    assert resultado["eh_focal"].tolist() == [True, False, False]


def test_foco_configurado_deve_ser_da_ies_focal():
    cursos = pd.DataFrame(
        {
            "CO_CURSO": ["12027"],
            "CO_IES": ["999"],
            "CO_UF_CURSO": ["15"],
            "CO_REGIAO_CURSO": ["1"],
            "CONCEITO_ENADE_NUM": [3],
        }
    )

    with pytest.raises(ValueError, match="não pertencem à IES focal"):
        aplicar_grupos_area(cursos, BIOLOGIA_BACHARELADO_2017)


def test_foco_configurado_ausente_do_universo_e_rejeitado():
    cursos = pd.DataFrame(
        {
            "CO_CURSO": ["12028"],
            "CO_IES": ["569"],
            "CO_UF_CURSO": ["15"],
            "CO_REGIAO_CURSO": ["1"],
            "CONCEITO_ENADE_NUM": [3],
        }
    )

    with pytest.raises(ValueError, match="ausentes no universo"):
        aplicar_grupos_area(cursos, BIOLOGIA_BACHARELADO_2017)


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
