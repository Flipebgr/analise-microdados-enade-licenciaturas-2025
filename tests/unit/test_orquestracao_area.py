from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import src.orquestracao.area as modulo
from src.core.configuracao_area import BIOLOGIA_BACHARELADO_2017
from src.edicoes import ENADE_2017


def _caracterizacao() -> pd.DataFrame:
    return pd.DataFrame({
        "CO_CURSO": ["00001", "00002"],
        "NU_ANO": ["2017", "2017"],
        "CO_GRUPO": ["1601", "1601"],
        "CO_IES": ["569", "9"],
        "CO_CATEGAD": ["1", "1"],
        "CO_ORGACAD": ["1", "1"],
        "CO_MODALIDADE": ["1", "1"],
        "CO_MUNIC_CURSO": ["1501402", "1501402"],
        "CO_UF_CURSO": ["15", "15"],
        "CO_REGIAO_CURSO": ["1", "1"],
    })


def _conceitos() -> pd.DataFrame:
    dados = _caracterizacao()[[
        "CO_CURSO", "NU_ANO", "CO_GRUPO", "CO_IES", "CO_MUNIC_CURSO"
    ]].copy()
    dados["INSCRITOS"] = [23, 10]
    dados["PARTICIPANTES"] = [13, 5]
    dados["CONCEITO_ENADE_ORIGINAL"] = ["3", "SC"]
    dados["CONCEITO_ENADE_NUM"] = pd.array([3, pd.NA], dtype="Int64")
    dados["CONCEITO_ENADE_CONTINUO"] = pd.array([2.5, pd.NA], dtype="Float64")
    dados["SITUACAO_CONCEITO"] = ["com_conceito", "sem_conceito"]
    dados["OBSERVACAO_CONCEITO"] = pd.NA
    return dados


def test_caracterizacao_agrega_somente_atributos_constantes(monkeypatch):
    dados = pd.concat([_caracterizacao(), _caracterizacao().iloc[[0]]], ignore_index=True)
    monkeypatch.setattr(modulo, "carregar_filtrado_edicao", lambda *a, **k: dados.copy())

    cursos = modulo.caracterizar_cursos(
        Path("micro.zip"), ENADE_2017, BIOLOGIA_BACHARELADO_2017
    )

    assert cursos["CO_CURSO"].tolist() == ["00001", "00002"]
    assert cursos["CO_IES"].tolist() == ["569", "9"]

    dados.loc[2, "CO_IES"] = "999"
    with pytest.raises(ValueError, match="Caracterização divergente"):
        modulo.caracterizar_cursos(
            Path("micro.zip"), ENADE_2017, BIOLOGIA_BACHARELADO_2017
        )


def test_preparacao_preserva_sc_e_registra_cobertura(monkeypatch):
    conceitos = _conceitos()
    conceitos.loc[1, "CO_CURSO"] = "00003"
    monkeypatch.setattr(modulo, "caracterizar_cursos", lambda *a, **k: _caracterizacao())
    monkeypatch.setattr(
        modulo, "carregar_conceitos_edicao",
        lambda *a, **k: (conceitos.copy(), pd.DataFrame(), pd.DataFrame([{"aba": "teste"}])),
    )

    resultado = modulo.preparar_area(
        Path("micro.zip"), Path("conceito.xlsx"), ENADE_2017, BIOLOGIA_BACHARELADO_2017
    )

    assert resultado.base_cursos["CO_CURSO"].tolist() == ["00001", "00002"]
    assert resultado.base_cursos.loc[0, "CONCEITO_ENADE_NUM"] == 3
    assert pd.isna(resultado.base_cursos.loc[1, "CONCEITO_ENADE_NUM"])
    cobertura = resultado.auditoria_cobertura.set_index("CO_CURSO")
    assert bool(cobertura.loc["00002", "em_conceito"]) is False
    assert bool(cobertura.loc["00003", "em_microdados"]) is False


def test_preparacao_falha_quando_ies_diverge(monkeypatch):
    conceitos = _conceitos()
    conceitos.loc[0, "CO_IES"] = "999"
    monkeypatch.setattr(modulo, "caracterizar_cursos", lambda *a, **k: _caracterizacao())
    monkeypatch.setattr(
        modulo, "carregar_conceitos_edicao",
        lambda *a, **k: (conceitos.copy(), pd.DataFrame(), pd.DataFrame()),
    )

    with pytest.raises(ValueError, match="CO_IES diverge"):
        modulo.preparar_area(
            Path("micro.zip"), Path("conceito.xlsx"), ENADE_2017, BIOLOGIA_BACHARELADO_2017
        )


def test_preparacao_rejeita_mesmo_curso_em_outro_grupo_na_planilha(monkeypatch):
    conceitos = _conceitos()
    conceitos.loc[0, "CO_GRUPO"] = "9999"
    monkeypatch.setattr(modulo, "caracterizar_cursos", lambda *a, **k: _caracterizacao())
    monkeypatch.setattr(
        modulo, "carregar_conceitos_edicao",
        lambda *a, **k: (conceitos.copy(), pd.DataFrame(), pd.DataFrame()),
    )

    with pytest.raises(ValueError, match="CO_GRUPO diverge"):
        modulo.preparar_area(
            Path("micro.zip"), Path("conceito.xlsx"), ENADE_2017, BIOLOGIA_BACHARELADO_2017
        )


