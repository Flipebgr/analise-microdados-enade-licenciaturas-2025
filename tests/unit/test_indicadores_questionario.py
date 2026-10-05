from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import src.agregacao.agregar_socioeconomico as modulo
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS
from src.edicoes.base import RegraIndicadorQuestionario


def test_regra_rejeita_categorias_incoerentes():
    with pytest.raises(ValueError, match="fora do domínio válido"):
        RegraIndicadorQuestionario(
            "teste_pct", "QE_I01", frozenset("B"), frozenset("A"), "Teste"
        )
    with pytest.raises(ValueError, match="se sobrepõem"):
        RegraIndicadorQuestionario(
            "teste_pct", "QE_I01", frozenset("A"), frozenset("A"), "Teste",
            respostas_excluidas=frozenset("A")
        )


def test_primeira_geracao_usa_categorias_do_instrumento_de_cada_edicao():
    regra_2017 = next(
        regra for regra in ENADE_2017.questionario.regras_indicadores
        if regra.nome == "primeira_geracao_pct"
    )
    regra_2025 = next(
        regra for regra in ENADE_2025_LICENCIATURAS.questionario.regras_indicadores
        if regra.nome == "primeira_geracao_pct"
    )

    assert regra_2017.item == "QE_I21"
    assert regra_2025.item == "QE_I05"
    assert modulo._classificar_resposta("B", regra_2017) == "positiva"
    assert modulo._classificar_resposta("A", regra_2017) == "negativa"
    assert modulo._classificar_resposta("C", regra_2025) == "excluida"


def test_bolsa_2025_trata_multiplas_respostas_e_inconsistencias():
    regra = next(
        regra for regra in ENADE_2025_LICENCIATURAS.questionario.regras_indicadores
        if regra.nome == "bolsa_academica_pct"
    )

    assert regra.multipla_escolha
    assert modulo._classificar_resposta("B,F", regra) == "positiva"
    assert modulo._classificar_resposta("A", regra) == "negativa"
    assert modulo._classificar_resposta("A,B", regra) == "invalida"
    assert modulo._classificar_resposta("B,B", regra) == "invalida"
    assert modulo._classificar_resposta(".", regra) == "ausente"


def test_agregacao_2025_declara_denominadores_e_le_cada_item_uma_vez(monkeypatch):
    leituras: list[str] = []

    def carregar(_fonte, _edicao, _numero, *, usecols, cursos, chunksize=None):
        item = usecols[0]
        leituras.append(item)
        respostas = {
            "QE_I05": ["A", "B", "C"],
            "QE_I10": ["B", "D", "A"],
            "QE_I16": ["B,F", "A", "A,B"],
        }.get(item, ["A", "A", "A"])
        return pd.DataFrame({"CO_CURSO": ["1", "1", "2"], item: respostas})

    monkeypatch.setattr(modulo, "carregar_filtrado_edicao", carregar)
    agregado, distribuicoes, proveniencia = modulo.agregar_indicadores_questionario(
        Path("sintetico.zip"), ENADE_2025_LICENCIATURAS, ["1", "2", "3"]
    )
    curso_1 = agregado.set_index("CO_CURSO").loc["1"]
    curso_2 = agregado.set_index("CO_CURSO").loc["2"]
    curso_3 = agregado.set_index("CO_CURSO").loc["3"]

    assert agregado["CO_CURSO"].is_unique
    assert leituras.count("QE_I10") == 1
    assert curso_1["primeira_geracao_pct"] == 0.5
    assert curso_1["bolsa_academica_n_valido"] == 2
    assert curso_1["bolsa_academica_n_positivo"] == 1
    assert curso_1["bolsa_academica_pct"] == 0.5
    assert curso_2["primeira_geracao_n_excluida"] == 1
    assert curso_2["bolsa_academica_n_invalida"] == 1
    assert pd.isna(curso_2["bolsa_academica_pct"])
    assert curso_3["bolsa_academica_n_total"] == 0
    assert pd.isna(curso_3["bolsa_academica_pct"])
    assert set(proveniencia["edicao"]) == {2025}
    assert proveniencia.loc[
        proveniencia["indicador"] == "bolsa_academica_pct", "multipla_escolha"
    ].iloc[0]
    assert set(distribuicoes["item"]) == set(leituras)


def test_agregacao_2017_nao_reutiliza_qe_i05_de_2025(monkeypatch):
    def carregar(_fonte, _edicao, _numero, *, usecols, cursos, chunksize=None):
        item = usecols[0]
        respostas = ["A", "B"] if item == "QE_I21" else ["A", "A"]
        return pd.DataFrame({"CO_CURSO": ["12027", "12027"], item: respostas})

    monkeypatch.setattr(modulo, "carregar_filtrado_edicao", carregar)
    agregado, _, proveniencia = modulo.agregar_indicadores_questionario(
        Path("sintetico.zip"), ENADE_2017, ["12027"]
    )

    assert agregado.loc[0, "primeira_geracao_pct"] == 0.5
    assert proveniencia.loc[
        proveniencia["indicador"] == "primeira_geracao_pct", "item"
    ].iloc[0] == "QE_I21"
