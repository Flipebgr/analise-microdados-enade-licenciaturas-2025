from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pandas as pd

from src.edicoes.base import ContratoEdicao, normalizar_conceito


IDENTIFICADORES = ("NU_ANO", "CO_GRUPO", "CO_IES", "CO_CURSO", "CO_MUNIC_CURSO")
CONTAGENS = ("INSCRITOS", "PARTICIPANTES", "TOTAL_PADRAO_PROFICIENCIA")


def _sha256(arquivo: Path) -> str:
    resumo = sha256()
    with arquivo.open("rb") as entrada:
        for bloco in iter(lambda: entrada.read(1024 * 1024), b""):
            resumo.update(bloco)
    return resumo.hexdigest()


def _normalizar_numero(valores: pd.Series, nome: str) -> pd.Series:
    texto = valores.astype("string").str.strip().replace("", pd.NA)
    numeros = pd.to_numeric(texto.str.replace(",", ".", regex=False), errors="coerce")
    invalidos = texto.notna() & numeros.isna()
    if invalidos.any():
        exemplos = texto.loc[invalidos].drop_duplicates().head(3).tolist()
        raise ValueError(f"Valores numéricos inválidos em {nome}: {exemplos}")
    if nome in CONTAGENS:
        nao_inteiros = numeros.notna() & (numeros.mod(1).ne(0) | numeros.lt(0))
        if nao_inteiros.any():
            raise ValueError(f"Contagem inválida em {nome}")
        return numeros.astype("Int64")
    return numeros.astype("Float64")


def carregar_conceitos_edicao(
    fonte: Path, edicao: ContratoEdicao
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Normaliza a planilha oficial sem alterar nem perder a tabela de origem."""

    schema = edicao.conceito
    original = pd.read_excel(fonte, sheet_name=schema.aba, dtype="string")
    mapa = dict(schema.mapa_colunas)
    faltantes = sorted(set(mapa) - set(original.columns))
    if faltantes:
        raise ValueError(f"Colunas ausentes na planilha de {edicao.ano}: {faltantes}")
    if original.columns.has_duplicates:
        raise ValueError(f"Colunas duplicadas na planilha de {edicao.ano}")

    coluna_curso = schema.coluna_origem("CO_CURSO")
    coluna_ano = schema.coluna_origem("NU_ANO")
    sem_curso = original[coluna_curso].isna() | original[coluna_curso].str.strip().eq("")
    sem_curso = sem_curso.fillna(True)
    linhas_nao_dados = sem_curso & original.drop(columns=coluna_ano).isna().all(axis=1)
    if (sem_curso & ~linhas_nao_dados).any():
        raise ValueError("Oferta da planilha de conceitos sem CO_CURSO")

    dados = original.loc[~linhas_nao_dados].rename(columns=mapa).copy()
    if dados.empty:
        raise ValueError(f"Planilha de Conceito Enade {edicao.ano} sem ofertas")
    for coluna in IDENTIFICADORES:
        dados[coluna] = dados[coluna].astype("string").str.strip()
        if dados[coluna].isna().any() or dados[coluna].eq("").any():
            raise ValueError(f"{coluna} ausente na planilha de conceitos")
        if coluna != "NU_ANO" and not dados[coluna].str.fullmatch(r"[0-9]+").all():
            raise ValueError(f"Código inválido em {coluna}")
    if dados["CO_CURSO"].duplicated().any():
        raise ValueError("CO_CURSO duplicado na planilha de conceitos")
    if dados["NU_ANO"].ne(str(edicao.ano)).fillna(True).any():
        raise ValueError(f"NU_ANO não corresponde à edição {edicao.ano}")

    for coluna in schema.colunas_numericas:
        dados[coluna] = _normalizar_numero(dados[coluna], coluna)

    conceito = dados[schema.campo_valor_original].map(normalizar_conceito)
    dados[schema.campo_conceito_numerico] = pd.array(
        [valor.conceito_numerico for valor in conceito], dtype="Int64"
    )
    dados[schema.campo_situacao] = pd.array(
        [valor.situacao.value for valor in conceito], dtype="string"
    )
    if "CONCEITO_ENADE_CONTINUO" not in dados:
        dados["CONCEITO_ENADE_CONTINUO"] = pd.Series(pd.NA, index=dados.index, dtype="Float64")
    if "OBSERVACAO_CONCEITO" not in dados:
        dados["OBSERVACAO_CONCEITO"] = pd.Series(pd.NA, index=dados.index, dtype="string")

    proveniencia = pd.DataFrame([{
        "edicao": edicao.ano,
        "fonte": str(fonte),
        "sha256": _sha256(fonte),
        "aba": schema.aba,
        "n_linhas_fonte": len(original),
        "n_linhas_nao_dados": int(linhas_nao_dados.sum()),
        "n_ofertas": len(dados),
    }])
    return dados.reset_index(drop=True), original, proveniencia
