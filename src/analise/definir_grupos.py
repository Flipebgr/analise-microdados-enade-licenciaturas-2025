from __future__ import annotations

import pandas as pd

GRUPOS = {
    "A": "UFPA — Conceito 1",
    "B": "UFPA — conceito superior",
    "C": "Outras IES do Pará",
    "D": "Restante da Região Norte",
    "E": "Restante do Brasil",
}


def _codigo_igual(valor, esperado: int | str) -> bool:
    if pd.isna(valor):
        return False
    return str(valor).strip().lstrip("0") == str(esperado).strip().lstrip("0")


def definir_grupo(linha: pd.Series, co_ies_ufpa: int = 569) -> str:
    co_ies = linha.get("CO_IES")
    uf = str(linha.get("UF", "")).strip().upper()
    uf_codigo = linha.get("CO_UF_CURSO")
    regiao = linha.get("CO_REGIAO_CURSO")
    conceito_origem = linha.get("CONCEITO_ENADE_NUM", linha.get("CONCEITO_ENADE"))
    conceito = pd.to_numeric(pd.Series([conceito_origem]), errors="coerce").iloc[0]
    if _codigo_igual(co_ies, co_ies_ufpa):
        if conceito == 1:
            return "A"
        if pd.notna(conceito) and conceito > 1:
            return "B"
        return "SEM_GRUPO"
    if uf == "PA" or _codigo_igual(uf_codigo, 15):
        return "C"
    if _codigo_igual(regiao, 1):
        return "D"
    if pd.notna(regiao):
        return "E"
    raise ValueError(f"Território ausente para curso {linha.get('CO_CURSO')}")


def aplicar_grupos(
    cursos: pd.DataFrame,
    co_ies_ufpa: int = 569,
    co_cursos_focais: tuple[str, ...] = (),
) -> pd.DataFrame:
    out = cursos.copy()
    out["GRUPO_CODIGO"] = out.apply(definir_grupo, axis=1, co_ies_ufpa=co_ies_ufpa)
    out["GRUPO"] = out["GRUPO_CODIGO"].map(GRUPOS).fillna("Fora do contraste principal")
    ies_focal = out["CO_IES"].map(lambda valor: _codigo_igual(valor, co_ies_ufpa))
    if co_cursos_focais:
        cursos_focais = set(map(str, co_cursos_focais))
        cursos_universo = set(out["CO_CURSO"].astype("string"))
        ausentes = sorted(cursos_focais - cursos_universo)
        if ausentes:
            raise ValueError(f"Cursos focais configurados ausentes no universo: {ausentes}")
        out["eh_focal"] = out["CO_CURSO"].astype("string").isin(cursos_focais)
        fora_ies = out["eh_focal"] & ~ies_focal
        if fora_ies.any():
            codigos = out.loc[fora_ies, "CO_CURSO"].tolist()[:5]
            raise ValueError(f"Cursos focais não pertencem à IES focal: {codigos}")
    else:
        out["eh_focal"] = ies_focal
    return out.sort_values("CO_CURSO", kind="stable").reset_index(drop=True)
