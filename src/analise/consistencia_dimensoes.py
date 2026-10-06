from __future__ import annotations

import numpy as np
import pandas as pd

from src.edicoes import ENADE_2025_LICENCIATURAS

# Agrupamento preliminar para diagnóstico. A validação final depende do texto oficial dos itens.
DIMENSOES = {
    "organizacao_didatico_pedagogica": [f"QE_I{i}" for i in range(20, 34)],
    "atuacao_docente": [f"QE_I{i}" for i in range(34, 42)],
    "infraestrutura_recursos": [f"QE_I{i}" for i in range(42, 50)],
    "oportunidades_formacao": [f"QE_I{i}" for i in range(50, 59)],
    "integracao_teoria_pratica": [f"QE_I{i}" for i in range(59, 67)],
}


def _respostas_validas(df: pd.DataFrame) -> pd.DataFrame:
    """Mantém apenas os códigos da escala 2025; 7/8 não são pontuações."""

    numericos = df.apply(pd.to_numeric, errors="coerce")
    codigos = ENADE_2025_LICENCIATURAS.questionario.codigos_validos_processo
    return numericos.where(numericos.isin(codigos))


def cronbach_alpha(df: pd.DataFrame) -> float:
    x = _respostas_validas(df).dropna()
    if x.shape[0] < 3 or x.shape[1] < 2:
        return np.nan
    variancias = x.var(axis=0, ddof=1).sum()
    total = x.sum(axis=1).var(ddof=1)
    if not np.isfinite(total) or total <= 0:
        return np.nan
    k = x.shape[1]
    return float(k / (k - 1) * (1 - variancias / total))


def diagnosticar_dimensoes(dados_individuais: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for nome, itens in DIMENSOES.items():
        presentes = [i for i in itens if i in dados_individuais.columns]
        alpha = cronbach_alpha(dados_individuais[presentes]) if presentes else np.nan
        linhas.append({
            "dimensao": nome,
            "itens": ", ".join(presentes),
            "n_itens": len(presentes),
            "n_casos_completos": int(_respostas_validas(dados_individuais[presentes]).dropna().shape[0]) if presentes else 0,
            "alpha_cronbach": alpha,
            "decisao": "diagnóstico preliminar; exige validação teórica dos itens",
        })
    return pd.DataFrame(linhas)
