from __future__ import annotations

import numpy as np
import pandas as pd

INDICADORES_DESEMPENHO = ("nt_ger_mean", "nt_obj_mean", "nt_dis_mean")


def _media_ponderada(valores: pd.Series, pesos: pd.Series) -> float:
    v = pd.to_numeric(valores, errors="coerce")
    w = pd.to_numeric(pesos, errors="coerce")
    mask = v.notna() & w.notna() & w.gt(0)
    if not mask.any():
        return float("nan")
    return float(np.average(v[mask], weights=w[mask]))


def rotulo_recorte(base: pd.DataFrame, co_ies_ufpa: int = 569) -> pd.Series:
    regiao = pd.to_numeric(base["CO_REGIAO_CURSO"], errors="coerce")
    ies = pd.to_numeric(base["CO_IES"], errors="coerce")
    return pd.Series(
        np.select(
            [
                ies.eq(co_ies_ufpa),
                regiao.eq(1) & ~ies.eq(co_ies_ufpa),
                regiao.eq(2), regiao.eq(3), regiao.eq(4), regiao.eq(5),
            ],
            [
                "UFPA", "Região Norte sem UFPA", "Nordeste", "Sudeste",
                "Sul", "Centro-Oeste",
            ],
            default="Não classificado",
        ),
        index=base.index,
        dtype="string",
    )


def construir_comparacoes_regionais(base: pd.DataFrame) -> pd.DataFrame:
    trabalho = base.copy()
    trabalho["RECORTE_REGIONAL"] = rotulo_recorte(trabalho)
    recortes: list[tuple[str, pd.Series]] = [
        ("UFPA agregada", trabalho["CO_IES"].eq(569)),
        (
            "Região Norte sem UFPA",
            trabalho["RECORTE_REGIONAL"].eq("Região Norte sem UFPA"),
        ),
        (
            "Região Norte completa",
            pd.to_numeric(trabalho["CO_REGIAO_CURSO"], errors="coerce").eq(1),
        ),
        ("Nordeste", trabalho["RECORTE_REGIONAL"].eq("Nordeste")),
        ("Sudeste", trabalho["RECORTE_REGIONAL"].eq("Sudeste")),
        ("Sul", trabalho["RECORTE_REGIONAL"].eq("Sul")),
        ("Centro-Oeste", trabalho["RECORTE_REGIONAL"].eq("Centro-Oeste")),
        ("Brasil geral", pd.Series(True, index=trabalho.index)),
        ("Brasil sem UFPA", ~trabalho["CO_IES"].eq(569)),
        (
            "Restante do Brasil sem Norte",
            ~pd.to_numeric(trabalho["CO_REGIAO_CURSO"], errors="coerce").eq(1),
        ),
    ]
    for _, oferta in trabalho[trabalho["CO_IES"].eq(569)].iterrows():
        recortes.insert(
            0,
            (
                f"UFPA — {oferta['ROTULO_OFERTA']}",
                trabalho["CO_CURSO"].eq(oferta["CO_CURSO"]),
            ),
        )

    linhas: list[dict[str, object]] = []
    for nome, mask in recortes:
        sub = trabalho.loc[mask]
        for indicador in INDICADORES_DESEMPENHO:
            valores = pd.to_numeric(sub.get(indicador), errors="coerce")
            validos = valores.dropna()
            linhas.append(
                {
                "RECORTE": nome,
                "INDICADOR": indicador,
                "N_CURSOS": int(validos.size),
                    "N_PARTICIPANTES": float(
                        pd.to_numeric(
                            sub.get("nt_ger_count"),
                            errors="coerce",
                        ).sum(min_count=1)
                    ),
                "MEDIA_CURSOS": validos.mean(),
                    "MEDIA_PONDERADA_PARTICIPANTES": _media_ponderada(
                        valores,
                        sub.get(
                            "nt_ger_count",
                            pd.Series(index=sub.index, dtype=float),
                        ),
                    ),
                "MEDIANA_CURSOS": validos.median(),
                "DP_CURSOS": validos.std(ddof=1),
                "P25": validos.quantile(0.25),
                "P75": validos.quantile(0.75),
                }
            )
    return pd.DataFrame(linhas)
