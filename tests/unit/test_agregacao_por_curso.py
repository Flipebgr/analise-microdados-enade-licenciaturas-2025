from __future__ import annotations

import pandas as pd
import pytest

from src.agregacao.comum import resumo_numerico, validar_unicidade


def test_resumo_numerico_produz_uma_linha_por_curso():
    individual = pd.DataFrame(
        {
            "CO_CURSO": [1, 1, 1, 2, 2],
            "NT_GER": [40, 50, pd.NA, 60, 70],
        }
    )

    agregado = resumo_numerico(individual, ["NT_GER"])

    assert agregado["CO_CURSO"].is_unique
    assert agregado.set_index("CO_CURSO").loc[1, "nt_ger_count"] == 2
    assert agregado.set_index("CO_CURSO").loc[1, "nt_ger_mean"] == 45
    assert agregado.set_index("CO_CURSO").loc[2, "nt_ger_mean"] == 65


def test_validar_unicidade_rejeita_tabela_nao_agregada():
    duplicada = pd.DataFrame({"CO_CURSO": [1, 1], "valor": [10, 20]})

    with pytest.raises(ValueError, match="uma linha por CO_CURSO"):
        validar_unicidade(duplicada, "tabela sintética")
