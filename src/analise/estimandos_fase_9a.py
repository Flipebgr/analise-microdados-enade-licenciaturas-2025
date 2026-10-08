"""Estimandos e medidas de efeito definidos para a Fase 9A."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from src.analise.contratos_fase_9a import TipoEstimando


def _validar_pesos(valores: pd.Series, pesos: pd.Series | None = None) -> tuple[np.ndarray, np.ndarray]:
    x = pd.to_numeric(valores, errors="coerce")
    if pesos is None:
        w = pd.Series(1.0, index=x.index)
    else:
        w = pd.to_numeric(pesos, errors="coerce")
    mascara = x.notna() & w.notna() & w.gt(0)
    xv = x.loc[mascara].to_numpy(dtype=float)
    wv = w.loc[mascara].to_numpy(dtype=float)
    if not len(xv):
        return np.array([], dtype=float), np.array([], dtype=float)
    return xv, wv


def media_cursos(valores: pd.Series) -> float | None:
    x, _ = _validar_pesos(valores)
    return float(np.mean(x)) if len(x) else None


def media_ponderada(valores: pd.Series, n_validos: pd.Series) -> float | None:
    x, w = _validar_pesos(valores, n_validos)
    return float(np.average(x, weights=w)) if len(x) else None


def resumo_contraste_foco_unico(
    valor_focal: float | None,
    benchmark: pd.Series,
    *,
    n_valido_benchmark: pd.Series | None = None,
) -> dict[str, float | int | str | None]:
    """Calcula estimandos de curso típico e respondente típico para foco único."""

    x, _ = _validar_pesos(benchmark)
    resultado: dict[str, float | int | str | None] = {
        "n_cursos_benchmark": int(len(x)),
        "tipo_estimando_principal": TipoEstimando.CURSO_TIPICO.value,
        "valor_focal": float(valor_focal) if valor_focal is not None and math.isfinite(valor_focal) else None,
        "media_benchmark": float(np.mean(x)) if len(x) else None,
        "mediana_benchmark": float(np.median(x)) if len(x) else None,
        "diferenca_media": None,
        "diferenca_mediana": None,
        "percentil_focal": None,
        "z_ref": None,
        "media_benchmark_ponderada": None,
        "tipo_estimando_secundario": TipoEstimando.PARTICIPANTE_TIPICO.value,
    }
    focal = resultado["valor_focal"]
    if focal is None or not len(x):
        return resultado
    resultado["diferenca_media"] = float(focal - np.mean(x))
    resultado["diferenca_mediana"] = float(focal - np.median(x))
    resultado["percentil_focal"] = float(
        100 * (np.sum(x < focal) + 0.5 * np.sum(x == focal)) / len(x)
    )
    dp = float(np.std(x, ddof=1)) if len(x) >= 2 else float("nan")
    if math.isfinite(dp) and dp > 0:
        resultado["z_ref"] = float((focal - np.mean(x)) / dp)
    if n_valido_benchmark is not None:
        valores_pesados, pesos = _validar_pesos(benchmark, n_valido_benchmark)
        if len(valores_pesados):
            resultado["media_benchmark_ponderada"] = float(
                np.average(valores_pesados, weights=pesos)
            )
    return resultado


def diferenca_proporcoes(p_focal: float | None, p_benchmark: float | None) -> dict[str, float | None]:
    """Diferença primária e razão secundária de proporções."""

    if p_focal is None or p_benchmark is None:
        return {"diferenca_proporcoes": None, "razao_proporcoes": None}
    if not 0 <= p_focal <= 1 or not 0 <= p_benchmark <= 1:
        raise ValueError("Proporções precisam estar no intervalo [0, 1]")
    return {
        "diferenca_proporcoes": float(p_focal - p_benchmark),
        "razao_proporcoes": float(p_focal / p_benchmark) if p_benchmark > 0 else None,
    }


def hedges_g_cursos(focal: pd.Series, benchmark: pd.Series) -> float | None:
    """Hedges g para dois grupos de cursos, nunca para foco único."""

    a, _ = _validar_pesos(focal)
    b, _ = _validar_pesos(benchmark)
    n_a, n_b = len(a), len(b)
    if n_a < 2 or n_b < 2:
        return None
    graus = n_a + n_b - 2
    variancia = ((n_a - 1) * np.var(a, ddof=1) + (n_b - 1) * np.var(b, ddof=1)) / graus
    if not math.isfinite(variancia) or variancia <= 0:
        return None
    correcao = 1 - 3 / (4 * (n_a + n_b) - 9)
    return float(correcao * (np.mean(a) - np.mean(b)) / np.sqrt(variancia))


