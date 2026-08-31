from __future__ import annotations

import pandas as pd

from src.relatorios.gerar_relatorio_geografia import (
    resumo_benchmarks,
    resumo_desempenho_ufpa,
    tabela_processo_interno,
)


def _base_ufpa() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_IES": [569, 569, 569, 569],
            "CO_CURSO": [11991, 12052, 1194057, 1330343],
            "ROTULO_OFERTA": [
                "Belém — Presencial",
                "Altamira — Presencial",
                "Cametá — Presencial",
                "Ananindeua — Presencial",
            ],
            "CONCEITO_ENADE_NUM": [4, 3, 3, 4],
            "INSCRITOS_NUM": [71, 27, 92, 77],
            "PARTICIPANTES_NUM": [57, 23, 68, 63],
            "TAXA_PARTICIPACAO_OFICIAL": [57 / 71, 23 / 27, 68 / 92, 63 / 77],
            "taxa_presenca_microdados": [57 / 71, 23 / 27, 68 / 92, 63 / 77],
            "nt_ger_mean": [66.844, 58.097, 55.866, 61.516],
            "nt_obj_mean": [68.139, 57.948, 54.382, 62.192],
            "nt_dis_mean": [6.167, 5.870, 6.180, 5.881],
        }
    )


def test_resumo_desempenho_preserva_carater_descritivo() -> None:
    contraste = pd.DataFrame(
        {
            "INDICADOR": ["nt_ger_mean"],
            "DIFERENCA_C3_C4": [-7.198],
            "D_PADRONIZADO_DESCRITIVO": [-2.492],
        }
    )
    texto = resumo_desempenho_ufpa(_base_ufpa(), contraste)
    assert "duas ofertas em cada estrato" in texto
    assert "não sustenta inferência causal" in texto


def test_resumo_benchmark_informa_20_combinacoes() -> None:
    sens = pd.DataFrame(
        {
            "CENARIO": ["estrutura_porte_0_5_2_0"] * 4,
            "ROTULO_ALVO": ["A", "B", "C", "D"],
            "nt_ger_mean_DIFERENCA": [-1.0, -2.0, -3.0, -4.0],
        }
    )
    texto = resumo_benchmarks(sens)
    assert "20 combinações oferta-cenário" in texto
    assert "quatro ofertas" in texto


def test_tabela_processo_adiciona_rotulos_oficiais() -> None:
    processo = pd.DataFrame(
        {
            "ITEM": ["QE_I20", "QE_I21"],
            "N_CURSOS_CONCEITO_3": [2, 2],
            "MEDIA_CONCEITO_3": [4.0, 4.2],
            "N_CURSOS_CONCEITO_4": [2, 2],
            "MEDIA_CONCEITO_4": [4.5, 4.1],
            "DIFERENCA_C3_C4": [-0.5, 0.1],
            "MEDIA_OUTRAS_IES_PARA": [4.2, 4.0],
            "MEDIA_NORTE_SEM_PARA": [4.1, 4.0],
            "MEDIA_BRASIL_SEM_NORTE": [4.3, 4.2],
        }
    )
    out = tabela_processo_interno(processo)
    assert "ROTULO_OFICIAL" in out.columns
    assert out["ROTULO_OFICIAL"].notna().all()
