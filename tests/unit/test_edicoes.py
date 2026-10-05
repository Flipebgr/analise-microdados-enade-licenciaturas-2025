from __future__ import annotations

import math

import pytest

from src.edicoes import (
    ENADE_2017,
    ENADE_2025_LICENCIATURAS,
    SituacaoConceito,
    normalizar_conceito,
    obter_edicao,
)


def test_inventarios_e_parametros_de_leitura_sao_especificos_da_edicao():
    assert ENADE_2017.quantidade_arquivos == 42
    assert ENADE_2017.nome_arquivo(42) == "microdados2017_arq42.txt"
    assert ENADE_2017.leitura.decimal == "."

    assert ENADE_2025_LICENCIATURAS.quantidade_arquivos == 28
    assert ENADE_2025_LICENCIATURAS.nome_arquivo(28) == "microdados2025_arq28.txt"
    assert ENADE_2025_LICENCIATURAS.leitura.decimal == ","


def test_desempenho_2017_preserva_formacao_geral_e_componente_especifico():
    desempenho = ENADE_2017.desempenho

    assert desempenho.formacao_geral_objetiva == "NT_OBJ_FG"
    assert desempenho.formacao_geral_discursiva == "NT_DIS_FG"
    assert desempenho.componente_especifico_objetiva == "NT_OBJ_CE"
    assert desempenho.componente_especifico_discursiva == "NT_DIS_CE"
    assert desempenho.proficiencia is None
    assert desempenho.acertos is None
    assert set(desempenho.vetores_string) == {
        "DS_VT_GAB_OFG_FIN",
        "DS_VT_GAB_OCE_FIN",
        "DS_VT_ESC_OFG",
        "DS_VT_ACE_OFG",
        "DS_VT_ESC_OCE",
        "DS_VT_ACE_OCE",
    }


def test_capacidades_2017_nao_fabricam_indicadores_de_2025():
    assert not ENADE_2017.capacidades.proficiencia
    assert not ENADE_2017.capacidades.recomendacao
    assert ENADE_2017.capacidades.questionario_licenciatura
    assert ENADE_2017.questionario.itens_recomendacao == ()


def test_instrumentos_mantem_semanticas_separadas_por_edicao():
    regras_2017 = {
        regra.nome: regra.item for regra in ENADE_2017.questionario.regras_indicadores
    }
    regras_2025 = {
        regra.nome: regra.item
        for regra in ENADE_2025_LICENCIATURAS.questionario.regras_indicadores
    }

    assert regras_2017["primeira_geracao_pct"] == "QE_I21"
    assert regras_2025["primeira_geracao_pct"] == "QE_I05"
    assert ENADE_2017.questionario.itens_processo_formativo[0] == "QE_I27"
    assert ENADE_2017.questionario.itens_processo_formativo[-1] == "QE_I68"
    assert ENADE_2025_LICENCIATURAS.questionario.itens_processo_formativo[0] == "QE_I20"
    assert ENADE_2025_LICENCIATURAS.questionario.itens_processo_formativo[-1] == "QE_I66"


def test_modalidade_e_declarada_por_edicao():
    assert dict(ENADE_2017.modalidades) == {0: "EaD", 1: "Presencial"}
    assert dict(ENADE_2025_LICENCIATURAS.modalidades) == {0: "EaD", 1: "Presencial"}


@pytest.mark.parametrize("valor", [1, "3", "5.0"])
def test_conceito_numerico_fica_separado_do_valor_original(valor):
    resultado = normalizar_conceito(valor)

    assert resultado.conceito_numerico == int(float(valor))
    assert resultado.situacao is SituacaoConceito.COM_CONCEITO
    assert resultado.valor_original == valor


def test_sc_nao_ocupa_a_representacao_numerica_do_conceito():
    resultado = normalizar_conceito("SC")

    assert resultado.conceito_numerico is None
    assert resultado.situacao is SituacaoConceito.SEM_CONCEITO
    assert resultado.valor_original == "SC"


def test_ausente_e_valor_nao_reconhecido_tem_situacoes_distintas():
    assert normalizar_conceito(None).situacao is SituacaoConceito.AUSENTE
    assert normalizar_conceito(math.nan).situacao is SituacaoConceito.AUSENTE
    assert normalizar_conceito("ND").situacao is SituacaoConceito.NAO_RECONHECIDA


def test_schema_conceito_declara_tres_campos_independentes():
    schema = ENADE_2017.conceito

    assert schema.campo_valor_original == "CONCEITO_ENADE_ORIGINAL"
    assert schema.campo_conceito_numerico == "CONCEITO_ENADE_NUM"
    assert schema.campo_situacao == "SITUACAO_CONCEITO"
    assert schema.coluna_origem(schema.campo_valor_original) == "Conceito Enade (Faixa)"


def test_resolucao_de_edicao_nao_possui_fallback():
    assert obter_edicao(2017) is ENADE_2017
    assert obter_edicao(2025) is ENADE_2025_LICENCIATURAS
    with pytest.raises(KeyError, match="Edição desconhecida"):
        obter_edicao(1999)
