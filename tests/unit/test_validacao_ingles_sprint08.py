from __future__ import annotations

import pandas as pd
import pytest

from src.ingles.validacao_analitica import (
    associacoes_ecologicas,
    diagnosticar_outliers,
    validar_comparacoes_regionais,
)


def test_validacao_regional_rejeita_recorte_ausente() -> None:
    df = pd.DataFrame({
        "RECORTE": ["Brasil geral"],
        "INDICADOR": ["nt_ger_mean"],
        "N_CURSOS": [10],
        "N_PARTICIPANTES": [100],
        "MEDIA_CURSOS": [50.0],
        "MEDIA_PONDERADA_PARTICIPANTES": [51.0],
        "MEDIANA_CURSOS": [49.0],
        "DP_CURSOS": [5.0],
        "P25": [47.0],
        "P75": [53.0],
    })
    with pytest.raises(ValueError, match="Recortes regionais ausentes"):
        validar_comparacoes_regionais(df)


def test_outlier_iqr_apenas_sinaliza_extremo() -> None:
    base = pd.DataFrame({
        "CO_CURSO": [1, 2, 3, 4, 5],
        "ROTULO_OFERTA": ["a", "b", "c", "d", "e"],
        "GRUPO_CODIGO": ["A", "B", "C", "D", "E"],
        "nt_ger_mean": [30.0, 31.0, 32.0, 33.0, 90.0],
    })
    out = diagnosticar_outliers(base)
    assert out["OUTLIER_IQR"].sum() == 1
    assert out.loc[out["OUTLIER_IQR"], "CO_CURSO"].iloc[0] == 5


def test_associacao_ecologica_informa_nivel_de_analise() -> None:
    base = pd.DataFrame({
        "nt_ger_mean": [30.0, 40.0, 50.0, 60.0],
        "renda_ate_3sm_pct": [0.9, 0.7, 0.5, 0.3],
    })
    resultado = associacoes_ecologicas(base)
    linha = resultado[resultado["INDICADOR_X"].eq("renda_ate_3sm_pct")].iloc[0]
    assert linha["N_CURSOS"] == 4
    assert linha["NIVEL_ANALISE"] == "curso (ecológico)"
    assert linha["SPEARMAN_RHO"] == pytest.approx(-1.0)
