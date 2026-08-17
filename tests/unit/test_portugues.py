from __future__ import annotations

import pandas as pd

from src.portugues import CO_CURSO_BELEM_EAD, PORTUGUES
from src.portugues.analise_portugues import construir_contraste_ufpa
from src.portugues.validar_portugues import (
    CURSOS_UFPA_ESPERADOS,
    validar_auditoria_relacao,
)


def test_configuracao_portugues():
    assert PORTUGUES.co_grupo == 904
    assert PORTUGUES.co_ies_focal == 569
    assert CO_CURSO_BELEM_EAD == 115161


def test_relacao_oficial_localizada_tem_oito_ofertas():
    assert len(CURSOS_UFPA_ESPERADOS) == 8
    assert CURSOS_UFPA_ESPERADOS[115161] == ("Belém", "EaD", 1)


def test_auditoria_soure_nao_inventa_curso():
    linhas = []
    municipios = [
        "Belém",
        "Belém",
        "Abaetetuba",
        "Altamira",
        "Bragança",
        "Breves",
        "Cametá",
        "Castanhal",
        "Soure",
    ]
    for i, municipio in enumerate(municipios):
        linhas.append(
            {
                "MUNICIPIO_INFORMADO": municipio,
                "STATUS_VALIDACAO": (
                    "Não localizado nas fontes" if municipio == "Soure" else "Validado"
                ),
                "CO_CURSO": pd.NA if municipio == "Soure" else 1000 + i,
            }
        )
    validar_auditoria_relacao(pd.DataFrame(linhas))


def test_contraste_ufpa_preserva_grupo_a_e_b():
    base = pd.DataFrame(
        {
            "CO_IES": [569, 569, 569],
            "GRUPO_CODIGO": ["A", "B", "B"],
            "GRUPO": [
                "UFPA — Conceito 1",
                "UFPA — conceito superior",
                "UFPA — conceito superior",
            ],
            "nt_ger_mean": [40.0, 50.0, 60.0],
            "nt_obj_mean": [39.0, 49.0, 59.0],
            "nt_dis_mean": [5.0, 6.0, 7.0],
            "taxa_presenca_microdados": [0.8, 0.9, 0.85],
            "renda_ate_3sm_pct": [0.7, 0.6, 0.5],
            "trabalha_pct": [0.4, 0.5, 0.6],
            "acao_afirmativa_pct": [0.3, 0.4, 0.5],
            "auxilio_permanencia_pct": [0.2, 0.3, 0.4],
            "qe_i68_media": [8.0, 8.5, 9.0],
            "qe_i69_media": [8.0, 8.5, 9.0],
        }
    )
    resultado = construir_contraste_ufpa(base)
    linha = resultado[resultado["INDICADOR"].eq("nt_ger_mean")].iloc[0]
    assert linha["N_CURSOS_A"] == 1
    assert linha["N_CURSOS_B"] == 2
    assert linha["DIFERENCA_A_MENOS_B"] == -15.0
