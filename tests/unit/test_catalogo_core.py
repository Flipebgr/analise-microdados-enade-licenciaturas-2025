import pandas as pd
import pytest

from src.core.catalogo import preparar_catalogo_area
from src.core.configuracao_area import QUIMICA


def cadastro_exemplo():
    return pd.DataFrame(
        {
            "CO_CURSO": ["10", "20", "30"],
            "CO_IES": ["569", "999", "569"],
            "CO_GRUPO": ["1502", "1502", "702"],
            "CO_MODALIDADE": ["1", "0", "1"],
        }
    )


def test_catalogo_filtra_area_e_marca_ies_focal():
    resultado = preparar_catalogo_area(
        cadastro_exemplo(), QUIMICA, colunas_adicionais=("CO_MODALIDADE",)
    )
    assert resultado["CO_CURSO"].tolist() == [10, 20]
    assert resultado["IES_FOCAL"].tolist() == [True, False]
    assert set(resultado["CO_GRUPO"]) == {1502}


def test_catalogo_nao_altera_entrada():
    original = cadastro_exemplo()
    copia = original.copy(deep=True)
    preparar_catalogo_area(original, QUIMICA)
    pd.testing.assert_frame_equal(original, copia)


def test_catalogo_rejeita_coluna_ausente():
    with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
        preparar_catalogo_area(cadastro_exemplo().drop(columns="CO_IES"), QUIMICA)


def test_catalogo_rejeita_curso_duplicado():
    cadastro = cadastro_exemplo()
    cadastro.loc[1, "CO_CURSO"] = "10"
    with pytest.raises(ValueError, match="duplicados"):
        preparar_catalogo_area(cadastro, QUIMICA)


def test_catalogo_rejeita_curso_ausente():
    cadastro = cadastro_exemplo()
    cadastro.loc[0, "CO_CURSO"] = None
    with pytest.raises(ValueError, match="CO_CURSO ausente"):
        preparar_catalogo_area(cadastro, QUIMICA)
