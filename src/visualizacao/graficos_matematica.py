from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ORDEM = ["A", "B", "C", "D", "E"]
ROTULOS = {
    "A": "UFPA conceito 1",
    "B": "UFPA conceito superior",
    "C": "Outras IES do Pará",
    "D": "Restante do Norte",
    "E": "Restante do Brasil",
}


def _salvar(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def painel_ufpa(base: pd.DataFrame, path: Path) -> None:
    df = base[base["CO_IES"].eq(569)].sort_values("PCT_PADRAO_PROFICIENCIA_NUM")
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(df))
    ax.scatter(df["PCT_PADRAO_PROFICIENCIA_NUM"] * 100, y, s=np.maximum(df["PARTICIPANTES_NUM"].fillna(1), 5) * 3, alpha=.75)
    ax.set_yticks(y, df["ROTULO_OFERTA"])
    ax.set_xlabel("Percentual no padrão de proficiência (%)")
    ax.set_title("Matemática na UFPA: proficiência, participantes e Conceito Enade")
    for yi, (_, r) in zip(y, df.iterrows()):
        ax.annotate(f"C{int(r['CONCEITO_ENADE_NUM'])} | N={int(r['PARTICIPANTES_NUM'])}", (r["PCT_PADRAO_PROFICIENCIA_NUM"] * 100, yi), xytext=(5, 0), textcoords="offset points", va="center", fontsize=8)
    ax.grid(axis="x", alpha=.25)
    _salvar(fig, path)


def posicao_relativa(base: pd.DataFrame, path: Path) -> None:
    df = base.dropna(subset=["nt_ger_mean"]).sort_values("nt_ger_mean").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(np.arange(len(df)), df["nt_ger_mean"], s=12, alpha=.35)
    ufpa = df["CO_IES"].eq(569)
    ax.scatter(np.arange(len(df))[ufpa], df.loc[ufpa, "nt_ger_mean"], s=60, marker="D", label="UFPA")
    for x, (_, r) in zip(np.arange(len(df))[ufpa], df[ufpa].iterrows()):
        ax.annotate(r["ROTULO_OFERTA"], (x, r["nt_ger_mean"]), xytext=(3, 4), textcoords="offset points", fontsize=7, rotation=25)
    ax.set_xlabel("Cursos ordenados pela média de NT_GER")
    ax.set_ylabel("Média de NT_GER")
    ax.set_title("Posição relativa dos cursos de Matemática no Brasil")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def boxplot_desempenho(individual: pd.DataFrame, cadastro: pd.DataFrame, path: Path) -> None:
    df = individual.merge(cadastro[["CO_CURSO", "GRUPO_CODIGO"]], on="CO_CURSO", how="left", validate="many_to_one")
    dados = [pd.to_numeric(df.loc[df["GRUPO_CODIGO"].eq(g), "NT_GER"], errors="coerce").dropna() for g in ORDEM]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot(dados, tick_labels=[f"{g}\nN={len(s)}" for g, s in zip(ORDEM, dados)], showfliers=False)
    ax.set_xticklabels([f"{g}\n{ROTULOS[g]}\nN={len(s)}" for g, s in zip(ORDEM, dados)], fontsize=8)
    ax.set_ylabel("NT_GER")
    ax.set_title("Distribuição de NT_GER por grupo comparativo")
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def ecdf_desempenho(individual: pd.DataFrame, cadastro: pd.DataFrame, path: Path) -> None:
    df = individual.merge(cadastro[["CO_CURSO", "GRUPO_CODIGO"]], on="CO_CURSO", how="left", validate="many_to_one")
    fig, ax = plt.subplots(figsize=(9, 5))
    for g in ORDEM:
        s = pd.to_numeric(df.loc[df["GRUPO_CODIGO"].eq(g), "NT_GER"], errors="coerce").dropna().sort_values()
        if len(s):
            ax.step(s, np.arange(1, len(s)+1)/len(s), where="post", label=f"{g}: {ROTULOS[g]} (N={len(s)})")
    ax.set_xlabel("NT_GER")
    ax.set_ylabel("Proporção acumulada")
    ax.set_title("ECDF de NT_GER por grupo comparativo")
    ax.legend(fontsize=8)
    ax.grid(alpha=.25)
    _salvar(fig, path)


def indicadores_socio(base: pd.DataFrame, path: Path) -> None:
    indicadores = ["renda_ate_3sm_pct", "trabalha_pct", "acao_afirmativa_pct", "auxilio_permanencia_pct", "bolsa_academica_pct", "estudo_4h_ou_mais_pct"]
    labels = ["Renda até 3 SM", "Trabalha", "Ação afirmativa", "Recebeu auxílio", "Bolsa acadêmica", "Estuda ≥4h"]
    resumo = base[base["GRUPO_CODIGO"].isin(ORDEM)].groupby("GRUPO_CODIGO")[indicadores].mean().reindex(ORDEM)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(indicadores))
    for i, g in enumerate(ORDEM):
        ax.plot(x, resumo.loc[g].to_numpy()*100, marker="o", label=f"{g}: {ROTULOS[g]}")
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel("Média dos percentuais dos cursos (%)")
    ax.set_title("Indicadores socioeconômicos agregados por grupo")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def heatmap_processo(itens: pd.DataFrame, cadastro: pd.DataFrame, path: Path) -> None:
    df = itens.merge(cadastro[["CO_CURSO", "GRUPO_CODIGO"]], on="CO_CURSO", how="left", validate="many_to_one")
    tab = df[df["GRUPO_CODIGO"].isin(ORDEM)].pivot_table(index="GRUPO_CODIGO", columns="ITEM", values="media", aggfunc="mean").reindex(ORDEM)
    fig, ax = plt.subplots(figsize=(14, 4))
    matriz = tab.apply(pd.to_numeric, errors="coerce").astype("float64").to_numpy()
    im = ax.imshow(matriz, aspect="auto", vmin=1, vmax=6)
    ax.set_yticks(range(len(tab.index)), [f"{g}: {ROTULOS[g]}" for g in tab.index])
    ax.set_xticks(range(len(tab.columns)), tab.columns, rotation=90, fontsize=7)
    ax.set_title("Média dos itens QE_I20–QE_I66 por grupo (escala válida 1–6)")
    fig.colorbar(im, ax=ax, label="Média")
    _salvar(fig, path)


def recomendacao(base: pd.DataFrame, path: Path) -> None:
    cols = ["qe_i68_media", "qe_i69_media"]
    resumo = base[base["GRUPO_CODIGO"].isin(ORDEM)].groupby("GRUPO_CODIGO")[cols].mean().reindex(ORDEM)
    x = np.arange(len(ORDEM))
    largura = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x-largura/2, resumo["qe_i68_media"], largura, label="Recomendação do curso")
    ax.bar(x+largura/2, resumo["qe_i69_media"], largura, label="Recomendação da IES")
    ax.set_xticks(x, [f"{g}\n{ROTULOS[g]}" for g in ORDEM], fontsize=8)
    ax.set_ylim(0, 10)
    ax.set_ylabel("Nota média (0–10)")
    ax.set_title("Recomendação do curso e da instituição")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)
