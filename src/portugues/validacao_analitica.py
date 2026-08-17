from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.analise.analise_sensibilidade import sensibilidade_desempenho
from src.analise.validar_benchmarks import sensibilidade_benchmarks
from src.analise.validar_indicadores import auditar_desempenho, auditar_indicadores
from src.portugues import CO_CURSO_BELEM_EAD, PORTUGUES

RECORTES_REGIONAIS_OBRIGATORIOS = {
    "UFPA agregada",
    "Região Norte sem UFPA",
    "Região Norte completa",
    "Nordeste",
    "Sudeste",
    "Sul",
    "Centro-Oeste",
    "Brasil geral",
    "Brasil sem UFPA",
    "Restante do Brasil sem Norte",
}

INDICADORES_ECOLOGICOS = (
    "renda_ate_3sm_pct",
    "trabalha_pct",
    "acao_afirmativa_pct",
    "auxilio_permanencia_pct",
    "bolsa_academica_pct",
    "estudo_4h_ou_mais_pct",
    "turno_noturno_pct",
    "anos_desde_ingresso_media",
    "qe_i68_media",
    "qe_i69_media",
)


def obter_belem_ead(base: pd.DataFrame) -> pd.Series:
    alvo = base.loc[
        pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_BELEM_EAD)
    ]
    if len(alvo) != 1:
        raise ValueError(
            f"Esperada exatamente uma oferta focal CO_CURSO={CO_CURSO_BELEM_EAD}; "
            f"encontradas {len(alvo)}."
        )
    linha = alvo.iloc[0]
    if int(linha["CO_IES"]) != PORTUGUES.co_ies_focal:
        raise ValueError("A oferta focal não pertence à UFPA.")
    if pd.to_numeric(pd.Series([linha["CONCEITO_ENADE_NUM"]]), errors="coerce").iloc[0] != 1:
        raise ValueError("A oferta focal não possui Conceito Enade 1.")
    return linha


