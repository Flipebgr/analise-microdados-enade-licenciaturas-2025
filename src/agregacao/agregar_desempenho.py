from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from src.agregacao.comum import carregar_filtrado, converter_numerico, resumo_numerico, validar_unicidade
from src.edicoes.base import ContratoEdicao
from src.utilitarios.leitura import carregar_filtrado_edicao

VARIAVEIS = ["NT_GER", "NT_OBJ", "NT_DIS", "PROFICIENCIA", "QT_ACERTOS"]


def agregar_desempenho(path: Path, cursos: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    colunas = ["CO_CURSO", "IN_REAPLICACAO", "TP_PRES", "TP_SIT_DISC", *VARIAVEIS]
    df = carregar_filtrado(path, cursos, usecols=colunas)
    for coluna in ["IN_REAPLICACAO", "TP_PRES", "TP_SIT_DISC"]:
        df[coluna] = converter_numerico(df[coluna])
    for variavel in VARIAVEIS:
        df[variavel] = converter_numerico(df[variavel])

    numerico = resumo_numerico(df, VARIAVEIS)
    participacao = df.groupby("CO_CURSO", observed=True).agg(
        registros_microdados=("CO_CURSO", "size"),
        presentes_validos=("TP_PRES", lambda s: int((s == 555).sum())),
        ausentes=("TP_PRES", lambda s: int(s.isin([222, 444]).sum())),
        eliminados=("TP_PRES", lambda s: int((s == 334).sum())),
        resultado_desconsiderado=("TP_PRES", lambda s: int((s == 888).sum())),
        reaplicacoes=("IN_REAPLICACAO", lambda s: int((s == 1).sum())),
        discursiva_valida=("TP_SIT_DISC", lambda s: int((s == 555).sum())),
        discursiva_zero=("TP_SIT_DISC", lambda s: int(s.isin([333, 335, 336]).sum())),
    ).reset_index()
    participacao["taxa_presenca_microdados"] = participacao["presentes_validos"] / participacao["registros_microdados"]
    agregado = participacao.merge(numerico, on="CO_CURSO", how="outer", validate="one_to_one")
    validar_unicidade(agregado, "agregado_desempenho")
    return agregado, df


def agregar_desempenho_edicao(
    fonte: Path,
    edicao: ContratoEdicao,
    cursos: Iterable[int | str],
    *,
    chunksize: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Resume o arq3 por curso usando apenas componentes da edição informada.

    A segunda tabela contém registros do próprio arq3 para auditoria; ela não
    deve ser juntada a registros individuais de outros arquivos temáticos.
    """

    mapa = edicao.desempenho.mapa_canonico
    colunas = list(dict.fromkeys(["CO_CURSO", *edicao.presenca.variaveis, *mapa.values()]))
    dados = carregar_filtrado_edicao(
        fonte, edicao, 3, usecols=colunas, cursos=cursos, chunksize=chunksize
    )
    if dados.empty:
        raise ValueError(f"Nenhum registro de desempenho encontrado para a edição {edicao.ano}")

    for variavel in mapa.values():
        dados[variavel] = converter_numerico(dados[variavel])
    presenca = converter_numerico(dados["TP_PRES"])
    dados["TP_PRES"] = presenca

    totais = dados.groupby("CO_CURSO", observed=True).size().rename("registros_microdados")
    participacao = totais.to_frame().reset_index()
    conhecidos = {codigo for codigo, _ in edicao.presenca.codigos_tp_pres}
    for codigo in sorted(conhecidos):
        contagem = (
            dados.assign(_codigo=presenca.eq(codigo).fillna(False))
            .groupby("CO_CURSO", observed=True)["_codigo"]
            .sum()
        )
        participacao[f"tp_pres_{codigo}_n"] = participacao["CO_CURSO"].map(contagem).astype(int)

    sem_codigo = presenca.isna().groupby(dados["CO_CURSO"], observed=True).sum()
    nao_mapeado = (presenca.notna() & ~presenca.isin(conhecidos)).groupby(
        dados["CO_CURSO"], observed=True
    ).sum()
    participacao["tp_pres_sem_codigo_n"] = participacao["CO_CURSO"].map(sem_codigo).astype(int)
    participacao["tp_pres_codigo_nao_mapeado_n"] = (
        participacao["CO_CURSO"].map(nao_mapeado).astype(int)
    )

    codigos_validos = [
        codigo for codigo, situacao in edicao.presenca.codigos_tp_pres
        if situacao == "presente_resultado_valido"
    ]
    if len(codigos_validos) != 1:
        raise ValueError(f"Edição {edicao.ano} deve declarar um código de presença válida")
    participacao["presentes_validos"] = participacao[f"tp_pres_{codigos_validos[0]}_n"]
    participacao["taxa_presenca_microdados"] = (
        participacao["presentes_validos"] / participacao["registros_microdados"]
    )

    # Notas fora da situação válida permanecem na tabela individual para QA,
    # mas não participam das estatísticas por curso.
    presenca_valida = presenca.eq(codigos_validos[0]).fillna(False)
    dados_validos = dados.copy()
    for canonico, origem in mapa.items():
        fora = (dados[origem].notna() & ~presenca_valida).groupby(
            dados["CO_CURSO"], observed=True
        ).sum()
        participacao[f"{canonico}_n_nota_fora_presenca_valida"] = (
            participacao["CO_CURSO"].map(fora).astype(int)
        )
        dados_validos[origem] = dados[origem].where(presenca_valida)

    numerico = resumo_numerico(dados_validos, list(mapa.values()))
    renomear = {}
    for canonico, origem in mapa.items():
        prefixo = f"{origem.lower()}_"
        for coluna in numerico.columns:
            if coluna.startswith(prefixo):
                sufixo = coluna[len(prefixo):]
                renomear[coluna] = f"{canonico}_{'n_valido' if sufixo == 'count' else sufixo}"
    numerico = numerico.rename(columns=renomear)

    agregado = participacao.merge(numerico, on="CO_CURSO", how="outer", validate="one_to_one")
    for canonico in mapa:
        agregado[f"{canonico}_n_ausente"] = (
            agregado["registros_microdados"] - agregado[f"{canonico}_n_valido"]
        )
        agregado[f"{canonico}_n_presente_sem_nota"] = (
            agregado["presentes_validos"] - agregado[f"{canonico}_n_valido"]
        )
    validar_unicidade(agregado, "agregado_desempenho_edicao")
    return agregado, dados
