from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _salvar(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def participacao_validada(base: pd.DataFrame, path: Path) -> None:
    ufpa = base[base["CO_IES"].eq(569)].sort_values("ROTULO_OFERTA")
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(ufpa))
    taxa_oficial = pd.to_numeric(ufpa["TAXA_PARTICIPACAO_OFICIAL"], errors="coerce") * 100
    taxa_micro = pd.to_numeric(ufpa["taxa_presenca_microdados"], errors="coerce") * 100
    largura = 0.36
    ax.bar(x - largura / 2, taxa_oficial, largura, label="Participação oficial")
    ax.bar(x + largura / 2, taxa_micro, largura, label="Presença nos microdados")
    ax.set_xticks(x, ufpa["ROTULO_OFERTA"], rotation=25, ha="right")
    ax.set_ylabel("Percentual (%)")
    ax.set_title("Letras–Inglês — auditoria de participação das ofertas da UFPA")
    ax.legend()
    _salvar(fig, path)


def sensibilidade_validada(sensibilidade: pd.DataFrame, path: Path) -> None:
    df = sensibilidade[sensibilidade["grupo"].isin(list("ABCDE"))].copy()
    cenarios = list(dict.fromkeys(df["cenario"].astype(str)))
    grupos = list("ABCDE")
    fig, ax = plt.subplots(figsize=(10, 5))
    for grupo in grupos:
        sub = df[df["grupo"].eq(grupo)].set_index("cenario").reindex(cenarios)
        ax.plot(cenarios, sub["media_cursos"], marker="o", label=f"Grupo {grupo}")
    ax.set_ylabel("NT_GER média dos cursos")
    ax.set_title("Letras–Inglês — sensibilidade do desempenho por cenário")
    ax.tick_params(axis="x", rotation=25)
    ax.legend(ncol=3, fontsize=8)
    _salvar(fig, path)


def benchmark_validado(benchmarks: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    df = benchmarks.copy()
    for criterio, sub in df.groupby("criterio", observed=True):
        ax.scatter(
            sub["nt_ger_alvo"],
            sub["media_benchmark"],
            label=str(criterio),
            s=55,
        )
    limites = pd.concat([df["nt_ger_alvo"], df["media_benchmark"]]).dropna()
    if not limites.empty:
        minimo, maximo = float(limites.min()), float(limites.max())
        ax.plot([minimo, maximo], [minimo, maximo], linestyle="--", linewidth=1)
    ax.set_xlabel("NT_GER da oferta UFPA Conceito 1")
    ax.set_ylabel("Média do benchmark comparável")
    ax.set_title("Letras–Inglês — sensibilidade do benchmark comparável")
    ax.legend(fontsize=8)
    _salvar(fig, path)


def regional_validado(comparacoes: pd.DataFrame, path: Path) -> None:
    ordem = [
        "UFPA agregada",
        "Região Norte sem UFPA",
        "Região Norte completa",
        "Brasil sem UFPA",
        "Brasil geral",
    ]
    df = comparacoes[
        comparacoes["INDICADOR"].eq("nt_ger_mean") & comparacoes["RECORTE"].isin(ordem)
    ].copy()
    df["RECORTE"] = pd.Categorical(df["RECORTE"], categories=ordem, ordered=True)
    df = df.sort_values("RECORTE")
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    ax.scatter(x, df["MEDIA_CURSOS"], label="Média simples", s=55)
    ax.scatter(x, df["MEDIA_PONDERADA_PARTICIPANTES"], marker="D", label="Média ponderada", s=55)
    ax.set_xticks(x, df["RECORTE"], rotation=25, ha="right")
    ax.set_ylabel("NT_GER média")
    ax.set_title("Letras–Inglês — validação regional e nacional")
    ax.legend()
    _salvar(fig, path)
