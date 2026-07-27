from __future__ import annotations

import numpy as np
import pandas as pd

CO_IES_UFPA = 569


def construir_auditoria_presenca(base: pd.DataFrame) -> pd.DataFrame:
    colunas = [
        "CO_CURSO", "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "INSCRITOS_NUM",
        "PARTICIPANTES_NUM", "registros_microdados", "presentes_validos", "ausentes",
        "eliminados", "resultado_desconsiderado", "nt_ger_count",
    ]
    out = base.loc[base["CO_IES"].eq(CO_IES_UFPA), colunas].copy()
    denom = pd.to_numeric(out["registros_microdados"], errors="coerce")
    presentes = pd.to_numeric(out["presentes_validos"], errors="coerce")
    out["taxa_presenca_pct"] = np.where(denom > 0, presentes / denom * 100, np.nan)
    out["diferenca_participantes_microdados"] = (
        pd.to_numeric(out["PARTICIPANTES_NUM"], errors="coerce")
        - pd.to_numeric(out["nt_ger_count"], errors="coerce")
    )
    return out.sort_values("taxa_presenca_pct")
