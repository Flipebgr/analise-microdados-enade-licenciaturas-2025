from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.utilitarios.leitura import ler_txt
from src.utilitarios.normalizacao import normalizar_codigo

REGIOES = {1: "Norte", 2: "Nordeste", 3: "Sudeste", 4: "Sul", 5: "Centro-Oeste"}
MODALIDADES = {1: "Presencial", 2: "EaD"}


def carregar_caracterizacao(path_arq1: Path) -> pd.DataFrame:
    df = ler_txt(path_arq1)
    for c in df.columns:
        if c.startswith("CO_") or c == "NU_ANO":
            df[c] = normalizar_codigo(df[c])
    return df


def construir_tabela_mestra(caracterizacao: pd.DataFrame, conceitos_ufpa: pd.DataFrame, areas: dict[int, str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    co_ies_values = conceitos_ufpa["CO_IES"].dropna().unique().tolist()
    if len(co_ies_values) != 1:
        raise ValueError(f"Esperado um único CO_IES para a UFPA, encontrados: {co_ies_values}")
    co_ies = int(co_ies_values[0])
    micro = caracterizacao[
        caracterizacao["CO_IES"].eq(co_ies) & caracterizacao["CO_GRUPO"].isin(list(areas))
    ].drop_duplicates().copy()
    chaves = ["NU_ANO", "CO_IES", "CO_GRUPO", "CO_CURSO", "CO_MUNIC_CURSO"]
    cols_conceito = chaves + ["AREA", "NO_IES", "SG_IES", "ORGANIZACAO_ACADEMICA", "CATEGORIA_ADMINISTRATIVA", "MODALIDADE", "MUNICIPIO", "UF", "INSCRITOS", "PARTICIPANTES", "TOTAL_PADRAO_PROFICIENCIA", "PCT_PADRAO_PROFICIENCIA", "CONCEITO_ENADE", "SITUACAO_CONCEITO", "FOCO_CONCEITO_1"]
    conceito = conceitos_ufpa[conceitos_ufpa["CO_GRUPO"].isin(list(areas))][cols_conceito].copy()
    mestre = micro.merge(conceito, on=chaves, how="outer", indicator=True, validate="one_to_one")
    mestre["AREA"] = mestre["AREA"].fillna(mestre["CO_GRUPO"].map(areas))
    mestre["REGIAO"] = mestre["CO_REGIAO_CURSO"].map(REGIOES)
    mestre["ROTULO_OFERTA"] = mestre.apply(lambda r: f"{r.get('MUNICIPIO', '')} - {r.get('MODALIDADE', '')}".strip(" -"), axis=1)
    mestre["SITUACAO_CRUZAMENTO"] = mestre["_merge"].map({"both": "Correspondência validada", "left_only": "Somente nos microdados", "right_only": "Somente na planilha de conceito"})
    mestre = mestre.drop(columns="_merge").sort_values(["CO_GRUPO", "MUNICIPIO", "MODALIDADE"], na_position="last")
    divergencias = mestre[mestre["SITUACAO_CRUZAMENTO"] != "Correspondência validada"].copy()
    return mestre, divergencias
