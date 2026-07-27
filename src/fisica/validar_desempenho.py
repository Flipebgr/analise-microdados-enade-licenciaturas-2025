from __future__ import annotations

import numpy as np
import pandas as pd


def auditar_desempenho(base: pd.DataFrame, co_ies: int = 569) -> pd.DataFrame:
    """Gera auditoria por oferta para NT_GER, NT_OBJ e NT_DIS."""
    dados = base.loc[base["CO_IES"].eq(co_ies)].copy()
    linhas: list[dict[str, object]] = []
    for _, row in dados.iterrows():
        presentes = pd.to_numeric(row.get("presentes_validos"), errors="coerce")
        for prefixo, rotulo in [("nt_ger", "NT_GER"), ("nt_obj", "NT_OBJ"), ("nt_dis", "NT_DIS")]:
            n = pd.to_numeric(row.get(f"{prefixo}_count"), errors="coerce")
            cobertura = n / presentes * 100 if pd.notna(presentes) and presentes > 0 else np.nan
            media = pd.to_numeric(row.get(f"{prefixo}_mean"), errors="coerce")
            mediana = pd.to_numeric(row.get(f"{prefixo}_median"), errors="coerce")
            dp = pd.to_numeric(row.get(f"{prefixo}_std"), errors="coerce")
            linhas.append({
                "CO_CURSO": row["CO_CURSO"],
                "ROTULO_OFERTA": row["ROTULO_OFERTA"],
                "CONCEITO_ENADE_NUM": row.get("CONCEITO_ENADE_NUM"),
                "indicador": rotulo,
                "n_valido": n,
                "presentes_validos": presentes,
                "cobertura_pct": cobertura,
                "media": media,
                "mediana": mediana,
                "desvio_padrao": dp,
                "p25": row.get(f"{prefixo}_p25"),
                "p75": row.get(f"{prefixo}_p75"),
                "ic95_inf": row.get(f"{prefixo}_ic95_inf"),
                "ic95_sup": row.get(f"{prefixo}_ic95_sup"),
                "alerta": "OK" if pd.isna(cobertura) or cobertura >= 95 else "Cobertura inferior a 95%",
            })
    return pd.DataFrame(linhas)


def comparacao_territorial(base: pd.DataFrame) -> pd.DataFrame:
    """Resume NT_GER de referências territoriais sem tratá-las como grupos independentes."""
    nt = pd.to_numeric(base["nt_ger_mean"], errors="coerce")
    grupos = {
        "UFPA agregada": base["CO_IES"].eq(569),
        "Outras IES do Pará": base["GRUPO_CODIGO"].eq("C"),
        "Região Norte completa": base["CO_REGIAO_CURSO"].eq(1),
        "Brasil completo": pd.Series(True, index=base.index),
    }
    linhas = []
    for nome, filtro in grupos.items():
        valores = nt[filtro & nt.notna()]
        pesos = pd.to_numeric(base.loc[valores.index, "nt_ger_count"], errors="coerce")
        ponderada = np.average(valores, weights=pesos) if len(valores) and pesos.notna().all() and pesos.sum() > 0 else np.nan
        linhas.append({
            "referencia": nome,
            "n_cursos": len(valores),
            "media_cursos": valores.mean(),
            "mediana_cursos": valores.median(),
            "media_ponderada_participantes": ponderada,
            "p25": valores.quantile(.25),
            "p75": valores.quantile(.75),
        })
    return pd.DataFrame(linhas)
