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
    x = np.arange(len(ufpa))
    largura = 0.36
    oficial = pd.to_numeric(ufpa["TAXA_PARTICIPACAO_OFICIAL"], errors="coerce") * 100
    micro = pd.to_numeric(ufpa["taxa_presenca_microdados"], errors="coerce") * 100
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x - largura / 2, oficial, largura, label="Participação oficial")
    ax.bar(x + largura / 2, micro, largura, label="Presença nos microdados")
    ax.set_xticks(x, ufpa["ROTULO_OFERTA"], rotation=25, ha="right")
    ax.set_ylabel("Percentual (%)")
    ax.set_title("Pedagogia — auditoria de participação das ofertas da UFPA")
    ax.legend()
    _salvar(fig, path)


def contraste_interno_validado(contraste: pd.DataFrame, path: Path) -> None:
    indicadores = ["nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "taxa_presenca_microdados"]
    nomes = ["NT_GER", "NT_OBJ", "NT_DIS", "Presença"]
    df = contraste.loc[contraste["INDICADOR"].isin(indicadores)].set_index("INDICADOR")
    x = np.arange(len(indicadores))
    largura = 0.36
    castanhal = [df.loc[i, "CASTANHAL"] for i in indicadores]
    conceito4 = [df.loc[i, "MEDIA_UFPA_CONCEITO_4"] for i in indicadores]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - largura / 2, castanhal, largura, label="Castanhal — Conceito 5")
    ax.bar(x + largura / 2, conceito4, largura, label="Média UFPA — Conceito 4")
    ax.set_xticks(x, nomes)
    ax.set_title("Pedagogia — contraste interno validado da UFPA")
    ax.legend()
    _salvar(fig, path)


def sensibilidade_benchmarks_validada(sensibilidade: pd.DataFrame, path: Path) -> None:
    df = sensibilidade.loc[
        sensibilidade["CENARIO"].eq("estrutura_porte_0_5_2_0")
    ].sort_values("ROTULO_ALVO")
    y = np.arange(len(df))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["nt_ger_mean_DIFERENCA"], y, s=60)
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_yticks(y, df["ROTULO_ALVO"])
    ax.set_xlabel("Oferta UFPA − média do benchmark em NT_GER")
    ax.set_title("Pedagogia — benchmark estrutural principal por oferta")
    _salvar(fig, path)


def processo_castanhal_validado(comparacao: pd.DataFrame, path: Path) -> None:
    df = comparacao.loc[comparacao["REFERENCIA"].eq("UFPA — Conceito 4")].copy()
    df["ABS_DIF"] = pd.to_numeric(
        df["DIFERENCA_CASTANHAL_REFERENCIA"], errors="coerce"
    ).abs()
    df = df.nlargest(12, "ABS_DIF").sort_values("DIFERENCA_CASTANHAL_REFERENCIA")
    fig, ax = plt.subplots(figsize=(9, 6))
    y = np.arange(len(df))
    ax.barh(y, df["DIFERENCA_CASTANHAL_REFERENCIA"])
    ax.set_yticks(y, df["ITEM"])
    ax.axvline(0, linewidth=1)
    ax.set_xlabel("Castanhal − média das ofertas UFPA Conceito 4")
    ax.set_title("Pedagogia — QE_I20–QE_I66 com maiores diferenças internas")
    _salvar(fig, path)


def perfil_interno_validado(perfil: pd.DataFrame, path: Path) -> None:
    indicadores = [
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
        "bolsa_academica_pct",
        "estudo_4h_ou_mais_pct",
    ]
    labels = ["Renda ≤3 SM", "Trabalha", "Ação afirmativa", "Auxílio", "Bolsa", "Estuda ≥4h"]
    c5 = perfil.loc[perfil["RECORTE_PEDAGOGIA"].eq("UFPA — Conceito 5")].set_index("INDICADOR")
    c4 = perfil.loc[perfil["RECORTE_PEDAGOGIA"].eq("UFPA — Conceito 4")].set_index("INDICADOR")
    x = np.arange(len(indicadores))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, [c5.loc[i, "MEDIA_CURSOS"] * 100 for i in indicadores], marker="o", label="Castanhal — Conceito 5")
    ax.plot(x, [c4.loc[i, "MEDIA_CURSOS"] * 100 for i in indicadores], marker="o", label="UFPA — Conceito 4")
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel("Percentual (%)")
    ax.set_title("Pedagogia — perfil agregado no contraste interno")
    ax.legend()
    _salvar(fig, path)


def regional_validada(comparacoes: pd.DataFrame, path: Path) -> None:
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
    df = comparacoes.loc[
        comparacoes["INDICADOR"].eq("nt_ger_mean")
        & comparacoes["RECORTE"].isin(ordem)
    ].copy()
    df["RECORTE"] = pd.Categorical(df["RECORTE"], categories=ordem, ordered=True)
    df = df.sort_values("RECORTE")
    x = np.arange(len(df))
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.scatter(x, df["MEDIA_CURSOS"], s=55, label="Média simples")
    ax.scatter(
        x,
        df["MEDIA_PONDERADA_PARTICIPANTES"],
        s=55,
        marker="D",
        label="Média ponderada por participantes",
    )
    ax.set_xticks(x, df["RECORTE"], rotation=30, ha="right")
    ax.set_ylabel("NT_GER média")
    ax.set_title("Pedagogia — comparação regional e nacional validada")
    ax.legend()
    _salvar(fig, path)
