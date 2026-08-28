from __future__ import annotations

import pandas as pd

from src.geografia.validacao_analitica import (
    recomendacao_validada,
    resumo_contraste_interno,
    validar_comparacoes_regionais,
)


def test_contraste_interno_preserva_duas_ofertas_por_conceito() -> None:
    base = pd.DataFrame(
        {
            "RECORTE_GEOGRAFIA": [
                "UFPA — Conceito 3",
                "UFPA — Conceito 3",
                "UFPA — Conceito 4",
                "UFPA — Conceito 4",
            ],
            "nt_ger_mean": [50.0, 52.0, 60.0, 62.0],
            "nt_obj_mean": [49.0, 51.0, 59.0, 61.0],
            "nt_dis_mean": [5.5, 5.7, 6.0, 6.2],
            "taxa_presenca_microdados": [0.75, 0.80, 0.82, 0.85],
        }
    )
    out = resumo_contraste_interno(base)
    linha = out.loc[out["INDICADOR"].eq("nt_ger_mean")].iloc[0]
    assert linha["N_CONCEITO_3"] == 2
    assert linha["N_CONCEITO_4"] == 2
    assert linha["DIFERENCA_C3_C4"] == -10.0


def test_validar_comparacoes_regionais_cria_iqr() -> None:
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


def test_recomendacao_preserva_itens_separados() -> None:
    base = pd.DataFrame(
        {
            "RECORTE_GEOGRAFIA": [
                "UFPA — Conceito 3",
                "UFPA — Conceito 4",
            ],
            "qe_i68_media": [8.0, 9.0],
            "qe_i69_media": [7.5, 8.5],
            "qe_i70_interesse_pct": [0.8, 0.9],
        }
    )
    out = recomendacao_validada(base)
    assert set(out["INDICADOR"]) == {
        "qe_i68_media",
        "qe_i69_media",
        "qe_i70_interesse_pct",
    }
