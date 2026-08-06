from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.biologia import CO_CURSO_SOURE


def _salvar(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def participacao_ufpa_validada(base: pd.DataFrame, path: Path) -> None:
    ufpa = base.loc[base["CO_IES"].eq(569)].sort_values("ROTULO_OFERTA")
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(ufpa))
    oficial = pd.to_numeric(ufpa["TAXA_PARTICIPACAO_OFICIAL"], errors="coerce") * 100
    micro = pd.to_numeric(ufpa["taxa_presenca_microdados"], errors="coerce") * 100
    largura = 0.36
    ax.bar(x - largura / 2, oficial, largura, label="Participação oficial")
    ax.bar(x + largura / 2, micro, largura, label="Presença nos microdados")
    ax.set_xticks(x, ufpa["ROTULO_OFERTA"], rotation=25, ha="right")
    ax.set_ylabel("Percentual (%)")
    ax.set_title("Ciências Biológicas — auditoria de participação das ofertas da UFPA")
    ax.legend()
    _salvar(fig, path)


def componentes_soure_validado(base: pd.DataFrame, benchmark: pd.DataFrame, path: Path) -> None:
    soure = base.loc[pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)].iloc[0]
    indicadores = ["nt_ger_mean", "nt_obj_mean", "nt_dis_mean"]
    alvo = [pd.to_numeric(pd.Series([soure.get(i)]), errors="coerce").iloc[0] for i in indicadores]
    medias = [pd.to_numeric(benchmark[i], errors="coerce").mean() for i in indicadores]
    labels = ["NT_GER", "NT_OBJ", "NT_DIS"]
    x = np.arange(len(labels))
    largura = 0.36
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - largura / 2, alvo, largura, label="Soure")
    ax.bar(x + largura / 2, medias, largura, label=f"Benchmark (N={len(benchmark)})")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Média")
    ax.set_title("Soure — componentes do desempenho versus benchmark comparável")
    ax.legend()
    _salvar(fig, path)


def sensibilidade_benchmark_validada(sensibilidade: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(sensibilidade))
    ax.plot(x, sensibilidade["nt_ger_mean_MEDIA_BENCHMARK"], marker="o", label="Benchmark NT_GER")
    ax.plot(x, sensibilidade["nt_obj_mean_MEDIA_BENCHMARK"], marker="o", label="Benchmark NT_OBJ")
    ax.plot(x, sensibilidade["nt_ger_mean_ALVO"], linestyle="--", label="Soure NT_GER")
    ax.plot(x, sensibilidade["nt_obj_mean_ALVO"], linestyle="--", label="Soure NT_OBJ")
    ax.set_xticks(x, sensibilidade["CENARIO"], rotation=25, ha="right")
    ax.set_ylabel("Média")
    ax.set_title("Soure — sensibilidade do benchmark estrutural")
    ax.legend(fontsize=8)
    _salvar(fig, path)


def processo_itens_validado(comparacao_itens: pd.DataFrame, path: Path) -> None:
    df = comparacao_itens.loc[comparacao_itens["REFERENCIA"].eq("Benchmark comparável")].copy()
    df["ABS_DIF"] = pd.to_numeric(df["DIFERENCA_SOURE_REFERENCIA"], errors="coerce").abs()
    df = df.nlargest(12, "ABS_DIF").sort_values("DIFERENCA_SOURE_REFERENCIA")
    fig, ax = plt.subplots(figsize=(9, 6))
    y = np.arange(len(df))
    ax.barh(y, df["DIFERENCA_SOURE_REFERENCIA"])
    ax.set_yticks(y, df["ITEM"])
    ax.axvline(0, linewidth=1)
    ax.set_xlabel("Soure − média do benchmark")
    ax.set_title("Soure — itens QE_I20–QE_I66 com maiores diferenças absolutas")
    _salvar(fig, path)


def perfil_focal_validado(perfil: pd.DataFrame, path: Path) -> None:
    indicadores = [
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
        "bolsa_academica_pct",
        "estudo_4h_ou_mais_pct",
    ]
    labels = ["Renda ≤3 SM", "Trabalha", "Ação afirmativa", "Auxílio", "Bolsa", "Estuda ≥4h"]
    soure = perfil.loc[perfil["RECORTE_FOCAL"].eq("Soure")].set_index("INDICADOR")
    ufpa = perfil.loc[perfil["RECORTE_FOCAL"].eq("UFPA sem Soure")].set_index("INDICADOR")
    x = np.arange(len(indicadores))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, [soure.loc[i, "MEDIA_CURSOS"] * 100 for i in indicadores], marker="o", label="Soure")
    ax.plot(x, [ufpa.loc[i, "MEDIA_CURSOS"] * 100 for i in indicadores], marker="o", label="UFPA sem Soure")
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel("Percentual (%)")
    ax.set_title("Soure — perfil socioeconômico em contraste com a UFPA")
    ax.legend()
    _salvar(fig, path)


def recomendacao_validada(perfil: pd.DataFrame, path: Path) -> None:
    indicadores = ["qe_i68_media", "qe_i69_media"]
    labels = ["QE_I68", "QE_I69"]
    recortes = ["Soure", "UFPA sem Soure", "Outras IES do Pará", "Norte sem Pará", "Brasil sem Norte"]
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(recortes))
    largura = 0.36
    for deslocamento, indicador, label in [(-largura / 2, indicadores[0], labels[0]), (largura / 2, indicadores[1], labels[1])]:
        valores = []
        for recorte in recortes:
            sub = perfil.loc[(perfil["RECORTE_FOCAL"].eq(recorte)) & (perfil["INDICADOR"].eq(indicador))]
            valores.append(sub["MEDIA_CURSOS"].iloc[0] if not sub.empty else np.nan)
        ax.bar(x + deslocamento, valores, largura, label=label)
    ax.set_xticks(x, recortes, rotation=25, ha="right")
    ax.set_ylabel("Média da resposta")
    ax.set_title("Ciências Biológicas — recomendação com foco em Soure")
    ax.legend()
    _salvar(fig, path)
