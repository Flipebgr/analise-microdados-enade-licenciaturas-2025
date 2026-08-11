from __future__ import annotations

import pandas as pd

from src.biologia.rotulos_questionario import ROTULOS_QE, rotulo_item
from src.relatorios.gerar_relatorio_biologia import (
    resumo_desempenho_geral,
    resumo_soure,
    tabela_itens_processo,
    tabela_ofertas_ufpa,
)


def _base() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [104640, 1, 2, 3, 4, 999],
            "CO_IES": [569, 569, 569, 569, 569, 999],
            "ROTULO_OFERTA": ["Soure", "Belém", "Altamira", "Bragança", "Belém EaD", "Outro"],
            "CONCEITO_ENADE_NUM": [3, 4, 4, 4, 3, 2],
            "INSCRITOS_NUM": [65, 100, 40, 40, 120, 40],
            "PARTICIPANTES_NUM": [49, 90, 35, 36, 100, 35],
            "TAXA_PARTICIPACAO_OFICIAL": [0.75, 0.9, 0.88, 0.9, 0.83, 0.9],
            "taxa_presenca_microdados": [0.75, 0.9, 0.88, 0.9, 0.83, 0.9],
            "nt_ger_mean": [53.5, 60.0, 58.0, 57.0, 55.0, 62.0],
            "nt_obj_mean": [50.6, 58.0, 57.0, 55.0, 53.0, 61.0],
            "nt_dis_mean": [6.53, 6.4, 6.2, 6.1, 6.0, 6.7],
            "nt_ger_percentil_brasil": [27.2, 60, 50, 45, 35, 70],
            "nt_ger_percentil_norte": [40.0, 70, 60, 55, 50, 80],
            "nt_ger_percentil_para": [41.2, 80, 70, 60, 50, 90],
        }
    )


def test_ofertas_ufpa_preservam_cinco_e_sem_conceito_1():
    tabela = tabela_ofertas_ufpa(_base())
    assert len(tabela) == 5
    assert not tabela["CONCEITO_ENADE_NUM"].eq(1).any()


def test_resumo_geral_nao_cria_grupo_conceito_1():
    texto = resumo_desempenho_geral(_base())
    assert "não existe oferta da UFPA com Conceito Enade 1" in texto
    assert "Soure" in texto


def test_resumo_soure_destaca_objetiva_quando_distancia_e_maior():
    sensibilidade = pd.DataFrame(
        {
            "CENARIO": ["estrutura_porte_0_5_2_0"],
            "N_CURSOS": [56],
            "nt_ger_mean_DIFERENCA": [-8.6],
            "nt_obj_mean_DIFERENCA": [-10.3],
            "nt_dis_mean_DIFERENCA": [-0.2],
        }
    )
    texto = resumo_soure(_base(), sensibilidade)
    assert "mais pronunciada no componente objetivo" in texto
    assert "não causal" in texto


def test_rotulos_oficiais_estao_mapeados():
    assert len([k for k in ROTULOS_QE if k.startswith("QE_I") and 20 <= int(k[4:]) <= 66]) == 47
    assert "extensão universitária" in rotulo_item("QE_I20")
    assert "recomendaria o seu curso" in rotulo_item("QE_I68")


def test_tabela_processo_adiciona_texto_oficial():
    dados = pd.DataFrame(
        {
            "ITEM": ["QE_I20", "QE_I52"],
            "REFERENCIA": ["Benchmark comparável", "Benchmark comparável"],
            "MEDIA_SOURE": [4.5, 5.1],
            "N_VALIDO_SOURE": [45, 51],
            "N_CURSOS_REFERENCIA": [56, 56],
            "MEDIA_REFERENCIA": [5.0, 4.3],
            "DIFERENCA_SOURE_REFERENCIA": [-0.5, 0.8],
        }
    )
    tabela = tabela_itens_processo(dados)
    assert "ROTULO_OFICIAL" in tabela.columns
    assert tabela["ROTULO_OFICIAL"].notna().all()
