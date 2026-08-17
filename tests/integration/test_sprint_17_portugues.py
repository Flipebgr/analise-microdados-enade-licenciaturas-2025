from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT
from src.portugues import CO_CURSO_BELEM_EAD


@pytest.mark.integration
def test_produtos_sprint17_portugues():
    pasta = ROOT / "dados_processados" / "portugues"
    base_path = pasta / "base_analitica_cursos.csv"
    if not base_path.exists():
        pytest.skip("Produtos locais da Sprint 16 não disponíveis.")

    base = pd.read_csv(base_path, low_memory=False)
    assert len(base) == 340
    ufpa = base.loc[base["CO_IES"].eq(569)]
    assert len(ufpa) == 8
    conceito1 = ufpa.loc[ufpa["CONCEITO_ENADE_NUM"].eq(1)]
    assert len(conceito1) == 1
    assert int(conceito1.iloc[0]["CO_CURSO"]) == CO_CURSO_BELEM_EAD

    esperados = [
        "auditoria_desempenho_sprint17.csv",
        "auditoria_indicadores_sprint17.csv",
        "comparacoes_regionais_validadas_sprint17.csv",
        "sensibilidade_desempenho_sprint17.csv",
        "sensibilidade_benchmarks_sprint17.csv",
        "membros_benchmarks_sprint17.csv",
        "perfil_grupos_validado_sprint17.csv",
        "processo_formativo_conceito1_validado.csv",
        "recomendacao_grupos_validada_sprint17.csv",
        "diagnostico_outliers_sprint17.csv",
        "associacoes_ecologicas_sprint17.csv",
    ]
    for nome in esperados:
        assert (pasta / nome).exists(), nome

    processo = pd.read_csv(
        pasta / "processo_formativo_conceito1_validado.csv",
        low_memory=False,
    )
    assert processo["ITEM"].nunique() == 47
    assert "Benchmark comparável" in set(processo["REFERENCIA"])

    figuras = ROOT / "figuras" / "portugues"
    for n in range(14, 20):
        assert list(figuras.glob(f"validada_{n:02d}_*.png"))
