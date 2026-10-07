from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace

import pytest

from src.core.configuracao_area import BIOLOGIA_BACHARELADO_2017
from src.edicoes import ENADE_2017
from src.evidencias import construir_evidencias, salvar_evidencias, validar_evidencias
from tests.suporte_evidencias import resultado_sintetico
from src.evidencias.validar import BLOCOS


@pytest.fixture(scope="module")
def analise(tmp_path_factory):
    return resultado_sintetico(tmp_path_factory.mktemp("evidencias"))


@pytest.fixture
def pacote(analise):
    resultado, fonte, _, _ = analise
    return construir_evidencias(resultado, ENADE_2017, BIOLOGIA_BACHARELADO_2017, fonte)


def test_construtor_preserva_proveniencia_e_regras_de_codigos_especiais(pacote):

    assert pacote["schema_version"] == "2.0"
    assert pacote["universo"]["n_cursos_base"] == 2
    assert pacote["ofertas_focais"][0]["CO_CURSO"] == "00001"
    assert pacote["ofertas_focais"][0]["CONCEITO_ENADE_NUM"] == 3
    assert "primeira_geracao_pct" in {r["indicador"] for r in pacote["perfil"]["regras"]}
    processo = pacote["processo_formativo"]["itens_por_curso"][0]
    assert processo["nao_sabe_responder_pct"] == pytest.approx(0.1)
    assert processo["nao_se_aplica_pct"] == pytest.approx(0.1)
    assert pacote["benchmarks"]["disponivel"] is False
    assert pacote["alertas"] == []


def test_validador_rejeita_denominador_especial_incorreto(pacote):
    pacote["processo_formativo"]["itens_por_curso"][0]["nao_se_aplica_pct"] = 0.2

    with pytest.raises(ValueError, match="n_total"):
        validar_evidencias(pacote)


def test_salvar_evidencias_produz_json_sem_nan(tmp_path, pacote):

    destino = salvar_evidencias(pacote, tmp_path / "evidencias.json")

    assert destino.exists()
    carregado = json.loads(destino.read_text(encoding="utf-8"))
    assert carregado["ofertas_focais"][0]["CONCEITO_ENADE_NUM"] == 3
    assert "NaN" not in destino.read_text(encoding="utf-8")


@pytest.mark.parametrize("campo", ["concordancia_pct", "ausencia_analitica_pct", "nao_sabe_responder_pct", "nao_se_aplica_pct"])
@pytest.mark.parametrize("valor", [-0.1, 2.0, float("nan"), float("inf"), float("-inf"), True])
def test_processo_rejeita_proporcao_invalida(pacote, campo, valor):
    pacote["processo_formativo"]["itens_por_curso"][0][campo] = valor
    with pytest.raises(ValueError):
        validar_evidencias(pacote)


@pytest.mark.parametrize("mudanca", [
    {"n_ausente": -1}, {"n_total": 1}, {"n_valido": 11}, {"n_valido": 7.5},
    {"concordancia_n": 8}, {"concordancia_pct": 0.2}, {"ausencia_analitica_pct": 0.1},
    {"n_ausente": -1, "n_invalido": 2}, {"n_ausente": True},
])
def test_processo_rejeita_contagens_e_razoes_incoerentes(pacote, mudanca):
    pacote["processo_formativo"]["itens_por_curso"][0].update(mudanca)
    with pytest.raises(ValueError):
        validar_evidencias(pacote)


@pytest.mark.parametrize("bloco", sorted(BLOCOS))
def test_todos_blocos_sao_obrigatorios(pacote, bloco):
    del pacote[bloco]
    with pytest.raises(ValueError):
        validar_evidencias(pacote)


@pytest.mark.parametrize("bloco,campo", [("processo_formativo", "itens_por_curso"),
    ("participacao", "por_curso"), ("desempenho", "por_curso"),
    ("perfil", "indicadores_por_curso"), ("perfil", "distribuicoes")])
def test_referencia_a_curso_inexistente_rejeitada(pacote, bloco, campo):
    pacote[bloco][campo][0]["CO_CURSO"] = "99999"
    with pytest.raises(ValueError):
        validar_evidencias(pacote)


def test_processo_duplicado_ou_incompleto_rejeitado(pacote):
    for variante in ([], pacote["processo_formativo"]["itens_por_curso"][:-1],
                     pacote["processo_formativo"]["itens_por_curso"] * 2):
        copia = deepcopy(pacote)
        copia["processo_formativo"]["itens_por_curso"] = variante
        with pytest.raises(ValueError):
            validar_evidencias(copia)


