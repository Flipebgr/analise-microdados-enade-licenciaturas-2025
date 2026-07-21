from __future__ import annotations

import pandas as pd


def construir_benchmark_comparavel(cursos: pd.DataFrame, co_ies_ufpa: int = 569) -> tuple[pd.DataFrame, pd.DataFrame]:
    alvos = cursos[cursos["CO_IES"].eq(co_ies_ufpa) & cursos["CONCEITO_ENADE_NUM"].eq(1)].copy()
    candidatos = cursos[~cursos["CO_IES"].eq(co_ies_ufpa)].copy()
    pares: list[pd.DataFrame] = []
    resumo: list[dict] = []
    for _, alvo in alvos.iterrows():
        n = alvo.get("PARTICIPANTES_NUM")
        mask = (
            candidatos["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
            & candidatos["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
            & candidatos["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])
        )
        if pd.notna(n) and n > 0:
            mask &= candidatos["PARTICIPANTES_NUM"].between(max(1, n * 0.5), n * 2.0)
        selecionados = candidatos.loc[mask].copy()
        selecionados.insert(0, "CO_CURSO_ALVO", alvo["CO_CURSO"])
        selecionados.insert(1, "ROTULO_ALVO", alvo.get("ROTULO_OFERTA", str(alvo["CO_CURSO"])))
        pares.append(selecionados)
        resumo.append({
            "CO_CURSO_ALVO": alvo["CO_CURSO"],
            "ROTULO_ALVO": alvo.get("ROTULO_OFERTA", str(alvo["CO_CURSO"])),
            "modalidade": alvo.get("MODALIDADE"),
            "participantes_alvo": n,
            "n_cursos_comparaveis": len(selecionados),
            "criterio": "mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5x e 2x o alvo",
        })
    return (pd.concat(pares, ignore_index=True) if pares else pd.DataFrame(), pd.DataFrame(resumo))
