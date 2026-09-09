from __future__ import annotations

import pandas as pd

import executar
from src.core.configuracao_area import MUSICA, obter_area
from src.musica.analise_musica import construir_benchmark_comparavel
from src.musica.preparar_catalogo import aplicar_recorte_musica


def _base_sintetica() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [114950, 9001, 9002, 9003],
            "CO_IES": [569, 100, 101, 102],
            "CO_GRUPO": [4301] * 4,
            "CO_UF_CURSO": [15, 13, 35, 16],
            "CO_REGIAO_CURSO": [1, 1, 3, 1],
            "CO_MODALIDADE": [1] * 4,
            "CO_CATEGAD": [1] * 4,
            "CO_ORGACAD": [10028] * 4,
            "MUNICIPIO": ["Belém", "Manaus", "São Paulo", "Macapá"],
            "ROTULO_OFERTA": [
                "Belém — Presencial",
                "Manaus — Presencial",
                "São Paulo — Presencial",
                "Macapá — Presencial",
            ],
            "CONCEITO_ENADE_NUM": [1, 1, 3, 2],
            "PARTICIPANTES_NUM": [37, 30, 35, 28],
            "nt_ger_mean": [41.6, 45.0, 60.0, 52.0],
            "nt_obj_mean": [39.3, 43.0, 59.0, 50.0],
            "nt_dis_mean": [5.11, 5.2, 6.2, 5.8],
        }
    )


def test_configuracao_musica_registrada() -> None:
    assert MUSICA.co_grupo == 4301
    assert obter_area("musica") is MUSICA


def test_recorte_territorial_musica() -> None:
    resultado = aplicar_recorte_musica(_base_sintetica())
    assert resultado["RECORTE_MUSICA"].tolist() == [
        "UFPA — Belém",
        "Norte sem Pará",
        "Brasil sem Norte",
        "Norte sem Pará",
    ]


def test_benchmark_exclui_ufpa() -> None:
    base = aplicar_recorte_musica(_base_sintetica())
    benchmark, resumo = construir_benchmark_comparavel(base)
    assert not benchmark["CO_IES"].eq(569).any()
    assert resumo["CO_CURSO_ALVO"].tolist() == [114950]
    assert resumo["N_CURSOS_COMPARAVEIS"].iloc[0] > 0


def test_executor_registra_musica() -> None:
    assert executar.etapas_disponiveis("música") == ["base", "validacao", "relatorio"]
