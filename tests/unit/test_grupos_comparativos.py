from __future__ import annotations

import pandas as pd

from src.analise.definir_grupos import aplicar_grupos


def test_grupos_comparativos_sao_exclusivos():
    cursos = pd.DataFrame(
        {
            "CO_CURSO": [1, 2, 3, 4, 5, 6],
            "CO_IES": [569, 569, 999, 998, 997, 569],
            "UF": ["PA", "PA", "PA", "AM", "SP", "PA"],
            "CO_UF_CURSO": [15, 15, 15, 13, 35, 15],
            "CO_REGIAO_CURSO": [1, 1, 1, 1, 3, 1],
            "CONCEITO_ENADE": [1, 3, 1, 1, 1, pd.NA],
        }
    )

    resultado = aplicar_grupos(cursos)

    assert resultado["CO_CURSO"].is_unique
    assert resultado["GRUPO_CODIGO"].tolist() == ["A", "B", "C", "D", "E", "SEM_GRUPO"]
    assert resultado.loc[resultado["CO_CURSO"].eq(6), "GRUPO_CODIGO"].item() == "SEM_GRUPO"
