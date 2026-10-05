from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from src.agregacao.comum import carregar_filtrado, validar_unicidade
from src.edicoes.base import ContratoEdicao, RegraIndicadorQuestionario
from src.edicoes.enade_2025_licenciaturas import ENADE_2025_LICENCIATURAS
from src.utilitarios.leitura import carregar_filtrado_edicao

REGRAS_INDICADORES = {
    "QE_I05": (set("B"), set("AB"), "primeira_geracao_pct"),
    "QE_I06": (set("EFG"), set("ABCDEFG"), "mae_superior_pct"),
    "QE_I07": (set("EFG"), set("ABCDEFG"), "pai_superior_pct"),
    "QE_I09": (set("AB"), set("ABCDEFG"), "renda_ate_3sm_pct"),
    "QE_I10": (set("BCDE"), set("ABCDE"), "trabalha_pct"),
    "QE_I10_D": (set("D"), set("ABCDE"), "trabalha_40h_pct"),
    "QE_I11": (set("BCDEF"), set("ABCDEF"), "acao_afirmativa_pct"),
    "QE_I15": (set("BCDEF"), set("ABCDEF"), "auxilio_permanencia_pct"),
    "QE_I16": (set("BCDEFGH"), set("ABCDEFGH"), "bolsa_academica_pct"),
    "QE_I17": (set("CDE"), set("ABCDE"), "estudo_4h_ou_mais_pct"),
    "QE_I18": (set("AB"), set("ABCD"), "pretende_magisterio_pct"),
}

REGRAS_MULTIPLA_ESCOLHA_2025 = {
    regra.item: regra
    for regra in ENADE_2025_LICENCIATURAS.questionario.regras_indicadores
    if regra.multipla_escolha
}


def _agregar_indicador(
    df: pd.DataFrame,
    positivos: set[str],
    validos: set[str],
    nome: str,
    *,
    regra: RegraIndicadorQuestionario | None = None,
) -> pd.DataFrame:
    if regra is None:
        mascara_valida = df["RESPOSTA"].isin(validos)
        mascara_positiva = df["RESPOSTA"].isin(positivos)
    else:
        classes = df["RESPOSTA"].map(lambda valor: _classificar_resposta(valor, regra))
        mascara_valida = classes.isin(("positiva", "negativa"))
        mascara_positiva = classes.eq("positiva")

    coluna_valida = f"{nome[:-4]}n_valido"
    coluna_positiva = f"{nome[:-4]}n_positivo"
    out = (
        df[["CO_CURSO"]]
        .assign(**{coluna_valida: mascara_valida, coluna_positiva: mascara_positiva})
        .groupby("CO_CURSO", observed=True)[[coluna_valida, coluna_positiva]]
        .sum()
        .reset_index()
    )
    out[nome] = out[coluna_positiva] / out[coluna_valida]
    return out


