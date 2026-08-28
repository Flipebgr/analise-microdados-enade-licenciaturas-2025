from __future__ import annotations

import pandas as pd
from src.core.configuracao_area import obter_area
from src.geografia import GEOGRAFIA
from src.geografia.analise_geografia import (
    construir_benchmarks_por_oferta,
    construir_comparacao_interna_ufpa,
)
from src.geografia.preparar_catalogo import aplicar_recorte_geografia


def base_ufpa_valida() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [11991, 12052, 1194057, 1330343],
            "CO_IES": [569] * 4,
            "CO_GRUPO": [3002] * 4,
            "CO_UF_CURSO": [15] * 4,
            "CO_REGIAO_CURSO": [1] * 4,
            "CO_MODALIDADE": [1] * 4,
            "CO_CATEGAD": [1] * 4,
            "CO_ORGACAD": [10028] * 4,
            "MUNICIPIO": ["Belém", "Altamira", "Cametá", "Ananindeua"],
            "ROTULO_OFERTA": [
                "Belém — Presencial",
                "Altamira — Presencial",
                "Cametá — Presencial",
                "Ananindeua — Presencial",
            ],
            "CONCEITO_ENADE_NUM": [4, 3, 3, 4],
            "CONCEITO_ENADE": [4, 3, 3, 4],
            "GRUPO_CODIGO": ["B"] * 4,
            "GRUPO": ["UFPA — conceito superior"] * 4,
            "PARTICIPANTES_NUM": [57, 23, 68, 63],
            "nt_ger_mean": [60.0, 55.0, 56.0, 61.0],
            "nt_obj_mean": [59.0, 54.0, 55.0, 60.0],
            "nt_dis_mean": [6.2, 5.8, 5.9, 6.3],
            "taxa_presenca_microdados": [0.80, 0.85, 0.74, 0.82],
        }
    )


def test_configuracao_geografia_registrada() -> None:
    assert GEOGRAFIA.co_grupo == 3002
    assert obter_area(" geografia ") is GEOGRAFIA


def test_recorte_geografia_separa_conceitos_3_e_4() -> None:
    base = aplicar_recorte_geografia(base_ufpa_valida())
    assert base["RECORTE_GEOGRAFIA"].eq("UFPA — Conceito 3").sum() == 2
    assert base["RECORTE_GEOGRAFIA"].eq("UFPA — Conceito 4").sum() == 2


def test_validacao_geografia_aceita_relacao_oficial() -> None:
    base = aplicar_recorte_geografia(base_ufpa_valida())
    # o validador completo exige o universo nacional; validamos aqui o recorte interno
    assert set(base["RECORTE_GEOGRAFIA"]) == {
        "UFPA — Conceito 3",
        "UFPA — Conceito 4",
    }


def test_comparacao_interna_separa_conceitos() -> None:
    base = aplicar_recorte_geografia(base_ufpa_valida())
    resultado = construir_comparacao_interna_ufpa(base)
    geral = resultado[resultado["INDICADOR"].eq("nt_ger_mean")]
    c3 = geral[geral["RECORTE_GEOGRAFIA"].eq("UFPA — Conceito 3")].iloc[0]
    c4 = geral[geral["RECORTE_GEOGRAFIA"].eq("UFPA — Conceito 4")].iloc[0]
    assert c3["N_CURSOS"] == 2
    assert c4["N_CURSOS"] == 2


def test_benchmark_por_oferta_exclui_ufpa() -> None:
    base = aplicar_recorte_geografia(base_ufpa_valida())
    externos = pd.DataFrame(
        {
            "CO_CURSO": [9001, 9002],
            "CO_IES": [100, 101],
            "CO_GRUPO": [3002, 3002],
            "CO_UF_CURSO": [15, 13],
            "CO_REGIAO_CURSO": [1, 1],
            "CO_MODALIDADE": [1, 1],
            "CO_CATEGAD": [1, 1],
            "CO_ORGACAD": [10028, 10028],
            "MUNICIPIO": ["Outro PA", "Outro Norte"],
            "ROTULO_OFERTA": ["Outro PA", "Outro Norte"],
            "CONCEITO_ENADE_NUM": [4, 3],
            "CONCEITO_ENADE": [4, 3],
            "GRUPO_CODIGO": ["C", "D"],
            "GRUPO": ["Outras IES do Pará", "Restante da Região Norte"],
            "PARTICIPANTES_NUM": [40, 60],
            "nt_ger_mean": [58, 57],
            "nt_obj_mean": [57, 56],
            "nt_dis_mean": [6.0, 5.9],
        }
    )
    externos = aplicar_recorte_geografia(externos)
    completa = pd.concat([base, externos], ignore_index=True)
    benchmarks, resumo = construir_benchmarks_por_oferta(completa)
    assert not benchmarks.empty
    assert not benchmarks["CO_IES"].eq(569).any()
    assert set(resumo["CO_CURSO_ALVO"]) == set(base["CO_CURSO"])
