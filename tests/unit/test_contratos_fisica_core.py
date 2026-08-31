from __future__ import annotations

import pandas as pd
import pytest

from src.core.configuracao_area import FISICA
from src.core.grupos import aplicar_grupos_area
from src.fisica.agregar_fisica import juntar_um_para_um
from src.fisica.validar_fisica import validar_base_fisica


def catalogo_fisica_minimo() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [1, 2, 3, 4, 5],
            "CO_GRUPO": [1402] * 5,
            "CO_IES": [569] * 5,
            "UF": ["PA"] * 5,
            "CO_UF_CURSO": [15] * 5,
            "CO_REGIAO_CURSO": [1] * 5,
            "CONCEITO_ENADE": [3, 1, 1, 1, None],
            "ROTULO_OFERTA": ["A", "B", "C", "D", "E"],
            "taxa_presenca_microdados": [0.8] * 5,
            "nt_ger_mean": [40] * 5,
            "nt_obj_mean": [40] * 5,
            "nt_dis_mean": [40] * 5,
        }
    )


def test_grupos_fisica_usam_configuracao_central() -> None:
    resultado = aplicar_grupos_area(catalogo_fisica_minimo(), FISICA)
    assert resultado["GRUPO_CODIGO"].tolist() == ["B", "A", "A", "A", "SEM_GRUPO"]


def test_ausencia_de_conceito_nao_vira_conceito_um() -> None:
    resultado = aplicar_grupos_area(catalogo_fisica_minimo(), FISICA)
    sem_conceito = resultado.loc[resultado["CO_CURSO"].eq(5)].iloc[0]
    assert sem_conceito["GRUPO_CODIGO"] == "SEM_GRUPO"


def test_juncao_fisica_rejeita_duplicidade() -> None:
    agregado = pd.DataFrame({"CO_CURSO": [1, 1], "N": [10, 20]})
    with pytest.raises((AssertionError, ValueError), match="duplicado"):
        juntar_um_para_um(catalogo_fisica_minimo(), [("teste", agregado)])


def test_validacao_fisica_delega_contrato_estrutural() -> None:
    validar_base_fisica(catalogo_fisica_minimo())


def test_validacao_fisica_rejeita_area_incorreta() -> None:
    base = catalogo_fisica_minimo()
    base.loc[0, "CO_GRUPO"] = 702
    with pytest.raises(ValueError, match="CO_GRUPO incompatível"):
        validar_base_fisica(base)