def agregar_socioeconomico(pasta_dados: Path, cursos: list[int]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    distribuicoes: list[pd.DataFrame] = []
    indicadores: list[pd.DataFrame] = []
    regras_log: list[dict] = []
    for i in range(1, 20):
        variavel = f"QE_I{i:02d}"
        path = pasta_dados / f"microdados2025_arq{i + 6}.txt"
        df = carregar_filtrado(path, cursos, usecols=["CO_CURSO", variavel])
        df["RESPOSTA"] = df[variavel].astype("string").str.strip().str.upper().replace({"": pd.NA, ".": pd.NA})
        dist = df.groupby(["CO_CURSO", "RESPOSTA"], dropna=False).size().rename("n").reset_index()
        dist["VARIAVEL"] = variavel
        total = dist.groupby("CO_CURSO")["n"].transform("sum")
        dist["pct_total"] = dist["n"] / total
        distribuicoes.append(dist[["CO_CURSO", "VARIAVEL", "RESPOSTA", "n", "pct_total"]])
        chave_regra = variavel
        if chave_regra in REGRAS_INDICADORES:
            positivos, validos, nome = REGRAS_INDICADORES[chave_regra]
            indicadores.append(
                _agregar_indicador(
                    df, positivos, validos, nome,
                    regra=REGRAS_MULTIPLA_ESCOLHA_2025.get(variavel),
                )
            )
            regras_log.append({"variavel": variavel, "indicador": nome, "positivos": "|".join(sorted(positivos)), "validos": "|".join(sorted(validos))})
        if variavel == "QE_I10":
            positivos, validos, nome = REGRAS_INDICADORES["QE_I10_D"]
            indicadores.append(_agregar_indicador(df, positivos, validos, nome))
            regras_log.append({"variavel": variavel, "indicador": nome, "positivos": "D", "validos": "A|B|C|D|E"})

    agregado = indicadores[0]
    for parte in indicadores[1:]:
        agregado = agregado.merge(parte, on="CO_CURSO", how="outer", validate="one_to_one")
    validar_unicidade(agregado, "agregado_socioeconomico")
    return agregado, pd.concat(distribuicoes, ignore_index=True), pd.DataFrame(regras_log)


def _classificar_resposta(valor: object, regra: RegraIndicadorQuestionario) -> str:
    """Classifica uma resposta conforme o instrumento da edição."""

    if pd.isna(valor):
        return "ausente"
    texto = str(valor).strip().upper()
    if texto in {"", "."}:
        return "ausente"

    if regra.multipla_escolha:
        partes = [parte.strip() for parte in texto.split(",")]
        if not all(partes) or len(set(partes)) != len(partes):
            return "invalida"
        if len(partes) > 1 and set(partes) & regra.respostas_exclusivas:
            return "invalida"
        categorias = set(partes)
    else:
        categorias = {texto}

    if categorias <= regra.respostas_nao_aplicaveis:
        return "nao_aplicavel"
    if categorias <= regra.respostas_excluidas:
        return "excluida"
    if not categorias <= regra.respostas_validas:
        return "invalida"
    return "positiva" if categorias & regra.respostas_positivas else "negativa"


def _resumir_regra(
    dados: pd.DataFrame,
    regra: RegraIndicadorQuestionario,
    cursos: list[str],
) -> pd.DataFrame:
    classes = dados[regra.item].map(lambda valor: _classificar_resposta(valor, regra))
    contagens = (
        dados.assign(_classe=classes)
        .groupby(["CO_CURSO", "_classe"], observed=True)
        .size()
        .unstack(fill_value=0)
        .reindex(cursos, fill_value=0)
    )
    for classe in ("positiva", "negativa", "ausente", "excluida", "nao_aplicavel", "invalida"):
        if classe not in contagens:
            contagens[classe] = 0

    prefixo = regra.nome.removesuffix("pct")
    resumo = pd.DataFrame({"CO_CURSO": cursos})
    resumo[f"{prefixo}n_total"] = contagens.sum(axis=1).to_numpy()
    resumo[f"{prefixo}n_valido"] = (contagens["positiva"] + contagens["negativa"]).to_numpy()
    resumo[f"{prefixo}n_positivo"] = contagens["positiva"].to_numpy()
    for classe in ("ausente", "excluida", "nao_aplicavel", "invalida"):
        resumo[f"{prefixo}n_{classe}"] = contagens[classe].to_numpy()
    denominador = resumo[f"{prefixo}n_valido"].where(lambda serie: serie > 0)
    resumo[regra.nome] = resumo[f"{prefixo}n_positivo"].div(denominador).astype("Float64")
    return resumo


def agregar_indicadores_questionario(
    fonte: Path,
    edicao: ContratoEdicao,
    cursos: Iterable[int | str],
    *,
    chunksize: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Agrega indicadores por curso sem juntar indivíduos de arquivos distintos.

    Retorna indicadores, distribuições brutas e regras/proveniência aplicadas.
    """

    codigos = sorted({str(curso).strip() for curso in cursos})
    if not codigos:
        raise ValueError("Informe ao menos um CO_CURSO")
    regras = edicao.questionario.regras_indicadores
    if len({regra.nome for regra in regras}) != len(regras):
        raise ValueError(f"Indicadores duplicados na edição {edicao.ano}")

    agregado = pd.DataFrame({"CO_CURSO": codigos})
    distribuicoes: list[pd.DataFrame] = []
    proveniencia: list[dict] = []
    itens = list(dict.fromkeys(regra.item for regra in regras))
    for item in itens:
        if item not in edicao.questionario.itens_gerais:
            raise ValueError(f"Item {item} não pertence ao questionário geral de {edicao.ano}")
        arquivos = [schema.numero for schema in edicao.arquivos if item in schema.colunas_obrigatorias]
        if len(arquivos) != 1:
            raise ValueError(f"Item {item} deve pertencer a exatamente um arquivo temático")
        numero = arquivos[0]
        dados = carregar_filtrado_edicao(
            fonte, edicao, numero, usecols=[item], cursos=codigos, chunksize=chunksize
        )
        dados[item] = dados[item].astype("string").str.strip().str.upper()
        dados[item] = dados[item].replace({"": pd.NA, ".": pd.NA})

        distribuicao = (
            dados.groupby(["CO_CURSO", item], dropna=False, observed=True)
            .size()
            .rename("n")
            .reset_index()
            .rename(columns={item: "RESPOSTA"})
        )
        distribuicao["edicao"] = edicao.ano
        distribuicao["item"] = item
        distribuicao["arquivo"] = edicao.nome_arquivo(numero)
        total = distribuicao.groupby("CO_CURSO", observed=True)["n"].transform("sum")
        distribuicao["pct_total"] = distribuicao["n"] / total
        distribuicoes.append(distribuicao)

        for regra in (regra for regra in regras if regra.item == item):
            parte = _resumir_regra(dados, regra, codigos)
            agregado = agregado.merge(parte, on="CO_CURSO", how="left", validate="one_to_one")
            proveniencia.append(
                {
                    "edicao": edicao.ano,
                    "arquivo": edicao.nome_arquivo(numero),
                    "item": item,
                    "indicador": regra.nome,
                    "rotulo": regra.descricao,
                    "positivas": "|".join(sorted(regra.respostas_positivas)),
                    "validas": "|".join(sorted(regra.respostas_validas)),
                    "excluidas": "|".join(sorted(regra.respostas_excluidas)),
                    "nao_aplicaveis": "|".join(sorted(regra.respostas_nao_aplicaveis)),
                    "multipla_escolha": regra.multipla_escolha,
                    "exclusivas": "|".join(sorted(regra.respostas_exclusivas)),
                    "denominador": "n_valido",
                    "ausencias": "vazio ou ponto excluído do denominador",
                }
            )

    validar_unicidade(agregado, "indicadores_questionario")
    distribuicoes_df = pd.concat(distribuicoes, ignore_index=True) if distribuicoes else pd.DataFrame()
    return agregado, distribuicoes_df, pd.DataFrame(proveniencia)
