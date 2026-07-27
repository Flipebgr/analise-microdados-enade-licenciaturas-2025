from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CO_IES_UFPA = 569
COR_PRINCIPAL = "#24436B"
COR_SECUNDARIA = "#2F7F7B"
COR_REFERENCIA = "#8A8A8A"


def _preparar_ax(titulo: str, subtitulo: str = "", figsize: tuple[float, float] = (11, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    fig.suptitle(titulo, x=0.06, y=0.97, ha="left", fontsize=25, fontweight="bold", color="#1F3D67")
    if subtitulo:
        fig.text(0.06, 0.90, subtitulo, ha="left", fontsize=12, style="italic", color="#555555")
    for lado in ["top", "right", "bottom"]:
        ax.spines[lado].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.grid(False)
    return fig, ax


def _salvar(fig, path: Path, rodape: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.text(0.06, 0.035, rodape, ha="left", fontsize=9.5, style="italic", color="#888888")
    fig.tight_layout(rect=(0.04, 0.08, 0.98, 0.86))
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def _barras_ofertas(df: pd.DataFrame, valor: str, titulo: str, subtitulo: str, path: Path, rodape: str, formato: str = ".1f") -> None:
    dados = df[["ROTULO_OFERTA", valor]].dropna().sort_values(valor)
    fig, ax = _preparar_ax(titulo, subtitulo, figsize=(11, 6.2))
    barras = ax.barh(dados["ROTULO_OFERTA"], dados[valor], color=COR_PRINCIPAL, height=0.42)
    maior = float(dados[valor].max()) if not dados.empty else 1
    ax.set_xlim(0, maior * 1.22 if maior > 0 else 1)
    ax.tick_params(axis="y", labelsize=11)
    for barra, valor_num in zip(barras, dados[valor], strict=False):
        ax.text(barra.get_width() + maior * 0.015, barra.get_y() + barra.get_height()/2, format(valor_num, formato), va="center", fontsize=11)
    _salvar(fig, path, rodape)


def ofertas_ufpa(base: pd.DataFrame, path: Path) -> None:
    dados = base[base["CO_IES"].eq(CO_IES_UFPA)].copy().sort_values("CONCEITO_ENADE_NUM")
    fig, ax = _preparar_ax("Ofertas de Física da UFPA", "Conceito Enade, modalidade e participantes oficiais", figsize=(11, 6))
    barras = ax.barh(dados["ROTULO_OFERTA"], dados["PARTICIPANTES_NUM"], color=COR_SECUNDARIA, height=0.44)
    maior = max(float(dados["PARTICIPANTES_NUM"].max()), 1)
    ax.set_xlim(0, maior * 1.35)
    for barra, (_, row) in zip(barras, dados.iterrows(), strict=False):
        ax.text(barra.get_width() + maior * .02, barra.get_y()+barra.get_height()/2,
                f"N={int(row['PARTICIPANTES_NUM'])} | Conceito {int(row['CONCEITO_ENADE_NUM'])}", va="center", fontsize=10)
    _salvar(fig, path, "Fonte: Conceito Enade 2025 e Microdados Enade das Licenciaturas 2025 — INEP.")


def taxa_presenca(auditoria: pd.DataFrame, path: Path) -> None:
    _barras_ofertas(
        auditoria, "taxa_presenca_pct", "Taxa de Presença na Prova",
        "Percentual de registros com TP_PRES = 555 por oferta de Física da UFPA",
        path, "TP_PRES = 555 (presente com resultado válido). Fonte: Microdados Enade das Licenciaturas 2025 — INEP.", ".1f"
    )


def nota_por_oferta(base: pd.DataFrame, variavel: str, titulo: str, path: Path) -> None:
    dados = base[base["CO_IES"].eq(CO_IES_UFPA)].copy()
    _barras_ofertas(
        dados, f"{variavel}_mean", titulo,
        "Média dos participantes com resultado válido | Escala de 0 a 100",
        path, f"{variavel.upper()} em escala de 0 a 100; N válido registrado por oferta. Fonte: Microdados Enade das Licenciaturas 2025 — INEP.", ".1f"
    )


def nt_ger_comparativo(base: pd.DataFrame, referencias: pd.DataFrame, path: Path) -> None:
    dados = base[base["CO_IES"].eq(CO_IES_UFPA)][["ROTULO_OFERTA", "nt_ger_mean"]].dropna().sort_values("nt_ger_mean")
    fig, ax = _preparar_ax("Nota Geral Comparativa", "Ofertas da UFPA com referências agregadas da Região Norte e do Brasil", figsize=(12, 6.5))
    barras = ax.barh(dados["ROTULO_OFERTA"], dados["nt_ger_mean"], color=COR_SECUNDARIA, height=0.42)
    refs = referencias.set_index("REFERENCIA")["MEDIA_DAS_MEDIAS"]
    estilos = {"UFPA agregada": "--", "Região Norte": "-.", "Brasil": ":"}
    cores = {"UFPA agregada": "#7A3E00", "Região Norte": "#884C7D", "Brasil": "#444444"}
    for nome in ["UFPA agregada", "Região Norte", "Brasil"]:
        if nome in refs and pd.notna(refs[nome]):
            ax.axvline(refs[nome], linestyle=estilos[nome], color=cores[nome], linewidth=2, label=f"{nome}: {refs[nome]:.1f}")
    maior = max(float(dados["nt_ger_mean"].max()), float(refs.dropna().max()))
    ax.set_xlim(0, maior * 1.18)
    for barra, valor in zip(barras, dados["nt_ger_mean"], strict=False):
        ax.text(barra.get_width()+maior*.01, barra.get_y()+barra.get_height()/2, f"{valor:.1f}", va="center", fontsize=10)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _salvar(fig, path, "Referências calculadas no nível do curso; não representam comparação individual. Fonte: Microdados Enade 2025 — INEP.")


def conceito_dificuldade(base: pd.DataFrame, path: Path) -> None:
    dados = base[base["CO_IES"].eq(CO_IES_UFPA)][
        ["ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "co_rs_i2_dificuldade_alta_pct"]
    ].dropna().sort_values("co_rs_i2_dificuldade_alta_pct")
    fig, ax = _preparar_ax("Conceito Enade × Percepção de Dificuldade", "Percentual que classificou o componente específico como difícil ou muito difícil", figsize=(11, 6.2))
    barras = ax.barh(dados["ROTULO_OFERTA"], dados["co_rs_i2_dificuldade_alta_pct"], color=COR_PRINCIPAL, height=.42)
    maior = max(float(dados["co_rs_i2_dificuldade_alta_pct"].max()), 1)
    ax.set_xlim(0, min(110, maior*1.28))
    for barra, (_, row) in zip(barras, dados.iterrows(), strict=False):
        ax.text(barra.get_width()+1.2, barra.get_y()+barra.get_height()/2,
                f"{row['co_rs_i2_dificuldade_alta_pct']:.1f}% | C{int(row['CONCEITO_ENADE_NUM'])}", va="center", fontsize=10)
    _salvar(fig, path, "CO_RS_I2 agregado por CO_CURSO. Associação ecológica; não vincula percepção e nota do mesmo estudante.")


def processo_formativo(itens: pd.DataFrame, cursos: pd.DataFrame, path: Path) -> None:
    ufpa_ids = set(cursos.loc[cursos["CO_IES"].eq(CO_IES_UFPA), "CO_CURSO"])
    selecionados = ["QE_I20", "QE_I27", "QE_I33", "QE_I40", "QE_I45", "QE_I52", "QE_I60", "QE_I66"]
    dados = itens[itens["CO_CURSO"].isin(ufpa_ids) & itens["ITEM"].isin(selecionados)].copy()
    rotulos = cursos.set_index("CO_CURSO")["ROTULO_OFERTA"]
    dados["OFERTA"] = dados["CO_CURSO"].map(rotulos)
    matriz = dados.pivot(index="OFERTA", columns="ITEM", values="concordancia_pct") * 100
    matriz = matriz.reindex(columns=selecionados).apply(pd.to_numeric, errors="coerce")
    fig, ax = _preparar_ax("Percepção do Processo Formativo", "Percentual de concordância em itens selecionados (respostas 4 a 6)", figsize=(12, 6.8))
    imagem = ax.imshow(matriz.astype(float).to_numpy(), aspect="auto", cmap="Blues", vmin=0, vmax=100)
    ax.set_xticks(range(len(matriz.columns)), matriz.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(matriz.index)), matriz.index, fontsize=10)
    ax.tick_params(axis="x", bottom=True, labelbottom=True)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            valor = matriz.iloc[i, j]
            if pd.notna(valor):
                ax.text(j, i, f"{valor:.0f}", ha="center", va="center", fontsize=8, color="black" if valor < 65 else "white")
    fig.colorbar(imagem, ax=ax, shrink=.72, label="Concordância (%)")
    _salvar(fig, path, "Itens QE_I20–QE_I66 analisados separadamente; seleção exploratória sem índice único. Fonte: Questionário do Estudante 2025.")


def recomendacao(base: pd.DataFrame, coluna: str, titulo: str, path: Path) -> None:
    dados = base[base["CO_IES"].eq(CO_IES_UFPA)].copy()
    _barras_ofertas(
        dados, coluna, titulo,
        "Percentual de avaliações 9 ou 10 entre respostas válidas",
        path, "Escala de 0 a 10; percentual de notas 9–10. Fonte: Questionário do Estudante — Enade 2025.", ".1%"
    )


def perfil_socioeconomico(base: pd.DataFrame, path: Path) -> None:
    ufpa = base[base["CO_IES"].eq(CO_IES_UFPA)].copy()
    indicadores = [
        ("primeira_geracao_pct", "Primeira geração"),
        ("mae_superior_pct", "Mãe com superior"),
        ("pai_superior_pct", "Pai com superior"),
        ("renda_ate_3sm_pct", "Renda até 3 SM"),
        ("trabalha_pct", "Trabalha"),
        ("trabalha_40h_pct", "Trabalha 40h"),
        ("acao_afirmativa_pct", "Ação afirmativa"),
        ("auxilio_permanencia_pct", "Auxílio permanência"),
        ("bolsa_academica_pct", "Bolsa acadêmica"),
        ("estudo_4h_ou_mais_pct", "Estuda 4h+"),
        ("pretende_magisterio_pct", "Pretende magistério"),
    ]
    disponiveis = [(col, nome) for col, nome in indicadores if col in ufpa.columns]
    cols = [col for col, _ in disponiveis]
    nomes = [nome for _, nome in disponiveis]
    matriz = ufpa.set_index("ROTULO_OFERTA")[cols].apply(pd.to_numeric, errors="coerce") * 100
    matriz.columns = nomes
    matriz = matriz.sort_index()

    fig, ax = _preparar_ax(
        "Perfil Socioeconômico Geral das Ofertas",
        "Percentuais válidos por oferta de Física da UFPA",
        figsize=(13.5, 7.2),
    )
    imagem = ax.imshow(matriz.to_numpy(dtype=float), aspect="auto", cmap="Blues", vmin=0, vmax=100)
    ax.set_xticks(range(len(matriz.columns)), matriz.columns, rotation=40, ha="right", fontsize=9)
    ax.set_yticks(range(len(matriz.index)), matriz.index, fontsize=10)
    ax.tick_params(axis="x", bottom=True, labelbottom=True)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            valor = matriz.iloc[i, j]
            if pd.notna(valor):
                ax.text(
                    j,
                    i,
                    f"{valor:.0f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white" if valor >= 60 else "black",
                )
    fig.colorbar(imagem, ax=ax, shrink=0.72, label="Percentual válido (%)")
    _salvar(
        fig,
        path,
        "Indicadores agregados por CO_CURSO, com denominadores válidos específicos. "
        "A leitura conjunta com NT_GER é ecológica e não permite inferência individual. "
        "Fonte: Questionário do Estudante — Enade 2025.",
    )


def sintese_socioeconomica_desempenho(base: pd.DataFrame, path: Path) -> None:
    colunas = [
        "ROTULO_OFERTA",
        "nt_ger_mean",
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "primeira_geracao_pct",
        "auxilio_permanencia_pct",
    ]
    dados = base.loc[base["CO_IES"].eq(CO_IES_UFPA), colunas].copy()
    dados = dados.dropna(subset=["nt_ger_mean"]).sort_values("nt_ger_mean")

    fig, ax = _preparar_ax(
        "Desempenho e Contexto Socioeconômico",
        "NT_GER média e indicadores agregados por oferta de Física da UFPA",
        figsize=(13, 7),
    )
    y = np.arange(len(dados))
    ax.barh(y, dados["nt_ger_mean"], color=COR_SECUNDARIA, height=0.42, label="NT_GER média")
    ax.set_yticks(y, dados["ROTULO_OFERTA"], fontsize=10)
    ax.tick_params(axis="x", bottom=True, labelbottom=True)
    ax.set_xlabel("NT_GER média (0–100)")
    ax.set_xlim(0, max(100, float(dados["nt_ger_mean"].max()) * 1.25))

    ax2 = ax.twiny()
    ax2.spines["top"].set_visible(True)
    ax2.spines["top"].set_color("#888888")
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("Indicadores socioeconômicos (%)")
    marcadores = [
        ("renda_ate_3sm_pct", "Renda até 3 SM", "o"),
        ("trabalha_pct", "Trabalha", "s"),
        ("primeira_geracao_pct", "Primeira geração", "^"),
        ("auxilio_permanencia_pct", "Auxílio permanência", "D"),
    ]
    for col, nome, marcador in marcadores:
        ax2.scatter(dados[col] * 100, y, marker=marcador, s=48, label=nome)
    ax2.legend(frameon=False, ncol=2, loc="lower right", fontsize=8)
    _salvar(
        fig,
        path,
        "A figura combina indicadores agregados por curso apenas para leitura contextual. "
        "Não atribui o desempenho individual ao perfil socioeconômico. Fonte: Microdados Enade 2025 — INEP.",
    )


def benchmark_comparavel(base: pd.DataFrame, resumo: pd.DataFrame, path: Path) -> None:
    dados = resumo.copy()
    if dados.empty:
        fig, ax = _preparar_ax("Benchmark Comparável", "Nenhum curso comparável localizado", figsize=(10, 5))
        ax.text(.5, .5, "Sem comparáveis sob o critério atual", ha="center", va="center", transform=ax.transAxes)
        _salvar(fig, path, "Critério: mesma modalidade, categoria, organização acadêmica e faixa de participantes.")
        return
    fig, ax = _preparar_ax("Benchmark Comparável", "Número de cursos comparáveis para cada oferta da UFPA com Conceito Enade 1", figsize=(11, 6))
    dados = dados.sort_values("n_cursos_comparaveis")
    barras = ax.barh(dados["ROTULO_ALVO"], dados["n_cursos_comparaveis"], color=COR_SECUNDARIA, height=.42)
    maior = max(float(dados["n_cursos_comparaveis"].max()), 1)
    ax.set_xlim(0, maior*1.22)
    for barra, valor in zip(barras, dados["n_cursos_comparaveis"], strict=False):
        ax.text(barra.get_width()+maior*.02, barra.get_y()+barra.get_height()/2, f"{int(valor)}", va="center")
    _salvar(fig, path, "Mesma modalidade, categoria administrativa e organização acadêmica; participantes entre 0,5× e 2× o alvo.")
