from __future__ import annotations

import pandas as pd

from src.relatorios.gerar_relatorio_ingles import (
    resumo_associacoes,
    resumo_desempenho,
    resumo_regional,
    tabela_ofertas_ufpa,
)


def _base() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [1, 2, 3, 4, 5, 6],
            "CO_IES": [569, 569, 569, 569, 569, 999],
            "ROTULO_OFERTA": ["Altamira", "Belém", "Bragança", "Cametá", "Soure", "Outro"],
            "CONCEITO_ENADE_NUM": [1, 3, 1, 1, 1, 2],
            "INSCRITOS_NUM": [10, 20, 10, 10, 10, 10],
            "PARTICIPANTES_NUM": [9, 18, 9, 9, 9, 9],
            "TAXA_PARTICIPACAO_OFICIAL": [0.9] * 6,
            "nt_ger_mean": [30.0, 55.0, 40.0, 35.0, 32.0, 50.0],
            "nt_obj_mean": [25.0, 50.0, 35.0, 30.0, 27.0, 45.0],
            "nt_dis_mean": [6.0, 7.0, 6.5, 6.2, 6.1, 6.8],
            "nt_ger_percentil_brasil": [5.0, 70.0, 30.0, 15.0, 8.0, 50.0],
        }
    )


def test_tabela_ofertas_ufpa_preserva_cinco_ofertas_e_quatro_conceito_1():
    tabela = tabela_ofertas_ufpa(_base())
    assert len(tabela) == 5
    assert int(tabela["CONCEITO_ENADE_NUM"].eq(1).sum()) == 4


def test_resumo_desempenho_e_descritivo_e_nao_causal():
    texto = resumo_desempenho(_base())
    assert "4 ofertas" in texto
    assert "não implica causalidade" in texto


def test_resumo_regional_explicita_media_simples_e_ponderada():
    comparacoes = pd.DataFrame(
        {
            "RECORTE": ["UFPA agregada", "Região Norte sem UFPA", "Brasil geral"],
            "INDICADOR": ["nt_ger_mean"] * 3,
            "N_CURSOS": [5, 9, 127],
            "N_PARTICIPANTES": [199, 186, 3666],
            "MEDIA_CURSOS": [40.0, 43.0, 51.0],
            "MEDIA_PONDERADA_PARTICIPANTES": [45.0, 43.5, 49.8],
            "MEDIANA_CURSOS": [35.0, 40.0, 50.0],
            "DP_CURSOS": [10.0, 7.0, 12.0],
            "P25": [32.0, 39.0, 43.0],
            "P75": [45.0, 47.0, 60.0],
        }
    )
    texto = resumo_regional(comparacoes)
    assert "média simples" in texto
    assert "média ponderada por participantes" in texto


def test_resumo_associacoes_declara_nivel_ecologico():
    associacoes = pd.DataFrame(
        {
            "INDICADOR_X": ["renda_ate_3sm_pct", "trabalha_pct"],
            "INDICADOR_Y": ["nt_ger_mean", "nt_ger_mean"],
            "N_CURSOS": [100, 90],
            "SPEARMAN_RHO": [-0.4, 0.2],
            "P_VALOR_EXPLORATORIO": [0.01, 0.10],
            "NIVEL_ANALISE": ["curso (ecológico)"] * 2,
        }
    )
    texto = resumo_associacoes(associacoes)
    assert "associação ecológica" in texto
    assert "não entre estudantes" in texto