def test_analise_junta_somente_agregados_unicos(monkeypatch):
    base = _caracterizacao()[["CO_CURSO", "CO_IES"]].copy()
    resultado = modulo.ResultadoArea(
        base, pd.DataFrame({"CO_CURSO": base["CO_CURSO"]}), pd.DataFrame()
    )
    monkeypatch.setattr(modulo, "preparar_area", lambda *a, **k: resultado)
    monkeypatch.setattr(
        modulo, "agregar_desempenho_edicao",
        lambda *a, **k: (
            pd.DataFrame({"CO_CURSO": ["00001", "00002"], "geral_mean": [55, 60]}),
            pd.DataFrame({"registro_individual": [1, 2]}),
        ),
    )
    monkeypatch.setattr(
        modulo, "agregar_indicadores_questionario",
        lambda *a, **k: (
            pd.DataFrame({"CO_CURSO": ["00001", "00002"], "renda_pct": [0.5, 0.7]}),
            pd.DataFrame(), pd.DataFrame(),
        ),
    )
    monkeypatch.setattr(
        modulo, "agregar_processo_formativo_edicao",
        lambda *a, **k: (
            pd.DataFrame({"CO_CURSO": ["00001", "00002"], "qe_i27_n_total": [10, 8]}),
            pd.DataFrame(), pd.DataFrame(),
        ),
    )

    obtido = modulo.analisar_area(
        Path("micro.zip"), Path("conceito.xlsx"), ENADE_2017, BIOLOGIA_BACHARELADO_2017
    )

    assert len(obtido.base_cursos) == 2
    assert obtido.base_cursos.loc[0, "geral_mean"] == 55
    assert "registro_individual" not in obtido.base_cursos
    assert obtido.auditoria_cobertura["em_desempenho"].all()


def test_analise_rejeita_agregado_duplicado(monkeypatch):
    base = _caracterizacao()[["CO_CURSO", "CO_IES"]].copy()
    monkeypatch.setattr(
        modulo, "preparar_area",
        lambda *a, **k: modulo.ResultadoArea(base, pd.DataFrame(), pd.DataFrame()),
    )
    monkeypatch.setattr(
        modulo, "agregar_desempenho_edicao",
        lambda *a, **k: (pd.DataFrame({"CO_CURSO": ["00001", "00001"]}), pd.DataFrame()),
    )
    monkeypatch.setattr(
        modulo, "agregar_indicadores_questionario",
        lambda *a, **k: (pd.DataFrame({"CO_CURSO": ["00001"]}), pd.DataFrame(), pd.DataFrame()),
    )
    monkeypatch.setattr(
        modulo, "agregar_processo_formativo_edicao",
        lambda *a, **k: (pd.DataFrame({"CO_CURSO": ["00001"]}), pd.DataFrame(), pd.DataFrame()),
    )

    with pytest.raises(ValueError, match="não possui uma linha"):
        modulo.analisar_area(
            Path("micro.zip"), Path("conceito.xlsx"), ENADE_2017, BIOLOGIA_BACHARELADO_2017
        )


def test_analise_rejeita_coluna_sobreposta(monkeypatch):
    base = _caracterizacao()[["CO_CURSO", "CO_IES"]].copy()
    monkeypatch.setattr(
        modulo, "preparar_area",
        lambda *a, **k: modulo.ResultadoArea(base, pd.DataFrame(), pd.DataFrame()),
    )
    monkeypatch.setattr(
        modulo, "agregar_desempenho_edicao",
        lambda *a, **k: (pd.DataFrame({"CO_CURSO": ["00001"], "CO_IES": ["999"]}), pd.DataFrame()),
    )
    monkeypatch.setattr(
        modulo, "agregar_indicadores_questionario",
        lambda *a, **k: (pd.DataFrame({"CO_CURSO": ["00001"]}), pd.DataFrame(), pd.DataFrame()),
    )
    monkeypatch.setattr(
        modulo, "agregar_processo_formativo_edicao",
        lambda *a, **k: (pd.DataFrame({"CO_CURSO": ["00001"]}), pd.DataFrame(), pd.DataFrame()),
    )

    with pytest.raises(ValueError, match="Colunas sobrepostas"):
        modulo.analisar_area(
            Path("micro.zip"), Path("conceito.xlsx"), ENADE_2017, BIOLOGIA_BACHARELADO_2017
        )


def test_salvar_resultado_nao_grava_tabela_individual(tmp_path):
    resultado = modulo.ResultadoArea(
        pd.DataFrame({"CO_CURSO": ["00001"]}),
        pd.DataFrame({"CO_CURSO": ["00001"], "em_microdados": [True]}),
        pd.DataFrame([{"fonte": "conceito.xlsx"}]),
    )

    arquivos = modulo.salvar_resultado_area(resultado, tmp_path)

    assert {arquivo.name for arquivo in arquivos} == {
        "base_cursos.csv", "auditoria_cobertura.csv", "proveniencia_conceito.csv"
    }
    assert (tmp_path / "base_cursos.csv").exists()
