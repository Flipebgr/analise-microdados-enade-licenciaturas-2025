from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.analise.validar_indicadores import auditar_desempenho, auditar_indicadores
from src.biologia import BIOLOGIA, CO_CURSO_SOURE
from src.biologia.analise_soure import obter_soure
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

DIMENSOES_CANDIDATAS = {
    "organizacao_didatico_pedagogica": range(20, 34),
    "atuacao_docente": range(34, 42),
    "infraestrutura_recursos": range(42, 50),
    "oportunidades_formacao": range(50, 59),
    "integracao_teoria_pratica": range(59, 67),
}


def auditar_participacao_desempenho(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return auditar_desempenho(base), auditar_indicadores(base)


def validar_comparacoes_regionais(comparacoes: pd.DataFrame) -> pd.DataFrame:
    faltantes = RECORTES_REGIONAIS_OBRIGATORIOS - set(
        comparacoes["RECORTE"].dropna().astype(str)
    )
    if faltantes:
        raise ValueError(f"Recortes regionais ausentes: {sorted(faltantes)}")

    trabalho = comparacoes.copy()
    numericas = [
        "N_CURSOS",
        "N_PARTICIPANTES",
        "MEDIA_CURSOS",
        "MEDIA_PONDERADA_PARTICIPANTES",
        "MEDIANA_CURSOS",
        "DP_CURSOS",
        "P25",
        "P75",
    ]
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


def _mascara_estrutural(
    candidatos: pd.DataFrame,
    alvo: pd.Series,
    incluir_categoria: bool,
    incluir_orgacad: bool,
) -> pd.Series:
    mask = candidatos["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
    if incluir_categoria:
        mask &= candidatos["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
    if incluir_orgacad:
        mask &= candidatos["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])
    return mask


def sensibilidade_benchmark_soure(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Avalia robustez do benchmark de Soure em cenários progressivamente restritivos."""
    alvo = obter_soure(base)
    candidatos = base.loc[~base["CO_IES"].eq(BIOLOGIA.co_ies_focal)].copy()
    participantes = pd.to_numeric(
        pd.Series([alvo.get("PARTICIPANTES_NUM")]), errors="coerce"
    ).iloc[0]

    cenarios = [
        ("modalidade", False, False, None),
        ("modalidade_categoria", True, False, None),
        ("modalidade_categoria_orgacad", True, True, None),
        ("estrutura_porte_0_5_2_0", True, True, (0.5, 2.0)),
        ("estrutura_porte_0_75_1_5", True, True, (0.75, 1.5)),
    ]
    indicadores = ("nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "taxa_presenca_microdados")
    linhas: list[dict[str, object]] = []
    membros: list[pd.DataFrame] = []

    for nome, categoria, orgacad, faixa in cenarios:
        mask = _mascara_estrutural(candidatos, alvo, categoria, orgacad)
        if faixa is not None and pd.notna(participantes) and participantes > 0:
            inferior = max(1, participantes * faixa[0])
            superior = participantes * faixa[1]
            mask &= pd.to_numeric(candidatos["PARTICIPANTES_NUM"], errors="coerce").between(
                inferior, superior
            )
        selecionados = candidatos.loc[mask].copy()
        if not selecionados.empty:
            selecionados.insert(0, "CENARIO", nome)
            membros.append(selecionados)

        linha: dict[str, object] = {
            "CENARIO": nome,
            "CO_CURSO_ALVO": CO_CURSO_SOURE,
            "N_CURSOS": len(selecionados),
        }
        for indicador in indicadores:
            alvo_valor = pd.to_numeric(pd.Series([alvo.get(indicador)]), errors="coerce").iloc[0]
            serie = pd.to_numeric(selecionados.get(indicador), errors="coerce").dropna()
            linha[f"{indicador}_ALVO"] = alvo_valor
            linha[f"{indicador}_MEDIA_BENCHMARK"] = serie.mean()
            linha[f"{indicador}_MEDIANA_BENCHMARK"] = serie.median()
            linha[f"{indicador}_DP_BENCHMARK"] = serie.std(ddof=1)
            linha[f"{indicador}_DIFERENCA"] = (
                alvo_valor - serie.mean() if pd.notna(alvo_valor) and not serie.empty else np.nan
            )
        linhas.append(linha)

    membros_df = pd.concat(membros, ignore_index=True) if membros else pd.DataFrame()
    return pd.DataFrame(linhas), membros_df


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
                    "RECORTE_FOCAL": base.loc[idx, "RECORTE_FOCAL"],
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
    linhas: list[dict[str, object]] = []
    y = pd.to_numeric(base["nt_ger_mean"], errors="coerce")
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
            }
        )
    return pd.DataFrame(linhas)


def desempenho_individual_soure(individual: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Descritivas e correlações somente entre variáveis do mesmo arquivo de desempenho."""
    variaveis = [
        coluna
        for coluna in ("NT_GER", "NT_OBJ", "NT_DIS", "QT_ACERTOS", "PROFICIENCIA")
        if coluna in individual.columns
    ]
    descritas: list[dict[str, object]] = []
    for coluna in variaveis:
        serie = pd.to_numeric(individual[coluna], errors="coerce").dropna()
        descritas.append(
            {
                "VARIAVEL": coluna,
                "N_VALIDO": int(serie.size),
                "MEDIA": serie.mean(),
                "MEDIANA": serie.median(),
                "DP": serie.std(ddof=1),
                "P25": serie.quantile(0.25),
                "P75": serie.quantile(0.75),
                "MIN": serie.min(),
                "MAX": serie.max(),
            }
        )

    correlacoes: list[dict[str, object]] = []
    for i, x_nome in enumerate(variaveis):
        for y_nome in variaveis[i + 1 :]:
            x = pd.to_numeric(individual[x_nome], errors="coerce")
            y = pd.to_numeric(individual[y_nome], errors="coerce")
            mask = x.notna() & y.notna()
            n = int(mask.sum())
            rho = np.nan
            pvalor = np.nan
            if n >= 3 and x[mask].nunique() > 1 and y[mask].nunique() > 1:
                resultado = spearmanr(x[mask], y[mask], nan_policy="omit")
                rho = float(resultado.statistic)
                pvalor = float(resultado.pvalue)
            correlacoes.append(
                {
                    "VARIAVEL_X": x_nome,
                    "VARIAVEL_Y": y_nome,
                    "N": n,
                    "SPEARMAN_RHO": rho,
                    "P_VALOR_EXPLORATORIO": pvalor,
                    "OBSERVACAO": "mesmo arquivo temático; relações com nota/acertos podem ser mecânicas",
                }
            )
    return pd.DataFrame(descritas), pd.DataFrame(correlacoes)


def perfil_focal(base: pd.DataFrame) -> pd.DataFrame:
    indicadores = [
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
    ]
    linhas: list[dict[str, object]] = []
    for recorte in ("Soure", "UFPA sem Soure", "Outras IES do Pará", "Norte sem Pará", "Brasil sem Norte"):
        sub = base.loc[base["RECORTE_FOCAL"].eq(recorte)]
        for indicador in indicadores:
            if indicador not in sub.columns:
                continue
            valores = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append(
                {
                    "RECORTE_FOCAL": recorte,
                    "INDICADOR": indicador,
                    "N_CURSOS": int(valores.size),
                    "MEDIA_CURSOS": valores.mean(),
                    "MEDIANA_CURSOS": valores.median(),
                    "DP_CURSOS": valores.std(ddof=1),
                }
            )
    return pd.DataFrame(linhas)


def comparar_itens_processo_soure(
    itens: pd.DataFrame,
    base: pd.DataFrame,
    benchmark: pd.DataFrame,
) -> pd.DataFrame:
    """Compara QE_I20-QE_I66 por código; não atribui rótulo substantivo sem fonte oficial."""
    cadastro = base[["CO_CURSO", "RECORTE_FOCAL"]].copy()
    trabalho = itens.merge(cadastro, on="CO_CURSO", how="left", validate="many_to_one")
    ids_benchmark = set(pd.to_numeric(benchmark["CO_CURSO"], errors="coerce").dropna().astype(int))
    linhas: list[dict[str, object]] = []
    for item, sub_item in trabalho.groupby("ITEM", observed=True):
        soure = sub_item.loc[pd.to_numeric(sub_item["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)]
        if soure.empty:
            continue
        valor_soure = pd.to_numeric(soure["media"], errors="coerce").iloc[0]
        n_soure = pd.to_numeric(soure["n_valido"], errors="coerce").iloc[0]
        referencias = {
            "UFPA sem Soure": sub_item.loc[sub_item["RECORTE_FOCAL"].eq("UFPA sem Soure")],
            "Benchmark comparável": sub_item.loc[
                pd.to_numeric(sub_item["CO_CURSO"], errors="coerce").isin(ids_benchmark)
            ],
            "Norte sem Pará": sub_item.loc[sub_item["RECORTE_FOCAL"].eq("Norte sem Pará")],
            "Brasil sem Norte": sub_item.loc[sub_item["RECORTE_FOCAL"].eq("Brasil sem Norte")],
        }
        for referencia, sub in referencias.items():
            valores = pd.to_numeric(sub["media"], errors="coerce").dropna()
            linhas.append(
                {
                    "ITEM": item,
                    "REFERENCIA": referencia,
                    "MEDIA_SOURE": valor_soure,
                    "N_VALIDO_SOURE": n_soure,
                    "N_CURSOS_REFERENCIA": int(valores.size),
                    "MEDIA_REFERENCIA": valores.mean(),
                    "DP_REFERENCIA": valores.std(ddof=1),
                    "DIFERENCA_SOURE_REFERENCIA": (
                        valor_soure - valores.mean() if pd.notna(valor_soure) and not valores.empty else np.nan
                    ),
                    "ROTULO_OFICIAL": pd.NA,
                    "STATUS_INTERPRETACAO": "interpretar apenas após vincular texto oficial do item",
                }
            )
    return pd.DataFrame(linhas)


def diagnosticar_dimensoes_exploratorias(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Resume dimensões candidatas usando concordância; uso estritamente exploratório."""
    scores = base[["CO_CURSO", "CO_IES", "ROTULO_OFERTA", "RECORTE_FOCAL"]].copy()
    resumo: list[dict[str, object]] = []
    for nome, itens in DIMENSOES_CANDIDATAS.items():
        colunas = [f"qe_i{i}_concordancia_pct" for i in itens]
        existentes = [coluna for coluna in colunas if coluna in base.columns]
        matriz = base[existentes].apply(pd.to_numeric, errors="coerce")
        scores[nome] = matriz.mean(axis=1, skipna=True)
        soure = scores.loc[pd.to_numeric(scores["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE), nome]
        resumo.append(
            {
                "DIMENSAO_CANDIDATA": nome,
                "N_ITENS_PREVISTOS": len(colunas),
                "N_ITENS_ENCONTRADOS": len(existentes),
                "MEDIA_NACIONAL_EXPLORATORIA": scores[nome].mean(),
                "VALOR_SOURE_EXPLORATORIO": soure.iloc[0] if len(soure) == 1 else np.nan,
                "DECISAO": (
                    "não usar como índice definitivo; exige texto oficial, direção da escala e coerência teórica"
                ),
            }
        )
    return pd.DataFrame(resumo), scores
