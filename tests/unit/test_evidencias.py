from __future__ import annotations

import json

import pandas as pd
import pytest

from src.core.configuracao_area import BIOLOGIA_BACHARELADO_2017
from src.edicoes import ENADE_2017
from src.evidencias import construir_evidencias, salvar_evidencias, validar_evidencias
from src.orquestracao.area import ResultadoArea


def _resultado() -> ResultadoArea:
    base = pd.DataFrame({
        "edicao": [2017, 2017], "area": ["biologia_bacharelado"] * 2,
        "CO_CURSO": ["00001", "00002"], "CO_GRUPO": ["1601", "1601"],
        "CO_IES": ["569", "9"], "CO_MUNIC_CURSO": ["1501402", "1501402"],
        "CO_UF_CURSO": ["15", "15"], "CO_REGIAO_CURSO": ["1", "1"],
        "CO_MODALIDADE": ["1", "1"], "INSCRITOS": [23, 10], "PARTICIPANTES": [13, 5],
        "CONCEITO_ENADE_ORIGINAL": ["3", "SC"],
        "CONCEITO_ENADE_NUM": pd.array([3, pd.NA], dtype="Int64"),
        "CONCEITO_ENADE_CONTINUO": pd.array([2.5, pd.NA], dtype="Float64"),
        "SITUACAO_CONCEITO": ["com_conceito", "sem_conceito"],
        "registros_microdados": [23, 10], "presentes_validos": [13, 5],
        "taxa_presenca_microdados": [13 / 23, 0.5], "geral_mean": [51.2, 60.0],
        "primeira_geracao_pct": [0.3, 0.4], "primeira_geracao_n_valido": [10, 8],
    })
    itens = pd.DataFrame({
        "edicao": [2017], "CO_CURSO": ["00001"], "ITEM": ["QE_I27"],
        "n_total": [10], "n_valido": [7], "n_ausente": [1], "n_invalido": [0],
        "n_nao_sabe_responder": [1], "n_nao_se_aplica": [1], "media": [4.0],
        "mediana": [4.0], "dp": [1.0], "concordancia_n": [5],
        "concordancia_pct": [5 / 7], "ausencia_analitica_pct": [0.3],
        "nao_sabe_responder_pct": [0.1], "nao_se_aplica_pct": [0.1],
    })
    return ResultadoArea(
        base,
        pd.DataFrame({"CO_CURSO": ["00001", "00002"], "em_microdados": [True, True], "em_conceito": [True, True], "em_desempenho": [True, True]}),
        pd.DataFrame([{"fonte": "conceitos.xlsx", "sha256": "a" * 64}]),
        processo_itens=itens,
        proveniencia_processo=pd.DataFrame([{"item": "QE_I27", "denominador_codigos_especiais": "n_total"}]),
        distribuicoes_questionario=pd.DataFrame([{"CO_CURSO": "00001", "item": "QE_I21", "n": 2}]),
        regras_indicadores=pd.DataFrame([{"indicador": "primeira_geracao_pct", "denominador": "n_valido"}]),
    )


def test_construtor_preserva_proveniencia_e_regras_de_codigos_especiais(tmp_path):
    fonte = tmp_path / "micro.zip"
    fonte.write_bytes(b"fonte oficial sintetica")

    pacote = construir_evidencias(_resultado(), ENADE_2017, BIOLOGIA_BACHARELADO_2017, fonte)

    assert pacote["schema_version"] == "1.0"
    assert pacote["universo"]["n_cursos_base"] == 2
    assert pacote["ofertas_focais"][0]["CO_CURSO"] == "00001"
    assert pacote["ofertas_focais"][0]["CONCEITO_ENADE_NUM"] == 3
    assert pacote["perfil"]["regras"][0]["indicador"] == "primeira_geracao_pct"
    processo = pacote["processo_formativo"]["itens_por_curso"][0]
    assert processo["nao_sabe_responder_pct"] == pytest.approx(0.1)
    assert processo["nao_se_aplica_pct"] == pytest.approx(0.1)
    assert pacote["benchmarks"]["disponivel"] is False
    assert pacote["alertas"] == []


def test_validador_rejeita_denominador_especial_incorreto(tmp_path):
    fonte = tmp_path / "micro.zip"
    fonte.write_bytes(b"fonte oficial sintetica")
    pacote = construir_evidencias(_resultado(), ENADE_2017, BIOLOGIA_BACHARELADO_2017, fonte)
    pacote["processo_formativo"]["itens_por_curso"][0]["nao_se_aplica_pct"] = 0.2

    with pytest.raises(ValueError, match="n_total"):
        validar_evidencias(pacote)


def test_salvar_evidencias_produz_json_sem_nan(tmp_path):
    fonte = tmp_path / "micro.zip"
    fonte.write_bytes(b"fonte oficial sintetica")
    pacote = construir_evidencias(_resultado(), ENADE_2017, BIOLOGIA_BACHARELADO_2017, fonte)

    destino = salvar_evidencias(pacote, tmp_path / "evidencias.json")

    assert destino.exists()
    carregado = json.loads(destino.read_text(encoding="utf-8"))
    assert carregado["ofertas_focais"][0]["CONCEITO_ENADE_NUM"] == 3
    assert "NaN" not in destino.read_text(encoding="utf-8")
