from __future__ import annotations

import pandas as pd
import pytest

from src.pedagogia import CO_CURSO_CASTANHAL
from src.pedagogia.validacao_analitica import (
    comparar_itens_processo_castanhal,
    resumo_contraste_interno,
    sensibilidade_benchmarks_pedagogia,
)


def _base() -> pd.DataFrame:
    ufpa = pd.DataFrame(
        {
            "CO_CURSO": [11996, 12048, 12061, 12069, 12085, 12111, 38276],
            "CO_IES": [569] * 7,
            "CO_MODALIDADE": [1] * 7,
            "CO_CATEGAD": [1] * 7,
            "CO_ORGACAD": [10028] * 7,
            "ROTULO_OFERTA": ["Belém", "Altamira", "Bragança", "Cametá", "Castanhal", "Breves", "Abaetetuba"],
            "CONCEITO_ENADE_NUM": [4, 4, 4, 4, 5, 4, 4],
            "PARTICIPANTES_NUM": [280, 51, 75, 122, 63, 42, 111],
            "RECORTE_PEDAGOGIA": ["UFPA — Conceito 4"] * 4 + ["UFPA — Conceito 5"] + ["UFPA — Conceito 4"] * 2,
            "nt_ger_mean": [60, 57, 58, 59, 64, 56, 58],
            "nt_obj_mean": [59, 56, 57, 58, 63, 55, 57],
            "nt_dis_mean": [6.2, 6.0, 6.1, 6.1, 6.5, 5.9, 6.0],
            "taxa_presenca_microdados": [0.82, 0.91, 0.90, 0.83, 0.73, 0.82, 0.89],
            "renda_ate_3sm_pct": [0.8, 0.85, 0.82, 0.81, 0.79, 0.88, 0.84],
            "trabalha_pct": [0.5, 0.4, 0.45, 0.48, 0.42, 0.39, 0.44],
            "acao_afirmativa_pct": [0.4] * 7,
            "auxilio_permanencia_pct": [0.2] * 7,
            "bolsa_academica_pct": [0.2] * 7,
            "estudo_4h_ou_mais_pct": [0.3] * 7,
            "qe_i68_media": [8.0] * 7,
            "qe_i69_media": [8.2] * 7,
        }
    )
    externos = pd.DataFrame(
        {
            "CO_CURSO": [9001, 9002, 9003],
            "CO_IES": [100, 101, 102],
            "CO_MODALIDADE": [1, 1, 1],
            "CO_CATEGAD": [1, 1, 1],
            "CO_ORGACAD": [10028, 10028, 10028],
            "ROTULO_OFERTA": ["Externo 1", "Externo 2", "Externo 3"],
            "CONCEITO_ENADE_NUM": [4, 4, 5],
            "PARTICIPANTES_NUM": [60, 80, 120],
            "RECORTE_PEDAGOGIA": ["Outras IES do Pará"] * 3,
            "nt_ger_mean": [61, 62, 60],
            "nt_obj_mean": [60, 61, 59],
            "nt_dis_mean": [6.2, 6.3, 6.1],
            "taxa_presenca_microdados": [0.85, 0.86, 0.84],
            "renda_ate_3sm_pct": [0.75, 0.77, 0.76],
            "trabalha_pct": [0.5, 0.52, 0.51],
            "acao_afirmativa_pct": [0.35] * 3,
            "auxilio_permanencia_pct": [0.15] * 3,
            "bolsa_academica_pct": [0.18] * 3,
            "estudo_4h_ou_mais_pct": [0.28] * 3,
            "qe_i68_media": [8.1] * 3,
            "qe_i69_media": [8.3] * 3,
        }
    )
    return pd.concat([ufpa, externos], ignore_index=True)


def test_sensibilidade_tem_cinco_cenarios_por_oferta() -> None:
    resumo, _ = sensibilidade_benchmarks_pedagogia(_base())
    assert len(resumo) == 35
    assert resumo["CO_CURSO_ALVO"].nunique() == 7
    assert resumo["CENARIO"].nunique() == 5


def test_benchmarks_excluem_ufpa() -> None:
    _, membros = sensibilidade_benchmarks_pedagogia(_base())
    assert not membros.empty
    assert not membros["CO_IES"].eq(569).any()


def test_contraste_interno_preserva_castanhal() -> None:
    resultado = resumo_contraste_interno(_base())
    nt_ger = resultado.loc[resultado["INDICADOR"].eq("nt_ger_mean")].iloc[0]
    assert nt_ger["CASTANHAL"] == pytest.approx(64.0)
    assert nt_ger["N_UFPA_CONCEITO_4"] == 6
    assert nt_ger["DIFERENCA"] > 0


def test_processo_compara_47_itens() -> None:
    base = _base()
    sensibilidade, membros = sensibilidade_benchmarks_pedagogia(base)
    assert not sensibilidade.empty
    linhas = []
    for curso in base["CO_CURSO"]:
        for i in range(20, 67):
            linhas.append(
                {
                    "CO_CURSO": curso,
                    "ITEM": f"QE_I{i}",
                    "media": 5.0 + (0.1 if curso == CO_CURSO_CASTANHAL else 0),
                    "n_valido": 30,
                }
            )
    itens = pd.DataFrame(linhas)
    comparacao = comparar_itens_processo_castanhal(itens, base, membros)
    assert comparacao["ITEM"].nunique() == 47
    assert "UFPA — Conceito 4" in set(comparacao["REFERENCIA"])
