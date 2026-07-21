from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from src.agregacao.comum import carregar_filtrado, converter_numerico, validar_unicidade

ITENS = [f"QE_I{i}" for i in range(20, 67)]


def cronbach_alpha(df: pd.DataFrame) -> float:
    completo = df.dropna()
    if completo.shape[0] < 10 or completo.shape[1] < 2:
        return float("nan")
    variancias = completo.var(axis=0, ddof=1)
    total = completo.sum(axis=1)
    var_total = total.var(ddof=1)
    if not np.isfinite(var_total) or var_total == 0:
        return float("nan")
    k = completo.shape[1]
    return float(k / (k - 1) * (1 - variancias.sum() / var_total))


def agregar_processo_formativo(path: Path, cursos: list[int]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = carregar_filtrado(path, cursos, usecols=["CO_CURSO", *ITENS])
    longos: list[pd.DataFrame] = []
    escala = pd.DataFrame({"CO_CURSO": sorted(df["CO_CURSO"].dropna().unique())})
    for item in ITENS:
        valor = converter_numerico(df[item])
        valido = valor.where(valor.between(1, 6))
        tmp = pd.DataFrame({"CO_CURSO": df["CO_CURSO"], "ITEM": item, "RESPOSTA": valor, "VALIDO": valido})
        agg = tmp.groupby(["CO_CURSO", "ITEM"], observed=True).agg(
            n_total=("RESPOSTA", "size"),
            n_valido=("VALIDO", "count"),
            media=("VALIDO", "mean"),
            mediana=("VALIDO", "median"),
            dp=("VALIDO", "std"),
            concordancia_n=("VALIDO", lambda s: int(s.isin([4, 5, 6]).sum())),
            nao_sabe_n=("RESPOSTA", lambda s: int((s == 7).sum())),
            nao_aplica_n=("RESPOSTA", lambda s: int((s == 8).sum())),
        ).reset_index()
        agg["concordancia_pct"] = agg["concordancia_n"] / agg["n_valido"]
        agg["ausencia_analitica_pct"] = 1 - agg["n_valido"] / agg["n_total"]
        longos.append(agg)
        por_curso = agg[["CO_CURSO", "media", "concordancia_pct"]].rename(columns={"media": f"{item.lower()}_media", "concordancia_pct": f"{item.lower()}_concordancia_pct"})
        escala = escala.merge(por_curso, on="CO_CURSO", how="left", validate="one_to_one")

    matriz = df[ITENS].apply(converter_numerico).where(lambda x: x.apply(lambda col: col.between(1, 6)))
    alpha_total = cronbach_alpha(matriz)
    diagnostico = pd.DataFrame([{
        "escala": "QE_I20-QE_I66 (exploratória, sem uso como índice)",
        "n_itens": len(ITENS),
        "n_casos_completos": int(matriz.dropna().shape[0]),
        "cronbach_alpha": alpha_total,
        "decisao": "Não formar índice único nesta sprint; resultado apenas diagnóstico.",
    }])
    validar_unicidade(escala, "agregado_processo_formativo")
    return escala, pd.concat(longos, ignore_index=True), diagnostico
