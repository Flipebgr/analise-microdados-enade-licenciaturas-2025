from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from src.biologia import BIOLOGIA, CO_CURSO_SOURE

RECORTES_FOCAIS = (
    "Soure",
    "UFPA sem Soure",
    "Outras IES do Pará",
    "Norte sem Pará",
    "Brasil sem Norte",
)

INDICADORES_FOCAIS = (
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


def obter_soure(base: pd.DataFrame) -> pd.Series:
    soure = base[pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)]
    if len(soure) != 1:
        raise ValueError(
            f"Esperada exatamente uma oferta focal de Soure ({CO_CURSO_SOURE}); "
            f"encontradas {len(soure)}."
        )
    return soure.iloc[0]


def construir_benchmark_soure(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Seleciona cursos externos à UFPA comparáveis à oferta focal de Soure."""
    alvo = obter_soure(base)
    candidatos = base[~base["CO_IES"].eq(BIOLOGIA.co_ies_focal)].copy()
    participantes = pd.to_numeric(pd.Series([alvo.get("PARTICIPANTES_NUM")]), errors="coerce").iloc[0]
    mask = (
        candidatos["CO_MODALIDADE"].eq(alvo["CO_MODALIDADE"])
        & candidatos["CO_CATEGAD"].eq(alvo["CO_CATEGAD"])
        & candidatos["CO_ORGACAD"].eq(alvo["CO_ORGACAD"])
    )
    criterio = (
        "mesma modalidade, categoria administrativa e organização acadêmica; "
        "participantes entre 0,5x e 2x Soure"
    )
    if pd.notna(participantes) and participantes > 0:
        mask &= candidatos["PARTICIPANTES_NUM"].between(
            max(1, participantes * 0.5), participantes * 2.0
        )
    selecionados = candidatos.loc[mask].copy()
    selecionados.insert(0, "CO_CURSO_ALVO", CO_CURSO_SOURE)
    selecionados.insert(1, "ROTULO_ALVO", alvo.get("ROTULO_OFERTA", "Soure"))
    resumo = pd.DataFrame([{
        "CO_CURSO_ALVO": CO_CURSO_SOURE,
        "ROTULO_ALVO": alvo.get("ROTULO_OFERTA", "Soure"),
        "participantes_alvo": participantes,
        "n_cursos_comparaveis": len(selecionados),
        "criterio": criterio,
    }])
    return selecionados.reset_index(drop=True), resumo


def construir_comparacao_focal(
    base: pd.DataFrame,
    indicadores: Iterable[str] = INDICADORES_FOCAIS,
) -> pd.DataFrame:
    """Resume Soure e referências sem cruzar registros individuais entre arquivos."""
    linhas: list[dict[str, object]] = []
    for recorte in RECORTES_FOCAIS:
        sub = base[base["RECORTE_FOCAL"].eq(recorte)]
        for indicador in indicadores:
            if indicador not in sub.columns:
                continue
            valores = pd.to_numeric(sub[indicador], errors="coerce").dropna()
            linhas.append({
                "RECORTE_FOCAL": recorte,
                "INDICADOR": indicador,
                "N_CURSOS": int(valores.size),
                "MEDIA_CURSOS": valores.mean(),
                "MEDIANA_CURSOS": valores.median(),
                "DP_CURSOS": valores.std(ddof=1),
                "P25": valores.quantile(0.25),
                "P75": valores.quantile(0.75),
            })
    return pd.DataFrame(linhas)


def construir_perfil_diferencial_soure(
    base: pd.DataFrame,
    benchmark: pd.DataFrame,
    indicadores: Iterable[str] = INDICADORES_FOCAIS,
) -> pd.DataFrame:
    """Calcula diferenças de Soure para referências no nível agregado do curso."""
    alvo = obter_soure(base)
    referencias = {
        "UFPA sem Soure": base[
            base["CO_IES"].eq(BIOLOGIA.co_ies_focal)
            & ~pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)
        ],
        "Benchmark comparável": benchmark,
        "Pará sem UFPA": base[base["RECORTE_FOCAL"].eq("Outras IES do Pará")],
        "Norte sem Pará": base[base["RECORTE_FOCAL"].eq("Norte sem Pará")],
        "Brasil sem Norte": base[base["RECORTE_FOCAL"].eq("Brasil sem Norte")],
    }
    linhas: list[dict[str, object]] = []
    for indicador in indicadores:
        if indicador not in base.columns:
            continue
        valor_soure = pd.to_numeric(pd.Series([alvo.get(indicador)]), errors="coerce").iloc[0]
        for nome, ref in referencias.items():
            if indicador not in ref.columns:
                continue
            s = pd.to_numeric(ref[indicador], errors="coerce").dropna()
            media = s.mean()
            dp = s.std(ddof=1)
            z = np.nan
            if pd.notna(valor_soure) and np.isfinite(dp) and dp > 0:
                z = (valor_soure - media) / dp
            linhas.append({
                "INDICADOR": indicador,
                "REFERENCIA": nome,
                "VALOR_SOURE": valor_soure,
                "N_CURSOS_REFERENCIA": int(s.size),
                "MEDIA_REFERENCIA": media,
                "DP_REFERENCIA": dp,
                "DIFERENCA_SOURE_REFERENCIA": valor_soure - media if pd.notna(valor_soure) else np.nan,
                "Z_SOURE_REFERENCIA": z,
            })
    return pd.DataFrame(linhas)


def resumir_percentis_soure(base: pd.DataFrame) -> pd.DataFrame:
    alvo = obter_soure(base)
    colunas = [
        "nt_ger_percentil_brasil",
        "nt_ger_percentil_norte",
        "nt_ger_percentil_para",
        "nt_ger_dif_mediana_brasil",
        "nt_ger_z_curso",
    ]
    return pd.DataFrame([
        {"INDICADOR": coluna, "VALOR": alvo.get(coluna)}
        for coluna in colunas if coluna in base.columns
    ])
