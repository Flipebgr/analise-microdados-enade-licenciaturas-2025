from __future__ import annotations

import pandas as pd
import pytest

from src.portugues.validacao_analitica import (
    obter_belem_ead,
    recomendacao_grupos,
    validar_comparacoes_regionais,
)


def test_obter_belem_ead_exige_conceito1_ufpa():
    base = pd.DataFrame(
        {
            "CO_CURSO": [115161],
            "CO_IES": [569],
            "CONCEITO_ENADE_NUM": [1],
        }
    )
    assert int(obter_belem_ead(base)["CO_CURSO"]) == 115161


def test_obter_belem_ead_rejeita_conceito_incorreto():
    base = pd.DataFrame(
        {
            "CO_CURSO": [115161],
            "CO_IES": [569],
            "CONCEITO_ENADE_NUM": [3],
        }
    )
    with pytest.raises(ValueError, match="Conceito Enade 1"):
        obter_belem_ead(base)


def test_validar_comparacoes_regionais_cria_iqr():
    recortes = [
        "UFPA agregada",
        "Região Norte sem UFPA",
        "Região Norte completa",
        "Nordeste",
        "Sudeste",
        "Sul",
        "Centro-Oeste",
        "Brasil geral",
        "Brasil sem UFPA",
        "Restante do Brasil sem Norte",
    ]
    df = pd.DataFrame(
        {
            "RECORTE": recortes,
            "N_CURSOS": [1] * len(recortes),
            "N_PARTICIPANTES": [10] * len(recortes),
            "MEDIA_CURSOS": [50.0] * len(recortes),
            "MEDIA_PONDERADA_PARTICIPANTES": [50.0] * len(recortes),
            "MEDIANA_CURSOS": [50.0] * len(recortes),
            "DP_CURSOS": [1.0] * len(recortes),
            "P25": [49.0] * len(recortes),
            "P75": [51.0] * len(recortes),
        }
    )
    out = validar_comparacoes_regionais(df)
    assert (out["AMPLITUDE_IQR"] == 2.0).all()


def test_recomendacao_grupos_preserva_itens_separados():
    base = pd.DataFrame(
        {
            "GRUPO_CODIGO": ["A", "B"],
            "qe_i68_media": [8.0, 9.0],
            "qe_i69_media": [7.5, 8.5],
            "qe_i70_interesse_pct": [0.8, 0.9],
        }
    )
    out = recomendacao_grupos(base)
    assert set(out["INDICADOR"]) == {
        "qe_i68_media",
        "qe_i69_media",
        "qe_i70_interesse_pct",
    }