def auditar_participacao_desempenho(
    base: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    return auditar_desempenho(base), auditar_indicadores(base)


def validar_comparacoes_regionais(comparacoes: pd.DataFrame) -> pd.DataFrame:
    faltantes = RECORTES_REGIONAIS_OBRIGATORIOS - set(
        comparacoes["RECORTE"].dropna().astype(str)
    )
    if faltantes:
        raise ValueError(f"Recortes regionais ausentes: {sorted(faltantes)}")

    trabalho = comparacoes.copy()
    numericas = (
        "N_CURSOS",
        "N_PARTICIPANTES",
        "MEDIA_CURSOS",
        "MEDIA_PONDERADA_PARTICIPANTES",
        "MEDIANA_CURSOS",
        "DP_CURSOS",
        "P25",
        "P75",
    )
    for coluna in numericas:
        trabalho[coluna] = pd.to_numeric(trabalho[coluna], errors="coerce")

    if (trabalho["N_CURSOS"].dropna() < 0).any():
        raise ValueError("Há N_CURSOS negativo nas comparações regionais.")
    if (trabalho["N_PARTICIPANTES"].dropna() < 0).any():
        raise ValueError("Há N_PARTICIPANTES negativo nas comparações regionais.")

    trabalho["AMPLITUDE_IQR"] = trabalho["P75"] - trabalho["P25"]
    trabalho["DIF_MEDIA_PONDERADA"] = (
        trabalho["MEDIA_PONDERADA_PARTICIPANTES"] - trabalho["MEDIA_CURSOS"]
    )
    trabalho["ALERTA_IQR_NEGATIVO"] = trabalho["AMPLITUDE_IQR"].lt(0)
    return trabalho


def construir_sensibilidades(
    base: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Executa sensibilidade dos grupos A-E e do benchmark da oferta Conceito 1."""
    desempenho = sensibilidade_desempenho(base)
    benchmarks, membros = sensibilidade_benchmarks(
        base,
        co_ies_ufpa=PORTUGUES.co_ies_focal,
    )
    return desempenho, benchmarks, membros


def perfil_grupos_validado(base: pd.DataFrame) -> pd.DataFrame:
    indicadores = (
        "sexo_feminino_pct",
        "idade_media",
        "mae_superior_pct",
        "pai_superior_pct",
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "trabalha_40h_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
        "bolsa_academica_pct",
        "estudo_4h_ou_mais_pct",
        "pretende_magisterio_pct",
        "turno_noturno_pct",
        "anos_desde_ingresso_media",
        "qe_i68_media",
        "qe_i69_media",
        "qe_i70_interesse_pct",
    )
    linhas: list[dict[str, object]] = []
    for grupo in "ABCDE":
        sub = base.loc[base["GRUPO_CODIGO"].eq(grupo)]
        for indicador in indicadores:
            if indicador not in base.columns:
                continue
            valores = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append(
                {
                    "GRUPO_CODIGO": grupo,
                    "GRUPO": (
                        sub["GRUPO"].dropna().astype(str).iloc[0]
                        if not sub.empty and sub["GRUPO"].notna().any()
                        else grupo
                    ),
                    "INDICADOR": indicador,
                    "N_CURSOS": int(valores.size),
                    "MEDIA_CURSOS": valores.mean(),
                    "MEDIANA_CURSOS": valores.median(),
                    "DP_CURSOS": valores.std(ddof=1),
                    "P25": valores.quantile(0.25),
                    "P75": valores.quantile(0.75),
                }
            )
    return pd.DataFrame(linhas)


def comparar_itens_processo_conceito1(
    itens: pd.DataFrame,
    base: pd.DataFrame,
    membros_benchmark: pd.DataFrame,
) -> pd.DataFrame:
    """Compara cada QE_I20-QE_I66 da oferta Conceito 1 com referências agregadas."""
    obter_belem_ead(base)
    alvo = itens.loc[
        pd.to_numeric(itens["CO_CURSO"], errors="coerce").eq(CO_CURSO_BELEM_EAD)
    ].copy()
    if alvo.empty:
        raise ValueError("Itens de processo formativo da oferta focal não localizados.")

    grupo_b = set(
        pd.to_numeric(
            base.loc[base["GRUPO_CODIGO"].eq("B"), "CO_CURSO"],
            errors="coerce",
        )
        .dropna()
        .astype(int)
        .tolist()
    )

    principal = membros_benchmark.loc[
        membros_benchmark["criterio"].eq("porte_2x")
    ].copy()
    comparaveis = set(
        pd.to_numeric(principal["CO_CURSO"], errors="coerce")
        .dropna()
        .astype(int)
        .tolist()
    )

    norte_sem_ufpa = set(
        pd.to_numeric(
            base.loc[
                base["CO_REGIAO_CURSO"].eq(1)
                & ~base["CO_IES"].eq(PORTUGUES.co_ies_focal),
                "CO_CURSO",
            ],
            errors="coerce",
        )
        .dropna()
        .astype(int)
        .tolist()
    )
    brasil_sem_ufpa = set(
        pd.to_numeric(
            base.loc[~base["CO_IES"].eq(PORTUGUES.co_ies_focal), "CO_CURSO"],
            errors="coerce",
        )
        .dropna()
        .astype(int)
        .tolist()
    )

    referencias = {
        "UFPA — conceitos superiores": grupo_b,
        "Benchmark comparável": comparaveis,
        "Norte sem UFPA": norte_sem_ufpa,
        "Brasil sem UFPA": brasil_sem_ufpa,
    }

    linhas: list[dict[str, object]] = []
    for _, linha_alvo in alvo.iterrows():
        item = linha_alvo["ITEM"]
        media_alvo = pd.to_numeric(
            pd.Series([linha_alvo["media"]]), errors="coerce"
        ).iloc[0]
        n_alvo = pd.to_numeric(
            pd.Series([linha_alvo["n_valido"]]), errors="coerce"
        ).iloc[0]

        item_todos = itens.loc[itens["ITEM"].eq(item)].copy()
        item_todos["CO_CURSO_NUM"] = pd.to_numeric(
            item_todos["CO_CURSO"], errors="coerce"
        )

        for nome, codigos in referencias.items():
            ref = item_todos.loc[item_todos["CO_CURSO_NUM"].isin(codigos)]
            medias = pd.to_numeric(ref["media"], errors="coerce").dropna()
            media_ref = medias.mean()
            linhas.append(
                {
                    "ITEM": item,
                    "REFERENCIA": nome,
                    "MEDIA_CONCEITO1": media_alvo,
                    "N_VALIDO_CONCEITO1": n_alvo,
                    "N_CURSOS_REFERENCIA": int(medias.size),
                    "MEDIA_REFERENCIA": media_ref,
                    "MEDIANA_REFERENCIA": medias.median(),
                    "DP_REFERENCIA": medias.std(ddof=1),
                    "DIFERENCA_CONCEITO1_REFERENCIA": (
                        media_alvo - media_ref
                        if pd.notna(media_alvo) and pd.notna(media_ref)
                        else np.nan
                    ),
                }
            )
    return pd.DataFrame(linhas)


def diagnosticar_outliers(
    base: pd.DataFrame,
    indicadores: Iterable[str] = ("nt_ger_mean", "nt_obj_mean", "nt_dis_mean"),
) -> pd.DataFrame:
    linhas: list[dict[str, object]] = []
    for indicador in indicadores:
        valores = pd.to_numeric(base[indicador], errors="coerce")
        validos = valores.dropna()
        q1 = validos.quantile(0.25)
        q3 = validos.quantile(0.75)
        iqr = q3 - q1
        inferior = q1 - 1.5 * iqr
        superior = q3 + 1.5 * iqr
        for idx, valor in valores.items():
            if pd.isna(valor):
                continue
            linhas.append(
                {
                    "CO_CURSO": base.loc[idx, "CO_CURSO"],
                    "ROTULO_OFERTA": base.loc[idx, "ROTULO_OFERTA"],
                    "GRUPO_CODIGO": base.loc[idx, "GRUPO_CODIGO"],
                    "INDICADOR": indicador,
                    "VALOR": float(valor),
                    "Q1": float(q1),
                    "Q3": float(q3),
                    "LIMITE_INFERIOR": float(inferior),
                    "LIMITE_SUPERIOR": float(superior),
                    "OUTLIER_IQR": bool(valor < inferior or valor > superior),
                }
            )
    return pd.DataFrame(linhas)


def associacoes_ecologicas(base: pd.DataFrame) -> pd.DataFrame:
    y = pd.to_numeric(base["nt_ger_mean"], errors="coerce")
    linhas: list[dict[str, object]] = []
    for indicador in INDICADORES_ECOLOGICOS:
        if indicador not in base.columns:
            continue
        x = pd.to_numeric(base[indicador], errors="coerce")
        mask = x.notna() & y.notna()
        n = int(mask.sum())
        rho = np.nan
        pvalor = np.nan
        if n >= 3 and x[mask].nunique() > 1 and y[mask].nunique() > 1:
            resultado = spearmanr(x[mask], y[mask], nan_policy="omit")
            rho = float(resultado.statistic)
            pvalor = float(resultado.pvalue)
        linhas.append(
            {
                "INDICADOR_X": indicador,
                "INDICADOR_Y": "nt_ger_mean",
                "N_CURSOS": n,
                "SPEARMAN_RHO": rho,
                "P_VALOR_EXPLORATORIO": pvalor,
                "NIVEL_ANALISE": "curso (ecológico)",
                "RESSALVA": "não interpretar como associação individual ou causal",
            }
        )
    return pd.DataFrame(linhas)


def recomendacao_grupos(base: pd.DataFrame) -> pd.DataFrame:
    indicadores = (
        "qe_i68_media",
        "qe_i69_media",
        "qe_i70_interesse_pct",
    )
    linhas: list[dict[str, object]] = []
    for grupo in "ABCDE":
        sub = base.loc[base["GRUPO_CODIGO"].eq(grupo)]
        for indicador in indicadores:
            if indicador not in base.columns:
                continue
            valores = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append(
                {
                    "GRUPO_CODIGO": grupo,
                    "INDICADOR": indicador,
                    "N_CURSOS": int(valores.size),
                    "MEDIA_CURSOS": valores.mean(),
                    "MEDIANA_CURSOS": valores.median(),
                    "DP_CURSOS": valores.std(ddof=1),
                }
            )
    return pd.DataFrame(linhas)
