from __future__ import annotations

from pathlib import Path

import pandas as pd


def exportar_apendices(base: Path, tabelas: dict[str, pd.DataFrame]) -> list[Path]:
    pasta = base / "relatorios" / "fisica" / "apendices"
    pasta.mkdir(parents=True, exist_ok=True)
    saidas: list[Path] = []
    for nome, tabela in tabelas.items():
        caminho = pasta / f"{nome}.csv"
        tabela.to_csv(caminho, index=False, encoding="utf-8-sig")
        saidas.append(caminho)
    return saidas
