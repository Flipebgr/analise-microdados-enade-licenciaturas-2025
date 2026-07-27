from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.agregacao.comum import carregar_filtrado

ITENS_DIFICULDADE = ["CO_RS_I1", "CO_RS_I2", "CO_RS_I7"]
ORDEM_GRAU = ["A", "B", "C", "D", "E"]
ROTULOS_GRAU = {
    "A": "Muito fácil",
    "B": "Fácil",
    "C": "Médio",
    "D": "Difícil",
    "E": "Muito difícil",
}
ROTULOS_TIPO = {
    "A": "Desconhecimento do conteúdo",
    "B": "Forma diferente de abordagem",
    "C": "Espaço insuficiente",
    "D": "Falta de motivação",
    "E": "Sem dificuldade",
}


def agregar_dificuldade(path: Path, cursos: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = carregar_filtrado(path, cursos, usecols=["CO_CURSO", *ITENS_DIFICULDADE])
    longos = []
    escalares = pd.DataFrame({"CO_CURSO": sorted(df["CO_CURSO"].dropna().unique())})
    for item in ITENS_DIFICULDADE:
        tmp = df[["CO_CURSO", item]].copy()
        tmp["RESPOSTA"] = tmp[item].astype("string").str.strip().str.upper()
        tmp.loc[~tmp["RESPOSTA"].isin(ORDEM_GRAU), "RESPOSTA"] = pd.NA
        dist = tmp.groupby(["CO_CURSO", "RESPOSTA"], dropna=False).size().rename("N").reset_index()
        dist["ITEM"] = item
        dist["ROTULO"] = dist["RESPOSTA"].map(ROTULOS_TIPO if item == "CO_RS_I7" else ROTULOS_GRAU)
        totais = dist.groupby("CO_CURSO")["N"].transform("sum")
        dist["PERCENTUAL"] = dist["N"] / totais * 100
        longos.append(dist)

        valido = tmp["RESPOSTA"].notna()
        dificuldade_alta = tmp["RESPOSTA"].isin(["D", "E"]) if item != "CO_RS_I7" else ~tmp["RESPOSTA"].eq("E")
        agg = tmp.assign(VALIDO=valido, DIFICULDADE_ALTA=dificuldade_alta & valido).groupby("CO_CURSO").agg(
            **{
                f"{item.lower()}_n": ("VALIDO", "sum"),
                f"{item.lower()}_dificuldade_alta_n": ("DIFICULDADE_ALTA", "sum"),
            }
        ).reset_index()
        agg[f"{item.lower()}_dificuldade_alta_pct"] = (
            agg[f"{item.lower()}_dificuldade_alta_n"] / agg[f"{item.lower()}_n"] * 100
        )
        escalares = escalares.merge(agg, on="CO_CURSO", how="left", validate="one_to_one")
    return escalares, pd.concat(longos, ignore_index=True)
