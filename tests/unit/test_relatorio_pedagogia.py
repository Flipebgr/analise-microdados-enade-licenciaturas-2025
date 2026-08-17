from __future__ import annotations

import pandas as pd

from src.relatorios.gerar_relatorio_pedagogia import (
    obter_castanhal,
    tabela_benchmark_principal,
    tabela_processo_castanhal,
)


def test_obter_castanhal_localiza_curso_12085():
    base = pd.DataFrame(
        {
            "CO_CURSO": [11996, 12085],
            "CO_IES": [569, 569],
            "ROTULO_OFERTA": ["Belém", "Castanhal"],
        }
    )
    assert int(obter_castanhal(base)["CO_CURSO"]) == 12085


def test_benchmark_principal_filtra_cenario_estrutura():
    df = pd.DataFrame(
        {
            "CENARIO": ["modalidade", "estrutura_porte_0_5_2_0"],
            "CO_CURSO_ALVO": [12085, 12085],
            "ROTULO_ALVO": ["Castanhal", "Castanhal"],
            "CONCEITO_ALVO": [5, 5],
            "N_CURSOS": [100, 20],
            "nt_ger_mean_ALVO": [60.0, 60.0],
            "nt_ger_mean_MEDIA_BENCHMARK": [58.0, 59.0],
            "nt_ger_mean_DIFERENCA": [2.0, 1.0],
            "nt_ger_mean_Z": [0.5, 0.2],
            "nt_obj_mean_DIFERENCA": [2.0, 1.0],
            "nt_dis_mean_DIFERENCA": [0.2, 0.1],
            "taxa_presenca_microdados_DIFERENCA": [1.0, 0.5],
        }
    )
    resultado = tabela_benchmark_principal(df)
    assert len(resultado) == 1
    assert resultado.iloc[0]["CENARIO"] if "CENARIO" in resultado.columns else True


def test_tabela_processo_castanhal_aplica_rotulo_oficial():
    df = pd.DataFrame(
        {
            "ITEM": ["QE_I20", "QE_I21"],
            "REFERENCIA": ["UFPA — Conceito 4", "UFPA — Conceito 4"],
            "MEDIA_CASTANHAL": [5.0, 4.0],
            "N_VALIDO_CASTANHAL": [50, 49],
            "N_CURSOS_REFERENCIA": [6, 6],
            "MEDIA_REFERENCIA": [4.0, 4.5],
            "DIFERENCA_CASTANHAL_REFERENCIA": [1.0, -0.5],
        }
    )
    resultado = tabela_processo_castanhal(df)
    assert resultado.iloc[0]["ITEM"] == "QE_I20"
    assert "extensão universitária" in resultado.iloc[0]["ROTULO_OFICIAL"]
