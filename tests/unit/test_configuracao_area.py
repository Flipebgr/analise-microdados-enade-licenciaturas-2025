import pytest

from src.core.configuracao_area import INGLES, ConfiguracaoArea, obter_area


def test_configuracao_ingles():
    assert INGLES.co_grupo == 6407
    assert INGLES.co_ies_focal == 569


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
    assert obter_area(" INGLES ") is INGLES


def test_obter_area_rejeita_slug_desconhecido():
    with pytest.raises(KeyError, match="Área desconhecida"):
        obter_area("inexistente")
