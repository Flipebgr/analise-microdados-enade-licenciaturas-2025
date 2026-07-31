from __future__ import annotations

import pandas as pd

from src.fisica.analisar_dificuldade import ROTULOS_GRAU, ROTULOS_TIPO
from src.fisica.analisar_presenca import construir_auditoria_presenca
from src.fisica.validar_fisica import validar_base_fisica


def base_minima() -> pd.DataFrame:
    return pd.DataFrame({
        "CO_CURSO": [1, 2, 3, 4, 5],
        "CO_GRUPO": [1402] * 5,
        "CO_IES": [569] * 5,
        "ROTULO_OFERTA": ["A", "B", "C", "D", "E"],
        "CONCEITO_ENADE_NUM": [3, 1, 1, 1, 1],
        "INSCRITOS_NUM": [10] * 5,
        "PARTICIPANTES_NUM": [8] * 5,
        "registros_microdados": [10] * 5,
        "presentes_validos": [8] * 5,
        "ausentes": [2] * 5,
        "eliminados": [0] * 5,
        "resultado_desconsiderado": [0] * 5,
        "nt_ger_count": [8] * 5,
        "nt_ger_mean": [40] * 5,
        "nt_obj_mean": [40] * 5,
        "nt_dis_mean": [40] * 5,
        "taxa_presenca_microdados": [.8] * 5,
    })


def test_valida_base_fisica_com_cinco_ofertas_ufpa():
    validar_base_fisica(base_minima())


def test_auditoria_presenca_calcula_percentual():
    out = construir_auditoria_presenca(base_minima())
    assert out["taxa_presenca_pct"].eq(80).all()


def test_rotulos_dificuldade_documentados():
    assert ROTULOS_GRAU["D"] == "Difícil"
    assert ROTULOS_TIPO["E"] == "Sem dificuldade"


def test_ofertas_permanecem_unicas():
    assert base_minima()["ROTULO_OFERTA"].is_unique


def test_gerador_de_figuras_socioeconomicas_existe():
    from src.fisica.gerar_figuras import perfil_socioeconomico, sintese_socioeconomica_desempenho

    assert callable(perfil_socioeconomico)
    assert callable(sintese_socioeconomica_desempenho)
