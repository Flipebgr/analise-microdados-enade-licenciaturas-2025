from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.edicoes import ENADE_2025_LICENCIATURAS
from src.edicoes.base import ContratoEdicao
from src.extracao.inventario import inventariar_arquivos
from src.utilitarios.leitura import detectar_encoding, ler_txt


def contar_linhas(path: Path, encoding: str) -> int:
    with path.open("r", encoding=encoding, errors="replace", newline="") as f:
        return max(sum(1 for _ in f) - 1, 0)


def inspecionar_txt(
    path: Path,
    co_ies_ufpa: int | None = None,
    edicao: ContratoEdicao = ENADE_2025_LICENCIATURAS,
) -> tuple[dict, pd.DataFrame]:
    encoding = detectar_encoding(path)
    amostra = ler_txt(path, encoding=encoding, nrows=10000, leitura=edicao.leitura)
    total_linhas = contar_linhas(path, encoding)
    faltantes = amostra.isna().sum().rename("ausentes_amostra").reset_index().rename(columns={"index": "variavel"})
    faltantes["percentual_amostra"] = faltantes["ausentes_amostra"] / max(len(amostra), 1)
    cursos = amostra["CO_CURSO"].nunique(dropna=True) if "CO_CURSO" in amostra else None
    resumo = {
        "arquivo": path.name,
        "tamanho_bytes": path.stat().st_size,
        "encoding_detectado": encoding,
        "separador": edicao.leitura.separador,
        "decimal": edicao.leitura.decimal,
        "quotechar": edicao.leitura.quotechar,
        "possui_cabecalho": True,
        "numero_linhas": total_linhas,
        "numero_colunas": len(amostra.columns),
        "colunas": "|".join(amostra.columns),
        "cursos_distintos_amostra": cursos,
        "registros_ufpa_amostra": None,
        "duplicatas_exatas_amostra": int(amostra.duplicated().sum()),
    }
    if co_ies_ufpa is not None and "CO_IES" in amostra.columns:
        resumo["registros_ufpa_amostra"] = int((pd.to_numeric(amostra["CO_IES"], errors="coerce") == co_ies_ufpa).sum())
    return resumo, faltantes


def inspecionar_todos(
    pasta: Path,
    co_ies_ufpa: int | None = None,
    edicao: ContratoEdicao = ENADE_2025_LICENCIATURAS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    resumos, ausencias = [], []
    arquivos = inventariar_arquivos(pasta, edicao)
    for arquivo in arquivos.values():
        if arquivo.membro_zip is not None:
            raise ValueError("A inspeção completa requer um diretório extraído")
        path = arquivo.fonte
        resumo, faltantes = inspecionar_txt(path, co_ies_ufpa, edicao)
        resumos.append(resumo)
        faltantes.insert(0, "arquivo", path.name)
        ausencias.append(faltantes)
    return pd.DataFrame(resumos), pd.concat(ausencias, ignore_index=True)
