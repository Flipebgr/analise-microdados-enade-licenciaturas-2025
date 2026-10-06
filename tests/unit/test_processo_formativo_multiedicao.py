from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pandas as pd
import pytest

import src.agregacao.agregar_processo_formativo as modulo
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS


def test_contratos_separam_itens_e_declaram_direcao_da_escala():
    assert ENADE_2017.questionario.itens_processo_formativo[0] == "QE_I27"
    assert ENADE_2017.questionario.itens_processo_formativo[-1] == "QE_I68"
    assert ENADE_2025_LICENCIATURAS.questionario.itens_processo_formativo[0] == "QE_I20"
    assert ENADE_2025_LICENCIATURAS.questionario.itens_processo_formativo[-1] == "QE_I66"
    for edicao in (ENADE_2017, ENADE_2025_LICENCIATURAS):
        assert edicao.questionario.codigos_concordancia_processo == {4, 5, 6}
        assert "1=discordância total" in edicao.questionario.descricao_escala_processo


def test_schema_rejeita_codigos_incoerentes_e_itens_duplicados():
    schema = ENADE_2017.questionario
    with pytest.raises(ValueError, match="se sobrepõem"):
        replace(schema, codigos_especiais_processo=((6, "nao_sabe_responder"),))
    with pytest.raises(ValueError, match="concordância"):
        replace(schema, codigos_concordancia_processo=frozenset((4, 9)))
    with pytest.raises(ValueError, match="únicos"):
        replace(schema, itens_processo_formativo=("QE_I27", "QE_I27"))


def test_agregador_classifica_ausencias_especiais_invalidos_e_curso_sem_linhas(monkeypatch):
    itens = ENADE_2017.questionario.itens_processo_formativo
    dados = pd.DataFrame({"CO_CURSO": ["1"] * 8 + ["2"] * 2})
    for item in itens:
        dados[item] = "4"
    dados["QE_I27"] = ["1", "4", "6", "7", "8", "x", ".", " ", "7", "8"]
    leituras = []

    def carregar(_fonte, _edicao, numero, *, usecols, cursos, chunksize=None):
        leituras.append((numero, tuple(usecols), tuple(cursos)))
        return dados.copy()

    monkeypatch.setattr(modulo, "carregar_filtrado_edicao", carregar)
    agregado, resumo, proveniencia = modulo.agregar_processo_formativo_edicao(
        Path("sintetico.zip"), ENADE_2017, ["1", "2", "3"]
    )
    item = resumo.set_index(["CO_CURSO", "ITEM"]).loc[("1", "QE_I27")]
    sem_validos = resumo.set_index(["CO_CURSO", "ITEM"]).loc[("2", "QE_I27")]
    sem_linhas = resumo.set_index(["CO_CURSO", "ITEM"]).loc[("3", "QE_I27")]

    assert leituras == [(4, itens, ("1", "2", "3"))]
    assert agregado["CO_CURSO"].is_unique
    assert len(resumo) == 3 * len(itens)
    assert item["n_total"] == 8
    assert item["n_valido"] == 3
    assert item["n_ausente"] == 2
    assert item["n_invalido"] == 1
    assert item["n_nao_sabe_responder"] == 1
    assert item["n_nao_se_aplica"] == 1
    assert item["nao_sabe_responder_pct"] == pytest.approx(1 / 8)
    assert item["nao_se_aplica_pct"] == pytest.approx(1 / 8)
    assert item["concordancia_n"] == 2
    assert item["concordancia_pct"] == pytest.approx(2 / 3)
    assert item["ausencia_analitica_pct"] == pytest.approx(5 / 8)
    assert item["media"] == pytest.approx(11 / 3)
    assert sem_validos["n_total"] == 2
    assert pd.isna(sem_validos["concordancia_pct"])
    assert sem_linhas["n_total"] == 0
    assert pd.isna(sem_linhas["ausencia_analitica_pct"])
    assert pd.isna(sem_linhas["nao_sabe_responder_pct"])
    assert pd.isna(sem_linhas["nao_se_aplica_pct"])
    assert set(proveniencia["item"]) == set(itens)
    assert set(proveniencia["denominador_codigos_especiais"]) == {"n_total"}
    assert "cronbach_alpha" not in proveniencia.columns


def test_agregador_falha_quando_item_nao_pertence_a_arquivo_tematico():
    questionario = replace(
        ENADE_2017.questionario,
        itens_processo_formativo=(*ENADE_2017.questionario.itens_processo_formativo, "QE_I99"),
    )
    edicao = replace(ENADE_2017, questionario=questionario)
    with pytest.raises(ValueError, match="um arquivo temático"):
        modulo.agregar_processo_formativo_edicao(
            Path("sintetico.zip"), edicao, ["12027"]
        )


def test_agregador_retorna_ausentes_quando_nenhum_curso_tem_linhas(monkeypatch):
    itens = ENADE_2017.questionario.itens_processo_formativo
    vazio = pd.DataFrame(columns=["CO_CURSO", *itens]).astype("string")
    monkeypatch.setattr(
        modulo, "carregar_filtrado_edicao", lambda *args, **kwargs: vazio.copy()
    )

    agregado, resumo, _ = modulo.agregar_processo_formativo_edicao(
        Path("sintetico.zip"), ENADE_2017, ["12027"]
    )

    assert len(agregado) == 1
    assert len(resumo) == len(itens)
    assert (resumo["n_total"] == 0).all()
    assert resumo["concordancia_pct"].isna().all()
    assert resumo["ausencia_analitica_pct"].isna().all()
    assert resumo["nao_sabe_responder_pct"].isna().all()
    assert resumo["nao_se_aplica_pct"].isna().all()
