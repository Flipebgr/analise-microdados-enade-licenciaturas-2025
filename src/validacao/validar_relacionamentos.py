from __future__ import annotations
import pandas as pd


def validar_unicidade_tabela_mestra(df: pd.DataFrame) -> list[str]:
    erros: list[str] = []
    chaves = ["NU_ANO", "CO_IES", "CO_GRUPO", "CO_CURSO"]
    duplicadas = df.duplicated(chaves, keep=False)
    if duplicadas.any():
        erros.append(f"Há {int(duplicadas.sum())} linhas duplicadas nas chaves {chaves}.")
    if df["CO_CURSO"].isna().any():
        erros.append("Há ofertas sem CO_CURSO.")
    return erros


def validar_join_agregado(df_esquerda: pd.DataFrame, df_direita: pd.DataFrame, chave: str = "CO_CURSO") -> None:
    if df_esquerda[chave].duplicated().any() or df_direita[chave].duplicated().any():
        raise ValueError("Join proibido: ambas as tabelas devem possuir uma linha por CO_CURSO.")
