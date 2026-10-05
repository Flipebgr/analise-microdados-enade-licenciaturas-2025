from __future__ import annotations

from pathlib import Path

import pytest

from src.agregacao.agregar_socioeconomico import (
    REGRAS_INDICADORES,
    REGRAS_MULTIPLA_ESCOLHA_2025,
    _agregar_indicador,
    agregar_indicadores_questionario,
)
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS
from src.utilitarios.leitura import carregar_filtrado_edicao

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]


def test_primeira_geracao_2017_usa_qe_i21_real():
    fonte = ROOT / "dados_brutos" / "enade_2017" / "microdados_enade_2017_LGPD.zip"
    if not fonte.exists():
        pytest.skip(f"Fonte local ausente: {fonte}")

    agregado, _, regras = agregar_indicadores_questionario(
        fonte, ENADE_2017, ["12027"]
    )
    curso = agregado.iloc[0]

    assert curso["primeira_geracao_n_total"] == 23
    assert curso["primeira_geracao_n_valido"] == 16
    assert curso["primeira_geracao_n_positivo"] == 1
    assert regras.loc[regras["indicador"] == "primeira_geracao_pct", "item"].iloc[0] == "QE_I21"


def test_bolsa_academica_2025_inclui_respostas_multiplas_reais():
    fonte = ROOT / "dados_brutos" / "microdados_enade_licenciaturas_2025.zip"
    if not fonte.exists():
        pytest.skip(f"Fonte local ausente: {fonte}")

    agregado, _, regras = agregar_indicadores_questionario(
        fonte, ENADE_2025_LICENCIATURAS, ["100148"]
    )
    curso = agregado.iloc[0]

    assert curso["bolsa_academica_n_total"] == 12
    assert curso["bolsa_academica_n_valido"] == 11
    assert curso["bolsa_academica_n_positivo"] == 7
    assert curso["bolsa_academica_pct"] == pytest.approx(7 / 11)
    assert regras.loc[regras["indicador"] == "bolsa_academica_pct", "multipla_escolha"].iloc[0]


def test_calculo_legado_bolsa_2025_concorda_com_agregador_novo_na_fonte_real():
    fonte = ROOT / "dados_brutos" / "microdados_enade_licenciaturas_2025.zip"
    if not fonte.exists():
        pytest.skip(f"Fonte local ausente: {fonte}")

    dados = carregar_filtrado_edicao(
        fonte, ENADE_2025_LICENCIATURAS, 22,
        usecols=["QE_I16"], cursos=["100148"],
    )
    dados["RESPOSTA"] = dados["QE_I16"].astype("string").str.strip().str.upper()
    positivos, validos, nome = REGRAS_INDICADORES["QE_I16"]
    legado = _agregar_indicador(
        dados, positivos, validos, nome,
        regra=REGRAS_MULTIPLA_ESCOLHA_2025["QE_I16"],
    ).iloc[0]
    novo, _, _ = agregar_indicadores_questionario(
        fonte, ENADE_2025_LICENCIATURAS, ["100148"]
    )

    assert legado["bolsa_academican_valido"] == novo.loc[0, "bolsa_academica_n_valido"] == 11
    assert legado["bolsa_academican_positivo"] == novo.loc[0, "bolsa_academica_n_positivo"] == 7
    assert legado["bolsa_academica_pct"] == pytest.approx(7 / 11)
