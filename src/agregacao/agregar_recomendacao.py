from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.agregacao.comum import carregar_filtrado, converter_numerico, validar_unicidade


def _agregar_numerica(path: Path, cursos: list[int], variavel: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = carregar_filtrado(path, cursos, usecols=["CO_CURSO", variavel])
    df[variavel] = converter_numerico(df[variavel])
    df.loc[~df[variavel].between(0, 10), variavel] = pd.NA
    g = df.groupby("CO_CURSO", observed=True)[variavel]
    agg = g.agg(**{
        f"{variavel.lower()}_n": "count",
        f"{variavel.lower()}_media": "mean",
        f"{variavel.lower()}_mediana": "median",
        f"{variavel.lower()}_dp": "std",
        f"{variavel.lower()}_nota_9_10_n": lambda s: int(s.isin([9, 10]).sum()),
        f"{variavel.lower()}_nota_0_6_n": lambda s: int(s.between(0, 6).sum()),
    }).reset_index()
    agg[f"{variavel.lower()}_nota_9_10_pct"] = agg[f"{variavel.lower()}_nota_9_10_n"] / agg[f"{variavel.lower()}_n"]
    agg[f"{variavel.lower()}_nota_0_6_pct"] = agg[f"{variavel.lower()}_nota_0_6_n"] / agg[f"{variavel.lower()}_n"]
    dist = df.groupby(["CO_CURSO", variavel], dropna=False).size().rename("n").reset_index()
    dist["VARIAVEL"] = variavel
    dist = dist.rename(columns={variavel: "RESPOSTA"})
    return agg, dist


def agregar_recomendacao(path68: Path, path69: Path, path70: Path, cursos: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    a68, d68 = _agregar_numerica(path68, cursos, "QE_I68")
    a69, d69 = _agregar_numerica(path69, cursos, "QE_I69")
    q70 = carregar_filtrado(path70, cursos, usecols=["CO_CURSO", "QE_I70"])
    q70["RESPOSTA"] = q70["QE_I70"].astype("string").str.strip().str.upper().replace({"": pd.NA, ".": pd.NA})
    a70 = q70.groupby("CO_CURSO", observed=True)["RESPOSTA"].agg(
        qe_i70_n="count",
        qe_i70_interesse_n=lambda s: int(s.fillna("").map(lambda x: any(letra in str(x).split(",") for letra in "ABCDE")).sum()),
    ).reset_index()
    a70["qe_i70_interesse_pct"] = a70["qe_i70_interesse_n"] / a70["qe_i70_n"]
    d70 = q70.groupby(["CO_CURSO", "RESPOSTA"], dropna=False).size().rename("n").reset_index()
    d70["VARIAVEL"] = "QE_I70"
    agregado = a68.merge(a69, on="CO_CURSO", how="outer", validate="one_to_one").merge(a70, on="CO_CURSO", how="outer", validate="one_to_one")
    validar_unicidade(agregado, "agregado_recomendacao")
    return agregado, pd.concat([d68, d69, d70], ignore_index=True)
