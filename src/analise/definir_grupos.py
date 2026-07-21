from __future__ import annotations

import pandas as pd

GRUPOS = {
    "A": "UFPA — Conceito 1",
    "B": "UFPA — conceito superior",
    "C": "Outras IES do Pará",
    "D": "Restante da Região Norte",
    "E": "Restante do Brasil",
}


def definir_grupo(linha: pd.Series, co_ies_ufpa: int = 569) -> str:
    co_ies = linha.get("CO_IES")
    uf = str(linha.get("UF", "")).strip().upper()
    regiao = linha.get("CO_REGIAO_CURSO")
    conceito = pd.to_numeric(pd.Series([linha.get("CONCEITO_ENADE")]), errors="coerce").iloc[0]
    if co_ies == co_ies_ufpa:
        if conceito == 1:
            return "A"
        if pd.notna(conceito) and conceito > 1:
            return "B"
        return "SEM_GRUPO"
    if uf == "PA" or linha.get("CO_UF_CURSO") == 15:
        return "C"
    if regiao == 1:
        return "D"
    return "E"


def aplicar_grupos(cursos: pd.DataFrame, co_ies_ufpa: int = 569) -> pd.DataFrame:
    out = cursos.copy()
    out["GRUPO_CODIGO"] = out.apply(definir_grupo, axis=1, co_ies_ufpa=co_ies_ufpa)
    out["GRUPO"] = out["GRUPO_CODIGO"].map(GRUPOS).fillna("Fora do contraste principal")
    return out
