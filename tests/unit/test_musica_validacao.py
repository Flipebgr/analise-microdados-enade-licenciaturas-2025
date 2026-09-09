from __future__ import annotations

import numpy as np
import pandas as pd

from src.musica.rotulos_questionario import (
    DIMENSOES_TEORICAS,
    ITENS_INVERTIDOS,
)
from src.musica.validacao_analitica import (
    associacoes_ecologicas,
    catalogo_itens_processo,
    cronbach_alpha,
)


def test_catalogo_processo_tem_47_itens() -> None:
    catalogo = catalogo_itens_processo()
    assert catalogo["ITEM"].nunique() == 47
    assert set(catalogo["ITEM"]) == {
        f"QE_I{i:02d}" for i in range(20, 67)
    }
    assert len(DIMENSOES_TEORICAS) == 8
    assert ITENS_INVERTIDOS == ()


def test_cronbach_alpha_consistente() -> None:
    x = pd.DataFrame(
        {
            "a": np.arange(1, 21),
            "b": np.arange(1, 21) * 2,
            "c": np.arange(1, 21) * 3,
        }
    )
    assert cronbach_alpha(x) > 0.9


def test_associacoes_retornam_diagnostico_outliers() -> None:
    n = 20
    base = pd.DataFrame(
        {
            "CO_CURSO": range(n),
            "PARTICIPANTES_NUM": [30] * n,
            "renda_ate_3sm_pct": np.linspace(0.1, 0.8, n),
            "trabalha_pct": np.linspace(0.2, 0.9, n),
            "auxilio_permanencia_pct": np.linspace(0.01, 0.3, n),
            "qe_i68_media": np.linspace(5, 9, n),
            "qe_i69_media": np.linspace(5.5, 9.5, n),
            "dim_atuacao_docente_media": np.linspace(3, 5.8, n),
            "dim_infraestrutura_recursos_media": np.linspace(3, 5.5, n),
            "dim_organizacao_integracao_media": np.linspace(3.2, 5.7, n),
            "nt_ger_mean": np.linspace(40, 70, n),
        }
    )
    associacoes, diagnostico = associacoes_ecologicas(base)
    assert len(associacoes) == 8
    assert len(diagnostico) == 8
    assert "N_OUTLIERS_QUALQUER" in diagnostico.columns
