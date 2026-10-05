from __future__ import annotations

import pytest

from src.configuracao.caminhos import carregar_config, carregar_config_area, carregar_config_edicao


def test_configuracao_legada_de_2025_permanece_disponivel():
    config = carregar_config()

    assert config["projeto"]["ano"] == 2025
    assert config["arquivos"]["zip_microdados"].endswith("microdados_enade_licenciaturas_2025.zip")


def test_configuracao_de_edicao_separa_fontes_e_destinos():
    config_2017 = carregar_config_edicao(2017)
    config_2025 = carregar_config_edicao(2025)

    assert config_2017["arquivos"]["pasta_extraida"] == "dados_extraidos/enade_2017"
    assert config_2025["arquivos"]["pasta_extraida"] == "dados_extraidos/enade_2025"
    assert config_2017["leitura_txt"]["decimal"] == "."
    assert config_2025["leitura_txt"]["decimal"] == ","


def test_configuracao_de_area_e_resolvida_dentro_da_edicao():
    area = carregar_config_area(2017, " BIOLOGIA_BACHARELADO ")

    assert area["co_grupo"] == 1601
    assert area["grau"] == "Bacharelado"
    assert not area["aplicabilidade"]["questionario_licenciatura"]

    with pytest.raises(KeyError, match="edição 2025"):
        carregar_config_area(2025, "biologia_bacharelado")


def test_edicao_desconhecida_falha_sem_fallback():
    with pytest.raises(KeyError, match="Edição não configurada"):
        carregar_config_edicao(1999)
