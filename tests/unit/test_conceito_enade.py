from __future__ import annotations

import pandas as pd

from src.utilitarios.normalizacao import situacao_conceito


def test_conceito_1_tem_rotulo_proprio():
    assert situacao_conceito(1) == "Conceito 1"
    assert situacao_conceito("1") == "Conceito 1"


def test_conceitos_superiores_nao_sao_reclassificados_como_1():
    for valor in [2, 3, 4, 5]:
        assert situacao_conceito(valor) == "Conceito superior a 1"


def test_ausencia_de_conceito_permanece_sem_conceito():
    for valor in [None, pd.NA, "", "SC", "Sem conceito", "-"]:
        assert situacao_conceito(valor) == "Sem conceito"
