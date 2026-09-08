from __future__ import annotations

import pandas as pd

import executar
from src.core.configuracao_area import EDUCACAO_FISICA, obter_area
from src.educacao_fisica.analise_educacao_fisica import (
    construir_benchmarks_por_oferta,
)
from src.educacao_fisica.preparar_catalogo import (
    aplicar_recorte_educacao_fisica,
)


def _base_sintetica() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [21849, 104598, 9001, 9002, 9003],
            "CO_IES": [569, 569, 100, 101, 102],
            "CO_GRUPO": [3502] * 5,
            "CO_UF_CURSO": [15, 15, 15, 13, 35],
            "CO_REGIAO_CURSO": [1, 1, 1, 1, 3],
            "CO_MODALIDADE": [1] * 5,
            "CO_CATEGAD": [1] * 5,
            "CO_ORGACAD": [10028] * 5,
            "MUNICIPIO": [
                "Castanhal",
                "Belém",
                "Outro PA",
                "Outro Norte",
                "Outro Brasil",
            ],
            "ROTULO_OFERTA": [
                "Castanhal — Presencial",
                "Belém — Presencial",
                "Outro PA — Presencial",
                "Outro Norte — Presencial",
                "Outro Brasil — Presencial",
            ],
            "CONCEITO_ENADE_NUM": [4, 4, 3, 4, 4],
            "PARTICIPANTES_NUM": [124, 72, 100, 80, 65],
            "nt_ger_mean": [58.4, 61.1, 55.0, 57.0, 60.0],
            "nt_obj_mean": [58.1, 61.7, 55.2, 57.1, 60.1],
            "nt_dis_mean": [5.98, 5.89, 5.5, 5.6, 5.8],
        }
    )


def test_configuracao_educacao_fisica_registrada() -> None:
    assert EDUCACAO_FISICA.co_grupo == 3502
    assert obter_area("educacao_fisica") is EDUCACAO_FISICA


def test_recorte_separa_campi_ufpa_e_territorios() -> None:
    resultado = aplicar_recorte_educacao_fisica(_base_sintetica())
    assert resultado["RECORTE_EDUCACAO_FISICA"].tolist() == [
        "UFPA — Castanhal",
        "UFPA — Belém",
        "Outras IES do Pará",
        "Norte sem Pará",
        "Brasil sem Norte",
    ]


def test_benchmark_inclui_todas_as_ofertas_ufpa_e_exclui_ufpa() -> None:
    base = aplicar_recorte_educacao_fisica(_base_sintetica())
    benchmarks, resumo = construir_benchmarks_por_oferta(base)

    assert set(resumo["CO_CURSO_ALVO"]) == {21849, 104598}
    assert not benchmarks["CO_IES"].eq(569).any()
    assert resumo["N_CURSOS_COMPARAVEIS"].gt(0).all()



def test_executor_registra_educacao_fisica() -> None:
    assert executar.etapas_disponiveis("educação-física") == ["base", "validacao"]
