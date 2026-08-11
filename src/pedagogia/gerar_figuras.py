from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.pedagogia import PEDAGOGIA

ORDEM_RECORTES = [
    "UFPA — Conceito 5",
    "UFPA — Conceito 4",
    "Outras IES do Pará",
    "Norte sem Pará",
    "Brasil sem Norte",
]


def _salvar(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def painel_ufpa(base: pd.DataFrame, path: Path) -> None:
    df = base[base["CO_IES"].eq(PEDAGOGIA.co_ies_focal)].sort_values(
        "PCT_PADRAO_PROFICIENCIA_NUM"
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    y = np.arange(len(df))
    x = df["PCT_PADRAO_PROFICIENCIA_NUM"] * 100
    tamanhos = np.maximum(df["PARTICIPANTES_NUM"].fillna(1), 5) * 3
    ref = df["CONCEITO_ENADE_NUM"].map({5: "Conceito 5", 4: "Conceito 4"})
    for rotulo, sub in df.assign(_tipo=ref).groupby("_tipo", observed=True):
        pos = [df.index.get_loc(i) for i in sub.index]
        ax.scatter(x.loc[sub.index], pos, s=tamanhos.loc[sub.index], alpha=0.8, label=rotulo)
    ax.set_yticks(y, df["ROTULO_OFERTA"])
    ax.set_xlabel("Percentual no padrão de proficiência (%)")
    ax.set_title("Pedagogia na UFPA: proficiência, participantes e Conceito Enade")
    for yi, (_, row) in zip(y, df.iterrows()):
        conceito = int(row["CONCEITO_ENADE_NUM"])
        n = int(row["PARTICIPANTES_NUM"])
        ax.annotate(
            f"C{conceito} | N={n}",
            (row["PCT_PADRAO_PROFICIENCIA_NUM"] * 100, yi),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            fontsize=8,
        )
    ax.legend()
    ax.grid(axis="x", alpha=0.25)
    _salvar(fig, path)


def posicao_relativa(base: pd.DataFrame, path: Path) -> None:
    df = base.dropna(subset=["nt_ger_mean"]).sort_values("nt_ger_mean").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(df))
    ax.scatter(x, df["nt_ger_mean"], s=10, alpha=0.25, label="Cursos do Brasil")
    ufpa = df["CO_IES"].eq(PEDAGOGIA.co_ies_focal)
    ax.scatter(x[ufpa], df.loc[ufpa, "nt_ger_mean"], s=55, marker="D", label="UFPA")
    for xi, (_, row) in zip(x[ufpa], df[ufpa].iterrows()):
        ax.annotate(
            row["ROTULO_OFERTA"],
            (xi, row["nt_ger_mean"]),
            xytext=(3, 4),
            textcoords="offset points",
            fontsize=7,
            rotation=25,
        )
    ax.set_xlabel("Cursos ordenados pela média de NT_GER")
    ax.set_ylabel("Média de NT_GER")
    ax.set_title("Posição relativa das ofertas de Pedagogia da UFPA no Brasil")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    _salvar(fig, path)


def distribuicao_notas(
    individual: pd.DataFrame,
    cadastro: pd.DataFrame,
    coluna: str,
    path: Path,
) -> None:
    df = individual.merge(
        cadastro[["CO_CURSO", "RECORTE_PEDAGOGIA"]],
        on="CO_CURSO",
        how="left",
        validate="many_to_one",
    )
    dados = [
        pd.to_numeric(
            df.loc[df["RECORTE_PEDAGOGIA"].eq(recorte), coluna],
            errors="coerce",
        ).dropna()
        for recorte in ORDEM_RECORTES
    ]
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.boxplot(
        dados,
        tick_labels=[f"{r}\nN={len(s)}" for r, s in zip(ORDEM_RECORTES, dados)],
        showfliers=False,
    )
    ax.set_ylabel(coluna)
    ax.set_title(f"Pedagogia: distribuição de {coluna} por recorte exclusivo")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.25)
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
    labels = ["Renda até 3 SM", "Trabalha", "Ação afirmativa", "Auxílio", "Bolsa", "Estuda ≥4h"]
    resumo = (
        base.groupby("RECORTE_PEDAGOGIA", observed=True)[indicadores]
        .mean()
        .reindex(ORDEM_RECORTES)
    )
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(indicadores))
    for recorte in ORDEM_RECORTES:
        if recorte in resumo.index:
            ax.plot(x, resumo.loc[recorte].to_numpy() * 100, marker="o", label=recorte)
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel("Média dos percentuais dos cursos (%)")
    ax.set_title("Pedagogia: perfil socioeconômico por recorte")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    _salvar(fig, path)


