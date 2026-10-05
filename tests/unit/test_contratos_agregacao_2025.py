from __future__ import annotations

from pathlib import Path

import pandas as pd

import src.agregacao.agregar_demografia as modulo_demografia
import src.agregacao.agregar_desempenho as modulo_desempenho
import src.agregacao.agregar_processo_formativo as modulo_processo
import src.agregacao.agregar_recomendacao as modulo_recomendacao
import src.agregacao.agregar_socioeconomico as modulo_socioeconomico
import src.agregacao.agregar_trajetoria as modulo_trajetoria


CAMINHO_SINTETICO = Path("fonte_sintetica.txt")


def test_contrato_legado_desempenho_2025(monkeypatch):
    dados = pd.DataFrame(
        {
            "CO_CURSO": [1, 1, 2],
            "IN_REAPLICACAO": [0, 1, 0],
            "TP_PRES": [555, 222, 555],
            "TP_SIT_DISC": [555, 333, 555],
            "NT_GER": [50, pd.NA, 70],
            "NT_OBJ": [45, pd.NA, 65],
            "NT_DIS": [55, pd.NA, 75],
            "PROFICIENCIA": [1, pd.NA, 2],
            "QT_ACERTOS": [20, pd.NA, 30],
        }
    )
    monkeypatch.setattr(modulo_desempenho, "carregar_filtrado", lambda *args, **kwargs: dados.copy())

    agregado, individual = modulo_desempenho.agregar_desempenho(CAMINHO_SINTETICO, [1, 2])

    curso_1 = agregado.set_index("CO_CURSO").loc[1]
    assert agregado["CO_CURSO"].is_unique
    assert curso_1["registros_microdados"] == 2
    assert curso_1["presentes_validos"] == 1
    assert curso_1["nt_ger_count"] == 1
    assert set(individual["CO_CURSO"]) == {1, 2}


def test_contrato_legado_demografia_2025(monkeypatch):
    def carregar(_path, _cursos, usecols=None):
        if usecols == ["CO_CURSO", "TP_SEXO"]:
            return pd.DataFrame({"CO_CURSO": [1, 1, 2], "TP_SEXO": ["F", "M", "F"]})
        return pd.DataFrame({"CO_CURSO": [1, 1, 2], "NU_IDADE": [20, 22, 30]})

    monkeypatch.setattr(modulo_demografia, "carregar_filtrado", carregar)

    agregado, distribuicao = modulo_demografia.agregar_demografia(
        CAMINHO_SINTETICO, CAMINHO_SINTETICO, [1, 2]
    )

    assert agregado["CO_CURSO"].is_unique
    assert agregado.set_index("CO_CURSO").loc[1, "sexo_feminino_pct"] == 0.5
    assert agregado.set_index("CO_CURSO").loc[1, "idade_media"] == 21
    assert not distribuicao.empty


def test_contrato_legado_trajetoria_usa_2025_quando_explicitado(monkeypatch):
    dados = pd.DataFrame(
        {
            "CO_CURSO": [1, 1],
            "ANO_FIM_EM": [2018, 2019],
            "ANO_IN_GRAD": [2020, 2021],
            "CO_TURNO_GRADUACAO": [1, 4],
        }
    )
    monkeypatch.setattr(modulo_trajetoria, "carregar_filtrado", lambda *args, **kwargs: dados.copy())

    agregado, _ = modulo_trajetoria.agregar_trajetoria(
        CAMINHO_SINTETICO, [1], ano_referencia=2025
    )

    curso = agregado.iloc[0]
    assert curso["anos_desde_ingresso_media"] == 4.5
    assert curso["turno_noturno_pct"] == 0.5


def test_contrato_legado_socioeconomico_2025(monkeypatch):
    def carregar(_path, _cursos, usecols=None):
        variavel = usecols[-1]
        respostas = ["A", "B"] if variavel == "QE_I05" else ["A", "A"]
        return pd.DataFrame({"CO_CURSO": [1, 1], variavel: respostas})

    monkeypatch.setattr(modulo_socioeconomico, "carregar_filtrado", carregar)

    agregado, distribuicoes, regras = modulo_socioeconomico.agregar_socioeconomico(
        Path("pasta_sintetica"), [1]
    )

    assert agregado["CO_CURSO"].is_unique
    assert agregado.loc[0, "primeira_geracao_pct"] == 0.5
    assert set(distribuicoes["VARIAVEL"]) == {f"QE_I{i:02d}" for i in range(1, 20)}
    assert "primeira_geracao_pct" in set(regras["indicador"])


def test_contrato_legado_processo_formativo_2025(monkeypatch):
    dados = {"CO_CURSO": [1] * 10}
    dados.update({item: [(indice % 6) + 1 for indice in range(10)] for item in modulo_processo.ITENS})
    monkeypatch.setattr(
        modulo_processo,
        "carregar_filtrado",
        lambda *args, **kwargs: pd.DataFrame(dados),
    )

    agregado, itens, diagnostico = modulo_processo.agregar_processo_formativo(
        CAMINHO_SINTETICO, [1]
    )

    assert agregado["CO_CURSO"].is_unique
    assert len(itens) == 47
    assert diagnostico.loc[0, "n_itens"] == 47
    assert diagnostico.loc[0, "escala"].startswith("QE_I20-QE_I66")


def test_contrato_legado_recomendacao_2025(monkeypatch):
    def carregar(_path, _cursos, usecols=None):
        variavel = usecols[-1]
        respostas = [8, 10] if variavel in {"QE_I68", "QE_I69"} else ["A", "F"]
        return pd.DataFrame({"CO_CURSO": [1, 1], variavel: respostas})

    monkeypatch.setattr(modulo_recomendacao, "carregar_filtrado", carregar)

    agregado, distribuicoes = modulo_recomendacao.agregar_recomendacao(
        CAMINHO_SINTETICO, CAMINHO_SINTETICO, CAMINHO_SINTETICO, [1]
    )

    assert agregado["CO_CURSO"].is_unique
    assert agregado.loc[0, "qe_i68_media"] == 9
    assert agregado.loc[0, "qe_i70_interesse_pct"] == 0.5
    assert set(distribuicoes["VARIAVEL"]) == {"QE_I68", "QE_I69", "QE_I70"}
