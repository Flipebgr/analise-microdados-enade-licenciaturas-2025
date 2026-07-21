from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.agregacao.comum import carregar_filtrado, validar_unicidade

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


def _agregar_indicador(df: pd.DataFrame, positivos: set[str], validos: set[str], nome: str) -> pd.DataFrame:
    g = df.groupby("CO_CURSO", observed=True)["RESPOSTA"]
    out = g.agg(
        **{
            f"{nome[:-4]}n_valido": lambda s: int(s.isin(validos).sum()),
            f"{nome[:-4]}n_positivo": lambda s: int(s.isin(positivos).sum()),
        }
    ).reset_index()
    out[nome] = out[f"{nome[:-4]}n_positivo"] / out[f"{nome[:-4]}n_valido"]
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
            indicadores.append(_agregar_indicador(df, positivos, validos, nome))
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
