from __future__ import annotations

import pytest

from src.analise.contratos_fase_9a import (
    NIVEIS_RELAXAMENTO_BENCHMARK,
    ConfiguracaoBootstrap,
    CriterioBenchmark,
    EstadoElegibilidade,
    PoliticaElegibilidade,
    PoliticaTamanhoBenchmark,
    classificar_elegibilidade,
    seed_para_contraste,
)
from src.core.configuracao_area import BIOLOGIA_BACHARELADO_2017


@pytest.mark.parametrize(
    ("n_total", "n_valido", "estado", "motivo"),
    [
        (0, 0, EstadoElegibilidade.INSUFICIENTE_COBERTURA, "denominador_zero"),
        (20, 9, EstadoElegibilidade.INSUFICIENTE_COBERTURA, "cobertura_abaixo_do_minimo"),
        (18, 9, EstadoElegibilidade.BAIXO_N, "n_valido_abaixo_do_minimo"),
        (20, 10, EstadoElegibilidade.ELEGIVEL, None),
        (20, 18, EstadoElegibilidade.ELEGIVEL, None),
    ],
)
def test_elegibilidade_aplica_primeiro_cobertura_depois_n(n_total, n_valido, estado, motivo):
    resultado = classificar_elegibilidade(
        n_total,
        n_valido,
        PoliticaElegibilidade(n_minimo=10),
    )

    assert resultado.estado == estado
    assert resultado.motivo == motivo


def test_niveis_de_relaxamento_preservam_modalidade_e_ordem_aprovada():
    assert [nivel.ordem for nivel in NIVEIS_RELAXAMENTO_BENCHMARK] == [1, 2, 3, 4]
    assert [nivel.criterio for nivel in NIVEIS_RELAXAMENTO_BENCHMARK] == [
        CriterioBenchmark.MODALIDADE_CATEGORIA_ORGANIZACAO_PORTE_75_125,
        CriterioBenchmark.MODALIDADE_CATEGORIA_ORGANIZACAO_PORTE_50_200,
        CriterioBenchmark.MODALIDADE_CATEGORIA_PORTE_50_200,
        CriterioBenchmark.MODALIDADE_PORTE_50_200,
    ]
    assert all(nivel.limite_inferior_porte > 0 for nivel in NIVEIS_RELAXAMENTO_BENCHMARK)


def test_politica_de_tamanho_documenta_limites_operacionais():
    politica = PoliticaTamanhoBenchmark()

    assert politica.n_minimo_sintese == 5
    assert politica.n_minimo_completo == 10
    assert politica.versao == "fase_9a_n_v1"


def test_foco_do_piloto_preserva_codigo_oficial_textual():
    assert BIOLOGIA_BACHARELADO_2017.co_ies_focal == 569
    assert BIOLOGIA_BACHARELADO_2017.co_cursos_focais == ("12027",)


def test_bootstrap_e_seed_por_contraste_sao_deterministicos():
    configuracao = ConfiguracaoBootstrap()

    assert configuracao.numero_reamostragens == 5_000
    assert configuracao.seed_base == 20250901
    assert configuracao.unidade_reamostragem == "CO_CURSO"
    assert seed_para_contraste("2017:biologia:12027:amplo_para:geral_mean") == seed_para_contraste(
        "2017:biologia:12027:amplo_para:geral_mean"
    )
    assert seed_para_contraste("contraste-a") != seed_para_contraste("contraste-b")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"cobertura_minima": 0},
        {"cobertura_minima": 1.1},
        {"n_minimo": 0},
    ],
)
def test_politica_elegibilidade_rejeita_limites_invalidos(kwargs):
    with pytest.raises(ValueError):
        PoliticaElegibilidade(**kwargs)


def test_classificador_rejeita_denominadores_incoerentes():
    with pytest.raises(ValueError, match="Denominadores inválidos"):
        classificar_elegibilidade(n_total=5, n_valido=6)


def test_bootstrap_rejeita_unidade_diferente_de_curso():
    with pytest.raises(ValueError, match="CO_CURSO"):
        ConfiguracaoBootstrap(unidade_reamostragem="estudante")
