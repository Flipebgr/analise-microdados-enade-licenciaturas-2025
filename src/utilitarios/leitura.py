from __future__ import annotations
from pathlib import Path
from charset_normalizer import from_path
import pandas as pd


def detectar_encoding(path: Path) -> str:
    resultado = from_path(path).best()
    return resultado.encoding if resultado and resultado.encoding else "utf-8-sig"


def ler_txt(path: Path, *, encoding: str | None = None, nrows: int | None = None, usecols=None) -> pd.DataFrame:
    enc = encoding or detectar_encoding(path)
    return pd.read_csv(path, sep=";", decimal=",", quotechar='"', encoding=enc, dtype="string", nrows=nrows, usecols=usecols, low_memory=False)


def encontrar_arquivo(base: Path, nome: str) -> Path:
    candidatos = list(base.rglob(nome))
    if not candidatos:
        raise FileNotFoundError(f"Arquivo não encontrado: {nome}")
    if len(candidatos) > 1:
        candidatos.sort(key=lambda p: len(str(p)))
    return candidatos[0]
