from __future__ import annotations

import pandas as pd


DIMENSOES_CANDIDATAS = {
    "organizacao_didatico_pedagogica": [f"qe_i{i}_concordancia_pct" for i in range(20, 28)],
    "atuacao_docente": [f"qe_i{i}_concordancia_pct" for i in range(28, 35)],
    "infraestrutura": [f"qe_i{i}_concordancia_pct" for i in range(35, 43)],
    "oportunidades_formacao": [f"qe_i{i}_concordancia_pct" for i in range(43, 53)],
    "integracao_teoria_pratica": [f"qe_i{i}_concordancia_pct" for i in range(53, 61)],
    "apoio_academico": [f"qe_i{i}_concordancia_pct" for i in range(61, 67)],
}


def diagnosticar_dimensoes(base: pd.DataFrame, co_ies: int = 569) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cria escores exploratórios por dimensão, sem validá-los como índices definitivos."""
    cursos = base.copy()
    resumo = []
    scores = cursos[["CO_CURSO", "CO_IES", "ROTULO_OFERTA"]].copy()
    for dimensao, colunas in DIMENSOES_CANDIDATAS.items():
        existentes = [c for c in colunas if c in cursos.columns]
        matriz = cursos[existentes].apply(pd.to_numeric, errors="coerce")
        scores[dimensao] = matriz.mean(axis=1, skipna=True)
        resumo.append({
            "dimensao": dimensao,
            "n_itens_previstos": len(colunas),
            "n_itens_encontrados": len(existentes),
            "n_cursos_com_score": int(scores[dimensao].notna().sum()),
            "media_nacional_exploratoria": scores[dimensao].mean(),
            "media_ufpa_exploratoria": scores.loc[scores["CO_IES"].eq(co_ies), dimensao].mean(),
            "decisao": "Uso exploratório; validar redação e coerência teórica antes do relatório final",
        })
    return pd.DataFrame(resumo), scores
