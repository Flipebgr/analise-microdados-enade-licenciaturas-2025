from __future__ import annotations

import math
from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.agregacao.comum import carregar_filtrado, converter_numerico
from src.educacao_fisica import EDUCACAO_FISICA
from src.educacao_fisica.rotulos_questionario import (
    DIMENSOES_TEORICAS,
    ITENS_INVERTIDOS,
    ROTULOS_DIMENSOES,
    ROTULOS_QE,
)

CRITERIOS_SENSIBILIDADE = {
    "porte_25pct": (0.75, 1.25),
    "porte_50pct": (0.50, 1.50),
    "porte_2x": (0.50, 2.00),
}


def cronbach_alpha(df: pd.DataFrame) -> float:
    x = df.apply(pd.to_numeric, errors="coerce").dropna()
    if x.shape[0] < 10 or x.shape[1] < 2:
        return float("nan")
    variancias = x.var(axis=0, ddof=1).sum()
    total = x.sum(axis=1).var(ddof=1)
    if not np.isfinite(total) or total <= 0:
        return float("nan")
    k = x.shape[1]
    return float(k / (k - 1) * (1 - variancias / total))


def carregar_processo_individual(
    path: Path,
    cursos: Iterable[int],
) -> pd.DataFrame:
    itens = sorted({item for valores in DIMENSOES_TEORICAS.values() for item in valores})
    df = carregar_filtrado(path, list(cursos), usecols=["CO_CURSO", *itens])
    for item in itens:
        df[item] = converter_numerico(df[item]).where(
            lambda s: s.between(1, 6)
        )
    return df


def catalogo_itens_processo() -> pd.DataFrame:
    linhas = []
    for dimensao, itens in DIMENSOES_TEORICAS.items():
        for item in itens:
            linhas.append(
                {
                    "ITEM": item,
                    "ROTULO_OFICIAL": ROTULOS_QE[item],
                    "DIMENSAO": dimensao,
                    "ROTULO_DIMENSAO": ROTULOS_DIMENSOES[dimensao],
                    "ESCALA_ANALITICA": "1-6",
                    "AUSENCIAS_ANALITICAS": "7=Não sei; 8=Não se aplica",
                    "INVERTIDO": item in ITENS_INVERTIDOS,
                }
            )
    # Registra explicitamente itens específicos de EaD excluídos das dimensões
    # comuns usadas para comparar as duas ofertas presenciais da UFPA.
    for item, rotulo_dimensao in (
        ("QE_I31", "Suporte docente/tutoria em EaD"),
        ("QE_I32", "Interação síncrona em EaD"),
        ("QE_I43", "Infraestrutura de polos (EaD)"),
    ):
        linhas.append(
            {
                "ITEM": item,
                "ROTULO_OFICIAL": ROTULOS_QE[item],
                "DIMENSAO": "item_especifico_ead",
                "ROTULO_DIMENSAO": rotulo_dimensao,
                "ESCALA_ANALITICA": "1-6",
                "AUSENCIAS_ANALITICAS": "7=Não sei; 8=Não se aplica",
                "INVERTIDO": False,
            }
        )
    return pd.DataFrame(linhas).sort_values("ITEM").reset_index(drop=True)


def diagnosticar_dimensoes(
    individual: pd.DataFrame,
    cursos_ufpa: set[int],
) -> pd.DataFrame:
    linhas: list[dict[str, object]] = []
    recortes = {
        "Brasil — Educação Física": individual,
        "UFPA": individual[individual["CO_CURSO"].isin(cursos_ufpa)],
    }
    for recorte, df in recortes.items():
        for dimensao, itens in DIMENSOES_TEORICAS.items():
            x = df[list(itens)]
            linhas.append(
                {
                    "RECORTE": recorte,
                    "DIMENSAO": dimensao,
                    "ROTULO_DIMENSAO": ROTULOS_DIMENSOES[dimensao],
                    "ITENS": "|".join(itens),
                    "N_ITENS": len(itens),
                    "N_CASOS_COMPLETOS": int(x.dropna().shape[0]),
                    "ALPHA_CRONBACH": cronbach_alpha(x),
                    "ITENS_INVERTIDOS": "",
                    "DECISAO": (
                        "Dimensão teórica exploratória; usar apenas após "
                        "consistência interna e com ressalva de unidimensionalidade."
                    ),
                }
            )
    return pd.DataFrame(linhas)


