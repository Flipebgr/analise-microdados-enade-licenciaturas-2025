import pandas as pd
import pytest

from src.core.juncoes import juntar_por_curso, validar_unicidade_por_curso


def test_juncao_um_para_um_preserva_ordem_esquerda():
    esquerda = pd.DataFrame({"CO_CURSO": [2, 1], "A": [20, 10]})
    direita = pd.DataFrame({"CO_CURSO": [1, 2], "B": [100, 200]})
    resultado = juntar_por_curso(esquerda, direita)
    assert resultado["CO_CURSO"].tolist() == [2, 1]
    assert resultado["B"].tolist() == [200, 100]


@pytest.mark.parametrize("lado", ["esquerda", "direita", "ambos"])
def test_juncao_rejeita_duplicidade(lado):
    esquerda = pd.DataFrame({"CO_CURSO": [1, 2], "A": [10, 20]})
    direita = pd.DataFrame({"CO_CURSO": [1, 2], "B": [100, 200]})
    if lado in {"esquerda", "ambos"}:
        esquerda.loc[1, "CO_CURSO"] = 1
    if lado in {"direita", "ambos"}:
        direita.loc[1, "CO_CURSO"] = 1
    with pytest.raises(ValueError, match="duplicados"):
        juntar_por_curso(esquerda, direita)


def test_juncao_rejeita_chave_ausente():
    esquerda = pd.DataFrame({"OUTRA": [1]})
    direita = pd.DataFrame({"CO_CURSO": [1]})
    with pytest.raises(ValueError, match="coluna obrigatória"):
        juntar_por_curso(esquerda, direita)


def test_juncao_rejeita_chave_nula():
    tabela = pd.DataFrame({"CO_CURSO": [1, None]})
    with pytest.raises(ValueError, match="ausente"):
        validar_unicidade_por_curso(tabela, nome="teste")


def test_juncao_aplica_sufixo_em_coluna_sobreposta():
    esquerda = pd.DataFrame({"CO_CURSO": [1], "VALOR": [10]})
    direita = pd.DataFrame({"CO_CURSO": [1], "VALOR": [20]})
    resultado = juntar_por_curso(esquerda, direita)
    assert resultado.loc[0, "VALOR"] == 10
    assert resultado.loc[0, "VALOR_direita"] == 20


def test_juncao_nao_altera_entradas():
    esquerda = pd.DataFrame({"CO_CURSO": [1], "A": [10]})
    direita = pd.DataFrame({"CO_CURSO": [1], "B": [20]})
    copia_esquerda = esquerda.copy(deep=True)
    copia_direita = direita.copy(deep=True)
    juntar_por_curso(esquerda, direita)
    pd.testing.assert_frame_equal(esquerda, copia_esquerda)
    pd.testing.assert_frame_equal(direita, copia_direita)
