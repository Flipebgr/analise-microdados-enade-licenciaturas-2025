from __future__ import annotations

import pandas as pd

from src.analise.construir_benchmarks import construir_benchmark_comparavel
from src.analise.estatisticas_descritivas import resumo_por_grupo


def construir_benchmarks_fisica(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    comparaveis, resumo = construir_benchmark_comparavel(base)
    indicadores = [
        "nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "taxa_presenca_microdados",
        "renda_ate_3sm_pct", "trabalha_pct", "acao_afirmativa_pct",
        "auxilio_permanencia_pct", "qe_i68_media", "qe_i69_media",
    ]
    amplos = resumo_por_grupo(base, indicadores)
    return comparaveis, resumo, amplos