def test_denominador_zero_exige_nulos(pacote):
    r = pacote["processo_formativo"]["itens_por_curso"][0]
    for campo in ("n_total", "n_valido", "n_ausente", "n_invalido", "n_nao_sabe_responder", "n_nao_se_aplica", "concordancia_n"):
        r[campo] = 0
    campos = ("concordancia_pct", "ausencia_analitica_pct", "nao_sabe_responder_pct", "nao_se_aplica_pct", "media", "mediana", "dp")
    r.update(dict.fromkeys(campos))
    validar_evidencias(pacote)
    for campo in campos:
        r[campo] = 0.0
        with pytest.raises(ValueError):
            validar_evidencias(pacote)
        r[campo] = None


def test_perfil_e_participacao_reconciliam_denominadores(pacote):
    for bloco, tabela, campo in (("perfil", "indicadores_por_curso", "primeira_geracao_pct"),
                                 ("participacao", "por_curso", "taxa_presenca_microdados")):
        copia = deepcopy(pacote)
        copia[bloco][tabela][0][campo] = 0.25
        with pytest.raises(ValueError):
            validar_evidencias(copia)


def test_participacao_preserva_medidas_distintas_e_sc(pacote):
    r = pacote["participacao"]["por_curso"][0]
    assert (r["INSCRITOS"], r["PARTICIPANTES"]) == (23, 13)
    assert (r["registros_microdados"], r["presentes_validos"]) == (10, 10)
    assert pacote["participacao"]["por_curso"][1]["CONCEITO_ENADE_NUM"] is None
    pacote["participacao"]["por_curso"][1]["CONCEITO_ENADE_NUM"] = 1
    with pytest.raises(ValueError, match="Conceito"):
        validar_evidencias(pacote)


def test_manifesto_rejeita_omissao_ou_fonte_nao_usada(pacote):
    for lista in ([], ["arquivo_nao_utilizado.txt"]):
        copia = deepcopy(pacote)
        copia["proveniencia"]["fontes"][0]["arquivos_tematicos"] = lista
        with pytest.raises(ValueError, match="Proveniência"):
            validar_evidencias(copia)


def test_processo_nao_aplicavel_e_explicito(analise):
    resultado, fonte, _, _ = analise
    resultado = deepcopy(resultado)
    resultado.processo_itens = resultado.proveniencia_processo = None
    area = replace(BIOLOGIA_BACHARELADO_2017, aplicabilidade=replace(
        BIOLOGIA_BACHARELADO_2017.aplicabilidade, processo_formativo=False))
    p = construir_evidencias(resultado, ENADE_2017, area, fonte)
    assert p["processo_formativo"]["status"] == "nao_aplicavel"
    assert p["processo_formativo"]["itens_por_curso"] == []
    assert ENADE_2017.nome_arquivo(4) not in p["proveniencia"]["fontes"][0]["arquivos_tematicos"]
    p["area"]["aplicabilidade"]["processo_formativo"] = True
    with pytest.raises(ValueError):
        validar_evidencias(p)


def test_capacidade_ausente_exige_aplicabilidade_compativel(analise):
    resultado, fonte, _, _ = analise
    edicao = replace(ENADE_2017, capacidades=replace(ENADE_2017.capacidades, processo_formativo=False))
    with pytest.raises(ValueError, match="Recursos não suportados"):
        construir_evidencias(resultado, edicao, BIOLOGIA_BACHARELADO_2017, fonte)
    resultado = deepcopy(resultado)
    resultado.processo_itens = resultado.proveniencia_processo = None
    area = replace(BIOLOGIA_BACHARELADO_2017, aplicabilidade=replace(
        BIOLOGIA_BACHARELADO_2017.aplicabilidade, processo_formativo=False))
    assert construir_evidencias(resultado, edicao, area, fonte)["processo_formativo"]["disponivel"] is False


@pytest.mark.parametrize("alterar", [
    lambda p: p["ofertas_focais"].clear(),
    lambda p: p["proveniencia"]["tabelas_auditaveis"].clear(),
    lambda p: p["desempenho"]["mapa_canonico"].clear(),
    lambda p: p["desempenho"]["por_curso"][0].pop("geral_mean"),
    lambda p: p["perfil"]["indicadores_por_curso"][0].pop("primeira_geracao_n_valido"),
    lambda p: p["perfil"]["distribuicoes"].clear(),
    lambda p: p["processo_formativo"]["proveniencia"].clear(),
])
def test_schema_interno_e_produtos_obrigatorios(pacote, alterar):
    alterar(pacote)
    with pytest.raises(ValueError):
        validar_evidencias(pacote)
