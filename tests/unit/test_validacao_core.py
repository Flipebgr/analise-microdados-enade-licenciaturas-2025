import pandas as pd

from src.core.configuracao_area import QUIMICA
from src.core.validacao import validar_base_area


def base_valida():
    return pd.DataFrame(
        {
            "CO_CURSO": [1, 2],
            "CO_IES": [569, 999],
            "CO_GRUPO": [1502, 1502],
            "CONCEITO_ENADE": [1, None],
        }
    )


def test_validacao_aprova_base_e_preserva_conceito_ausente():
    base = base_valida()
    resultado = validar_base_area(
        base,
        QUIMICA,
        total_cursos_esperado=2,
        ofertas_ies_esperadas=1,
    )
    assert resultado.valido
    assert resultado.total_ofertas_ies_focal == 1
    assert resultado.avisos
    assert pd.isna(base.loc[1, "CONCEITO_ENADE"])


def test_validacao_rejeita_grupo_incorreto():
    base = base_valida()
    base.loc[1, "CO_GRUPO"] = 702
    resultado = validar_base_area(base, QUIMICA)
    assert not resultado.valido
    assert any("CO_GRUPO incompatível" in erro for erro in resultado.erros)


def test_validacao_rejeita_contagens_divergentes():
    resultado = validar_base_area(
        base_valida(),
        QUIMICA,
        total_cursos_esperado=3,
        ofertas_ies_esperadas=2,
    )
    assert not resultado.valido
    assert len(resultado.erros) == 2


def test_validacao_rejeita_colunas_ausentes():
    resultado = validar_base_area(
        base_valida().drop(columns="CO_IES"),
        QUIMICA,
    )
    assert not resultado.valido
    assert resultado.total_ofertas_ies_focal == 0


def test_exigir_valido_levanta_erro():
    resultado = validar_base_area(base_valida(), QUIMICA, total_cursos_esperado=99)
    try:
        resultado.exigir_valido()
    except ValueError as exc:
        assert "Base inválida" in str(exc)
    else:
        raise AssertionError("Era esperado ValueError")
