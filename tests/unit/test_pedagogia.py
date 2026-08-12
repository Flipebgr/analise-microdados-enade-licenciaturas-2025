from __future__ import annotations

import pandas as pd
import pytest

from src.core.configuracao_area import obter_area
from src.pedagogia import CO_CURSO_CASTANHAL, PEDAGOGIA
from src.pedagogia.analise_pedagogia import (
    construir_benchmarks_por_oferta,
    construir_comparacao_interna_ufpa,
)
from src.pedagogia.preparar_catalogo import aplicar_recorte_pedagogia
from src.pedagogia.validar_pedagogia import validar_base_pedagogia


def base_ufpa_valida() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [11996, 12048, 12061, 12069, 12085, 12111, 38276],
            "CO_IES": [569] * 7,
            "CO_GRUPO": [2001] * 7,
            "CO_UF_CURSO": [15] * 7,
            "CO_REGIAO_CURSO": [1] * 7,
            "CO_MODALIDADE": [1] * 7,
            "CO_CATEGAD": [1] * 7,
            "CO_ORGACAD": [10028] * 7,
            "MUNICIPIO": [
                "Belém",
                "Altamira",
                "Bragança",
                "Cametá",
                "Castanhal",
                "Breves",
                "Abaetetuba",
            ],
            "ROTULO_OFERTA": [
                "Belém — Presencial",
                "Altamira — Presencial",
                "Bragança — Presencial",
                "Cametá — Presencial",
                "Castanhal — Presencial",
                "Breves — Presencial",
                "Abaetetuba — Presencial",
            ],
            "CONCEITO_ENADE_NUM": [4, 4, 4, 4, 5, 4, 4],
            "CONCEITO_ENADE": [4, 4, 4, 4, 5, 4, 4],
            "GRUPO_CODIGO": ["B"] * 7,
            "GRUPO": ["UFPA — conceito superior"] * 7,
            "PARTICIPANTES_NUM": [280, 51, 75, 122, 63, 42, 111],
            "nt_ger_mean": [60, 57, 58, 59, 64, 56, 58],
            "nt_obj_mean": [59, 56, 57, 58, 63, 55, 57],
            "nt_dis_mean": [6.2, 6.0, 6.1, 6.1, 6.5, 5.9, 6.0],
            "taxa_presenca_microdados": [0.82, 0.91, 0.90, 0.83, 0.73, 0.82, 0.89],
        }
    )


def test_configuracao_pedagogia_registrada() -> None:
    assert PEDAGOGIA.co_grupo == 2001
    assert obter_area(" pedagogia ") is PEDAGOGIA


def test_recorte_pedagogia_separa_conceitos_4_e_5() -> None:
    base = aplicar_recorte_pedagogia(base_ufpa_valida())
    castanhal = base[base["CO_CURSO"].eq(CO_CURSO_CASTANHAL)].iloc[0]
    assert castanhal["RECORTE_PEDAGOGIA"] == "UFPA — Conceito 5"
    assert bool(castanhal["REFERENCIA_INTERNA_CASTANHAL"])
    assert base["RECORTE_PEDAGOGIA"].eq("UFPA — Conceito 4").sum() == 6


def test_validacao_pedagogia_aceita_relacao_oficial() -> None:
    validar_base_pedagogia(aplicar_recorte_pedagogia(base_ufpa_valida()))


def test_validacao_pedagogia_rejeita_conceito_1() -> None:
    base = aplicar_recorte_pedagogia(base_ufpa_valida())
    base.loc[base["CO_CURSO"].eq(11996), "CONCEITO_ENADE_NUM"] = 1
    base.loc[base["CO_CURSO"].eq(11996), "GRUPO_CODIGO"] = "A"
    with pytest.raises((ValueError, AssertionError)):
        validar_base_pedagogia(base)


def test_comparacao_interna_mantem_castanhal_separada() -> None:
    base = aplicar_recorte_pedagogia(base_ufpa_valida())
    resultado = construir_comparacao_interna_ufpa(base)
    geral = resultado[resultado["INDICADOR"].eq("nt_ger_mean")]
    c5 = geral[geral["RECORTE_PEDAGOGIA"].eq("UFPA — Conceito 5")].iloc[0]
    c4 = geral[geral["RECORTE_PEDAGOGIA"].eq("UFPA — Conceito 4")].iloc[0]
    assert c5["N_CURSOS"] == 1
    assert c5["MEDIA_CURSOS"] == pytest.approx(64.0)
    assert c4["N_CURSOS"] == 6


def test_benchmark_por_oferta_exclui_ufpa() -> None:
    base = aplicar_recorte_pedagogia(base_ufpa_valida())
    externos = pd.DataFrame(
        {
            "CO_CURSO": [9001, 9002],
            "CO_IES": [100, 101],
            "CO_GRUPO": [2001, 2001],
            "CO_UF_CURSO": [15, 13],
            "CO_REGIAO_CURSO": [1, 1],
            "CO_MODALIDADE": [1, 1],
            "CO_CATEGAD": [1, 1],
            "CO_ORGACAD": [10028, 10028],
            "MUNICIPIO": ["Outro PA", "Outro Norte"],
            "ROTULO_OFERTA": ["Outro PA", "Outro Norte"],
            "CONCEITO_ENADE_NUM": [4, 4],
            "CONCEITO_ENADE": [4, 4],
            "GRUPO_CODIGO": ["C", "D"],
            "GRUPO": ["Outras IES do Pará", "Restante da Região Norte"],
            "PARTICIPANTES_NUM": [70, 100],
            "nt_ger_mean": [60, 61],
            "nt_obj_mean": [59, 60],
            "nt_dis_mean": [6.1, 6.2],
        }
    )
    externos = aplicar_recorte_pedagogia(externos)
    completa = pd.concat([base, externos], ignore_index=True)
    benchmarks, resumo = construir_benchmarks_por_oferta(completa)
    assert not benchmarks.empty
    assert not benchmarks["CO_IES"].eq(569).any()
    assert set(resumo["CO_CURSO_ALVO"]) == set(base["CO_CURSO"])
