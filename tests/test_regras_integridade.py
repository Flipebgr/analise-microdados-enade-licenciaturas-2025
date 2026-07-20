import pandas as pd
import pytest
from src.validacao.validar_relacionamentos import validar_join_agregado
from src.utilitarios.normalizacao import situacao_conceito


def test_sem_conceito_nao_e_conceito_1():
    assert situacao_conceito("SC") == "Sem conceito"
    assert situacao_conceito(None) == "Sem conceito"


def test_join_muitos_para_muitos_e_bloqueado():
    a = pd.DataFrame({"CO_CURSO": [1, 1], "x": [1, 2]})
    b = pd.DataFrame({"CO_CURSO": [1], "y": [3]})
    with pytest.raises(ValueError):
        validar_join_agregado(a, b)
