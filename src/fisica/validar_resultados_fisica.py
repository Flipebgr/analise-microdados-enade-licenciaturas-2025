from __future__ import annotations

from pathlib import Path
import pandas as pd


def validar_resultados(
    base: pd.DataFrame,
    presenca: pd.DataFrame,
    desempenho: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    figuras: list[Path],
) -> None:
    ufpa = base[base["CO_IES"].eq(569)]
    if len(base) != 257:
        raise ValueError(f"Esperados 257 cursos de Física; encontrados {len(base)}")
    if len(ufpa) != 5:
        raise ValueError(f"Esperadas 5 ofertas da UFPA; encontradas {len(ufpa)}")
    if not presenca["taxa_presenca_pct"].between(0, 100).all():
        raise ValueError("Taxa de presença inválida")
    if set(desempenho["indicador"]) != {"NT_GER", "NT_OBJ", "NT_DIS"}:
        raise ValueError("Auditoria de desempenho incompleta")
    if sensibilidade.empty:
        raise ValueError("Análise de sensibilidade vazia")
    if not all(path.exists() and path.stat().st_size > 0 for path in figuras):
        raise ValueError("Uma ou mais figuras validadas não foram geradas")
