from __future__ import annotations

import pandas as pd
import pytest

from src.biologia import BIOLOGIA, CO_CURSO_SOURE
from src.biologia.analise_soure import construir_benchmark_soure, construir_comparacao_focal
from src.biologia.preparar_catalogo import aplicar_recorte_focal
from src.biologia.validar_biologia import validar_base_biologia
from src.core.configuracao_area import obter_area


def base_ufpa_valida() -> pd.DataFrame:
    return pd.DataFrame({
        "CO_CURSO": [12023, 18487, 18491, CO_CURSO_SOURE, 1148030],
        "CO_IES": [569] * 5,
        "CO_GRUPO": [1602] * 5,
        "CO_UF_CURSO": [15] * 5,
        "CO_REGIAO_CURSO": [1] * 5,
        "CO_MODALIDADE": [1, 1, 1, 1, 0],
        "CO_CATEGAD": [1] * 5,
        "CO_ORGACAD": [1] * 5,
        "MUNICIPIO": ["Belém", "Bragança", "Altamira", "Soure", "Belém"],
        "ROTULO_OFERTA": [
            "Belém — Presencial",
            "Bragança — Presencial",
            "Altamira — Presencial",
            "Soure — Presencial",
            "Belém — EaD",
        ],
        "CONCEITO_ENADE_NUM": [4, 4, 4, 3, 3],
        "CONCEITO_ENADE": [4, 4, 4, 3, 3],
        "GRUPO_CODIGO": ["B"] * 5,
        "GRUPO": ["UFPA — conceito superior"] * 5,
        "PARTICIPANTES_NUM": [94, 36, 39, 49, 101],
        "nt_ger_mean": [55, 53, 54, 51, 52],
        "nt_obj_mean": [54, 52, 53, 50, 51],
        "nt_dis_mean": [57, 55, 56, 53, 54],
    })


def test_configuracao_biologia_registrada() -> None:
    assert BIOLOGIA.co_grupo == 1602
    assert obter_area(" BIOLOGIA ") is BIOLOGIA


def test_recorte_focal_identifica_soure() -> None:
    base = aplicar_recorte_focal(base_ufpa_valida())
    soure = base[base["CO_CURSO"].eq(CO_CURSO_SOURE)].iloc[0]
    assert soure["RECORTE_FOCAL"] == "Soure"
    assert bool(soure["FOCO_SOURE"])
    assert base["RECORTE_FOCAL"].eq("Soure").sum() == 1


def test_validacao_biologia_aceita_relacao_ufpa() -> None:
    validar_base_biologia(aplicar_recorte_focal(base_ufpa_valida()))


def test_validacao_biologia_rejeita_conceito_1_ufpa() -> None:
    base = aplicar_recorte_focal(base_ufpa_valida())
    base.loc[base["CO_CURSO"].eq(CO_CURSO_SOURE), "CONCEITO_ENADE_NUM"] = 1
    base.loc[base["CO_CURSO"].eq(CO_CURSO_SOURE), "GRUPO_CODIGO"] = "A"
    with pytest.raises((ValueError, AssertionError)):
        validar_base_biologia(base)


def test_comparacao_focal_mantem_soure_separada() -> None:
    base = aplicar_recorte_focal(base_ufpa_valida())
    resultado = construir_comparacao_focal(base, indicadores=["nt_ger_mean"])
    soure = resultado[resultado["RECORTE_FOCAL"].eq("Soure")].iloc[0]
    assert soure["N_CURSOS"] == 1
    assert soure["MEDIA_CURSOS"] == pytest.approx(51.0)


def test_benchmark_soure_exclui_ufpa() -> None:
    base = aplicar_recorte_focal(base_ufpa_valida())
    externos = pd.DataFrame({
        "CO_CURSO": [9001, 9002],
        "CO_IES": [100, 101],
        "CO_GRUPO": [1602, 1602],
        "CO_UF_CURSO": [15, 13],
        "CO_REGIAO_CURSO": [1, 1],
        "CO_MODALIDADE": [1, 1],
        "CO_CATEGAD": [1, 1],
        "CO_ORGACAD": [1, 1],
        "MUNICIPIO": ["Outro PA", "Outro Norte"],
        "ROTULO_OFERTA": ["Outro PA", "Outro Norte"],
        "CONCEITO_ENADE_NUM": [3, 4],
        "CONCEITO_ENADE": [3, 4],
        "GRUPO_CODIGO": ["C", "D"],
        "GRUPO": ["Outras IES do Pará", "Restante da Região Norte"],
        "PARTICIPANTES_NUM": [45, 60],
        "nt_ger_mean": [50, 52],
        "nt_obj_mean": [49, 51],
        "nt_dis_mean": [52, 54],
    })
    externos = aplicar_recorte_focal(externos)
    completa = pd.concat([base, externos], ignore_index=True)
    benchmark, resumo = construir_benchmark_soure(completa)
    assert not benchmark.empty
    assert not benchmark["CO_IES"].eq(569).any()
    assert resumo.iloc[0]["n_cursos_comparaveis"] == 2
