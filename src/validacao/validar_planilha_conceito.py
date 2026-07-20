from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.utilitarios.normalizacao import normalizar_texto, normalizar_codigo, situacao_conceito

MAPA_COLUNAS = {
    "Ano": "NU_ANO",
    "Código da Área": "CO_GRUPO",
    "Área de Avaliação": "AREA",
    "Código da IES": "CO_IES",
    "Nome da IES¹": "NO_IES",
    "Sigla da IES ¹": "SG_IES",
    "Organização Acadêmica ¹": "ORGANIZACAO_ACADEMICA",
    "Categoria Administrativa ²": "CATEGORIA_ADMINISTRATIVA",
    "Código do Curso": "CO_CURSO",
    "Modalidade de Ensino": "MODALIDADE",
    "Código do Município": "CO_MUNIC_CURSO",
    "Município do Curso": "MUNICIPIO",
    "Sigla da UF": "UF",
    "Nº de Concluintes Inscritos": "INSCRITOS",
    "Nº  de Concluintes Participantes": "PARTICIPANTES",
    "Total de Concluinte  Igual ou Acima do Padrão 1 de Proficiência": "TOTAL_PADRAO_PROFICIENCIA",
    "Percentual de Concluintes Igual ou Acima do Padrão 1 de Proficiência": "PCT_PADRAO_PROFICIENCIA",
    "Conceito Enade (Faixa)": "CONCEITO_ENADE",
}


def carregar_conceitos(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Conceito Enade Licenciaturas", dtype="string")
    faltantes = [c for c in MAPA_COLUNAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Colunas ausentes na planilha de conceitos: {faltantes}")
    df = df.rename(columns=MAPA_COLUNAS)
    for c in ["NU_ANO", "CO_GRUPO", "CO_IES", "CO_CURSO", "CO_MUNIC_CURSO", "INSCRITOS", "PARTICIPANTES", "TOTAL_PADRAO_PROFICIENCIA"]:
        df[c] = normalizar_codigo(df[c])
    df["IES_NORMALIZADA"] = df["NO_IES"].map(normalizar_texto)
    df["SITUACAO_CONCEITO"] = df["CONCEITO_ENADE"].map(situacao_conceito)
    df["FOCO_CONCEITO_1"] = df["SITUACAO_CONCEITO"].eq("Conceito 1")
    return df


def localizar_ufpa(df: pd.DataFrame, nome_oficial: str, sigla: str) -> pd.DataFrame:
    alvo = normalizar_texto(nome_oficial)
    mask = df["IES_NORMALIZADA"].eq(alvo) | df["SG_IES"].str.upper().eq(sigla.upper())
    resultado = df.loc[mask].copy()
    if resultado.empty:
        raise ValueError("UFPA não localizada na planilha de conceitos.")
    return resultado
