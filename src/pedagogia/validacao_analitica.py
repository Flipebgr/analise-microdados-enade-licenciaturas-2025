from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.analise.validar_indicadores import auditar_desempenho, auditar_indicadores
from src.pedagogia import CO_CURSO_CASTANHAL, PEDAGOGIA

RECORTES_REGIONAIS_OBRIGATORIOS = {
    "UFPA agregada",
    "Região Norte sem UFPA",
    "Região Norte completa",
    "Nordeste",
    "Sudeste",
    "Sul",
    "Centro-Oeste",
    "Brasil geral",
    "Brasil sem UFPA",
    "Restante do Brasil sem Norte",
}

INDICADORES_ECOLOGICOS = (
    "renda_ate_3sm_pct",
    "trabalha_pct",
    "acao_afirmativa_pct",
    "auxilio_permanencia_pct",
    "bolsa_academica_pct",
    "estudo_4h_ou_mais_pct",
    "turno_noturno_pct",
    "anos_desde_ingresso_media",
    "qe_i68_media",
    "qe_i69_media",
)


def auditar_participacao_desempenho(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Aplica as auditorias compartilhadas à base de Pedagogia."""
    return auditar_desempenho(base), auditar_indicadores(base)


def validar_comparacoes_regionais(comparacoes: pd.DataFrame) -> pd.DataFrame:
    """Valida recortes territoriais e acrescenta diagnósticos de dispersão."""
    faltantes = RECORTES_REGIONAIS_OBRIGATORIOS - set(
        comparacoes["RECORTE"].dropna().astype(str)
    )
    if faltantes:
        raise ValueError(f"Recortes regionais ausentes: {sorted(faltantes)}")

    trabalho = comparacoes.copy()
    numericas = (
        "N_CURSOS",
        "N_PARTICIPANTES",
        "MEDIA_CURSOS",
        "MEDIA_PONDERADA_PARTICIPANTES",
        "MEDIANA_CURSOS",
        "DP_CURSOS",
        "P25",
        "P75",
    )
    for coluna in numericas:
        trabalho[coluna] = pd.to_numeric(trabalho[coluna], errors="coerce")
    if (trabalho["N_CURSOS"].dropna() < 0).any():
        raise ValueError("Há N_CURSOS negativo nas comparações regionais.")
    if (trabalho["N_PARTICIPANTES"].dropna() < 0).any():
        raise ValueError("Há N_PARTICIPANTES negativo nas comparações regionais.")

    trabalho["AMPLITUDE_IQR"] = trabalho["P75"] - trabalho["P25"]
    trabalho["DIF_MEDIA_PONDERADA"] = (
        trabalho["MEDIA_PONDERADA_PARTICIPANTES"] - trabalho["MEDIA_CURSOS"]
    )
    trabalho["ALERTA_IQR_NEGATIVO"] = trabalho["AMPLITUDE_IQR"].lt(0)
    return trabalho


def _selecionar_cenario(
    candidatos: pd.DataFrame,
    alvo: pd.Series,
    *,
    categoria: bool,
    orgacad: bool,
    faixa_porte: tuple[float, float] | None,
) -> pd.DataFrame:
    mask = candidatos["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
    if categoria:
        mask &= candidatos["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
    if orgacad:
        mask &= candidatos["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])

    n_alvo = pd.to_numeric(
        pd.Series([alvo.get("PARTICIPANTES_NUM")]), errors="coerce"
    ).iloc[0]
    if faixa_porte is not None and pd.notna(n_alvo) and n_alvo > 0:
        inferior = max(1, n_alvo * faixa_porte[0])
        superior = n_alvo * faixa_porte[1]
        participantes = pd.to_numeric(candidatos["PARTICIPANTES_NUM"], errors="coerce")
        mask &= participantes.between(inferior, superior)
    return candidatos.loc[mask].copy()


def sensibilidade_benchmarks_pedagogia(
    base: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Testa cinco definições de benchmark para cada oferta da UFPA."""
    alvos = base.loc[base["CO_IES"].eq(PEDAGOGIA.co_ies_focal)].copy()
    candidatos = base.loc[~base["CO_IES"].eq(PEDAGOGIA.co_ies_focal)].copy()
    cenarios = (
        ("modalidade", False, False, None),
        ("modalidade_categoria", True, False, None),
        ("modalidade_categoria_orgacad", True, True, None),
        ("estrutura_porte_0_5_2_0", True, True, (0.5, 2.0)),
        ("estrutura_porte_0_75_1_5", True, True, (0.75, 1.5)),
    )
    indicadores = (
        "nt_ger_mean",
        "nt_obj_mean",
        "nt_dis_mean",
        "taxa_presenca_microdados",
    )
    resumos: list[dict[str, object]] = []
    membros: list[pd.DataFrame] = []

    for _, alvo in alvos.iterrows():
        for nome, categoria, orgacad, faixa in cenarios:
            selecionados = _selecionar_cenario(
                candidatos,
                alvo,
                categoria=categoria,
                orgacad=orgacad,
                faixa_porte=faixa,
            )
            if not selecionados.empty:
                parte = selecionados.copy()
                parte.insert(0, "CENARIO", nome)
                parte.insert(0, "ROTULO_ALVO", alvo["ROTULO_OFERTA"])
                parte.insert(0, "CO_CURSO_ALVO", int(alvo["CO_CURSO"]))
                membros.append(parte)

            linha: dict[str, object] = {
                "CO_CURSO_ALVO": int(alvo["CO_CURSO"]),
                "ROTULO_ALVO": alvo["ROTULO_OFERTA"],
                "CONCEITO_ALVO": alvo["CONCEITO_ENADE_NUM"],
                "CENARIO": nome,
                "N_CURSOS": len(selecionados),
            }
            for indicador in indicadores:
                valor_alvo = pd.to_numeric(
                    pd.Series([alvo.get(indicador)]), errors="coerce"
                ).iloc[0]
                serie = pd.to_numeric(
                    selecionados.get(indicador), errors="coerce"
                ).dropna()
                media = serie.mean()
                dp = serie.std(ddof=1)
                linha[f"{indicador}_ALVO"] = valor_alvo
                linha[f"{indicador}_MEDIA_BENCHMARK"] = media
                linha[f"{indicador}_MEDIANA_BENCHMARK"] = serie.median()
                linha[f"{indicador}_DP_BENCHMARK"] = dp
                linha[f"{indicador}_DIFERENCA"] = (
                    valor_alvo - media
                    if pd.notna(valor_alvo) and pd.notna(media)
                    else np.nan
                )
                linha[f"{indicador}_Z"] = (
                    (valor_alvo - media) / dp
                    if pd.notna(valor_alvo) and np.isfinite(dp) and dp > 0
                    else np.nan
                )
            resumos.append(linha)

    membros_df = pd.concat(membros, ignore_index=True) if membros else pd.DataFrame()
    return pd.DataFrame(resumos), membros_df


def diagnosticar_outliers(
    base: pd.DataFrame,
    indicadores: Iterable[str] = ("nt_ger_mean", "nt_obj_mean", "nt_dis_mean"),
) -> pd.DataFrame:
    """Marca outliers de curso pelo critério 1,5 IQR no universo nacional."""
    linhas: list[dict[str, object]] = []
    for indicador in indicadores:
        valores = pd.to_numeric(base[indicador], errors="coerce")
        validos = valores.dropna()
        q1 = validos.quantile(0.25)
        q3 = validos.quantile(0.75)
        iqr = q3 - q1
        inferior = q1 - 1.5 * iqr
        superior = q3 + 1.5 * iqr
        for idx, valor in valores.items():
            if pd.isna(valor):
                continue
            linhas.append(
                {
                    "CO_CURSO": base.loc[idx, "CO_CURSO"],
                    "ROTULO_OFERTA": base.loc[idx, "ROTULO_OFERTA"],
                    "RECORTE_PEDAGOGIA": base.loc[idx, "RECORTE_PEDAGOGIA"],
                    "INDICADOR": indicador,
                    "VALOR": float(valor),
                    "Q1": float(q1),
                    "Q3": float(q3),
                    "LIMITE_INFERIOR": float(inferior),
                    "LIMITE_SUPERIOR": float(superior),
                    "OUTLIER_IQR": bool(valor < inferior or valor > superior),
                }
            )
    return pd.DataFrame(linhas)


def associacoes_ecologicas(base: pd.DataFrame) -> pd.DataFrame:
    """Calcula Spearman entre indicadores agregados por curso e NT_GER médio."""
    y = pd.to_numeric(base["nt_ger_mean"], errors="coerce")
    linhas: list[dict[str, object]] = []
    for indicador in INDICADORES_ECOLOGICOS:
        if indicador not in base.columns:
            continue
        x = pd.to_numeric(base[indicador], errors="coerce")
        mask = x.notna() & y.notna()
        n = int(mask.sum())
        rho = np.nan
        pvalor = np.nan
        if n >= 3 and x[mask].nunique() > 1 and y[mask].nunique() > 1:
            resultado = spearmanr(x[mask], y[mask], nan_policy="omit")
            rho = float(resultado.statistic)
            pvalor = float(resultado.pvalue)
        linhas.append(
            {
                "INDICADOR_X": indicador,
                "INDICADOR_Y": "nt_ger_mean",
                "N_CURSOS": n,
                "SPEARMAN_RHO": rho,
                "P_VALOR_EXPLORATORIO": pvalor,
                "NIVEL_ANALISE": "curso (ecológico)",
                "RESSALVA": "não interpretar como associação individual ou causal",
            }
        )
    return pd.DataFrame(linhas)


def perfil_validado(base: pd.DataFrame) -> pd.DataFrame:
    """Resume composição e trajetória nos cinco recortes exclusivos de Pedagogia."""
    indicadores = (
        "sexo_feminino_pct",
        "idade_media",
        "mae_superior_pct",
        "pai_superior_pct",
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "trabalha_40h_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
        "bolsa_academica_pct",
        "estudo_4h_ou_mais_pct",
        "pretende_magisterio_pct",
        "turno_noturno_pct",
        "anos_desde_ingresso_media",
        "qe_i68_media",
        "qe_i69_media",
        "qe_i70_interesse_pct",
    )
    recortes = (
        "UFPA — Conceito 5",
        "UFPA — Conceito 4",
        "Outras IES do Pará",
        "Norte sem Pará",
        "Brasil sem Norte",
    )
    linhas: list[dict[str, object]] = []
    for recorte in recortes:
        sub = base.loc[base["RECORTE_PEDAGOGIA"].eq(recorte)]
        for indicador in indicadores:
            if indicador not in sub.columns:
                continue
            serie = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append(
                {
                    "RECORTE_PEDAGOGIA": recorte,
                    "INDICADOR": indicador,
                    "N_CURSOS": int(serie.size),
                    "MEDIA_CURSOS": serie.mean(),
                    "MEDIANA_CURSOS": serie.median(),
                    "DP_CURSOS": serie.std(ddof=1),
                    "P25": serie.quantile(0.25),
                    "P75": serie.quantile(0.75),
                }
            )
    return pd.DataFrame(linhas)


def comparar_itens_processo_castanhal(
    itens: pd.DataFrame,
    base: pd.DataFrame,
    membros_benchmark: pd.DataFrame,
) -> pd.DataFrame:
    """Compara Castanhal com UFPA Conceito 4 e benchmark estrutural principal."""
    cadastro = base[["CO_CURSO", "RECORTE_PEDAGOGIA"]].copy()
    trabalho = itens.merge(cadastro, on="CO_CURSO", how="left", validate="many_to_one")

    membros_principais = membros_benchmark.loc[
        membros_benchmark["CO_CURSO_ALVO"].eq(CO_CURSO_CASTANHAL)
        & membros_benchmark["CENARIO"].eq("estrutura_porte_0_5_2_0")
    ]
    ids_benchmark = set(
        pd.to_numeric(membros_principais["CO_CURSO"], errors="coerce")
        .dropna()
        .astype(int)
    )

    linhas: list[dict[str, object]] = []
    for item, sub_item in trabalho.groupby("ITEM", observed=True):
        alvo = sub_item.loc[
            pd.to_numeric(sub_item["CO_CURSO"], errors="coerce").eq(
                CO_CURSO_CASTANHAL
            )
        ]
        if alvo.empty:
            continue
        valor_alvo = pd.to_numeric(alvo["media"], errors="coerce").iloc[0]
        n_alvo = pd.to_numeric(alvo["n_valido"], errors="coerce").iloc[0]
        referencias = {
            "UFPA — Conceito 4": sub_item.loc[
                sub_item["RECORTE_PEDAGOGIA"].eq("UFPA — Conceito 4")
            ],
            "Benchmark comparável de Castanhal": sub_item.loc[
                pd.to_numeric(sub_item["CO_CURSO"], errors="coerce").isin(ids_benchmark)
            ],
            "Outras IES do Pará": sub_item.loc[
                sub_item["RECORTE_PEDAGOGIA"].eq("Outras IES do Pará")
            ],
            "Norte sem Pará": sub_item.loc[
                sub_item["RECORTE_PEDAGOGIA"].eq("Norte sem Pará")
            ],
        }
        for referencia, sub in referencias.items():
            valores = pd.to_numeric(sub["media"], errors="coerce").dropna()
            media = valores.mean()
            linhas.append(
                {
                    "ITEM": item,
                    "REFERENCIA": referencia,
                    "MEDIA_CASTANHAL": valor_alvo,
                    "N_VALIDO_CASTANHAL": n_alvo,
                    "N_CURSOS_REFERENCIA": int(valores.size),
                    "MEDIA_REFERENCIA": media,
                    "DP_REFERENCIA": valores.std(ddof=1),
                    "DIFERENCA_CASTANHAL_REFERENCIA": (
                        valor_alvo - media
                        if pd.notna(valor_alvo) and pd.notna(media)
                        else np.nan
                    ),
                    "STATUS_INTERPRETACAO": (
                        "interpretar substantivamente somente com o texto oficial do item"
                    ),
                }
            )
    return pd.DataFrame(linhas)


def resumo_contraste_interno(base: pd.DataFrame) -> pd.DataFrame:
    """Contrasta Castanhal com a média das seis ofertas Conceito 4 da UFPA."""
    castanhal = base.loc[
        pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_CASTANHAL)
    ]
    if len(castanhal) != 1:
        raise ValueError("Castanhal não foi localizada de forma única.")
    alvo = castanhal.iloc[0]
    c4 = base.loc[base["RECORTE_PEDAGOGIA"].eq("UFPA — Conceito 4")]
    indicadores = (
        "nt_ger_mean",
        "nt_obj_mean",
        "nt_dis_mean",
        "taxa_presenca_microdados",
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
        "bolsa_academica_pct",
        "estudo_4h_ou_mais_pct",
        "qe_i68_media",
        "qe_i69_media",
    )
    linhas: list[dict[str, object]] = []
    for indicador in indicadores:
        if indicador not in base.columns:
            continue
        valor = pd.to_numeric(pd.Series([alvo.get(indicador)]), errors="coerce").iloc[0]
        ref = pd.to_numeric(c4[indicador], errors="coerce").dropna()
        media = ref.mean()
        dp = ref.std(ddof=1)
        linhas.append(
            {
                "INDICADOR": indicador,
                "CASTANHAL": valor,
                "N_UFPA_CONCEITO_4": int(ref.size),
                "MEDIA_UFPA_CONCEITO_4": media,
                "MEDIANA_UFPA_CONCEITO_4": ref.median(),
                "DP_UFPA_CONCEITO_4": dp,
                "DIFERENCA": valor - media if pd.notna(valor) and pd.notna(media) else np.nan,
                "Z_DESCRITIVO": (
                    (valor - media) / dp
                    if pd.notna(valor) and np.isfinite(dp) and dp > 0
                    else np.nan
                ),
                "INTERPRETACAO": "contraste descritivo entre cursos; não causal",
            }
        )
    return pd.DataFrame(linhas)
