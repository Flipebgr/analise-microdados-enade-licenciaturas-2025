from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from src.agregacao.comum import carregar_filtrado, converter_numerico, validar_unicidade
from src.edicoes.base import ContratoEdicao
from src.utilitarios.leitura import carregar_filtrado_edicao

ITENS = [f"QE_I{i}" for i in range(20, 67)]


def cronbach_alpha(df: pd.DataFrame) -> float:
    completo = df.dropna()
    if completo.shape[0] < 10 or completo.shape[1] < 2:
        return float("nan")
    variancias = completo.var(axis=0, ddof=1)
    total = completo.sum(axis=1)
    var_total = total.var(ddof=1)
    if not np.isfinite(var_total) or var_total == 0:
        return float("nan")
    k = completo.shape[1]
    return float(k / (k - 1) * (1 - variancias.sum() / var_total))


def agregar_processo_formativo(path: Path, cursos: list[int]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = carregar_filtrado(path, cursos, usecols=["CO_CURSO", *ITENS])
    longos: list[pd.DataFrame] = []
    escala = pd.DataFrame({"CO_CURSO": sorted(df["CO_CURSO"].dropna().unique())})
    for item in ITENS:
        valor = converter_numerico(df[item])
        valido = valor.where(valor.between(1, 6))
        tmp = pd.DataFrame({"CO_CURSO": df["CO_CURSO"], "ITEM": item, "RESPOSTA": valor, "VALIDO": valido})
        agg = tmp.groupby(["CO_CURSO", "ITEM"], observed=True).agg(
            n_total=("RESPOSTA", "size"),
            n_valido=("VALIDO", "count"),
            media=("VALIDO", "mean"),
            mediana=("VALIDO", "median"),
            dp=("VALIDO", "std"),
            concordancia_n=("VALIDO", lambda s: int(s.isin([4, 5, 6]).sum())),
            nao_sabe_n=("RESPOSTA", lambda s: int((s == 7).sum())),
            nao_aplica_n=("RESPOSTA", lambda s: int((s == 8).sum())),
        ).reset_index()
        agg["concordancia_pct"] = agg["concordancia_n"] / agg["n_valido"]
        agg["ausencia_analitica_pct"] = 1 - agg["n_valido"] / agg["n_total"]
        longos.append(agg)
        por_curso = agg[["CO_CURSO", "media", "concordancia_pct"]].rename(columns={"media": f"{item.lower()}_media", "concordancia_pct": f"{item.lower()}_concordancia_pct"})
        escala = escala.merge(por_curso, on="CO_CURSO", how="left", validate="one_to_one")

    matriz = df[ITENS].apply(converter_numerico).where(lambda x: x.apply(lambda col: col.between(1, 6)))
    alpha_total = cronbach_alpha(matriz)
    diagnostico = pd.DataFrame([{
        "escala": "QE_I20-QE_I66 (exploratória, sem uso como índice)",
        "n_itens": len(ITENS),
        "n_casos_completos": int(matriz.dropna().shape[0]),
        "cronbach_alpha": alpha_total,
        "decisao": "Não formar índice único nesta sprint; resultado apenas diagnóstico.",
    }])
    validar_unicidade(escala, "agregado_processo_formativo")
    return escala, pd.concat(longos, ignore_index=True), diagnostico


def agregar_processo_formativo_edicao(
    fonte: Path,
    edicao: ContratoEdicao,
    cursos: Iterable[int | str],
    *,
    chunksize: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Resume itens oficiais por curso, sem formar índice ou dimensão não validada."""

    codigos = sorted({str(curso).strip() for curso in cursos})
    if not codigos or "" in codigos:
        raise ValueError("Informe ao menos um CO_CURSO não vazio")

    questionario = edicao.questionario
    itens = questionario.itens_processo_formativo
    arquivos = [
        schema.numero for schema in edicao.arquivos
        if set(itens) <= set(schema.colunas_obrigatorias)
    ]
    if len(arquivos) != 1:
        raise ValueError(
            f"Itens de processo formativo de {edicao.ano} devem estar em um arquivo temático"
        )
    numero_arquivo = arquivos[0]
    dados = carregar_filtrado_edicao(
        fonte, edicao, numero_arquivo, usecols=itens, cursos=codigos, chunksize=chunksize
    )
    dados["CO_CURSO"] = dados["CO_CURSO"].astype("string").str.strip()

    validos = {str(codigo) for codigo in questionario.codigos_validos_processo}
    concordancia = {str(codigo) for codigo in questionario.codigos_concordancia_processo}
    especiais = {
        str(codigo): rotulo for codigo, rotulo in questionario.codigos_especiais_processo
    }
    agregado = pd.DataFrame({"CO_CURSO": codigos})
    resumos: list[pd.DataFrame] = []
    proveniencia: list[dict] = []

    for item in itens:
        respostas = dados[item].astype("string").str.strip()
        respostas = respostas.mask(respostas.isin(("", ".")))
        mascara_valida = respostas.isin(validos)
        mascara_ausente = respostas.isna()
        mascara_especial = respostas.isin(especiais)
        valores = pd.to_numeric(respostas.where(mascara_valida), errors="coerce")
        temp = pd.DataFrame({
            "CO_CURSO": dados["CO_CURSO"],
            "RESPOSTA": respostas,
            "VALIDO": valores,
            "_valido": mascara_valida.astype(int),
            "_ausente": mascara_ausente.astype(int),
            "_invalido": (~(mascara_valida | mascara_ausente | mascara_especial)).astype(int),
            "_concordancia": respostas.isin(concordancia).astype(int),
        })
        agregacoes = {
            "n_total": ("RESPOSTA", "size"),
            "n_valido": ("_valido", "sum"),
            "n_ausente": ("_ausente", "sum"),
            "n_invalido": ("_invalido", "sum"),
            "media": ("VALIDO", "mean"),
            "mediana": ("VALIDO", "median"),
            "dp": ("VALIDO", "std"),
            "concordancia_n": ("_concordancia", "sum"),
        }
        for codigo, rotulo in especiais.items():
            coluna = f"_especial_{rotulo}"
            temp[coluna] = respostas.eq(codigo).fillna(False).astype(int)
            agregacoes[f"n_{rotulo}"] = (coluna, "sum")

        resumo = (
            temp.groupby("CO_CURSO", observed=True)
            .agg(**agregacoes)
            .reindex(codigos)
        )
        contagens = ["n_total", "n_valido", "n_ausente", "n_invalido", "concordancia_n"]
        contagens.extend(f"n_{rotulo}" for rotulo in especiais.values())
        resumo[contagens] = resumo[contagens].fillna(0).astype(int)
        denominador_valido = resumo["n_valido"].where(lambda serie: serie > 0)
        denominador_total = resumo["n_total"].where(lambda serie: serie > 0)
        resumo["concordancia_pct"] = (
            resumo["concordancia_n"].div(denominador_valido).astype("Float64")
        )
        resumo["ausencia_analitica_pct"] = (
            (resumo["n_total"] - resumo["n_valido"])
            .div(denominador_total)
            .astype("Float64")
        )
        resumo = resumo.reset_index().rename(columns={"index": "CO_CURSO"})
        resumo.insert(0, "edicao", edicao.ano)
        resumo.insert(2, "ITEM", item)
        resumos.append(resumo)

        colunas_agregado = (
            "n_total", "n_valido", "n_ausente", "n_invalido", "media", "concordancia_pct"
        )
        por_curso = resumo[["CO_CURSO", *colunas_agregado]].rename(
            columns={coluna: f"{item.lower()}_{coluna}" for coluna in colunas_agregado}
        )
        agregado = agregado.merge(por_curso, on="CO_CURSO", how="left", validate="one_to_one")
        proveniencia.append({
            "edicao": edicao.ano,
            "arquivo": edicao.nome_arquivo(numero_arquivo),
            "item": item,
            "codigos_validos": "|".join(sorted(validos, key=int)),
            "codigos_concordancia": "|".join(sorted(concordancia, key=int)),
            "codigos_especiais": "|".join(
                f"{codigo}={rotulo}" for codigo, rotulo in especiais.items()
            ),
            "escala": questionario.descricao_escala_processo,
            "denominador_concordancia": "n_valido",
            "decisao_dimensao": "não formar índice sem validação teórica dos itens",
        })

    validar_unicidade(agregado, "agregado_processo_formativo_edicao")
    return agregado, pd.concat(resumos, ignore_index=True), pd.DataFrame(proveniencia)
