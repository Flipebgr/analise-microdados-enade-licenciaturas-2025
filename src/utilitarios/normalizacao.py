from __future__ import annotations
import re
import unicodedata
import pandas as pd


def normalizar_texto(valor: object) -> str:
    if pd.isna(valor):
        return ""
    texto = unicodedata.normalize("NFKD", str(valor)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", texto).strip().upper()


def normalizar_codigo(serie: pd.Series) -> pd.Series:
    return pd.to_numeric(serie, errors="coerce").astype("Int64")


def situacao_conceito(valor: object) -> str:
    if pd.isna(valor) or str(valor).strip() == "":
        return "Sem conceito"
    texto = str(valor).strip().upper()
    if texto in {"SC", "SEM CONCEITO", "-"}:
        return "Sem conceito"
    try:
        faixa = int(float(texto.replace(",", ".")))
    except ValueError:
        return "Situação não reconhecida"
    return "Conceito 1" if faixa == 1 else "Conceito superior a 1"
