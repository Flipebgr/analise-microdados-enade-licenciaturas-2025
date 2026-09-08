from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.educacao_fisica import EDUCACAO_FISICA
from src.educacao_fisica.rotulos_questionario import ROTULOS_DIMENSOES

UFPA_IDS = {21849: "Castanhal", 104598: "Belém"}


def _salvar(fig: plt.Figure, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(caminho, dpi=180, bbox_inches="tight")
    plt.close(fig)


def painel_ufpa(base: pd.DataFrame, caminho: Path) -> None:
    df = base[base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)].copy()
    df = df.sort_values("ROTULO_OFERTA")
    fig, ax = plt.subplots(figsize=(9, 4.8))
    y = np.arange(len(df))
    taxas = pd.to_numeric(df["TAXA_PARTICIPACAO_OFICIAL"], errors="coerce") * 100
    ax.barh(y, taxas)
    ax.set_yticks(y, df["ROTULO_OFERTA"])
    ax.set_xlabel("Taxa oficial de participação (%)")
    ax.set_title("Educação Física — ofertas UFPA no Enade 2025")
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(
            taxas.iloc[i] + 1,
            i,
            (
                f"N={int(row['PARTICIPANTES_NUM'])} participantes | "
                f"Conceito {int(row['CONCEITO_ENADE_NUM'])}"
            ),
            va="center",
            fontsize=9,
        )
    ax.set_xlim(0, max(105, float(taxas.max()) + 28))
    _salvar(fig, caminho)


def posicao_relativa(base: pd.DataFrame, caminho: Path) -> None:
    ufpa = base[base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)].copy()
    nacional = pd.to_numeric(base["nt_ger_mean"], errors="coerce").dropna()
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.boxplot(
        nacional,
        vert=False,
        widths=0.35,
        showfliers=False,
        tick_labels=["Brasil — cursos"],
    )
    for _, row in ufpa.iterrows():
        ax.scatter(row["nt_ger_mean"], 1, s=65, zorder=3)
        ax.annotate(
            f"{row['ROTULO_OFERTA']}\n{row['nt_ger_mean']:.1f}",
            (row["nt_ger_mean"], 1),
            xytext=(0, 18 if row["CO_CURSO"] == 104598 else -34),
            textcoords="offset points",
            ha="center",
        )
    ax.set_xlabel("Média do curso em NT_GER")
    ax.set_title(
        "Posição das ofertas da UFPA na distribuição nacional de Educação Física"
    )
    _salvar(fig, caminho)


def distribuicao_nota(
    individual: pd.DataFrame,
    variavel: str,
    titulo: str,
    caminho: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    dados = []
    labels = []
    for curso, campus in UFPA_IDS.items():
        valores = pd.to_numeric(
            individual.loc[individual["CO_CURSO"].eq(curso), variavel],
            errors="coerce",
        ).dropna()
        dados.append(valores.to_numpy())
        labels.append(f"{campus}\nN={len(valores)}")
    ax.boxplot(dados, tick_labels=labels, showmeans=True)
    ax.set_ylabel(variavel)
    ax.set_title(titulo)
    _salvar(fig, caminho)


def perfil_socioeconomico(base: pd.DataFrame, caminho: Path) -> None:
    df = base[base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)].copy()
    indicadores = {
        "renda_ate_3sm_pct": "Renda até 3 SM",
        "trabalha_pct": "Trabalha",
        "acao_afirmativa_pct": "Ação afirmativa",
        "auxilio_permanencia_pct": "Auxílio permanência",
        "bolsa_academica_pct": "Bolsa acadêmica",
        "estudo_4h_ou_mais_pct": "Estuda ≥4h/semana",
    }
    x = np.arange(len(indicadores))
    largura = 0.35
    fig, ax = plt.subplots(figsize=(11, 5.2))
    for j, (_, row) in enumerate(df.sort_values("ROTULO_OFERTA").iterrows()):
        vals = [
            100 * pd.to_numeric(pd.Series([row.get(col)]), errors="coerce").iloc[0]
            for col in indicadores
        ]
        ax.bar(
            x + (j - 0.5) * largura,
            vals,
            largura,
            label=row["ROTULO_OFERTA"],
        )
    ax.set_xticks(x, list(indicadores.values()), rotation=25, ha="right")
    ax.set_ylabel("% entre respostas válidas")
    ax.set_title("Perfil socioeconômico — ofertas UFPA")
    ax.legend()
    _salvar(fig, caminho)


def processo_formativo(base: pd.DataFrame, caminho: Path) -> None:
    ufpa = base[base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)].copy()
    dimensoes = list(ROTULOS_DIMENSOES)
    matriz = []
    labels_campus = []
    for _, row in ufpa.sort_values("ROTULO_OFERTA").iterrows():
        matriz.append(
            [
                pd.to_numeric(
                    pd.Series([row.get(f"dim_{dim}_media")]),
                    errors="coerce",
                ).iloc[0]
                for dim in dimensoes
            ]
        )
        labels_campus.append(row["ROTULO_OFERTA"])
    arr = np.array(matriz, dtype=float)

    fig, ax = plt.subplots(figsize=(12, 4.8))
    im = ax.imshow(arr, aspect="auto", vmin=1, vmax=6)
    ax.set_yticks(np.arange(len(labels_campus)), labels_campus)
    ax.set_xticks(
        np.arange(len(dimensoes)),
        [ROTULOS_DIMENSOES[d] for d in dimensoes],
        rotation=35,
        ha="right",
    )
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if np.isfinite(arr[i, j]):
                ax.text(j, i, f"{arr[i, j]:.2f}", ha="center", va="center")
    ax.set_title("Processo formativo — médias das dimensões exploratórias (1–6)")
    fig.colorbar(im, ax=ax, label="Média")
    _salvar(fig, caminho)


