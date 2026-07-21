from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.agregacao.comum import carregar_filtrado, converter_numerico, resumo_numerico, validar_unicidade

VARIAVEIS = ["NT_GER", "NT_OBJ", "NT_DIS", "PROFICIENCIA", "QT_ACERTOS"]


def agregar_desempenho(path: Path, cursos: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    colunas = ["CO_CURSO", "IN_REAPLICACAO", "TP_PRES", "TP_SIT_DISC", *VARIAVEIS]
    df = carregar_filtrado(path, cursos, usecols=colunas)
    for coluna in ["IN_REAPLICACAO", "TP_PRES", "TP_SIT_DISC"]:
        df[coluna] = converter_numerico(df[coluna])
    for variavel in VARIAVEIS:
        df[variavel] = converter_numerico(df[variavel])

    numerico = resumo_numerico(df, VARIAVEIS)
    participacao = df.groupby("CO_CURSO", observed=True).agg(
        registros_microdados=("CO_CURSO", "size"),
        presentes_validos=("TP_PRES", lambda s: int((s == 555).sum())),
        ausentes=("TP_PRES", lambda s: int(s.isin([222, 444]).sum())),
        eliminados=("TP_PRES", lambda s: int((s == 334).sum())),
        resultado_desconsiderado=("TP_PRES", lambda s: int((s == 888).sum())),
        reaplicacoes=("IN_REAPLICACAO", lambda s: int((s == 1).sum())),
        discursiva_valida=("TP_SIT_DISC", lambda s: int((s == 555).sum())),
        discursiva_zero=("TP_SIT_DISC", lambda s: int(s.isin([333, 335, 336]).sum())),
    ).reset_index()
    participacao["taxa_presenca_microdados"] = participacao["presentes_validos"] / participacao["registros_microdados"]
    agregado = participacao.merge(numerico, on="CO_CURSO", how="outer", validate="one_to_one")
    validar_unicidade(agregado, "agregado_desempenho")
    return agregado, df
