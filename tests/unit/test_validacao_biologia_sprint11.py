from __future__ import annotations

import pandas as pd
import pytest

from src.biologia import CO_CURSO_SOURE
from src.biologia.preparar_catalogo import aplicar_recorte_focal
from src.biologia.validacao_analitica import (
    comparar_itens_processo_soure,
    desempenho_individual_soure,
    sensibilidade_benchmark_soure,
)


def _base() -> pd.DataFrame:
    dados = pd.DataFrame(
        {
            "CO_CURSO": [CO_CURSO_SOURE, 12023, 9001, 9002, 9003],
            "CO_IES": [569, 569, 100, 101, 102],
            "CO_UF_CURSO": [15, 15, 15, 13, 35],
            "CO_REGIAO_CURSO": [1, 1, 1, 1, 3],
            "CO_MODALIDADE": [1, 1, 1, 1, 1],
            "CO_CATEGAD": [1, 1, 1, 1, 2],
            "CO_ORGACAD": [1, 1, 1, 1, 1],
            "PARTICIPANTES_NUM": [49, 94, 45, 60, 50],
            "ROTULO_OFERTA": ["Soure", "Belém", "Outro PA", "Outro Norte", "Sudeste"],
            "nt_ger_mean": [53.5, 60.0, 62.0, 61.0, 70.0],
            "nt_obj_mean": [50.5, 59.0, 61.0, 60.0, 69.0],
            "nt_dis_mean": [6.5, 6.6, 6.7, 6.8, 7.1],
            "taxa_presenca_microdados": [0.75, 0.82, 0.85, 0.80, 0.90],
        }
    )
    return aplicar_recorte_focal(dados)


def test_sensibilidade_benchmark_soure_preserva_alvo_e_exclui_ufpa() -> None:
    sensibilidade, membros = sensibilidade_benchmark_soure(_base())
    assert len(sensibilidade) == 5
    assert sensibilidade["CO_CURSO_ALVO"].eq(CO_CURSO_SOURE).all()
    assert not membros["CO_IES"].eq(569).any()
    principal = sensibilidade.loc[
        sensibilidade["CENARIO"].eq("estrutura_porte_0_5_2_0")
    ].iloc[0]
    assert principal["N_CURSOS"] == 2
    assert principal["nt_obj_mean_DIFERENCA"] < 0


def test_desempenho_individual_soure_usa_apenas_mesmo_arquivo() -> None:
    individual = pd.DataFrame(
        {
            "NT_GER": [50, 55, 60, 65],
            "NT_OBJ": [48, 53, 58, 63],
            "NT_DIS": [6.0, 6.2, 6.4, 6.8],
            "QT_ACERTOS": [30, 34, 38, 42],
            "PROFICIENCIA": [1, 1, 1, 1],
        }
    )
    descritas, correlacoes = desempenho_individual_soure(individual)
    assert set(descritas["VARIAVEL"]) == {
        "NT_GER", "NT_OBJ", "NT_DIS", "QT_ACERTOS", "PROFICIENCIA"
    }
    linha = correlacoes.loc[
        correlacoes["VARIAVEL_X"].eq("NT_GER")
        & correlacoes["VARIAVEL_Y"].eq("NT_OBJ")
    ].iloc[0]
    assert linha["SPEARMAN_RHO"] == pytest.approx(1.0)


def test_comparacao_itens_preserva_codigo_sem_inventar_rotulo() -> None:
    base = _base()
    itens = pd.DataFrame(
        {
            "CO_CURSO": [CO_CURSO_SOURE, 12023, 9001, 9002] * 2,
            "ITEM": ["QE_I20"] * 4 + ["QE_I21"] * 4,
            "n_valido": [40, 80, 35, 45] * 2,
            "media": [4.0, 4.4, 4.5, 4.6, 5.0, 4.8, 4.7, 4.9],
        }
    )
    benchmark = base.loc[base["CO_CURSO"].isin([9001, 9002])]
    resultado = comparar_itens_processo_soure(itens, base, benchmark)
    assert resultado["ITEM"].nunique() == 2
    assert resultado["ROTULO_OFICIAL"].isna().all()
    assert resultado["STATUS_INTERPRETACAO"].str.contains("texto oficial").all()