def benchmark_sensibilidade(resumo: pd.DataFrame, caminho: Path) -> None:
    df = resumo[
        resumo["INDICADOR"].eq("nt_ger_mean")
    ].copy()
    criterios = ["porte_25pct", "porte_50pct", "porte_2x"]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    for curso, parte in df.groupby("CO_CURSO_ALVO", observed=True):
        parte = parte.set_index("CRITERIO").reindex(criterios).reset_index()
        label = parte["ROTULO_ALVO"].dropna().iloc[0]
        ax.plot(
            np.arange(len(criterios)),
            parte["MEDIANA_BENCHMARK"],
            marker="o",
            label=f"Mediana benchmark — {label}",
        )
        alvo = parte["VALOR_ALVO"].dropna().iloc[0]
        ax.axhline(alvo, linestyle="--", linewidth=1)
    ax.set_xticks(
        np.arange(len(criterios)),
        ["±25% porte", "0,5–1,5x", "0,5–2x"],
    )
    ax.set_ylabel("NT_GER média do curso")
    ax.set_title("Sensibilidade do benchmark comparável")
    ax.legend(fontsize=8)
    _salvar(fig, caminho)


def recomendacao(base: pd.DataFrame, caminho: Path) -> None:
    df = base[base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)].copy()
    x = np.arange(2)
    largura = 0.34
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for j, (_, row) in enumerate(df.sort_values("ROTULO_OFERTA").iterrows()):
        vals = [row.get("qe_i68_media"), row.get("qe_i69_media")]
        ax.bar(
            x + (j - 0.5) * largura,
            vals,
            largura,
            label=row["ROTULO_OFERTA"],
        )
    ax.set_xticks(x, ["Recomendaria o curso", "Recomendaria a IES"])
    ax.set_ylim(0, 10)
    ax.set_ylabel("Média (0–10)")
    ax.set_title("Recomendação — rótulos oficiais QE_I68 e QE_I69")
    ax.legend()
    _salvar(fig, caminho)


def sintese(base: pd.DataFrame, caminho: Path) -> None:
    df = base[base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)].copy()
    indicadores = [
        ("nt_ger_percentil_brasil", "NT_GER — percentil Brasil"),
        ("TAXA_PARTICIPACAO_OFICIAL", "Participação oficial"),
        ("renda_ate_3sm_pct", "Renda até 3 SM"),
        ("auxilio_permanencia_pct", "Auxílio permanência"),
    ]
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(indicadores))
    for _, row in df.sort_values("ROTULO_OFERTA").iterrows():
        vals = []
        for col, _ in indicadores:
            val = pd.to_numeric(pd.Series([row.get(col)]), errors="coerce").iloc[0]
            if col != "nt_ger_percentil_brasil":
                val *= 100
            vals.append(val)
        ax.plot(vals, y, marker="o", label=row["ROTULO_OFERTA"])
    ax.set_yticks(y, [rot for _, rot in indicadores])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percentual / percentil")
    ax.set_title("Síntese descritiva das duas ofertas UFPA")
    ax.legend()
    _salvar(fig, caminho)


def gerar_todas(
    base: pd.DataFrame,
    individual: pd.DataFrame,
    benchmark: pd.DataFrame,
    pasta: Path,
) -> list[Path]:
    arquivos = [
        pasta / "01_painel_ofertas_ufpa.png",
        pasta / "02_posicao_relativa_nt_ger.png",
        pasta / "03a_distribuicao_nt_ger.png",
        pasta / "03b_distribuicao_nt_obj.png",
        pasta / "03c_distribuicao_nt_dis.png",
        pasta / "04_perfil_socioeconomico.png",
        pasta / "05_processo_formativo_dimensoes.png",
        pasta / "06_benchmark_sensibilidade.png",
        pasta / "07_recomendacao.png",
        pasta / "08_sintese_ufpa.png",
    ]
    painel_ufpa(base, arquivos[0])
    posicao_relativa(base, arquivos[1])
    distribuicao_nota(
        individual,
        "NT_GER",
        "Distribuição individual de NT_GER — mesmo arquivo temático",
        arquivos[2],
    )
    distribuicao_nota(
        individual,
        "NT_OBJ",
        "Distribuição individual de NT_OBJ — mesmo arquivo temático",
        arquivos[3],
    )
    distribuicao_nota(
        individual,
        "NT_DIS",
        "Distribuição individual de NT_DIS — mesmo arquivo temático",
        arquivos[4],
    )
    perfil_socioeconomico(base, arquivos[5])
    processo_formativo(base, arquivos[6])
    benchmark_sensibilidade(benchmark, arquivos[7])
    recomendacao(base, arquivos[8])
    sintese(base, arquivos[9])
    return arquivos
