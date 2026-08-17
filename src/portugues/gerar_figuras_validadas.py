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


def participacao_ufpa_validada(base: pd.DataFrame, path: Path) -> None:
    ufpa = base.loc[base["CO_IES"].eq(569)].sort_values("ROTULO_OFERTA")
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(ufpa))
    oficial = pd.to_numeric(
        ufpa["TAXA_PARTICIPACAO_OFICIAL"], errors="coerce"
    )
    micro = pd.to_numeric(
        ufpa["taxa_presenca_microdados"], errors="coerce"
    )
    if oficial.dropna().max() <= 1.5:
        oficial = oficial * 100
    if micro.dropna().max() <= 1.5:
        micro = micro * 100
    largura = 0.36
    ax.bar(x - largura / 2, oficial, largura, label="Participação oficial")
    ax.bar(x + largura / 2, micro, largura, label="Presença nos microdados")
    ax.set_xticks(x, ufpa["ROTULO_OFERTA"], rotation=25, ha="right")
    ax.set_ylabel("Percentual (%)")
    ax.set_title("Letras–Português — auditoria de participação das ofertas da UFPA")
    ax.legend()
    _salvar(fig, path)


def sensibilidade_desempenho_validada(
    sensibilidade: pd.DataFrame,
    path: Path,
) -> None:
    df = sensibilidade.loc[
        sensibilidade["grupo"].isin(list("ABCDE"))
    ].copy()
    cenarios = list(dict.fromkeys(df["cenario"].astype(str)))
    fig, ax = plt.subplots(figsize=(10, 5))
    for grupo in "ABCDE":
        sub = df.loc[df["grupo"].eq(grupo)].set_index("cenario").reindex(cenarios)
        ax.plot(cenarios, sub["media_cursos"], marker="o", label=f"Grupo {grupo}")
    ax.set_ylabel("NT_GER média dos cursos")
    ax.set_title("Letras–Português — sensibilidade do desempenho por cenário")
    ax.tick_params(axis="x", rotation=25)
    ax.legend(ncol=3, fontsize=8)
    _salvar(fig, path)


def benchmark_conceito1_validado(
    benchmarks: pd.DataFrame,
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    df = benchmarks.copy()
    ax.scatter(
        df["criterio"],
        df["media_benchmark"],
        s=65,
        label="Média benchmark",
    )
    if not df.empty:
        ax.axhline(
            float(df["nt_ger_alvo"].iloc[0]),
            linestyle="--",
            linewidth=1.2,
            label="Belém EaD — Conceito 1",
        )
    for _, r in df.iterrows():
        ax.annotate(
            f"N={int(r['n_comparaveis'])}",
            (r["criterio"], r["media_benchmark"]),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )
    ax.set_ylabel("NT_GER média")
    ax.set_title("Letras–Português — sensibilidade do benchmark da oferta Conceito 1")
    ax.tick_params(axis="x", rotation=20)
    ax.legend()
    _salvar(fig, path)


def processo_conceito1_validado(
    processo: pd.DataFrame,
    path: Path,
) -> None:
    df = processo.loc[
        processo["REFERENCIA"].eq("UFPA — conceitos superiores")
    ].copy()
    df["ABS_DIF"] = pd.to_numeric(
        df["DIFERENCA_CONCEITO1_REFERENCIA"], errors="coerce"
    ).abs()
    df = df.nlargest(12, "ABS_DIF").sort_values(
        "DIFERENCA_CONCEITO1_REFERENCIA"
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    y = np.arange(len(df))
    ax.barh(y, df["DIFERENCA_CONCEITO1_REFERENCIA"])
    ax.axvline(0, linewidth=1)
    ax.set_yticks(y, df["ITEM"])
    ax.set_xlabel("Diferença de média: Conceito 1 − UFPA conceitos superiores")
    ax.set_title("Letras–Português — itens QE_I20–QE_I66 com maiores diferenças")
    _salvar(fig, path)


def perfil_ab_validado(perfil: pd.DataFrame, path: Path) -> None:
    indicadores = [
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
        "bolsa_academica_pct",
        "estudo_4h_ou_mais_pct",
    ]
    labels = [
        "Renda ≤3 SM",
        "Trabalha",
        "Ação afirmativa",
        "Auxílio",
        "Bolsa acadêmica",
        "Estuda ≥4h",
    ]
    df = perfil.loc[
        perfil["GRUPO_CODIGO"].isin(["A", "B"])
        & perfil["INDICADOR"].isin(indicadores)
    ].copy()
    piv = df.pivot(
        index="INDICADOR",
        columns="GRUPO_CODIGO",
        values="MEDIA_CURSOS",
    ).reindex(indicadores)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(indicadores))
    largura = 0.36
    a = piv["A"] * 100
    b = piv["B"] * 100
    ax.bar(x - largura / 2, a, largura, label="A: UFPA Conceito 1")
    ax.bar(x + largura / 2, b, largura, label="B: UFPA conceitos superiores")
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel("Percentual médio dos cursos (%)")
    ax.set_title("Letras–Português — perfil agregado no contraste A × B")
    ax.legend()
    _salvar(fig, path)


def regional_validada(comparacoes: pd.DataFrame, path: Path) -> None:
    ordem = [
        "UFPA agregada",
        "Região Norte sem UFPA",
        "Região Norte completa",
        "Brasil sem UFPA",
        "Brasil geral",
    ]
    df = comparacoes.loc[
        comparacoes["INDICADOR"].eq("nt_ger_mean")
        & comparacoes["RECORTE"].isin(ordem)
    ].copy()
    df["RECORTE"] = pd.Categorical(
        df["RECORTE"], categories=ordem, ordered=True
    )
    df = df.sort_values("RECORTE")
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    ax.scatter(x, df["MEDIA_CURSOS"], label="Média simples", s=55)
    ax.scatter(
        x,
        df["MEDIA_PONDERADA_PARTICIPANTES"],
        marker="D",
        label="Média ponderada",
        s=55,
    )
    ax.set_xticks(x, df["RECORTE"], rotation=25, ha="right")
    ax.set_ylabel("NT_GER média")
    ax.set_title("Letras–Português — validação regional e nacional")
    ax.legend()
    _salvar(fig, path)
