from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.biologia import CO_CURSO_SOURE

ORDEM_FOCAL = [
    "Soure", "UFPA sem Soure", "Outras IES do Pará",
    "Norte sem Pará", "Brasil sem Norte",
]


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
    marcadores = df["FOCO_SOURE"].map({True: "Soure", False: "Demais UFPA"})
    for rotulo, sub in df.assign(_tipo=marcadores).groupby("_tipo", observed=True):
        idx = sub.index
        pos = [df.index.get_loc(i) for i in idx]
        ax.scatter(x.loc[idx], pos, s=tamanhos.loc[idx], alpha=.8, label=rotulo)
    ax.set_yticks(y, df["ROTULO_OFERTA"])
    ax.set_xlabel("Percentual no padrão de proficiência (%)")
    ax.set_title("Ciências Biológicas na UFPA: proficiência, participantes e Conceito Enade")
    for yi, (_, r) in zip(y, df.iterrows()):
        conceito = "SC" if pd.isna(r["CONCEITO_ENADE_NUM"]) else f"C{int(r['CONCEITO_ENADE_NUM'])}"
        n = 0 if pd.isna(r["PARTICIPANTES_NUM"]) else int(r["PARTICIPANTES_NUM"])
        ax.annotate(f"{conceito} | N={n}", (r["PCT_PADRAO_PROFICIENCIA_NUM"] * 100, yi),
                    xytext=(5, 0), textcoords="offset points", va="center", fontsize=8)
    ax.legend()
    ax.grid(axis="x", alpha=.25)
    _salvar(fig, path)


