from __future__ import annotations

import pandas as pd

from src.core.validacao import validar_base_area
from src.musica import MUSICA
from src.validacao.validar_agregacoes import validar_percentuais
from src.validacao.validar_grupos import validar_grupos

CURSO_UFPA_ESPERADO = 114950
CONTAGEM_GRUPOS_ESPERADA = {
    "A": 1,
    "D": 8,
    "E": 98,
}


def validar_base_musica(base: pd.DataFrame) -> None:
    resultado = validar_base_area(
        base,
        MUSICA,
        total_cursos_esperado=107,
        ofertas_ies_esperadas=1,
    )
    resultado.exigir_valido()

    validar_grupos(base, co_ies_focal=MUSICA.co_ies_focal)
    validar_percentuais(base)

    ufpa = base[base["CO_IES"].eq(MUSICA.co_ies_focal)].copy()
    if len(ufpa) != 1:
        raise AssertionError(
            f"Música deve ter uma oferta UFPA; encontradas {len(ufpa)}"
        )

    curso = int(pd.to_numeric(ufpa["CO_CURSO"], errors="coerce").iloc[0])
    if curso != CURSO_UFPA_ESPERADO:
        raise AssertionError(
            f"CO_CURSO UFPA esperado {CURSO_UFPA_ESPERADO}; encontrado {curso}"
        )

    conceito = pd.to_numeric(
        ufpa["CONCEITO_ENADE_NUM"],
        errors="coerce",
    ).iloc[0]
    if conceito != 1:
        raise AssertionError(
            f"A oferta UFPA de Música deve ter Conceito Enade 1; encontrado {conceito}"
        )

    modalidade = pd.to_numeric(
        ufpa["CO_MODALIDADE"],
        errors="coerce",
    ).iloc[0]
    if modalidade != 1:
        raise AssertionError("A oferta UFPA de Música deve ser presencial")

    if ufpa["GRUPO_CODIGO"].iloc[0] != "A":
        raise AssertionError("A oferta UFPA de Música deve integrar o Grupo A")

    contagem = base["GRUPO_CODIGO"].value_counts().to_dict()
    if contagem != CONTAGEM_GRUPOS_ESPERADA:
        raise AssertionError(
            "Contagem dos grupos de Música divergente: "
            f"esperado {CONTAGEM_GRUPOS_ESPERADA}; encontrado {contagem}"
        )

    # Grupo B e C são estruturalmente vazios para Música.
    if base["GRUPO_CODIGO"].isin(["B", "C"]).any():
        raise AssertionError("Música não deve possuir cursos nos grupos B ou C")
