from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.musica import MUSICA
from src.musica.rotulos_questionario import ROTULOS_DIMENSOES

UFPA_CURSO = 114950


def _salvar(fig: plt.Figure, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(caminho, dpi=180, bbox_inches="tight")
    plt.close(fig)


def painel_ufpa(base: pd.DataFrame, caminho: Path) -> None:
    df = base[base["CO_IES"].eq(MUSICA.co_ies_focal)].copy()
    row = df.iloc[0]
    taxa = float(
        pd.to_numeric(
            pd.Series([row["TAXA_PARTICIPACAO_OFICIAL"]]),
            errors="coerce",
        ).iloc[0]
        * 100
    )
    prof = float(
        pd.to_numeric(
            pd.Series([row["PCT_PADRAO_PROFICIENCIA_NUM"]]),
            errors="coerce",
        ).iloc[0]
    )

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.barh(
        ["Participação oficial", "Padrão de proficiência"],
        [taxa, prof],
    )
    ax.set_xlim(0, 100)
    ax.set_xlabel("%")
    ax.set_title("Música — oferta UFPA no Enade 2025")
    ax.text(
        taxa + 1,
        0,
        f"{taxa:.1f}% | N={int(row['PARTICIPANTES_NUM'])}",
        va="center",
    )
    ax.text(
        prof + 1,
        1,
        f"{prof:.1f}% | Conceito {int(row['CONCEITO_ENADE_NUM'])}",
        va="center",
    )
    _salvar(fig, caminho)


def posicao_relativa(base: pd.DataFrame, caminho: Path) -> None:
    ufpa = base[base["CO_IES"].eq(MUSICA.co_ies_focal)].iloc[0]
    nacional = pd.to_numeric(base["nt_ger_mean"], errors="coerce").dropna()

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.boxplot(
        nacional,
        vert=False,
        widths=0.35,
        showfliers=False,
        tick_labels=["Brasil — cursos"],
    )
    valor = float(ufpa["nt_ger_mean"])
    ax.scatter(valor, 1, s=75, zorder=3)
    ax.annotate(
        f"UFPA — Belém\n{valor:.1f}",
        (valor, 1),
        xytext=(0, 22),
        textcoords="offset points",
        ha="center",
    )
    ax.set_xlabel("Média do curso em NT_GER")
    ax.set_title(
        "Posição da Música/UFPA na distribuição nacional de Música"
    )
    _salvar(fig, caminho)


def distribuicao_nota(
    individual: pd.DataFrame,
    base: pd.DataFrame,
    variavel: str,
    titulo: str,
    caminho: Path,
) -> None:
    grupos = [
        ("UFPA — Belém", base["CO_IES"].eq(MUSICA.co_ies_focal)),
        ("Norte sem Pará", base["RECORTE_MUSICA"].eq("Norte sem Pará")),
        ("Brasil sem Norte", base["RECORTE_MUSICA"].eq("Brasil sem Norte")),
    ]
    dados: list[np.ndarray] = []
    labels: list[str] = []

    for rotulo, mask in grupos:
        ids = set(
            pd.to_numeric(
                base.loc[mask, "CO_CURSO"],
                errors="coerce",
            ).dropna().astype(int)
        )
        valores = pd.to_numeric(
            individual.loc[
                pd.to_numeric(
                    individual["CO_CURSO"],
                    errors="coerce",
                ).isin(ids),
                variavel,
            ],
            errors="coerce",
        ).dropna()
        dados.append(valores.to_numpy())
        labels.append(f"{rotulo}\nN={len(valores)}")

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.boxplot(dados, tick_labels=labels, showmeans=True)
    ax.set_ylabel(variavel)
    ax.set_title(titulo)
    _salvar(fig, caminho)


def perfil_socioeconomico(base: pd.DataFrame, caminho: Path) -> None:
    indicadores = {
        "renda_ate_3sm_pct": "Renda até 3 SM",
        "trabalha_pct": "Trabalha",
        "acao_afirmativa_pct": "Ação afirmativa",
        "auxilio_permanencia_pct": "Auxílio permanência",
        "bolsa_academica_pct": "Bolsa acadêmica",
        "estudo_4h_ou_mais_pct": "Estuda ≥4h/semana",
    }
    grupos = [
        "UFPA — Belém",
        "Norte sem Pará",
        "Brasil sem Norte",
    ]
    x = np.arange(len(indicadores))
    largura = 0.24
    fig, ax = plt.subplots(figsize=(12, 5.5))

    for j, grupo in enumerate(grupos):
        if grupo == "UFPA — Belém":
            sub = base[base["CO_IES"].eq(MUSICA.co_ies_focal)]
        else:
            sub = base[base["RECORTE_MUSICA"].eq(grupo)]

        vals = [
            100
            * pd.to_numeric(
                sub[col],
                errors="coerce",
            ).median()
            for col in indicadores
        ]
        ax.bar(
            x + (j - 1) * largura,
            vals,
            largura,
            label=grupo,
        )

    ax.set_xticks(x, list(indicadores.values()), rotation=25, ha="right")
    ax.set_ylabel("% entre respostas válidas — mediana dos cursos")
    ax.set_title("Perfil socioeconômico — UFPA e benchmarks territoriais")
    ax.legend()
    _salvar(fig, caminho)


def processo_formativo(base: pd.DataFrame, caminho: Path) -> None:
    dimensoes = list(ROTULOS_DIMENSOES)
    grupos = [
        "UFPA — Belém",
        "Norte sem Pará",
        "Brasil sem Norte",
    ]
    matriz: list[list[float]] = []

    for grupo in grupos:
        if grupo == "UFPA — Belém":
            sub = base[base["CO_IES"].eq(MUSICA.co_ies_focal)]
        else:
            sub = base[base["RECORTE_MUSICA"].eq(grupo)]

        matriz.append(
            [
                pd.to_numeric(
                    sub[f"dim_{dim}_media"],
                    errors="coerce",
                ).median()
                for dim in dimensoes
            ]
        )

    arr = np.array(matriz, dtype=float)
    fig, ax = plt.subplots(figsize=(12, 5.4))
    im = ax.imshow(arr, aspect="auto", vmin=1, vmax=6)
    ax.set_yticks(np.arange(len(grupos)), grupos)
    ax.set_xticks(
        np.arange(len(dimensoes)),
        [ROTULOS_DIMENSOES[d] for d in dimensoes],
        rotation=35,
        ha="right",
    )
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if np.isfinite(arr[i, j]):
                ax.text(
                    j,
                    i,
                    f"{arr[i, j]:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                )
    ax.set_title(
        "Processo formativo — médias/medianas das dimensões exploratórias (1–6)"
    )
    fig.colorbar(im, ax=ax, label="Média / mediana")
    _salvar(fig, caminho)


def benchmark_sensibilidade(
    resumo: pd.DataFrame,
    caminho: Path,
) -> None:
    df = resumo[resumo["INDICADOR"].eq("nt_ger_mean")].copy()
    criterios = ["porte_25pct", "porte_50pct", "porte_2x"]
    df = df.set_index("CRITERIO").reindex(criterios).reset_index()

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(
        np.arange(len(criterios)),
        df["MEDIANA_BENCHMARK"],
        marker="o",
        label="Mediana benchmark",
    )
    alvo = pd.to_numeric(df["VALOR_ALVO"], errors="coerce").dropna()
    if not alvo.empty:
        ax.axhline(
            alvo.iloc[0],
            linestyle="--",
            linewidth=1,
            label="UFPA — Belém",
        )
    ax.set_xticks(
        np.arange(len(criterios)),
        ["±25% porte", "0,5–1,5x", "0,5–2x"],
    )
    ax.set_ylabel("NT_GER média do curso")
    ax.set_title("Sensibilidade do benchmark comparável — Música/UFPA")
    ax.legend()
    _salvar(fig, caminho)


def recomendacao(base: pd.DataFrame, caminho: Path) -> None:
    grupos = [
        "UFPA — Belém",
        "Norte sem Pará",
        "Brasil sem Norte",
    ]
    x = np.arange(2)
    largura = 0.24
    fig, ax = plt.subplots(figsize=(9, 5))

    for j, grupo in enumerate(grupos):
        if grupo == "UFPA — Belém":
            sub = base[base["CO_IES"].eq(MUSICA.co_ies_focal)]
        else:
            sub = base[base["RECORTE_MUSICA"].eq(grupo)]
        vals = [
            pd.to_numeric(sub["qe_i68_media"], errors="coerce").median(),
            pd.to_numeric(sub["qe_i69_media"], errors="coerce").median(),
        ]
        ax.bar(
            x + (j - 1) * largura,
            vals,
            largura,
            label=grupo,
        )

    ax.set_xticks(x, ["Recomendaria o curso", "Recomendaria a IES"])
    ax.set_ylim(0, 10)
    ax.set_ylabel("Média UFPA / mediana dos cursos (0–10)")
    ax.set_title("Recomendação — rótulos oficiais QE_I68 e QE_I69")
    ax.legend()
    _salvar(fig, caminho)


def associacao_ecologica(
    base: pd.DataFrame,
    associacoes: pd.DataFrame,
    caminho: Path,
) -> None:
    validas = associacoes.dropna(subset=["SPEARMAN_RHO"]).copy()
    if validas.empty:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.text(
            0.5,
            0.5,
            "Sem associação com N suficiente",
            ha="center",
            va="center",
        )
        ax.axis("off")
        _salvar(fig, caminho)
        return

    idx = validas["SPEARMAN_RHO"].abs().idxmax()
    row = validas.loc[idx]
    xcol = row["X"]
    ycol = row["Y"]

    x = pd.to_numeric(base[xcol], errors="coerce")
    y = pd.to_numeric(base[ycol], errors="coerce")
    mask = x.notna() & y.notna()

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.scatter(x[mask], y[mask], alpha=0.65)

    ufpa = base["CO_IES"].eq(MUSICA.co_ies_focal) & mask
    if ufpa.any():
        ax.scatter(
            x[ufpa],
            y[ufpa],
            s=90,
            marker="D",
            label="UFPA — Belém",
        )
        ax.legend()

    ax.set_xlabel(xcol)
    ax.set_ylabel(ycol)
    ax.set_title(
        "Associação ecológica de maior |rho| "
        f"(Spearman ρ={row['SPEARMAN_RHO']:.2f}; N={int(row['N_CURSOS'])})"
    )
    _salvar(fig, caminho)


def sintese(base: pd.DataFrame, caminho: Path) -> None:
    ufpa = base[base["CO_IES"].eq(MUSICA.co_ies_focal)].iloc[0]
    indicadores = [
        ("nt_ger_percentil_brasil", "NT_GER — percentil Brasil"),
        ("TAXA_PARTICIPACAO_OFICIAL", "Participação oficial"),
        ("PCT_PADRAO_PROFICIENCIA_NUM", "Padrão de proficiência"),
        ("renda_ate_3sm_pct", "Renda até 3 SM"),
        ("auxilio_permanencia_pct", "Auxílio permanência"),
    ]

    vals: list[float] = []
    for col, _ in indicadores:
        val = pd.to_numeric(
            pd.Series([ufpa.get(col)]),
            errors="coerce",
        ).iloc[0]
        if col == "TAXA_PARTICIPACAO_OFICIAL":
            val *= 100
        elif col in {"renda_ate_3sm_pct", "auxilio_permanencia_pct"}:
            val *= 100
        vals.append(val)

    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(indicadores))
    ax.scatter(vals, y, s=70)
    ax.set_yticks(y, [rot for _, rot in indicadores])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percentual / percentil")
    ax.set_title("Síntese descritiva — Música/UFPA")
    _salvar(fig, caminho)


def gerar_todas(
    base: pd.DataFrame,
    individual: pd.DataFrame,
    benchmark: pd.DataFrame,
    associacoes: pd.DataFrame,
    pasta: Path,
) -> list[Path]:
    arquivos = [
        pasta / "01_painel_oferta_ufpa.png",
        pasta / "02_posicao_relativa_nt_ger.png",
        pasta / "03a_distribuicao_nt_ger.png",
        pasta / "03b_distribuicao_nt_obj.png",
        pasta / "03c_distribuicao_nt_dis.png",
        pasta / "04_perfil_socioeconomico.png",
        pasta / "05_processo_formativo_dimensoes.png",
        pasta / "06_benchmark_sensibilidade.png",
        pasta / "07_recomendacao.png",
        pasta / "08_associacao_ecologica.png",
        pasta / "09_sintese_ufpa.png",
    ]
    painel_ufpa(base, arquivos[0])
    posicao_relativa(base, arquivos[1])
    distribuicao_nota(
        individual,
        base,
        "NT_GER",
        "Distribuição de NT_GER — mesmo arquivo temático",
        arquivos[2],
    )
    distribuicao_nota(
        individual,
        base,
        "NT_OBJ",
        "Distribuição de NT_OBJ — mesmo arquivo temático",
        arquivos[3],
    )
    distribuicao_nota(
        individual,
        base,
        "NT_DIS",
        "Distribuição de NT_DIS — mesmo arquivo temático",
        arquivos[4],
    )
    perfil_socioeconomico(base, arquivos[5])
    processo_formativo(base, arquivos[6])
    benchmark_sensibilidade(benchmark, arquivos[7])
    recomendacao(base, arquivos[8])
    associacao_ecologica(base, associacoes, arquivos[9])
    sintese(base, arquivos[10])
    return arquivos
