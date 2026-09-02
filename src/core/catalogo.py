from __future__ import annotations

from collections.abc import Collection

import pandas as pd

from src.core.configuracao_area import ConfiguracaoArea
from src.core.juncoes import validar_unicidade_por_curso
from src.utilitarios.normalizacao import normalizar_codigo

COLUNAS_CATALOGO_MINIMAS = ("CO_CURSO", "CO_IES", "CO_GRUPO")


def _validar_colunas(tabela: pd.DataFrame, obrigatorias: Collection[str]) -> None:
    ausentes = sorted(set(obrigatorias) - set(tabela.columns))
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes no cadastro: {ausentes}")


def preparar_catalogo_area(
    cadastro: pd.DataFrame,
    configuracao: ConfiguracaoArea,
    *,
    colunas_adicionais: Collection[str] = (),
) -> pd.DataFrame:
    """Normaliza e filtra o cadastro para uma única área.

    Não lê arquivos, não associa conceitos e não cria grupos comparativos.
    """

    obrigatorias = tuple(dict.fromkeys((*COLUNAS_CATALOGO_MINIMAS, *colunas_adicionais)))
    _validar_colunas(cadastro, obrigatorias)

    resultado = cadastro.loc[:, list(obrigatorias)].copy(deep=True)
    for coluna in COLUNAS_CATALOGO_MINIMAS:
        resultado[coluna] = normalizar_codigo(resultado[coluna])

    resultado = resultado[resultado["CO_GRUPO"].eq(configuracao.co_grupo)].copy()
    if resultado["CO_CURSO"].isna().any():
        raise ValueError("O catálogo filtrado contém CO_CURSO ausente")

    validar_unicidade_por_curso(resultado, nome=f"catálogo de {configuracao.nome}")
    resultado["IES_FOCAL"] = resultado["CO_IES"].eq(configuracao.co_ies_focal)
    resultado["AREA_SLUG"] = configuracao.slug
    resultado["AREA_NOME"] = configuracao.nome
    return resultado.reset_index(drop=True)
