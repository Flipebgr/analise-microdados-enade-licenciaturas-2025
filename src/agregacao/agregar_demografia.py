from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.agregacao.comum import carregar_filtrado, converter_numerico, validar_unicidade


def agregar_demografia(path_sexo: Path, path_idade: Path, cursos: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    sexo = carregar_filtrado(path_sexo, cursos, usecols=["CO_CURSO", "TP_SEXO"])
    sexo["TP_SEXO"] = sexo["TP_SEXO"].astype("string").str.strip()
    gsexo = sexo.groupby("CO_CURSO", observed=True)["TP_SEXO"]
    agg_sexo = gsexo.agg(
        sexo_n_total="size",
        sexo_n_valido=lambda s: int(s.isin(["F", "M"]).sum()),
        sexo_feminino_n=lambda s: int((s == "F").sum()),
        sexo_masculino_n=lambda s: int((s == "M").sum()),
        sexo_indefinido_n=lambda s: int((s == "9").sum()),
    ).reset_index()
    agg_sexo["sexo_feminino_pct"] = agg_sexo["sexo_feminino_n"] / agg_sexo["sexo_n_valido"]
    agg_sexo["sexo_masculino_pct"] = agg_sexo["sexo_masculino_n"] / agg_sexo["sexo_n_valido"]

    idade = carregar_filtrado(path_idade, cursos, usecols=["CO_CURSO", "NU_IDADE"])
    idade["NU_IDADE"] = converter_numerico(idade["NU_IDADE"])
    idade.loc[~idade["NU_IDADE"].between(14, 100), "NU_IDADE"] = pd.NA
    gidade = idade.groupby("CO_CURSO", observed=True)["NU_IDADE"]
    agg_idade = gidade.agg(idade_n="count", idade_media="mean", idade_mediana="median", idade_dp="std", idade_min="min", idade_max="max").reset_index()
    agregado = agg_sexo.merge(agg_idade, on="CO_CURSO", how="outer", validate="one_to_one")
    validar_unicidade(agregado, "agregado_demografia")
    distribuicao = sexo.groupby(["CO_CURSO", "TP_SEXO"], dropna=False).size().rename("n").reset_index()
    return agregado, distribuicao
