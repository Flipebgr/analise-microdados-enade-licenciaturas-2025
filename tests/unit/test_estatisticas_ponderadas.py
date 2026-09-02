from __future__ import annotations

import numpy as np
import pandas as pd

from src.analise.analise_sensibilidade import sensibilidade_desempenho


def _base(valores: list[float], pesos: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": range(1, len(valores) + 1),
            "GRUPO_CODIGO": ["A"] * len(valores),
            "nt_ger_mean": valores,
            "nt_ger_count": pesos,
            "CO_MODALIDADE": [1] * len(valores),
            "CO_CATEGAD": [1] * len(valores),
        }
    )


def test_media_ponderada_difere_da_media_simples_quando_pesos_diferem():
    resultado = sensibilidade_desempenho(_base([40.0, 60.0], [1, 3]))
    todos = resultado.query("cenario == 'todos' and grupo == 'A'").iloc[0]

    assert todos["media_cursos"] == 50.0
    assert todos["media_ponderada_participantes"] == 55.0


def test_peso_zero_e_valor_ausente_nao_entram_na_media_ponderada():
    resultado = sensibilidade_desempenho(_base([40.0, 60.0, np.nan], [0, 2, 5]))
    todos = resultado.query("cenario == 'todos' and grupo == 'A'").iloc[0]

    assert todos["media_ponderada_participantes"] == 60.0