def posicao_relativa(base: pd.DataFrame, path: Path) -> None:
    df = base.dropna(subset=["nt_ger_mean"]).sort_values("nt_ger_mean").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(df))
    ax.scatter(x, df["nt_ger_mean"], s=12, alpha=.3, label="Cursos do Brasil")
    ufpa = df["CO_IES"].eq(569)
    ax.scatter(x[ufpa], df.loc[ufpa, "nt_ger_mean"], s=55, marker="D", label="UFPA")
    soure = pd.to_numeric(df["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)
    ax.scatter(x[soure], df.loc[soure, "nt_ger_mean"], s=120, marker="*", label="Soure")
    for xi, (_, r) in zip(x[ufpa], df[ufpa].iterrows()):
        ax.annotate(r["ROTULO_OFERTA"], (xi, r["nt_ger_mean"]), xytext=(3, 4),
                    textcoords="offset points", fontsize=7, rotation=25)
    ax.set_xlabel("Cursos ordenados pela média de NT_GER")
    ax.set_ylabel("Média de NT_GER")
    ax.set_title("Posição relativa dos cursos de Ciências Biológicas no Brasil")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def distribuicao_notas_focal(
    individual: pd.DataFrame,
    cadastro: pd.DataFrame,
    coluna: str,
    path: Path,
) -> None:
    df = individual.merge(
        cadastro[["CO_CURSO", "RECORTE_FOCAL"]],
        on="CO_CURSO",
        how="left",
        validate="many_to_one",
    )
    dados = [
        pd.to_numeric(
            df.loc[df["RECORTE_FOCAL"].eq(recorte), coluna],
            errors="coerce",
        ).dropna()
        for recorte in ORDEM_FOCAL
    ]
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.boxplot(dados, tick_labels=[f"{r}\nN={len(s)}" for r, s in zip(ORDEM_FOCAL, dados)], showfliers=False)
    ax.set_ylabel(coluna)
    ax.set_title(f"Ciências Biológicas: distribuição de {coluna} com foco em Soure")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def perfil_socioeconomico_focal(base: pd.DataFrame, path: Path) -> None:
    indicadores = [
        "renda_ate_3sm_pct", "trabalha_pct", "acao_afirmativa_pct",
        "auxilio_permanencia_pct", "bolsa_academica_pct", "estudo_4h_ou_mais_pct",
    ]
    labels = ["Renda até 3 SM", "Trabalha", "Ação afirmativa", "Auxílio", "Bolsa", "Estuda ≥4h"]
    resumo = base.groupby("RECORTE_FOCAL", observed=True)[indicadores].mean().reindex(ORDEM_FOCAL)
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(indicadores))
    for recorte in ORDEM_FOCAL:
        if recorte not in resumo.index:
            continue
        ax.plot(x, resumo.loc[recorte].to_numpy() * 100, marker="o", label=recorte)
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel("Média dos percentuais dos cursos (%)")
    ax.set_title("Perfil socioeconômico: Soure e recortes de referência")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def processo_formativo_focal(itens: pd.DataFrame, cadastro: pd.DataFrame, path: Path) -> None:
    df = itens.merge(
        cadastro[["CO_CURSO", "RECORTE_FOCAL"]],
        on="CO_CURSO",
        how="left",
        validate="many_to_one",
    )
    tab = df[df["RECORTE_FOCAL"].isin(ORDEM_FOCAL)].pivot_table(
        index="RECORTE_FOCAL", columns="ITEM", values="media", aggfunc="mean"
    ).reindex(ORDEM_FOCAL)
    fig, ax = plt.subplots(figsize=(15, 5))
    matriz = tab.apply(pd.to_numeric, errors="coerce").astype("float64").to_numpy()
    im = ax.imshow(matriz, aspect="auto", vmin=1, vmax=6)
    ax.set_yticks(range(len(tab.index)), tab.index)
    ax.set_xticks(range(len(tab.columns)), tab.columns, rotation=90, fontsize=7)
    ax.set_title("QE_I20–QE_I66: Soure e referências (média da escala válida 1–6)")
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
    df = comparacoes[comparacoes["INDICADOR"].eq("nt_ger_mean") & comparacoes["RECORTE"].isin(ordem)].copy()
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
    ax.set_title("Ciências Biológicas: comparação regional e nacional")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def desempenho_ufpa(base: pd.DataFrame, path: Path) -> None:
    df = base[base["CO_IES"].eq(569)].sort_values("nt_ger_mean")
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    largura = .24
    ax.bar(x - largura, df["nt_ger_mean"], largura, label="NT_GER")
    ax.bar(x, df["nt_obj_mean"], largura, label="NT_OBJ")
    ax.bar(x + largura, df["nt_dis_mean"], largura, label="NT_DIS")
    ax.set_xticks(x, df["ROTULO_OFERTA"], rotation=25, ha="right")
    ax.set_ylabel("Média")
    ax.set_title("Desempenho das ofertas da UFPA, com destaque para Soure")
    ax.legend()
    _salvar(fig, path)


def percentis_soure(percentis: pd.DataFrame, path: Path) -> None:
    df = percentis.copy()
    df = df[df["INDICADOR"].str.contains("percentil", na=False)]
    labels = {
        "nt_ger_percentil_brasil": "Brasil",
        "nt_ger_percentil_norte": "Norte",
        "nt_ger_percentil_para": "Pará",
    }
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([labels.get(v, v) for v in df["INDICADOR"]], pd.to_numeric(df["VALOR"], errors="coerce"))
    ax.set_ylim(0, 100)
    ax.set_ylabel("Percentil de NT_GER")
    ax.set_title("Posição percentílica da oferta de Soure")
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def benchmark_soure(base: pd.DataFrame, benchmark: pd.DataFrame, path: Path) -> None:
    soure = base[pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)].iloc[0]
    indicadores = ["nt_ger_mean", "nt_obj_mean", "nt_dis_mean"]
    medias = [pd.to_numeric(benchmark[i], errors="coerce").mean() for i in indicadores]
    alvo = [soure.get(i) for i in indicadores]
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(indicadores))
    largura = 0.36
    ax.bar(x-largura/2, alvo, largura, label="Soure")
    ax.bar(x+largura/2, medias, largura, label=f"Benchmark (N={len(benchmark)})")
    ax.set_xticks(x, ["NT_GER", "NT_OBJ", "NT_DIS"])
    ax.set_ylabel("Média")
    ax.set_title("Soure versus benchmark estruturalmente comparável")
    ax.legend()
    _salvar(fig, path)


def recomendacao_focal(base: pd.DataFrame, path: Path) -> None:
    indicadores = ["qe_i68_media", "qe_i69_media"]
    resumo = base.groupby("RECORTE_FOCAL", observed=True)[indicadores].mean().reindex(ORDEM_FOCAL)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(resumo))
    largura = 0.36
    ax.bar(x-largura/2, resumo["qe_i68_media"], largura, label="QE_I68")
    ax.bar(x+largura/2, resumo["qe_i69_media"], largura, label="QE_I69")
    ax.set_xticks(x, resumo.index, rotation=25, ha="right")
    ax.set_ylabel("Média da escala válida")
    ax.set_title("Recomendação: Soure e recortes de referência")
    ax.legend()
    _salvar(fig, path)


def perfil_diferencial(diferencas: pd.DataFrame, path: Path) -> None:
    df = diferencas[diferencas["REFERENCIA"].eq("Benchmark comparável")].copy()
    df = df.dropna(subset=["Z_SOURE_REFERENCIA"])
    fig, ax = plt.subplots(figsize=(10, 6))
    y = np.arange(len(df))
    ax.scatter(df["Z_SOURE_REFERENCIA"], y, s=55)
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_yticks(y, df["INDICADOR"])
    ax.set_xlabel("Distância padronizada de Soure em relação ao benchmark")
    ax.set_title("Perfil diferencial de Soure — indicadores agregados por curso")
    ax.grid(axis="x", alpha=.25)
    _salvar(fig, path)
