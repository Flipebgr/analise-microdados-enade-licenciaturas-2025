"""Incerteza ecológica por bootstrap no nível de curso."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd

from src.analise.contratos_fase_9a import (
    ConfiguracaoBootstrap,
    N_MINIMO_INFERENCIA,
    seed_para_contraste,
)


def _valores_ordenados(
    valores: pd.Series,
    cursos: pd.Series | None = None,
) -> np.ndarray:
    """Normaliza a ordem antes do bootstrap, preferencialmente por CO_CURSO."""

    numericos = pd.to_numeric(valores, errors="coerce")
    if cursos is None:
        return np.sort(numericos.dropna().to_numpy(dtype=float), kind="stable")
    if len(cursos) != len(numericos):
        raise ValueError("CO_CURSO e valores do bootstrap devem ter o mesmo tamanho")
    tabela = pd.DataFrame({"CO_CURSO": cursos.astype("string"), "valor": numericos}).dropna(
        subset=["valor"]
    )
    if tabela["CO_CURSO"].isna().any() or tabela["CO_CURSO"].duplicated().any():
        raise ValueError("Bootstrap exige CO_CURSO presente e único em cada braço")
    return tabela.sort_values("CO_CURSO", kind="stable")["valor"].to_numpy(dtype=float)


def bootstrap_ic_condicional_ao_foco(
    valor_focal: float,
    benchmark: pd.Series,
    *,
    identificador: str,
    cursos_benchmark: pd.Series | None = None,
    estatistica_referencia: Callable[[np.ndarray], float] = np.mean,
    configuracao: ConfiguracaoBootstrap = ConfiguracaoBootstrap(),
) -> dict:
    """Calcula IC percentil da diferença, mantendo foco fixo e reamostrando cursos."""

    valores = _valores_ordenados(benchmark, cursos_benchmark)
    seed = seed_para_contraste(identificador, configuracao)
    metadados = {
        "tipo_incerteza": "IC ecológico condicional ao foco",
        "unidade_reamostragem": configuracao.unidade_reamostragem,
        "foco_reamostrado": False,
        "numero_reamostragens": configuracao.numero_reamostragens,
        "seed": seed,
        "nivel_confianca": configuracao.nivel_confianca,
        "n_cursos_benchmark": int(len(valores)),
    }
    if len(valores) < N_MINIMO_INFERENCIA:
        return {
            **metadados,
            "estimativa": None,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "n_benchmark_abaixo_do_minimo",
            "n_replicas_validas": 0,
        }
    if not np.isfinite(valor_focal) or not np.isfinite(valores).all():
        return {
            **metadados,
            "estimativa": None,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "valor_nao_finito",
            "n_replicas_validas": 0,
        }
    media_ref = float(estatistica_referencia(valores))
    if not np.isfinite(media_ref):
        return {
            **metadados,
            "estimativa": None,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "estimativa_indefinida",
            "n_replicas_validas": 0,
        }
    rng = np.random.default_rng(seed)
    amostras = rng.choice(
        valores,
        size=(configuracao.numero_reamostragens, len(valores)),
        replace=True,
    )
    try:
        referencias = estatistica_referencia(amostras, axis=1)
    except TypeError:
        referencias = np.array([estatistica_referencia(amostra) for amostra in amostras])
    replicacoes = valor_focal - np.asarray(referencias, dtype=float)
    validas = replicacoes[np.isfinite(replicacoes)]
    minimo_validas = int(np.ceil(0.95 * configuracao.numero_reamostragens))
    estimativa = float(valor_focal - media_ref)
    if len(validas) < minimo_validas:
        return {
            **metadados,
            "estimativa": estimativa,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "menos_de_95_porcento_replicas_validas",
            "n_replicas_validas": int(len(validas)),
        }
    alfa = 1 - configuracao.nivel_confianca
    inferior, superior = np.quantile(validas, [alfa / 2, 1 - alfa / 2])
    return {
        **metadados,
        "estimativa": estimativa,
        "ic_inf": float(inferior),
        "ic_sup": float(superior),
        "status": "disponivel",
        "motivo": None,
        "n_replicas_validas": int(len(validas)),
    }


def bootstrap_ic_dois_grupos(
    grupo_a: pd.Series,
    grupo_b: pd.Series,
    *,
    identificador: str,
    cursos_a: pd.Series | None = None,
    cursos_b: pd.Series | None = None,
    configuracao: ConfiguracaoBootstrap = ConfiguracaoBootstrap(),
) -> dict:
    """Bootstrap ecológico da diferença de médias reamostrando ambos os grupos."""

    a = _valores_ordenados(grupo_a, cursos_a)
    b = _valores_ordenados(grupo_b, cursos_b)
    seed = seed_para_contraste(identificador, configuracao)
    metadados = {
        "tipo_incerteza": "IC ecológico de dois grupos",
        "unidade_reamostragem": configuracao.unidade_reamostragem,
        "foco_reamostrado": True,
        "numero_reamostragens": configuracao.numero_reamostragens,
        "seed": seed,
        "nivel_confianca": configuracao.nivel_confianca,
        "n_cursos_grupo_a": int(len(a)),
        "n_cursos_grupo_b": int(len(b)),
    }
    if len(a) < N_MINIMO_INFERENCIA or len(b) < N_MINIMO_INFERENCIA:
        return {
            **metadados,
            "estimativa": None,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "um_dos_grupos_abaixo_do_minimo",
            "n_replicas_validas": 0,
        }
    estimativa = float(np.mean(a) - np.mean(b))
    rng = np.random.default_rng(seed)
    indices_a = rng.integers(0, len(a), size=(configuracao.numero_reamostragens, len(a)))
    indices_b = rng.integers(0, len(b), size=(configuracao.numero_reamostragens, len(b)))
    replicacoes = a[indices_a].mean(axis=1) - b[indices_b].mean(axis=1)
    validas = replicacoes[np.isfinite(replicacoes)]
    minimo_validas = int(np.ceil(0.95 * configuracao.numero_reamostragens))
    if len(validas) < minimo_validas:
        return {
            **metadados,
            "estimativa": estimativa,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "menos_de_95_porcento_replicas_validas",
            "n_replicas_validas": int(len(validas)),
        }
    alfa = 1 - configuracao.nivel_confianca
    inferior, superior = np.quantile(validas, [alfa / 2, 1 - alfa / 2])
    return {
        **metadados,
        "estimativa": estimativa,
        "ic_inf": float(inferior),
        "ic_sup": float(superior),
        "status": "disponivel",
        "motivo": None,
        "n_replicas_validas": int(len(validas)),
    }


def bootstrap_ic_multifoco(
    focos: pd.Series,
    benchmark: pd.Series,
    *,
    identificador: str,
    cursos_focais: pd.Series,
    cursos_benchmark: pd.Series,
    configuracao: ConfiguracaoBootstrap = ConfiguracaoBootstrap(),
) -> dict:
    """IC ecológico do contraste entre a média dos focos e a referência.

    Ambos os braços são reamostrados por ``CO_CURSO``. Com apenas um foco o
    chamador deve usar o IC condicional, mantendo-o fixo.
    """

    a = _valores_ordenados(focos, cursos_focais)
    b = _valores_ordenados(benchmark, cursos_benchmark)
    seed = seed_para_contraste(identificador, configuracao)
    metadados = {
        "tipo_incerteza": "IC ecológico multifoco",
        "unidade_reamostragem": configuracao.unidade_reamostragem,
        "foco_reamostrado": True,
        "numero_reamostragens": configuracao.numero_reamostragens,
        "seed": seed,
        "nivel_confianca": configuracao.nivel_confianca,
        "n_focos": int(len(a)),
        "n_cursos_benchmark": int(len(b)),
    }
    if len(a) < 2:
        return {
            **metadados,
            "estimativa": None,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "menos_de_dois_focos_elegiveis",
            "n_replicas_validas": 0,
        }
    if len(b) < N_MINIMO_INFERENCIA:
        return {
            **metadados,
            "estimativa": None,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "n_benchmark_abaixo_do_minimo",
            "n_replicas_validas": 0,
        }
    rng = np.random.default_rng(seed)
    indices_a = rng.integers(0, len(a), size=(configuracao.numero_reamostragens, len(a)))
    indices_b = rng.integers(0, len(b), size=(configuracao.numero_reamostragens, len(b)))
    replicacoes = a[indices_a].mean(axis=1) - b[indices_b].mean(axis=1)
    validas = replicacoes[np.isfinite(replicacoes)]
    estimativa = float(a.mean() - b.mean())
    minimo_validas = int(np.ceil(0.95 * configuracao.numero_reamostragens))
    if len(validas) < minimo_validas:
        return {
            **metadados,
            "estimativa": estimativa,
            "ic_inf": None,
            "ic_sup": None,
            "status": "insuficiente",
            "motivo": "menos_de_95_porcento_replicas_validas",
            "n_replicas_validas": int(len(validas)),
        }
    alfa = 1 - configuracao.nivel_confianca
    inferior, superior = np.quantile(validas, [alfa / 2, 1 - alfa / 2])
    return {
        **metadados,
        "estimativa": estimativa,
        "ic_inf": float(inferior),
        "ic_sup": float(superior),
        "status": "disponivel",
        "motivo": None,
        "n_replicas_validas": int(len(validas)),
    }