def agregar_dimensoes_por_curso(
    individual: pd.DataFrame,
) -> pd.DataFrame:
    resultado = pd.DataFrame(
        {"CO_CURSO": sorted(individual["CO_CURSO"].dropna().unique())}
    )
    for dimensao, itens in DIMENSOES_TEORICAS.items():
        minimo = math.ceil(len(itens) / 2)
        x = individual[list(itens)]
        escore = x.mean(axis=1, skipna=True).where(x.notna().sum(axis=1).ge(minimo))
        tmp = pd.DataFrame(
            {
                "CO_CURSO": individual["CO_CURSO"],
                "ESCORE": escore,
            }
        )
        agg = (
            tmp.groupby("CO_CURSO", observed=True)["ESCORE"]
            .agg(["count", "mean", "median", "std"])
            .reset_index()
            .rename(
                columns={
                    "count": f"dim_{dimensao}_n",
                    "mean": f"dim_{dimensao}_media",
                    "median": f"dim_{dimensao}_mediana",
                    "std": f"dim_{dimensao}_dp",
                }
            )
        )
        resultado = resultado.merge(
            agg,
            on="CO_CURSO",
            how="left",
            validate="one_to_one",
        )
    return resultado


def sensibilidade_benchmarks(
    base: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    alvos = base[base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)].copy()
    externos = base[~base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)].copy()

    resumos: list[dict[str, object]] = []
    membros: list[pd.DataFrame] = []

    for _, alvo in alvos.iterrows():
        participantes = pd.to_numeric(
            pd.Series([alvo.get("PARTICIPANTES_NUM")]),
            errors="coerce",
        ).iloc[0]

        for criterio, (inferior, superior) in CRITERIOS_SENSIBILIDADE.items():
            mask = (
                externos["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
                & externos["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
                & externos["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])
            )
            if pd.notna(participantes) and participantes > 0:
                n = pd.to_numeric(
                    externos["PARTICIPANTES_NUM"],
                    errors="coerce",
                )
                mask &= n.between(
                    max(1, participantes * inferior),
                    participantes * superior,
                )

            sel = externos.loc[mask].copy()
            if not sel.empty:
                tmp = sel[
                    [
                        "CO_CURSO",
                        "ROTULO_OFERTA",
                        "PARTICIPANTES_NUM",
                        "nt_ger_mean",
                        "nt_obj_mean",
                        "nt_dis_mean",
                    ]
                ].copy()
                tmp.insert(0, "CRITERIO", criterio)
                tmp.insert(0, "CO_CURSO_ALVO", int(alvo["CO_CURSO"]))
                membros.append(tmp)

            for indicador in ("nt_ger_mean", "nt_obj_mean", "nt_dis_mean"):
                valores = pd.to_numeric(sel.get(indicador), errors="coerce").dropna()
                valor_alvo = pd.to_numeric(
                    pd.Series([alvo.get(indicador)]),
                    errors="coerce",
                ).iloc[0]
                resumos.append(
                    {
                        "CO_CURSO_ALVO": int(alvo["CO_CURSO"]),
                        "ROTULO_ALVO": alvo["ROTULO_OFERTA"],
                        "CRITERIO": criterio,
                        "INDICADOR": indicador,
                        "N_COMPARAVEIS": int(valores.size),
                        "VALOR_ALVO": valor_alvo,
                        "MEDIA_BENCHMARK": valores.mean(),
                        "MEDIANA_BENCHMARK": valores.median(),
                        "P25_BENCHMARK": valores.quantile(0.25),
                        "P75_BENCHMARK": valores.quantile(0.75),
                        "DIF_MEDIA": valor_alvo - valores.mean(),
                        "DIF_MEDIANA": valor_alvo - valores.median(),
                    }
                )

    membros_df = (
        pd.concat(membros, ignore_index=True)
        if membros
        else pd.DataFrame()
    )
    return pd.DataFrame(resumos), membros_df


def associacoes_ecologicas(
    base: pd.DataFrame,
) -> pd.DataFrame:
    pares = [
        ("renda_ate_3sm_pct", "nt_ger_mean"),
        ("trabalha_pct", "nt_ger_mean"),
        ("auxilio_permanencia_pct", "nt_ger_mean"),
        ("qe_i68_media", "nt_ger_mean"),
        ("qe_i69_media", "nt_ger_mean"),
        ("dim_atuacao_docente_media", "nt_ger_mean"),
        ("dim_infraestrutura_recursos_media", "nt_ger_mean"),
        ("dim_organizacao_integracao_media", "nt_ger_mean"),
    ]

    linhas = []
    for xcol, ycol in pares:
        if xcol not in base.columns or ycol not in base.columns:
            continue
        tmp = base[[xcol, ycol, "PARTICIPANTES_NUM"]].copy()
        tmp[xcol] = pd.to_numeric(tmp[xcol], errors="coerce")
        tmp[ycol] = pd.to_numeric(tmp[ycol], errors="coerce")
        tmp = tmp.dropna(subset=[xcol, ycol])
        if len(tmp) < 10:
            rho = pvalor = np.nan
        else:
            rho, pvalor = spearmanr(tmp[xcol], tmp[ycol])

        linhas.append(
            {
                "X": xcol,
                "Y": ycol,
                "N_CURSOS": len(tmp),
                "SPEARMAN_RHO": rho,
                "P_VALOR": pvalor,
                "X_MIN": tmp[xcol].min(),
                "X_MAX": tmp[xcol].max(),
                "Y_MIN": tmp[ycol].min(),
                "Y_MAX": tmp[ycol].max(),
                "PARTICIPANTES_MEDIANA": pd.to_numeric(
                    tmp["PARTICIPANTES_NUM"],
                    errors="coerce",
                ).median(),
                "RESSALVA": (
                    "Associação ecológica entre indicadores agregados por curso; "
                    "não permite inferência individual ou causal."
                ),
            }
        )
    return pd.DataFrame(linhas)


def resumo_qualidade(
    base: pd.DataFrame,
    itens: pd.DataFrame,
    dimensoes: pd.DataFrame,
    benchmark: pd.DataFrame,
) -> pd.DataFrame:
    ufpa = base[base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)]
    checks = [
        ("cursos_nacionais", len(base) == 406, len(base)),
        ("ofertas_ufpa", len(ufpa) == 2, len(ufpa)),
        (
            "ufpa_sem_conceito_1",
            not ufpa["CONCEITO_ENADE_NUM"].eq(1).any(),
            int(ufpa["CONCEITO_ENADE_NUM"].eq(1).sum()),
        ),
        (
            "co_curso_unico",
            bool(base["CO_CURSO"].is_unique),
            int(base["CO_CURSO"].duplicated().sum()),
        ),
        (
            "itens_processo_20_66",
            set(itens["ITEM"]).issuperset({f"QE_I{i}" for i in range(20, 67)}),
            int(itens["ITEM"].nunique()),
        ),
        (
            "sem_itens_invertidos",
            not itens["INVERTIDO"].any(),
            int(itens["INVERTIDO"].sum()),
        ),
        (
            "dimensoes_diagnosticadas",
            dimensoes["DIMENSAO"].nunique() == len(DIMENSOES_TEORICAS),
            int(dimensoes["DIMENSAO"].nunique()),
        ),
        (
            "benchmark_duas_ofertas",
            benchmark["CO_CURSO_ALVO"].nunique() == 2,
            int(benchmark["CO_CURSO_ALVO"].nunique()),
        ),
    ]
    return pd.DataFrame(
        checks,
        columns=["CHECK", "APROVADO", "VALOR_OBSERVADO"],
    )
