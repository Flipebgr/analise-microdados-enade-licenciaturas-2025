from __future__ import annotations

import pandas as pd

CO_IES_UFPA = 569


def desempenho_ufpa(base: pd.DataFrame) -> pd.DataFrame:
    colunas = [
        "CO_CURSO", "ROTULO_OFERTA", "MODALIDADE", "CONCEITO_ENADE_NUM",
        "nt_ger_count", "nt_ger_mean", "nt_ger_median", "nt_ger_std", "nt_ger_p25", "nt_ger_p75",
        "nt_obj_count", "nt_obj_mean", "nt_obj_median", "nt_obj_std", "nt_obj_p25", "nt_obj_p75",
        "nt_dis_count", "nt_dis_mean", "nt_dis_median", "nt_dis_std", "nt_dis_p25", "nt_dis_p75",
    ]
    existentes = [c for c in colunas if c in base.columns]
    return base.loc[base["CO_IES"].eq(CO_IES_UFPA), existentes].copy()


def referencias_nt_ger(base: pd.DataFrame) -> pd.DataFrame:
    mascaras = {
        "UFPA agregada": base["CO_IES"].eq(CO_IES_UFPA),
        "Outras IES do Pará": (~base["CO_IES"].eq(CO_IES_UFPA)) & base["CO_UF_CURSO"].eq(15),
        "Região Norte": base["CO_REGIAO_CURSO"].eq(1),
        "Brasil": pd.Series(True, index=base.index),
    }
    linhas = []
    for rotulo, mask in mascaras.items():
        s = pd.to_numeric(base.loc[mask, "nt_ger_mean"], errors="coerce").dropna()
        linhas.append({
            "REFERENCIA": rotulo,
            "N_CURSOS": int(s.size),
            "MEDIA_DAS_MEDIAS": s.mean(),
            "MEDIANA_DAS_MEDIAS": s.median(),
            "DP_DAS_MEDIAS": s.std(ddof=1),
        })
    return pd.DataFrame(linhas)
