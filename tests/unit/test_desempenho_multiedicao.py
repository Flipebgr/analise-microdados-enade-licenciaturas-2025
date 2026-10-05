from __future__ import annotations

from pathlib import Path

import pandas as pd

import src.agregacao.agregar_desempenho as modulo
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS


def test_desempenho_2017_mantem_fg_e_ce_separados(monkeypatch):
    dados = pd.DataFrame(
        {
            "CO_CURSO": ["12027", "12027", "12027", "12027", "900"],
            "TP_PRES": ["555", "222", "556", "555", "555"],
            "NT_GER": ["50", ".", "60", ".", "40"],
            "NT_FG": ["80", ".", "20", ".", "30"],
            "NT_OBJ_FG": ["70", ".", "30", ".", "20"],
            "NT_DIS_FG": ["90", ".", "10", ".", "40"],
            "NT_CE": ["40", ".", "70", ".", "50"],
            "NT_OBJ_CE": ["35", ".", "65", ".", "45"],
            "NT_DIS_CE": ["45", ".", "75", ".", "55"],
        }
    )
    monkeypatch.setattr(modulo, "carregar_filtrado_edicao", lambda *args, **kwargs: dados.copy())

    agregado, individual = modulo.agregar_desempenho_edicao(
        Path("sintetico.zip"), ENADE_2017, ["12027", "900"]
    )
    curso = agregado.set_index("CO_CURSO").loc["12027"]

    assert agregado["CO_CURSO"].is_unique
    assert curso["registros_microdados"] == 4
    assert curso["presentes_validos"] == 2
    assert curso["tp_pres_556_n"] == 1
    assert curso["formacao_geral_total_mean"] == 80
    assert curso["componente_especifico_total_mean"] == 40
    assert curso["geral_n_valido"] == 1
    assert curso["geral_n_ausente"] == 3
    assert curso["geral_n_presente_sem_nota"] == 1
    assert curso["geral_n_nota_fora_presenca_valida"] == 1
    assert "proficiencia_n_valido" not in agregado.columns
    assert "objetiva_mean" not in agregado.columns
    assert {"NT_FG", "NT_CE"} <= set(individual.columns)


def test_desempenho_2025_expoe_apenas_componentes_disponiveis(monkeypatch):
    dados = pd.DataFrame(
        {
            "CO_CURSO": ["1", "1", "1"],
            "TP_PRES": ["555", "222", "999"],
            "NT_GER": ["50,5", ".", "60,5"],
            "NT_OBJ": ["40", ".", "60"],
            "NT_DIS": ["60", ".", "70"],
            "PROFICIENCIA": ["1", ".", "2"],
            "QT_ACERTOS": ["20", ".", "30"],
        }
    )
    monkeypatch.setattr(modulo, "carregar_filtrado_edicao", lambda *args, **kwargs: dados.copy())

    agregado, _ = modulo.agregar_desempenho_edicao(
        Path("sintetico.zip"), ENADE_2025_LICENCIATURAS, ["1"]
    )
    curso = agregado.iloc[0]

    assert curso["geral_mean"] == 50.5
    assert curso["objetiva_mean"] == 40
    assert curso["geral_n_nota_fora_presenca_valida"] == 1
    assert curso["tp_pres_codigo_nao_mapeado_n"] == 1
    assert curso["presentes_validos"] == 1
    assert "formacao_geral_total_mean" not in agregado.columns
    assert "componente_especifico_total_mean" not in agregado.columns


def test_curso_sem_nota_valida_permanece_na_base_agregada(monkeypatch):
    dados = pd.DataFrame(
        {
            "CO_CURSO": ["7", "7"],
            "TP_PRES": ["222", "444"],
            **{variavel: [".", "."] for variavel in ENADE_2017.desempenho.variaveis_numericas},
        }
    )
    monkeypatch.setattr(modulo, "carregar_filtrado_edicao", lambda *args, **kwargs: dados.copy())

    agregado, _ = modulo.agregar_desempenho_edicao(
        Path("sintetico.zip"), ENADE_2017, ["7"]
    )

    assert agregado["CO_CURSO"].tolist() == ["7"]
    assert agregado.loc[0, "registros_microdados"] == 2
    assert agregado.loc[0, "presentes_validos"] == 0
    assert agregado.loc[0, "geral_n_valido"] == 0
    assert agregado.loc[0, "geral_n_ausente"] == 2
    assert pd.isna(agregado.loc[0, "geral_mean"])
