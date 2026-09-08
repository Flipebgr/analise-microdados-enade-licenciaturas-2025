from __future__ import annotations

import pandas as pd

from src.educacao_fisica.rotulos_questionario import (
    DIMENSOES_TEORICAS,
    ITENS_INVERTIDOS,
)
from src.educacao_fisica.validacao_analitica import (
    agregar_dimensoes_por_curso,
    catalogo_itens_processo,
)


def test_dimensoes_nao_inventam_estagio():
    assert "estagio" not in DIMENSOES_TEORICAS
    assert ITENS_INVERTIDOS == ()


def test_itens_ead_ficam_fora_das_dimensoes_comuns():
    for item in ("QE_I31", "QE_I32", "QE_I43"):
        assert all(item not in itens for itens in DIMENSOES_TEORICAS.values())
    catalogo = catalogo_itens_processo()
    assert set(catalogo["ITEM"]) == {f"QE_I{i}" for i in range(20, 67)}
    assert set(
        catalogo.loc[catalogo["DIMENSAO"].eq("item_especifico_ead"), "ITEM"]
    ) == {"QE_I31", "QE_I32", "QE_I43"}


def test_agregacao_dimensoes_preserva_uma_linha_por_curso():
    colunas = sorted(
        {item for itens in DIMENSOES_TEORICAS.values() for item in itens}
    )
    dados = pd.DataFrame({"CO_CURSO": [1, 1, 2, 2]})
    for item in colunas:
        dados[item] = [4, 5, 3, 6]

    resultado = agregar_dimensoes_por_curso(dados)
    assert resultado["CO_CURSO"].is_unique
    assert set(resultado["CO_CURSO"]) == {1, 2}
