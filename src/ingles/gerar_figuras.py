from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ORDEM = ["A", "B", "C", "D", "E"]
ROTULOS = {
    "A": "UFPA conceito 1", "B": "UFPA conceito superior",
    "C": "Outras IES do Pará", "D": "Norte sem Pará",
    "E": "Brasil sem Norte",
}


def _salvar(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def painel_ufpa(base: pd.DataFrame, path: Path) -> None:
    df = base[base["CO_IES"].eq(569)].sort_values("PCT_PADRAO_PROFICIENCIA_NUM")
    fig, ax = plt.subplots(figsize=(10, 5))
    y = np.arange(len(df))
    x = df["PCT_PADRAO_PROFICIENCIA_NUM"] * 100
    tamanhos = np.maximum(df["PARTICIPANTES_NUM"].fillna(1), 5) * 4
    ax.scatter(x, y, s=tamanhos, alpha=.75)
    ax.set_yticks(y, df["ROTULO_OFERTA"])
    ax.set_xlabel("Percentual no padrão de proficiência (%)")
    ax.set_title("Letras–Inglês na UFPA: proficiência, participantes e Conceito Enade")
    for yi, (_, r) in zip(y, df.iterrows()):
        conceito = (
            "SC"
            if pd.isna(r["CONCEITO_ENADE_NUM"])
            else f"C{int(r['CONCEITO_ENADE_NUM'])}"
        )
        n = 0 if pd.isna(r["PARTICIPANTES_NUM"]) else int(r["PARTICIPANTES_NUM"])
        ax.annotate(
            f"{conceito} | N={n}",
            (r["PCT_PADRAO_PROFICIENCIA_NUM"] * 100, yi),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            fontsize=8,
        )
    ax.grid(axis="x", alpha=.25)
    _salvar(fig, path)


def posicao_relativa(base: pd.DataFrame, path: Path) -> None:
    df = (
        base.dropna(subset=["nt_ger_mean"])
        .sort_values("nt_ger_mean")
        .reset_index(drop=True)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(np.arange(len(df)), df["nt_ger_mean"], s=12, alpha=.35)
    ufpa = df["CO_IES"].eq(569)
    ax.scatter(
        np.arange(len(df))[ufpa],
        df.loc[ufpa, "nt_ger_mean"],
        s=60,
        marker="D",
        label="UFPA",
    )
    for x, (_, r) in zip(np.arange(len(df))[ufpa], df[ufpa].iterrows()):
        ax.annotate(
            r["ROTULO_OFERTA"],
            (x, r["nt_ger_mean"]),
            xytext=(3, 4),
            textcoords="offset points",
            fontsize=7,
            rotation=25,
        )
    ax.set_xlabel("Cursos ordenados pela média de NT_GER")
    ax.set_ylabel("Média de NT_GER")
    ax.set_title("Posição relativa dos cursos de Letras–Inglês no Brasil")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def distribuicao_notas(
    individual: pd.DataFrame,
    cadastro: pd.DataFrame,
    coluna: str,
    path: Path,
) -> None:
    df = individual.merge(
        cadastro[["CO_CURSO", "GRUPO_CODIGO"]],
        on="CO_CURSO",
        how="left",
        validate="many_to_one",
    )
    dados = [
        pd.to_numeric(
            df.loc[df["GRUPO_CODIGO"].eq(grupo), coluna],
            errors="coerce",
        ).dropna()
        for grupo in ORDEM
    ]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot(
        dados,
        tick_labels=[f"{g}\nN={len(s)}" for g, s in zip(ORDEM, dados)],
        showfliers=False,
    )
    ax.set_xticklabels(
        [f"{g}\n{ROTULOS[g]}\nN={len(s)}" for g, s in zip(ORDEM, dados)],
        fontsize=8,
    )
    ax.set_ylabel(coluna)
    ax.set_title(f"Distribuição de {coluna} por grupo comparativo")
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def perfil_socioeconomico(base: pd.DataFrame, path: Path) -> None:
    indicadores = [
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
        "bolsa_academica_pct",
        "estudo_4h_ou_mais_pct",
    ]
    labels = [
        "Renda até 3 SM",
        "Trabalha",
        "Ação afirmativa",
        "Recebeu auxílio",
        "Bolsa acadêmica",
        "Estuda ≥4h",
    ]
    resumo = (
        base[base["GRUPO_CODIGO"].isin(ORDEM)]
        .groupby("GRUPO_CODIGO")[indicadores]
        .mean()
        .reindex(ORDEM)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(indicadores))
    for g in ORDEM:
        ax.plot(
            x,
            resumo.loc[g].to_numpy() * 100,
            marker="o",
            label=f"{g}: {ROTULOS[g]}",
        )
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel("Média dos percentuais dos cursos (%)")
    ax.set_title("Perfil socioeconômico agregado por grupo")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def processo_formativo(itens: pd.DataFrame, cadastro: pd.DataFrame, path: Path) -> None:
    df = itens.merge(
        cadastro[["CO_CURSO", "GRUPO_CODIGO"]],
        on="CO_CURSO",
        how="left",
        validate="many_to_one",
    )
    tab = (
        df[df["GRUPO_CODIGO"].isin(ORDEM)]
        .pivot_table(
            index="GRUPO_CODIGO",
            columns="ITEM",
            values="media",
            aggfunc="mean",
        )
        .reindex(ORDEM)
    )
    fig, ax = plt.subplots(figsize=(14, 4))
    matriz = tab.apply(pd.to_numeric, errors="coerce").astype("float64").to_numpy()
    im = ax.imshow(matriz, aspect="auto", vmin=1, vmax=6)
    ax.set_yticks(range(len(tab.index)), [f"{g}: {ROTULOS[g]}" for g in tab.index])
    ax.set_xticks(range(len(tab.columns)), tab.columns, rotation=90, fontsize=7)
    ax.set_title("Itens QE_I20–QE_I66 por grupo (média da escala válida 1–6)")
    fig.colorbar(im, ax=ax, label="Média")
    _salvar(fig, path)


def comparacao_regional(comparacoes: pd.DataFrame, path: Path) -> None:
    ordem = [
        "UFPA agregada",
        "Região Norte sem UFPA",
        "Região Norte completa",
        "Nordeste",
        "Sudeste",
        "Sul",
        "Centro-Oeste",
        "Brasil geral",
    ]
    df = comparacoes[
        comparacoes["INDICADOR"].eq("nt_ger_mean")
        & comparacoes["RECORTE"].isin(ordem)
    ].copy()
    df["RECORTE"] = pd.Categorical(df["RECORTE"], categories=ordem, ordered=True)
    df = df.sort_values("RECORTE")
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(df))
    ax.scatter(x, df["MEDIA_CURSOS"], label="Média simples dos cursos", s=55)
    ax.scatter(
        x,
        df["MEDIA_PONDERADA_PARTICIPANTES"],
        marker="D",
        label="Média ponderada por participantes",
        s=55,
    )
    ax.set_xticks(x, df["RECORTE"], rotation=30, ha="right")
    ax.set_ylabel("NT_GER média")
    ax.set_title("Letras–Inglês: comparação regional e nacional de desempenho")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)
