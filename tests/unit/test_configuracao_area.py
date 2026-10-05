import pytest

from src.core.configuracao_area import (
    BIOLOGIA,
    BIOLOGIA_BACHARELADO_2017,
    QUIMICA,
    AREAS,
    AplicabilidadeArea,
    ConfiguracaoArea,
    obter_area,
    validar_compatibilidade_area,
)
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS


def test_configuracao_quimica():
    assert QUIMICA.co_grupo == 1502
    assert QUIMICA.co_ies_focal == 569
    assert QUIMICA.edicao == 2025
    assert AREAS["quimica"] is QUIMICA


def test_configuracao_remove_espacos():
    area = ConfiguracaoArea(" teste ", " Área ", 1)
    assert area.slug == "teste"
    assert area.nome == "Área"


@pytest.mark.parametrize("campo", ["slug", "nome"])
def test_configuracao_rejeita_texto_vazio(campo):
    valores = {"slug": "teste", "nome": "Teste", "co_grupo": 1}
    valores[campo] = " "
    with pytest.raises(ValueError):
        ConfiguracaoArea(**valores)


@pytest.mark.parametrize("valor", [0, -1, 1.5, True])
def test_configuracao_rejeita_codigo_invalido(valor):
    with pytest.raises(ValueError):
        ConfiguracaoArea("teste", "Teste", valor)


def test_obter_area_normaliza_slug():
    assert obter_area(2025, " QUIMICA ") is QUIMICA


def test_obter_area_rejeita_slug_desconhecido():
    with pytest.raises(KeyError, match="Área desconhecida na edição 2025"):
        obter_area(2025, "inexistente")


def test_resolucao_de_area_exige_a_edicao_correta():
    assert obter_area(2017, "biologia_bacharelado") is BIOLOGIA_BACHARELADO_2017
    assert obter_area(2025, "biologia") is BIOLOGIA

    with pytest.raises(KeyError, match="edição 2017"):
        obter_area(2017, "biologia")
    with pytest.raises(KeyError, match="edição 2025"):
        obter_area(2025, "biologia_bacharelado")


def test_capacidade_da_edicao_nao_implica_aplicabilidade_na_area():
    assert ENADE_2017.capacidades.questionario_licenciatura
    assert not BIOLOGIA_BACHARELADO_2017.aplicabilidade.questionario_licenciatura
    validar_compatibilidade_area(ENADE_2017, BIOLOGIA_BACHARELADO_2017)


def test_compatibilidade_rejeita_recurso_que_edicao_nao_suporta():
    area = ConfiguracaoArea(
        "teste",
        "Teste",
        9999,
        edicao=2017,
        aplicabilidade=AplicabilidadeArea(proficiencia=True),
    )
    with pytest.raises(ValueError, match="proficiencia"):
        validar_compatibilidade_area(ENADE_2017, area)


def test_compatibilidade_rejeita_area_de_outra_edicao():
    with pytest.raises(ValueError, match="pertence a 2025"):
        validar_compatibilidade_area(ENADE_2017, QUIMICA)

    validar_compatibilidade_area(ENADE_2025_LICENCIATURAS, QUIMICA)
