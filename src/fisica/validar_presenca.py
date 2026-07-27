from __future__ import annotations

import numpy as np
import pandas as pd


COLUNAS = [
    "CO_CURSO", "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "INSCRITOS_NUM",
    "PARTICIPANTES_NUM", "registros_microdados", "presentes_validos",
    "ausentes", "eliminados", "resultado_desconsiderado", "reaplicacoes",
    "nt_ger_count", "taxa_presenca_microdados",
]


def auditar_presenca(base: pd.DataFrame, co_ies: int = 569) -> pd.DataFrame:
    """Audita cobertura e coerência da participação nas ofertas da UFPA."""
    dados = base.loc[base["CO_IES"].eq(co_ies), [c for c in COLUNAS if c in base.columns]].copy()
    dados["taxa_presenca_pct"] = pd.to_numeric(
        dados.get("taxa_presenca_microdados"), errors="coerce"
    ) * 100
    dados["diferenca_participantes"] = (
        pd.to_numeric(dados["PARTICIPANTES_NUM"], errors="coerce")
        - pd.to_numeric(dados["presentes_validos"], errors="coerce")
    )
    dados["cobertura_nt_ger_pct"] = np.where(
        pd.to_numeric(dados["presentes_validos"], errors="coerce") > 0,
        pd.to_numeric(dados["nt_ger_count"], errors="coerce")
        / pd.to_numeric(dados["presentes_validos"], errors="coerce") * 100,
        np.nan,
    )
    dados["alerta"] = "OK"
    dados.loc[dados["diferenca_participantes"].abs() > 0, "alerta"] = (
        "Participantes oficiais divergem dos presentes válidos"
    )
    dados.loc[~dados["taxa_presenca_pct"].between(0, 100), "alerta"] = (
        "Taxa de presença fora de 0–100"
    )
    dados.loc[dados["cobertura_nt_ger_pct"] < 95, "alerta"] = (
        "Cobertura de NT_GER inferior a 95% dos presentes"
    )
    return dados.sort_values("taxa_presenca_pct").reset_index(drop=True)
