"""Associações ecológicas entre indicadores agregados por curso."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

from src.analise.contratos_fase_9a import (
    ConfiguracaoBootstrap,
    N_MINIMO_CORRELACAO,
    seed_para_contraste,
)


def _limites_iqr(valores: np.ndarray) -> tuple[float, float]:
    if not len(valores):
        return float("-inf"), float("inf")
    q1, q3 = np.quantile(valores, [0.25, 0.75])
    amplitude = q3 - q1
    return float(q1 - 1.5 * amplitude), float(q3 + 1.5 * amplitude)


def _correlacao(x: np.ndarray, y: np.ndarray) -> float | None:
    if len(np.unique(x)) < 5 or len(np.unique(y)) < 5:
        return None
    valor = float(spearmanr(x, y).statistic)
    return valor if np.isfinite(valor) else None


def _bootstrap_correlacao(x, y, identificador, configuracao):
    seed = seed_para_contraste(identificador, configuracao)
    rng = np.random.default_rng(seed)
    n = len(x)
    indices = rng.integers(0, n, size=(configuracao.numero_reamostragens, n))
    rx = rankdata(x[indices], axis=1)
    ry = rankdata(y[indices], axis=1)
    rx -= rx.mean(axis=1, keepdims=True)
    ry -= ry.mean(axis=1, keepdims=True)
    denominador = np.sqrt(np.sum(rx * rx, axis=1) * np.sum(ry * ry, axis=1))
    numerador = np.sum(rx * ry, axis=1)
    valores = np.divide(
        numerador,
        denominador,
        out=np.full(configuracao.numero_reamostragens, np.nan),
        where=denominador > 0,
    )
    validas = valores[np.isfinite(valores)]
    min_validas = int(np.ceil(0.95 * configuracao.numero_reamostragens))
    if len(validas) < min_validas:
        return None, None, seed, len(validas)
    alfa = 1 - configuracao.nivel_confianca
    inferior, superior = np.quantile(validas, [alfa / 2, 1 - alfa / 2])
    return float(inferior), float(superior), seed, int(len(validas))


def correlacao_spearman_ecologica(
    base: pd.DataFrame,
    variavel_x: str,
    variavel_y: str,
    *,
    identificador: str,
    coluna_curso: str = "CO_CURSO",
    configuracao: ConfiguracaoBootstrap = ConfiguracaoBootstrap(),
) -> tuple[dict, pd.DataFrame]:
    """Calcula Spearman não ponderado e sensibilidade sem outliers sinalizados."""

    obrigatorias = {coluna_curso, variavel_x, variavel_y}
    ausentes = sorted(obrigatorias - set(base.columns))
    if ausentes:
        raise ValueError(f"Colunas ausentes para correlação ecológica: {ausentes}")
    pares = base[[coluna_curso, variavel_x, variavel_y]].copy()
    pares[variavel_x] = pd.to_numeric(pares[variavel_x], errors="coerce")
    pares[variavel_y] = pd.to_numeric(pares[variavel_y], errors="coerce")
    pares = pares.dropna(subset=[variavel_x, variavel_y])
    if pares[coluna_curso].duplicated().any():
        raise ValueError("A correlação ecológica exige no máximo uma linha por CO_CURSO")
    pares = pares.sort_values(coluna_curso, kind="stable").reset_index(drop=True)
    x = pares[variavel_x].to_numpy(dtype=float)
    y = pares[variavel_y].to_numpy(dtype=float)
    sinalizados: set[str] = set()
    for variavel, valores in ((variavel_x, x), (variavel_y, y)):
        inferior, superior = _limites_iqr(valores)
        sinalizados.update(
            pares.loc[(valores < inferior) | (valores > superior), coluna_curso].astype(str)
        )
    n = len(pares)
    seed = seed_para_contraste(identificador, configuracao)
    saida = {
        "identificador": identificador,
        "variavel_x": variavel_x,
        "variavel_y": variavel_y,
        "unidade_analise": "CO_CURSO",
        "metodo": "spearman_nao_ponderado",
        "n_cursos": n,
        "n_pares_completos": n,
        "n_outliers_sinalizados": len(sinalizados),
        "cursos_outlier_sinalizados": sorted(sinalizados),
        "rho": None,
        "ic_inf": None,
        "ic_sup": None,
        "seed": seed,
        "numero_reamostragens": configuracao.numero_reamostragens,
        "tipo_incerteza": "bootstrap ecologico de pares de cursos",
        "status": "insuficiente",
        "motivo": None,
    }
    rho = _correlacao(x, y) if n >= N_MINIMO_CORRELACAO else None
    if n < N_MINIMO_CORRELACAO:
        saida["motivo"] = "n_cursos_abaixo_do_minimo_20"
    elif rho is None:
        saida["motivo"] = "variavel_constante_ou_menos_de_cinco_valores_distintos"
    else:
        ic_inf, ic_sup, seed, n_validas = _bootstrap_correlacao(
            x, y, identificador, configuracao
        )
        saida.update({
            "rho": rho,
            "ic_inf": ic_inf,
            "ic_sup": ic_sup,
            "seed": seed,
            "n_replicas_validas": n_validas,
            "status": "disponivel" if ic_inf is not None else "descritivo_apenas",
            "motivo": None if ic_inf is not None else "bootstrap_com_replicas_insuficientes",
        })

    sem_outliers = pares.loc[~pares[coluna_curso].astype(str).isin(sinalizados)].copy()
    n_sem = len(sem_outliers)
    sensibilidade = {
        "identificador": identificador,
        "variavel_x": variavel_x,
        "variavel_y": variavel_y,
        "cenario": "sem_outliers_sinalizados",
        "cursos_excluidos": sorted(sinalizados),
        "n_cursos": n_sem,
        "rho": None,
        "status": "insuficiente",
        "motivo": None,
    }
    if n_sem >= N_MINIMO_CORRELACAO:
        valores_sem = _correlacao(
            sem_outliers[variavel_x].to_numpy(dtype=float),
            sem_outliers[variavel_y].to_numpy(dtype=float),
        )
        if valores_sem is not None:
            sensibilidade.update({"rho": valores_sem, "status": "disponivel"})
        else:
            sensibilidade["motivo"] = "variavel_constante_ou_menos_de_cinco_valores_distintos"
    else:
        sensibilidade["motivo"] = "n_cursos_apos_sensibilidade_abaixo_do_minimo_20"
    return saida, pd.DataFrame([sensibilidade])
