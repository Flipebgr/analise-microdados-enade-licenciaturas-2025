from __future__ import annotations

import pandas as pd
import pytest

from src.analise.consistencia_dimensoes import cronbach_alpha, diagnosticar_dimensoes


def test_codigos_especiais_e_invalidos_nao_entram_no_alpha_nem_nos_casos_completos():
    respostas = pd.DataFrame({
        "QE_I20": ["1", "2", "3", "7", "8", "0", "9", "1.5", "x", None],
        "QE_I21": ["1", "3", "2", "8", "7", "0", "9", "2", "4", "5"],
    })

    esperado = 2 / 3  # Alfa calculado somente nas três primeiras respostas válidas.
    assert cronbach_alpha(respostas) == pytest.approx(esperado)

    diagnostico = diagnosticar_dimensoes(respostas)
    organizacao = diagnostico.set_index("dimensao").loc["organizacao_didatico_pedagogica"]
    assert organizacao["n_itens"] == 2
    assert organizacao["n_casos_completos"] == 3
    assert organizacao["alpha_cronbach"] == pytest.approx(esperado)


def test_alpha_ausente_quando_exclusao_de_7_e_8_deixa_menos_de_tres_casos():
    respostas = pd.DataFrame({
        "QE_I20": ["1", "2", "7", "8"],
        "QE_I21": ["1", "2", "7", "8"],
    })

    assert pd.isna(cronbach_alpha(respostas))
    diagnostico = diagnosticar_dimensoes(respostas)
    organizacao = diagnostico.set_index("dimensao").loc["organizacao_didatico_pedagogica"]
    assert organizacao["n_casos_completos"] == 2
    assert pd.isna(organizacao["alpha_cronbach"])
