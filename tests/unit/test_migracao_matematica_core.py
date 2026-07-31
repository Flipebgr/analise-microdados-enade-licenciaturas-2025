from __future__ import annotations

import pandas as pd
import pytest

from src.core.configuracao_area import MATEMATICA
from src.core.grupos import aplicar_grupos_area
from src.matematica.agregar_matematica import juntar_um_para_um
from src.matematica.validar_matematica import validar_base_matematica


def catalogo_matematica_minimo() -> pd.DataFrame:
    conceitos = [3, 1, 1, 1, 1, 1, 1, 1]
    return pd.DataFrame(
        {
            "CO_CURSO": list(range(1, 9)),
            "CO_GRUPO": [702] * 8,
            "CO_IES": [569] * 8,
            "UF": ["PA"] * 8,
            "CO_UF_CURSO": [15] * 8,
            "CO_REGIAO_CURSO": [1] * 8,
            "CONCEITO_ENADE": conceitos,
            "CONCEITO_ENADE_NUM": conceitos,
            "ROTULO_OFERTA": [f"Oferta {indice}" for indice in range(1, 9)],
        }
    )


def test_grupos_matematica_usam_configuracao_central() -> None:
    resultado = aplicar_grupos_area(catalogo_matematica_minimo(), MATEMATICA)
    assert resultado["GRUPO_CODIGO"].tolist() == ["B"] + ["A"] * 7


def test_validacao_matematica_preserva_oito_ofertas_e_sete_conceito_um() -> None:
    base = aplicar_grupos_area(catalogo_matematica_minimo(), MATEMATICA)
    validar_base_matematica(base)


def test_ausencia_de_conceito_nao_vira_conceito_um() -> None:
    base = catalogo_matematica_minimo()
    base.loc[7, ["CONCEITO_ENADE", "CONCEITO_ENADE_NUM"]] = None
    resultado = aplicar_grupos_area(base, MATEMATICA)
    assert resultado.loc[7, "GRUPO_CODIGO"] == "SEM_GRUPO"


def test_juncao_matematica_rejeita_duplicidade() -> None:
    agregado = pd.DataFrame({"CO_CURSO": [1, 1], "N": [10, 20]})
    with pytest.raises((AssertionError, ValueError), match="duplicado"):
        juntar_um_para_um(catalogo_matematica_minimo(), [("teste", agregado)])


def test_validacao_matematica_rejeita_area_incorreta() -> None:
    base = aplicar_grupos_area(catalogo_matematica_minimo(), MATEMATICA)
    base.loc[0, "CO_GRUPO"] = 1402
    with pytest.raises(ValueError, match="CO_GRUPO incompatível"):
        validar_base_matematica(base)
