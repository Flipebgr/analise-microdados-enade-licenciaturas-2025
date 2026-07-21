from __future__ import annotations

import pandas as pd

from src.analise.validar_indicadores import auditar_desempenho, auditar_indicadores
from src.analise.validar_benchmarks import sensibilidade_benchmarks
from src.analise.analise_sensibilidade import sensibilidade_desempenho


def _base() -> pd.DataFrame:
    linhas = []
    for i, grupo in enumerate(list("ABCDE"), start=1):
        linhas.append({
            "CO_CURSO": i, "ROTULO_OFERTA": f"Curso {i}", "GRUPO_CODIGO": grupo,
            "CO_IES": 569 if grupo in ["A", "B"] else 100+i,
            "CONCEITO_ENADE_NUM": 1 if grupo == "A" else 3,
            "CO_MODALIDADE": 1, "CO_CATEGAD": 1, "CO_ORGACAD": 10028,
            "PARTICIPANTES_NUM": 20, "registros_microdados": 22, "presentes_validos": 20,
            "nt_ger_count": 20, "nt_obj_count": 20, "nt_dis_count": 20, "reaplicacoes": 0,
            "nt_ger_mean": 40+i, "nt_ger_median": 40+i, "taxa_presenca_microdados": .9,
            "renda_ate_3sm_pct": .5,
        })
    return pd.DataFrame(linhas)


def test_auditorias_dominios():
    base = _base()
    aud = auditar_desempenho(base)
    ind = auditar_indicadores(base)
    assert not aud["alerta_n_superior_registros"].any()
    assert ind["fora_0_1"].sum() == 0


def test_sensibilidade_nao_vazia():
    base = _base()
    # transforma quatro cursos em alvos para exercitar a função; validação completa usa dados reais.
    base.loc[base.index[:4], ["CO_IES", "CONCEITO_ENADE_NUM"]] = [569, 1]
    resumo, _ = sensibilidade_benchmarks(base)
    sens = sensibilidade_desempenho(base)
    assert not resumo.empty
    assert not sens.empty