def processo_formativo(itens: pd.DataFrame, cadastro: pd.DataFrame, path: Path) -> None:
    df = itens.merge(
        cadastro[["CO_CURSO", "RECORTE_PEDAGOGIA"]],
        on="CO_CURSO",
        how="left",
        validate="many_to_one",
    )
    tab = (
        df[df["RECORTE_PEDAGOGIA"].isin(ORDEM_RECORTES)]
        .pivot_table(index="RECORTE_PEDAGOGIA", columns="ITEM", values="media", aggfunc="mean")
        .reindex(ORDEM_RECORTES)
    )
    fig, ax = plt.subplots(figsize=(15, 5))
    matriz = tab.apply(pd.to_numeric, errors="coerce").astype("float64").to_numpy()
    im = ax.imshow(matriz, aspect="auto", vmin=1, vmax=6)
    ax.set_yticks(range(len(tab.index)), tab.index)
    ax.set_xticks(range(len(tab.columns)), tab.columns, rotation=90, fontsize=7)
    ax.set_title("QE_I20–QE_I66: médias da escala válida 1–6")
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
        comparacoes["INDICADOR"].eq("nt_ger_mean") & comparacoes["RECORTE"].isin(ordem)
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
    ax.set_title("Pedagogia: comparação regional e nacional")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    _salvar(fig, path)


def desempenho_ufpa(base: pd.DataFrame, path: Path) -> None:
    df = base[base["CO_IES"].eq(PEDAGOGIA.co_ies_focal)].sort_values("nt_ger_mean")
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    largura = 0.24
    ax.bar(x - largura, df["nt_ger_mean"], largura, label="NT_GER")
    ax.bar(x, df["nt_obj_mean"], largura, label="NT_OBJ")
    ax.bar(x + largura, df["nt_dis_mean"], largura, label="NT_DIS")
    ax.set_xticks(x, df["ROTULO_OFERTA"], rotation=25, ha="right")
    ax.set_ylabel("Média")
    ax.set_title("Desempenho das ofertas de Pedagogia da UFPA")
    ax.legend()
    _salvar(fig, path)


def percentis_ufpa(base: pd.DataFrame, path: Path) -> None:
    df = base[base["CO_IES"].eq(PEDAGOGIA.co_ies_focal)].sort_values("nt_ger_percentil_brasil")
    fig, ax = plt.subplots(figsize=(10, 5))
    y = np.arange(len(df))
    ax.scatter(df["nt_ger_percentil_brasil"], y, label="Brasil", s=55)
    ax.scatter(df["nt_ger_percentil_norte"], y, marker="D", label="Norte", s=45)
    ax.scatter(df["nt_ger_percentil_para"], y, marker="s", label="Pará", s=45)
    ax.set_yticks(y, df["ROTULO_OFERTA"])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percentil de NT_GER")
    ax.set_title("Posição percentílica das ofertas da UFPA")
    ax.legend()
    ax.grid(axis="x", alpha=0.25)
    _salvar(fig, path)


def benchmarks_ufpa(resumo: pd.DataFrame, path: Path) -> None:
    df = resumo.sort_values("nt_ger_mean_DIFERENCA")
    fig, ax = plt.subplots(figsize=(10, 5))
    y = np.arange(len(df))
    ax.scatter(df["nt_ger_mean_DIFERENCA"], y, s=60)
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_yticks(y, df["ROTULO_ALVO"])
    ax.set_xlabel("Diferença NT_GER: oferta UFPA − média do benchmark")
    ax.set_title("Pedagogia: contraste com benchmark comparável por oferta")
    ax.grid(axis="x", alpha=0.25)
    _salvar(fig, path)


def recomendacao(base: pd.DataFrame, path: Path) -> None:
    indicadores = ["qe_i68_media", "qe_i69_media"]
    resumo = (
        base.groupby("RECORTE_PEDAGOGIA", observed=True)[indicadores]
        .mean()
        .reindex(ORDEM_RECORTES)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(resumo))
    largura = 0.36
    ax.bar(x - largura / 2, resumo["qe_i68_media"], largura, label="QE_I68")
    ax.bar(x + largura / 2, resumo["qe_i69_media"], largura, label="QE_I69")
    ax.set_xticks(x, resumo.index, rotation=25, ha="right")
    ax.set_ylabel("Média")
    ax.set_title("Recomendação de curso e IES por recorte")
    ax.legend()
    _salvar(fig, path)


def contraste_interno_ufpa(comparacao: pd.DataFrame, path: Path) -> None:
    indicadores = ["nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "taxa_presenca_microdados"]
    tab = comparacao[comparacao["INDICADOR"].isin(indicadores)].pivot(
        index="INDICADOR",
        columns="RECORTE_PEDAGOGIA",
        values="MEDIA_CURSOS",
    )
    tab = tab.reindex(indicadores)
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(tab.index))
    largura = 0.36
    c4 = tab.get("UFPA — Conceito 4", pd.Series(index=tab.index, dtype=float))
    c5 = tab.get("UFPA — Conceito 5", pd.Series(index=tab.index, dtype=float))
    ax.bar(x - largura / 2, c4, largura, label="UFPA — Conceito 4")
    ax.bar(x + largura / 2, c5, largura, label="UFPA — Conceito 5")
    ax.set_xticks(x, ["NT_GER", "NT_OBJ", "NT_DIS", "Presença"])
    ax.set_title("Contraste interno: ofertas UFPA Conceito 4 versus Conceito 5")
    ax.legend()
    _salvar(fig, path)
