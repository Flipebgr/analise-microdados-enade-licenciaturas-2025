from __future__ import annotations

from typing import Literal

import pandas as pd

CHAVE_CURSO = "CO_CURSO"


def _validar_chave(tabela: pd.DataFrame, *, nome: str) -> None:
    if CHAVE_CURSO not in tabela.columns:
        raise ValueError(f"{nome} não contém a coluna obrigatória {CHAVE_CURSO}")
    if tabela[CHAVE_CURSO].isna().any():
        linhas = tabela.index[tabela[CHAVE_CURSO].isna()].tolist()[:10]
        raise ValueError(f"{nome} contém {CHAVE_CURSO} ausente. Linhas: {linhas}")


def validar_unicidade_por_curso(tabela: pd.DataFrame, *, nome: str) -> None:
    """Garante uma e somente uma linha por ``CO_CURSO``."""

    _validar_chave(tabela, nome=nome)
    duplicados = tabela.loc[
        tabela[CHAVE_CURSO].duplicated(keep=False), CHAVE_CURSO
    ].drop_duplicates()
    if not duplicados.empty:
        exemplos = duplicados.tolist()[:10]
        raise ValueError(
            f"{nome} não possui uma linha por {CHAVE_CURSO}. "
            f"Cursos duplicados: {exemplos}"
        )


def juntar_por_curso(
    esquerda: pd.DataFrame,
    direita: pd.DataFrame,
    *,
    como: Literal["left", "inner", "outer"] = "left",
    sufixos: tuple[str, str] = ("", "_direita"),
) -> pd.DataFrame:
    """Realiza junção estritamente um-para-um pela chave de curso.

    A função não altera os DataFrames recebidos e rejeita duplicidade ou
    ausência na chave antes de executar o merge.
    """

    if como not in {"left", "inner", "outer"}:
        raise ValueError("como deve ser 'left', 'inner' ou 'outer'")
    if len(sufixos) != 2 or sufixos[0] == sufixos[1]:
        raise ValueError("sufixos deve conter dois valores distintos")

    validar_unicidade_por_curso(esquerda, nome="tabela esquerda")
    validar_unicidade_por_curso(direita, nome="tabela direita")

    sobrepostas = (set(esquerda.columns) & set(direita.columns)) - {CHAVE_CURSO}
    if sobrepostas and not sufixos[1]:
        nomes = ", ".join(sorted(sobrepostas))
        raise ValueError(f"Colunas sobrepostas exigem sufixo para a direita: {nomes}")

    resultado = esquerda.merge(
        direita,
        on=CHAVE_CURSO,
        how=como,
        validate="one_to_one",
        suffixes=sufixos,
        sort=False,
    )
    validar_unicidade_por_curso(resultado, nome="resultado da junção")
    return resultado
