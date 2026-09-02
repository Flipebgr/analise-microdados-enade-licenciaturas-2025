from __future__ import annotations

import pandas as pd


def _conceito_numerico(df: pd.DataFrame) -> pd.Series:
    """Obtém o Conceito Enade numérico sem exigir coluna derivada específica."""

    if "CONCEITO_ENADE_NUM" in df.columns:
        origem = df["CONCEITO_ENADE_NUM"]
    elif "CONCEITO_ENADE" in df.columns:
        origem = df["CONCEITO_ENADE"]
    else:
        raise AssertionError(
            "Base sem coluna de Conceito Enade "
            "('CONCEITO_ENADE' ou 'CONCEITO_ENADE_NUM')"
        )

    return pd.to_numeric(origem, errors="coerce")


def validar_grupos(
    df: pd.DataFrame,
    *,
    co_ies_focal: int = 569,
) -> None:
    """Valida invariantes dos grupos comparativos exclusivos A–E.

    Cursos sem conceito podem permanecer como ``SEM_GRUPO``. Em particular,
    ausência de conceito nunca é tratada como Conceito Enade 1.
    """

    obrigatorias = {"GRUPO_CODIGO", "CO_IES"}
    ausentes = obrigatorias.difference(df.columns)
    if ausentes:
        raise AssertionError(
            "Colunas obrigatórias ausentes para validar grupos: "
            + ", ".join(sorted(ausentes))
        )

    if df["GRUPO_CODIGO"].isna().any():
        raise AssertionError("Há cursos sem classificação explícita de grupo")

    conceito = _conceito_numerico(df)
    co_ies = pd.to_numeric(df["CO_IES"], errors="coerce")

    grupo_a = df["GRUPO_CODIGO"].eq("A")
    if (grupo_a & (co_ies.ne(co_ies_focal) | conceito.ne(1))).any():
        raise AssertionError(
            "Grupo A contém curso que não é da IES focal com Conceito 1"
        )

    grupo_b = df["GRUPO_CODIGO"].eq("B")
    if (
        grupo_b
        & (
            co_ies.ne(co_ies_focal)
            | conceito.isna()
            | conceito.le(1)
        )
    ).any():
        raise AssertionError(
            "Grupo B contém curso que não é da IES focal com conceito superior a 1"
        )

    grupo_c = df["GRUPO_CODIGO"].eq("C")
    if (grupo_c & co_ies.eq(co_ies_focal)).any():
        raise AssertionError("Grupo C contém curso da IES focal")
