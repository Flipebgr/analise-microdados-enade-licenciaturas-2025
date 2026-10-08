from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.analise.associacoes_ecologicas import correlacao_spearman_ecologica
from src.analise.contratos_fase_9a import ConfiguracaoBootstrap


def _base(n: int = 30) -> pd.DataFrame:
    x = np.arange(n, dtype=float)
    y = x**2 + (x % 3)
    return pd.DataFrame({"CO_CURSO": [str(i) for i in range(n)], "x": x, "y": y})


def test_spearman_ecologico_com_pares_completos_e_sensibilidade():
    base = _base()
    base.loc[0, "y"] = np.nan

    resultado, sensibilidade = correlacao_spearman_ecologica(
        base,
        "x",
        "y",
        identificador="2017:biologia:x:y",
        configuracao=ConfiguracaoBootstrap(numero_reamostragens=250),
    )

    assert resultado["unidade_analise"] == "CO_CURSO"
    assert resultado["metodo"] == "spearman_nao_ponderado"
    assert resultado["n_pares_completos"] == 29
    assert resultado["rho"] is not None
    assert resultado["tipo_incerteza"] == "bootstrap ecologico de pares de cursos"
    assert sensibilidade.loc[0, "cenario"] == "sem_outliers_sinalizados"


def test_spearman_ecologico_nao_calcula_com_n_insuficiente():
    resultado, sensibilidade = correlacao_spearman_ecologica(
        _base(19), "x", "y", identificador="n-insuficiente"
    )

    assert resultado["rho"] is None
    assert resultado["motivo"] == "n_cursos_abaixo_do_minimo_20"
    assert sensibilidade.loc[0, "status"] == "insuficiente"


def test_spearman_ecologico_rejeita_curso_duplicado():
    base = pd.concat([_base(), _base().iloc[[0]]], ignore_index=True)

    with pytest.raises(ValueError, match="no máximo uma linha por CO_CURSO"):
        correlacao_spearman_ecologica(base, "x", "y", identificador="duplicado")
