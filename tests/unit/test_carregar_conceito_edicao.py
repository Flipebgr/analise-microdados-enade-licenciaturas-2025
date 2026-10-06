from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import src.edicoes.conceito as modulo
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS


def _planilha(edicao, conceitos: list[str | None]) -> pd.DataFrame:
    dados = pd.DataFrame({
        origem: [pd.NA] * len(conceitos)
        for origem, _ in edicao.conceito.mapa_colunas
    })
    mapa = {destino: origem for origem, destino in edicao.conceito.mapa_colunas}
    dados[mapa["NU_ANO"]] = str(edicao.ano)
    for coluna in ("CO_GRUPO", "CO_IES", "CO_MUNIC_CURSO"):
        dados[mapa[coluna]] = "100"
    dados[mapa["CO_CURSO"]] = [f"{numero:05d}" for numero in range(1, len(conceitos) + 1)]
    for coluna in edicao.conceito.colunas_numericas:
        dados[mapa[coluna]] = "1"
    dados[mapa["INSCRITOS"]] = "23"
    dados[mapa["PARTICIPANTES"]] = "13"
    dados[mapa["CONCEITO_ENADE_ORIGINAL"]] = conceitos
    return dados


def _simular_leitura(monkeypatch, dados: pd.DataFrame) -> None:
    monkeypatch.setattr(modulo.pd, "read_excel", lambda *args, **kwargs: dados.copy())
    monkeypatch.setattr(modulo, "_sha256", lambda _: "a" * 64)


def test_loader_preserva_fonte_codigos_e_situacoes_distintas(monkeypatch):
    dados = _planilha(ENADE_2017, ["3", "SC", None])
    origem_curso = ENADE_2017.conceito.coluna_origem("CO_CURSO")
    origem_continuo = ENADE_2017.conceito.coluna_origem("CONCEITO_ENADE_CONTINUO")
    dados.loc[0, origem_continuo] = "2.5"
    _simular_leitura(monkeypatch, dados)

    normalizado, original, proveniencia = modulo.carregar_conceitos_edicao(
        Path("sintetico.xlsx"), ENADE_2017
    )

    assert original.equals(dados)
    assert original.loc[0, origem_curso] == "00001"
    assert normalizado["CO_CURSO"].tolist() == ["00001", "00002", "00003"]
    assert normalizado["INSCRITOS"].tolist() == [23, 23, 23]
    assert normalizado["CONCEITO_ENADE_CONTINUO"].iloc[0] == pytest.approx(2.5)
    assert normalizado["CONCEITO_ENADE_NUM"].iloc[0] == 3
    assert pd.isna(normalizado["CONCEITO_ENADE_NUM"].iloc[1])
    assert pd.isna(normalizado["CONCEITO_ENADE_NUM"].iloc[2])
    assert normalizado["SITUACAO_CONCEITO"].tolist() == [
        "com_conceito", "sem_conceito", "ausente"
    ]
    assert proveniencia.loc[0, "n_linhas_nao_dados"] == 0
    assert proveniencia.loc[0, "sha256"] == "a" * 64


def test_loader_2025_separa_rodape_de_oferta_sem_criar_conceito_continuo(monkeypatch):
    dados = _planilha(ENADE_2025_LICENCIATURAS, ["SC"])
    rodape = {coluna: pd.NA for coluna in dados.columns}
    rodape[ENADE_2025_LICENCIATURAS.conceito.coluna_origem("NU_ANO")] = "Nota da fonte"
    dados = pd.concat([dados, pd.DataFrame([rodape])], ignore_index=True)
    _simular_leitura(monkeypatch, dados)

    normalizado, original, proveniencia = modulo.carregar_conceitos_edicao(
        Path("sintetico.xlsx"), ENADE_2025_LICENCIATURAS
    )

    assert len(original) == 2
    assert len(normalizado) == 1
    assert normalizado.loc[0, "SITUACAO_CONCEITO"] == "sem_conceito"
    assert pd.isna(normalizado.loc[0, "CONCEITO_ENADE_CONTINUO"])
    assert proveniencia.loc[0, "n_linhas_nao_dados"] == 1


@pytest.mark.parametrize("defeito", [
    "sem_coluna", "curso_duplicado", "curso_parcial", "ano_errado",
    "numero_invalido", "contagem_fracionaria", "contagem_negativa",
])
def test_loader_falha_em_schema_e_registros_incoerentes(monkeypatch, defeito):
    dados = _planilha(ENADE_2017, ["3", "SC"])
    schema = ENADE_2017.conceito
    coluna_curso = schema.coluna_origem("CO_CURSO")
    if defeito == "sem_coluna":
        dados = dados.drop(columns=schema.coluna_origem("INSCRITOS"))
    elif defeito == "curso_duplicado":
        dados.loc[1, coluna_curso] = dados.loc[0, coluna_curso]
    elif defeito == "curso_parcial":
        dados.loc[1, coluna_curso] = pd.NA
    elif defeito == "ano_errado":
        dados.loc[1, schema.coluna_origem("NU_ANO")] = "2025"
    elif defeito == "contagem_fracionaria":
        dados.loc[1, schema.coluna_origem("INSCRITOS")] = "1,5"
    elif defeito == "contagem_negativa":
        dados.loc[1, schema.coluna_origem("INSCRITOS")] = "-1"
    else:
        dados.loc[1, schema.coluna_origem("INSCRITOS")] = "x"
    _simular_leitura(monkeypatch, dados)

    with pytest.raises(ValueError):
        modulo.carregar_conceitos_edicao(Path("sintetico.xlsx"), ENADE_2017)


def test_loader_mantem_participantes_ausentes_sem_inventar_zero(monkeypatch):
    dados = _planilha(ENADE_2025_LICENCIATURAS, ["SC"])
    dados.loc[0, ENADE_2025_LICENCIATURAS.conceito.coluna_origem("PARTICIPANTES")] = pd.NA
    _simular_leitura(monkeypatch, dados)

    normalizado, _, _ = modulo.carregar_conceitos_edicao(
        Path("sintetico.xlsx"), ENADE_2025_LICENCIATURAS
    )

    assert pd.isna(normalizado.loc[0, "PARTICIPANTES"])
    assert normalizado.loc[0, "SITUACAO_CONCEITO"] == "sem_conceito"
