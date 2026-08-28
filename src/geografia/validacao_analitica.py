from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.analise.validar_indicadores import auditar_desempenho, auditar_indicadores
from src.geografia import GEOGRAFIA

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


def auditar_participacao_desempenho(
    base: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    return auditar_desempenho(base), auditar_indicadores(base)


def validar_comparacoes_regionais(comparacoes: pd.DataFrame) -> pd.DataFrame:
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
        participantes = pd.to_numeric(
            candidatos["PARTICIPANTES_NUM"], errors="coerce"
        )
        mask &= participantes.between(
            max(1, n_alvo * faixa_porte[0]),
            n_alvo * faixa_porte[1],
        )
    return candidatos.loc[mask].copy()


def sensibilidade_benchmarks_geografia(
    base: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    alvos = base.loc[base["CO_IES"].eq(GEOGRAFIA.co_ies_focal)].copy()
    candidatos = base.loc[~base["CO_IES"].eq(GEOGRAFIA.co_ies_focal)].copy()

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

    membros_df = (
        pd.concat(membros, ignore_index=True) if membros else pd.DataFrame()
    )
    return pd.DataFrame(resumos), membros_df


def resumo_contraste_interno(base: pd.DataFrame) -> pd.DataFrame:
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
    c3 = base.loc[base["RECORTE_GEOGRAFIA"].eq("UFPA — Conceito 3")]
    c4 = base.loc[base["RECORTE_GEOGRAFIA"].eq("UFPA — Conceito 4")]

    linhas: list[dict[str, object]] = []
    for indicador in indicadores:
        if indicador not in base.columns:
            continue
        s3 = pd.to_numeric(c3[indicador], errors="coerce").dropna()
        s4 = pd.to_numeric(c4[indicador], errors="coerce").dropna()
        m3 = s3.mean()
        m4 = s4.mean()
        dp3 = s3.std(ddof=1)
        dp4 = s4.std(ddof=1)
        dp_pooled = np.nan
        if len(s3) > 1 and len(s4) > 1:
            numerador = (len(s3) - 1) * dp3**2 + (len(s4) - 1) * dp4**2
            denominador = len(s3) + len(s4) - 2
            if denominador > 0 and numerador >= 0:
                dp_pooled = float(np.sqrt(numerador / denominador))

        linhas.append(
            {
                "INDICADOR": indicador,
                "N_CONCEITO_3": int(s3.size),
                "MEDIA_CONCEITO_3": m3,
                "MEDIANA_CONCEITO_3": s3.median(),
                "DP_CONCEITO_3": dp3,
                "N_CONCEITO_4": int(s4.size),
                "MEDIA_CONCEITO_4": m4,
                "MEDIANA_CONCEITO_4": s4.median(),
                "DP_CONCEITO_4": dp4,
                "DIFERENCA_C3_C4": (
                    m3 - m4 if pd.notna(m3) and pd.notna(m4) else np.nan
                ),
                "D_PADRONIZADO_DESCRITIVO": (
                    (m3 - m4) / dp_pooled
                    if pd.notna(m3)
                    and pd.notna(m4)
                    and np.isfinite(dp_pooled)
                    and dp_pooled > 0
                    else np.nan
                ),
                "INTERPRETACAO": (
                    "contraste descritivo entre quatro ofertas; não causal"
                ),
            }
        )
    return pd.DataFrame(linhas)


def perfil_validado(base: pd.DataFrame) -> pd.DataFrame:
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
        "UFPA — Conceito 3",
        "UFPA — Conceito 4",
        "Outras IES do Pará",
        "Norte sem Pará",
        "Brasil sem Norte",
    )
    linhas: list[dict[str, object]] = []
    for recorte in recortes:
        sub = base.loc[base["RECORTE_GEOGRAFIA"].eq(recorte)]
        for indicador in indicadores:
            if indicador not in base.columns:
                continue
            serie = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append(
                {
                    "RECORTE_GEOGRAFIA": recorte,
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


def comparar_itens_processo_grupos(
    itens: pd.DataFrame,
    base: pd.DataFrame,
) -> pd.DataFrame:
    cadastro = base[["CO_CURSO", "RECORTE_GEOGRAFIA"]].copy()
    trabalho = itens.merge(
        cadastro,
        on="CO_CURSO",
        how="left",
        validate="many_to_one",
    )

    linhas: list[dict[str, object]] = []
    for item, sub_item in trabalho.groupby("ITEM", observed=True):
        grupos = {}
        for recorte in (
            "UFPA — Conceito 3",
            "UFPA — Conceito 4",
            "Outras IES do Pará",
            "Norte sem Pará",
            "Brasil sem Norte",
        ):
            sub = sub_item.loc[sub_item["RECORTE_GEOGRAFIA"].eq(recorte)]
            grupos[recorte] = pd.to_numeric(
                sub["media"], errors="coerce"
            ).dropna()

        c3 = grupos["UFPA — Conceito 3"]
        c4 = grupos["UFPA — Conceito 4"]
        linhas.append(
            {
                "ITEM": item,
                "N_CURSOS_CONCEITO_3": int(c3.size),
                "MEDIA_CONCEITO_3": c3.mean(),
                "N_CURSOS_CONCEITO_4": int(c4.size),
                "MEDIA_CONCEITO_4": c4.mean(),
                "DIFERENCA_C3_C4": (
                    c3.mean() - c4.mean()
                    if not c3.empty and not c4.empty
                    else np.nan
                ),
                "MEDIA_OUTRAS_IES_PARA": grupos["Outras IES do Pará"].mean(),
                "N_OUTRAS_IES_PARA": int(grupos["Outras IES do Pará"].size),
                "MEDIA_NORTE_SEM_PARA": grupos["Norte sem Pará"].mean(),
                "N_NORTE_SEM_PARA": int(grupos["Norte sem Pará"].size),
                "MEDIA_BRASIL_SEM_NORTE": grupos["Brasil sem Norte"].mean(),
                "N_BRASIL_SEM_NORTE": int(grupos["Brasil sem Norte"].size),
                "STATUS_INTERPRETACAO": (
                    "interpretar substantivamente somente com o texto oficial do item"
                ),
            }
        )
    return pd.DataFrame(linhas)


def recomendacao_validada(base: pd.DataFrame) -> pd.DataFrame:
    indicadores = (
        "qe_i68_media",
        "qe_i69_media",
        "qe_i70_interesse_pct",
    )
    recortes = (
        "UFPA — Conceito 3",
        "UFPA — Conceito 4",
        "Outras IES do Pará",
        "Norte sem Pará",
        "Brasil sem Norte",
    )
    linhas: list[dict[str, object]] = []
    for recorte in recortes:
        sub = base.loc[base["RECORTE_GEOGRAFIA"].eq(recorte)]
        for indicador in indicadores:
            if indicador not in base.columns:
                continue
            serie = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append(
                {
                    "RECORTE_GEOGRAFIA": recorte,
                    "INDICADOR": indicador,
                    "N_CURSOS": int(serie.size),
                    "MEDIA_CURSOS": serie.mean(),
                    "MEDIANA_CURSOS": serie.median(),
                    "DP_CURSOS": serie.std(ddof=1),
                }
            )
    return pd.DataFrame(linhas)


def diagnosticar_outliers(
    base: pd.DataFrame,
    indicadores: Iterable[str] = ("nt_ger_mean", "nt_obj_mean", "nt_dis_mean"),
) -> pd.DataFrame:
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
                    "RECORTE_GEOGRAFIA": base.loc[idx, "RECORTE_GEOGRAFIA"],
                    "INDICADOR": indicador,
                    "VALOR": float(valor),
                    "Q1": float(q1),
                    "Q3": float(q3),
                    "LIMITE_INFERIOR": float(inferior),
                    "LIMITE_SUPERIOR": float(superior),
                    "OUTLIER_IQR": bool(
                        valor < inferior or valor > superior
                    ),
                }
            )
    return pd.DataFrame(linhas)


def associacoes_ecologicas(base: pd.DataFrame) -> pd.DataFrame:
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
                "RESSALVA": (
                    "não interpretar como associação individual ou causal"
                ),
            }
        )
    return pd.DataFrame(linhas)
