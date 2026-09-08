from __future__ import annotations

import pandas as pd

from src.core.validacao import validar_base_area
from src.educacao_fisica import EDUCACAO_FISICA
from src.validacao.validar_agregacoes import validar_percentuais
from src.validacao.validar_grupos import validar_grupos

CURSOS_UFPA_ESPERADOS = {21849, 104598}
CONTAGEM_GRUPOS_ESPERADA = {
    "B": 2,
    "C": 5,
    "D": 17,
    "E": 382,
}


def validar_base_educacao_fisica(base: pd.DataFrame) -> None:
    resultado = validar_base_area(
        base,
        EDUCACAO_FISICA,
        total_cursos_esperado=406,
        ofertas_ies_esperadas=2,
    )
    resultado.exigir_valido()

    validar_grupos(
        base,
        co_ies_focal=EDUCACAO_FISICA.co_ies_focal,
    )
    validar_percentuais(base)

    ufpa = base[
        base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)
    ].copy()
    cursos_ufpa = set(
        pd.to_numeric(ufpa["CO_CURSO"], errors="coerce")
        .dropna()
        .astype(int)
        .tolist()
    )
    if cursos_ufpa != CURSOS_UFPA_ESPERADOS:
        raise AssertionError(
            "Ofertas UFPA de Educação Física divergentes: "
            f"esperado {sorted(CURSOS_UFPA_ESPERADOS)}, "
            f"encontrado {sorted(cursos_ufpa)}"
        )

    conceitos = pd.to_numeric(
        ufpa["CONCEITO_ENADE_NUM"],
        errors="coerce",
    )
    if not conceitos.eq(4).all():
        raise AssertionError(
            "As duas ofertas UFPA localizadas devem ter Conceito Enade 4"
        )

    if ufpa["GRUPO_CODIGO"].eq("A").any():
        raise AssertionError(
            "Educação Física da UFPA não possui oferta Conceito Enade 1"
        )

    modalidades = pd.to_numeric(
        ufpa["CO_MODALIDADE"],
        errors="coerce",
    )
    if not modalidades.eq(1).all():
        raise AssertionError(
            "As duas ofertas UFPA localizadas devem ser presenciais"
        )

    contagem = (
        base["GRUPO_CODIGO"]
        .value_counts()
        .to_dict()
    )
    for grupo, esperado in CONTAGEM_GRUPOS_ESPERADA.items():
        encontrado = int(contagem.get(grupo, 0))
        if encontrado != esperado:
            raise AssertionError(
                f"Grupo {grupo}: esperado {esperado}, encontrado {encontrado}"
            )
