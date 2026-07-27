from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CO_IES_UFPA = 569


def _salvar(fig: plt.Figure, path: Path, nota: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.text(0.01, 0.01, nota, fontsize=8, ha="left", va="bottom", wrap=True)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def presenca_validada(auditoria: pd.DataFrame, path: Path) -> None:
    dados = auditoria.sort_values("taxa_presenca_pct")
    fig, ax = plt.subplots(figsize=(11, 6))
    barras = ax.barh(dados["ROTULO_OFERTA"], dados["taxa_presenca_pct"])
    ax.set_title("Taxa de Presença na Prova por Oferta da UFPA", loc="left", fontsize=16, weight="bold")
    ax.set_xlabel("Presença (%)")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", alpha=.25)
    for barra, valor, n in zip(barras, dados["taxa_presenca_pct"], dados["presentes_validos"], strict=False):
        ax.text(min(valor + 1.2, 98), barra.get_y() + barra.get_height()/2, f"{valor:.1f}% | N={int(n)}", va="center", fontsize=9)
    _salvar(fig, path, "Taxa derivada de TP_PRES nos registros elegíveis; participantes oficiais preservados separadamente. Fonte: Microdados Enade 2025 — INEP.")


def desempenho_validado(base: pd.DataFrame, path: Path) -> None:
    dados = base[base["CO_IES"].eq(CO_IES_UFPA)].sort_values("nt_ger_mean")
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    barras = ax.barh(dados["ROTULO_OFERTA"], dados["nt_ger_mean"])
    ax.errorbar(
        dados["nt_ger_mean"], np.arange(len(dados)),
        xerr=[dados["nt_ger_mean"] - dados["nt_ger_ic95_inf"], dados["nt_ger_ic95_sup"] - dados["nt_ger_mean"]],
        fmt="none", ecolor="black", capsize=3, linewidth=1,
    )
    ax.set_title("Nota Geral por Oferta de Física da UFPA", loc="left", fontsize=16, weight="bold")
    ax.set_xlabel("NT_GER média (0–100)")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", alpha=.25)
    for barra, valor, n in zip(barras, dados["nt_ger_mean"], dados["nt_ger_count"], strict=False):
        ax.text(valor + 1, barra.get_y() + barra.get_height()/2, f"{valor:.1f} | N={int(n)}", va="center", fontsize=9)
    _salvar(fig, path, "Barras: média; hastes: IC95% aproximado. Resultados por CO_CURSO. Fonte: Microdados Enade 2025 — INEP.")


def dificuldade_validada(base: pd.DataFrame, path: Path) -> None:
    dados = base[base["CO_IES"].eq(CO_IES_UFPA)].copy().sort_values("CONCEITO_ENADE_NUM")
    itens = [
        ("co_rs_i1_dificuldade_alta_pct", "CO_RS_I1"),
        ("co_rs_i2_dificuldade_alta_pct", "CO_RS_I2"),
        ("co_rs_i7_dificuldade_alta_pct", "CO_RS_I7"),
    ]
    x = np.arange(len(dados))
    largura = .24
    fig, ax = plt.subplots(figsize=(12, 6.3))
    for i, (col, nome) in enumerate(itens):
        ax.bar(x + (i-1)*largura, pd.to_numeric(dados[col], errors="coerce"), largura, label=nome)
    ax.set_xticks(x, [f"{r}\nConceito {int(c)}" for r, c in zip(dados["ROTULO_OFERTA"], dados["CONCEITO_ENADE_NUM"], strict=False)], rotation=20, ha="right")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Dificuldade alta (%)")
    ax.set_title("Conceito Enade e Percepção de Dificuldade", loc="left", fontsize=16, weight="bold")
    ax.legend(frameon=False, ncol=3)
    ax.grid(axis="y", alpha=.25)
    _salvar(fig, path, "Indicadores agregados por curso a partir de itens do arquivo de desempenho. Associação ecológica; não vincula percepção e nota do mesmo estudante.")


def socioeconomico_validado(base: pd.DataFrame, path: Path) -> None:
    indicadores = [
        ("renda_ate_3sm_pct", "Renda até 3 SM"),
        ("trabalha_pct", "Trabalha"),
        ("primeira_geracao_pct", "Primeira geração"),
        ("acao_afirmativa_pct", "Ação afirmativa"),
        ("auxilio_permanencia_pct", "Auxílio permanência"),
        ("estudo_4h_ou_mais_pct", "Estuda 4h+"),
    ]
    dados = base[base["CO_IES"].eq(CO_IES_UFPA)].set_index("ROTULO_OFERTA")
    matriz = pd.DataFrame({nome: pd.to_numeric(dados[col], errors="coerce") * 100 for col, nome in indicadores})
    fig, ax = plt.subplots(figsize=(12.5, 6.5))
    imagem = ax.imshow(matriz.to_numpy(), aspect="auto", vmin=0, vmax=100, cmap="Blues")
    ax.set_xticks(range(len(matriz.columns)), matriz.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(matriz.index)), matriz.index)
    ax.set_title("Síntese Socioeconômica por Oferta de Física da UFPA", loc="left", fontsize=16, weight="bold")
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            valor = matriz.iloc[i, j]
            if pd.notna(valor):
                ax.text(j, i, f"{valor:.0f}", ha="center", va="center", color="white" if valor >= 60 else "black", fontsize=9)
    fig.colorbar(imagem, ax=ax, shrink=.75, label="Percentual válido (%)")
    _salvar(fig, path, "Indicadores agregados por CO_CURSO, com denominadores válidos específicos. Leitura ecológica e contextual. Fonte: Questionário do Estudante — Enade 2025.")
