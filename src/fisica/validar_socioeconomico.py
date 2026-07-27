from __future__ import annotations

import pandas as pd


INDICADORES = [
    "primeira_geracao_pct", "mae_superior_pct", "pai_superior_pct",
    "renda_ate_3sm_pct", "trabalha_pct", "trabalha_40h_pct",
    "acao_afirmativa_pct", "auxilio_permanencia_pct", "bolsa_academica_pct",
    "estudo_4h_ou_mais_pct", "pretende_magisterio_pct",
]


def auditar_socioeconomico(base: pd.DataFrame, co_ies: int = 569) -> tuple[pd.DataFrame, pd.DataFrame]:
    ufpa = base[base["CO_IES"].eq(co_ies)].copy()
    longas = []
    for _, row in ufpa.iterrows():
        for indicador in INDICADORES:
            valor = pd.to_numeric(row.get(indicador), errors="coerce")
            prefixo = indicador.removesuffix("_pct")
            ncol = f"{prefixo}n_valido"
            n = pd.to_numeric(row.get(ncol), errors="coerce")
            longas.append({
                "CO_CURSO": row["CO_CURSO"],
                "ROTULO_OFERTA": row["ROTULO_OFERTA"],
                "indicador": indicador,
                "n_valido": n,
                "percentual": valor,
                "alerta": "OK" if pd.notna(valor) and 0 <= valor <= 1 else "Percentual inválido ou ausente",
            })
    sintese_cols = [
        "CO_CURSO", "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "nt_ger_mean",
        "nt_ger_median", "taxa_presenca_microdados", *INDICADORES,
    ]
    return pd.DataFrame(longas), ufpa[[c for c in sintese_cols if c in ufpa.columns]].copy()
