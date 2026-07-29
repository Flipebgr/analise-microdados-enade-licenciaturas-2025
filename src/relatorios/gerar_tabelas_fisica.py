from __future__ import annotations

import pandas as pd

UFPA = 569


def ofertas_ufpa(cursos: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "CO_CURSO", "ROTULO_OFERTA", "MODALIDADE", "INSCRITOS_NUM",
        "PARTICIPANTES_NUM", "PCT_PADRAO_PROFICIENCIA_NUM",
        "CONCEITO_ENADE", "SITUACAO_CONCEITO",
    ]
    df = cursos.loc[cursos["CO_IES"].eq(UFPA), cols].copy()
    df["PCT_PADRAO_PROFICIENCIA_NUM"] *= 100
    return df.rename(columns={
        "CO_CURSO": "Código", "ROTULO_OFERTA": "Oferta",
        "MODALIDADE": "Modalidade", "INSCRITOS_NUM": "Inscritos",
        "PARTICIPANTES_NUM": "Participantes",
        "PCT_PADRAO_PROFICIENCIA_NUM": "% no padrão",
        "CONCEITO_ENADE": "Conceito", "SITUACAO_CONCEITO": "Situação",
    }).sort_values("Oferta")


def participacao(auditoria: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "ROTULO_OFERTA", "INSCRITOS_NUM", "PARTICIPANTES_NUM",
        "presentes_validos", "taxa_presenca_pct", "cobertura_nt_ger_pct", "alerta",
    ]
    return auditoria[cols].rename(columns={
        "ROTULO_OFERTA": "Oferta", "INSCRITOS_NUM": "Inscritos",
        "PARTICIPANTES_NUM": "Participantes oficiais",
        "presentes_validos": "Presentes válidos",
        "taxa_presenca_pct": "Taxa de presença (%)",
        "cobertura_nt_ger_pct": "Cobertura NT_GER (%)", "alerta": "Auditoria",
    }).sort_values("Taxa de presença (%)")


def desempenho_ufpa(base: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "nt_ger_count", "nt_ger_mean",
        "nt_ger_median", "nt_ger_std", "nt_obj_count", "nt_obj_mean",
        "nt_obj_median", "nt_dis_count", "nt_dis_mean", "nt_dis_median",
        "nt_ger_percentil_brasil",
    ]
    df = base.loc[base["CO_IES"].eq(UFPA), cols].copy()
    return df.rename(columns={
        "ROTULO_OFERTA": "Oferta", "CONCEITO_ENADE_NUM": "Conceito",
        "nt_ger_count": "N NT_GER", "nt_ger_mean": "Média NT_GER",
        "nt_ger_median": "Mediana NT_GER", "nt_ger_std": "DP NT_GER",
        "nt_obj_count": "N NT_OBJ", "nt_obj_mean": "Média NT_OBJ",
        "nt_obj_median": "Mediana NT_OBJ", "nt_dis_count": "N NT_DIS",
        "nt_dis_mean": "Média NT_DIS", "nt_dis_median": "Mediana NT_DIS",
        "nt_ger_percentil_brasil": "Percentil Brasil",
    }).sort_values("Média NT_GER", ascending=False)


def comparacao_territorial(comparacao: pd.DataFrame) -> pd.DataFrame:
    return comparacao.rename(columns={
        "referencia": "Referência", "n_cursos": "N cursos",
        "media_cursos": "Média dos cursos", "mediana_cursos": "Mediana dos cursos",
        "media_ponderada_participantes": "Média ponderada",
        "p25": "P25", "p75": "P75",
    })


def socioeconomico(tabela: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "nt_ger_mean",
        "primeira_geracao_pct", "renda_ate_3sm_pct", "trabalha_pct",
        "acao_afirmativa_pct", "auxilio_permanencia_pct",
        "bolsa_academica_pct", "estudo_4h_ou_mais_pct",
        "pretende_magisterio_pct",
    ]
    df = tabela[cols].copy()
    for col in cols[3:]:
        df[col] *= 100
    return df.rename(columns={
        "ROTULO_OFERTA": "Oferta", "CONCEITO_ENADE_NUM": "Conceito",
        "nt_ger_mean": "Média NT_GER", "primeira_geracao_pct": "Primeira geração (%)",
        "renda_ate_3sm_pct": "Renda até 3 SM (%)", "trabalha_pct": "Trabalha (%)",
        "acao_afirmativa_pct": "Ação afirmativa (%)",
        "auxilio_permanencia_pct": "Auxílio permanência (%)",
        "bolsa_academica_pct": "Bolsa acadêmica (%)",
        "estudo_4h_ou_mais_pct": "Estudo ≥4h (%)",
        "pretende_magisterio_pct": "Pretende magistério (%)",
    }).sort_values("Média NT_GER", ascending=False)


def recomendacao_dificuldade(base: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "co_rs_i1_n",
        "co_rs_i1_dificuldade_alta_pct", "qe_i68_n", "qe_i68_nota_9_10_pct",
        "qe_i69_n", "qe_i69_nota_9_10_pct",
    ]
    df = base.loc[base["CO_IES"].eq(UFPA), cols].copy()
    for col in ["qe_i68_nota_9_10_pct", "qe_i69_nota_9_10_pct"]:
        df[col] *= 100
    return df.rename(columns={
        "ROTULO_OFERTA": "Oferta", "CONCEITO_ENADE_NUM": "Conceito",
        "co_rs_i1_n": "N dificuldade", "co_rs_i1_dificuldade_alta_pct": "Dificuldade alta (%)",
        "qe_i68_n": "N recomendação curso", "qe_i68_nota_9_10_pct": "Recomendação curso 9–10 (%)",
        "qe_i69_n": "N recomendação IES", "qe_i69_nota_9_10_pct": "Recomendação IES 9–10 (%)",
    }).sort_values("Oferta")


def dimensoes_processo(diagnostico: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "dimensao", "n_itens_encontrados", "n_cursos_com_score",
        "media_nacional_exploratoria", "media_ufpa_exploratoria", "decisao",
    ]
    return diagnostico[cols].rename(columns={
        "dimensao": "Dimensão", "n_itens_encontrados": "N itens",
        "n_cursos_com_score": "N cursos", "media_nacional_exploratoria": "Média Brasil",
        "media_ufpa_exploratoria": "Média UFPA", "decisao": "Decisão metodológica",
    })


def associacoes_selecionadas(associacoes: pd.DataFrame) -> pd.DataFrame:
    cols = ["desfecho", "preditor", "n_cursos", "spearman_rho", "p_valor_exploratorio", "interpretacao"]
    df = associacoes[cols].copy()
    df["abs_rho"] = df["spearman_rho"].abs()
    df = df.sort_values("abs_rho", ascending=False).head(8).drop(columns="abs_rho")
    return df.rename(columns={
        "desfecho": "Desfecho", "preditor": "Indicador agregado", "n_cursos": "N cursos",
        "spearman_rho": "Spearman ρ", "p_valor_exploratorio": "p exploratório",
        "interpretacao": "Interpretação",
    })


def benchmark_sensibilidade(sens: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "ROTULO_ALVO", "criterio", "n_cursos_comparaveis", "nt_ger_alvo",
        "media_comparaveis", "diferenca_media", "percentil_alvo",
    ]
    return sens[cols].rename(columns={
        "ROTULO_ALVO": "Oferta", "criterio": "Critério",
        "n_cursos_comparaveis": "N comparáveis", "nt_ger_alvo": "NT_GER oferta",
        "media_comparaveis": "Média comparáveis", "diferenca_media": "Diferença",
        "percentil_alvo": "Percentil no conjunto",
    })
