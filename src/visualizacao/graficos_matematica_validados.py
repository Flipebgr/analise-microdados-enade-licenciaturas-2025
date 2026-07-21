from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROTULOS = {"A": "UFPA conceito 1", "B": "UFPA conceito superior", "C": "Outras IES do Pará", "D": "Restante do Norte", "E": "Restante do Brasil"}
ORDEM = list("ABCDE")


def _salvar(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def grafico_auditoria_participacao(auditoria: pd.DataFrame, path: Path) -> None:
    df = auditoria[auditoria["GRUPO_CODIGO"].isin(["A", "B"])].copy().sort_values("ROTULO_OFERTA")
    x = np.arange(len(df))
    largura = .36
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x-largura/2, df["PARTICIPANTES_NUM"], largura, label="Participantes oficiais")
    ax.bar(x+largura/2, df["nt_ger_count"], largura, label="NT_GER válida")
    ax.set_xticks(x, df["ROTULO_OFERTA"], rotation=30, ha="right")
    ax.set_ylabel("N")
    ax.set_title("Matemática/UFPA: participantes oficiais e registros válidos de NT_GER")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def grafico_sensibilidade(sens: pd.DataFrame, path: Path) -> None:
    foco = sens[sens["grupo"].isin(ORDEM)].copy()
    cenarios = foco["cenario"].drop_duplicates().tolist()
    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.arange(len(cenarios))
    for grupo in ORDEM:
        g = foco[foco["grupo"].eq(grupo)].set_index("cenario").reindex(cenarios)
        ax.plot(x, g["media_ponderada_participantes"], marker="o", label=f"{grupo}: {ROTULOS[grupo]}")
    ax.set_xticks(x, cenarios, rotation=20, ha="right")
    ax.set_ylabel("Média de NT_GER ponderada por N válido")
    ax.set_title("Sensibilidade do desempenho a critérios alternativos")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)


def grafico_benchmarks(bench: pd.DataFrame, path: Path) -> None:
    df = bench.copy()
    alvos = df["ROTULO_ALVO"].drop_duplicates().tolist()
    criterios = df["criterio"].drop_duplicates().tolist()
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(alvos))
    largura = .22
    for i, criterio in enumerate(criterios):
        g = df[df["criterio"].eq(criterio)].set_index("ROTULO_ALVO").reindex(alvos)
        ax.bar(x + (i-(len(criterios)-1)/2)*largura, g["diferenca_media"], largura, label=criterio)
    ax.axhline(0, linewidth=1)
    ax.set_xticks(x, alvos, rotation=30, ha="right")
    ax.set_ylabel("NT_GER do curso − média do benchmark")
    ax.set_title("Estabilidade da diferença para benchmarks comparáveis")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path)
