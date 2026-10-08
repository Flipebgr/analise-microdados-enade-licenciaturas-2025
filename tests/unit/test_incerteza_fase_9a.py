from __future__ import annotations

import numpy as np
import pandas as pd

from src.analise.contratos_fase_9a import ConfiguracaoBootstrap
from src.analise.incerteza_fase_9a import (
    bootstrap_ic_condicional_ao_foco,
    bootstrap_ic_multifoco,
)


def test_bootstrap_foco_unico_e_condicional_e_deterministico():
    benchmark = pd.Series(np.linspace(40, 70, 20))
    configuracao = ConfiguracaoBootstrap(numero_reamostragens=250)

    primeira = bootstrap_ic_condicional_ao_foco(
        60.0,
        benchmark,
        identificador="2017:biologia:12027:amplo_para:geral",
        configuracao=configuracao,
    )
    segunda = bootstrap_ic_condicional_ao_foco(
        60.0,
        benchmark,
        identificador="2017:biologia:12027:amplo_para:geral",
        configuracao=configuracao,
    )

    assert primeira == segunda
    assert primeira["tipo_incerteza"] == "IC ecológico condicional ao foco"
    assert primeira["unidade_reamostragem"] == "CO_CURSO"
    assert primeira["foco_reamostrado"] is False
    assert primeira["status"] == "disponivel"
    assert primeira["ic_inf"] <= primeira["estimativa"] <= primeira["ic_sup"]


def test_bootstrap_nao_emite_ic_com_menos_de_dez_cursos():
    resultado = bootstrap_ic_condicional_ao_foco(
        50.0,
        pd.Series([40.0] * 9),
        identificador="contraste",
        configuracao=ConfiguracaoBootstrap(numero_reamostragens=100),
    )

    assert resultado["status"] == "insuficiente"
    assert resultado["ic_inf"] is None
    assert resultado["ic_sup"] is None
    assert resultado["motivo"] == "n_benchmark_abaixo_do_minimo"


def test_bootstrap_independe_da_ordem_das_linhas_quando_cursos_sao_informados():
    valores = pd.Series(np.linspace(40, 70, 20))
    cursos = pd.Series([f"c{i:02d}" for i in range(20)])
    ordem = np.random.default_rng(7).permutation(len(valores))
    configuracao = ConfiguracaoBootstrap(numero_reamostragens=100)

    original = bootstrap_ic_condicional_ao_foco(
        60.0,
        valores,
        cursos_benchmark=cursos,
        identificador="ordem-estavel",
        configuracao=configuracao,
    )
    embaralhado = bootstrap_ic_condicional_ao_foco(
        60.0,
        valores.iloc[ordem],
        cursos_benchmark=cursos.iloc[ordem],
        identificador="ordem-estavel",
        configuracao=configuracao,
    )

    assert original == embaralhado


def test_bootstrap_multifoco_reamostra_os_dois_bracos():
    resultado = bootstrap_ic_multifoco(
        pd.Series([50.0, 60.0, 70.0]),
        pd.Series(np.linspace(40, 59, 20)),
        cursos_focais=pd.Series(["f3", "f1", "f2"]),
        cursos_benchmark=pd.Series([f"b{i:02d}" for i in range(20)]),
        identificador="multifoco",
        configuracao=ConfiguracaoBootstrap(numero_reamostragens=100),
    )

    assert resultado["status"] == "disponivel"
    assert resultado["tipo_incerteza"] == "IC ecológico multifoco"
    assert resultado["foco_reamostrado"] is True
    assert resultado["n_focos"] == 3
