from __future__ import annotations

import pandas as pd
import pytest

from src.biologia import CO_CURSO_SOURE
from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_produtos_sprint_10_biologia_quando_disponiveis() -> None:
    base_path = ROOT / "dados_processados" / "biologia" / "base_analitica_cursos.csv"
    if not base_path.exists():
        pytest.skip("Produtos locais da Sprint 10 de Biologia ainda não foram gerados.")
    base = pd.read_csv(base_path)
    assert base["CO_CURSO"].is_unique
    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 5
    assert int(ufpa["CONCEITO_ENADE_NUM"].eq(1).sum()) == 0
    soure = base[pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)]
    assert len(soure) == 1
    assert int(soure.iloc[0]["CONCEITO_ENADE_NUM"]) == 3
    assert soure.iloc[0]["RECORTE_FOCAL"] == "Soure"
    benchmark = pd.read_csv(ROOT / "dados_processados" / "biologia" / "benchmark_soure_cursos.csv")
    assert not benchmark["CO_IES"].eq(569).any()
    assert (ROOT / "dados_processados" / "biologia" / "comparacao_focal_soure.csv").exists()
    assert (ROOT / "dados_processados" / "biologia" / "desempenho_individual_soure.csv").exists()
    figuras = list((ROOT / "figuras" / "biologia").glob("*.png"))
    assert len(figuras) >= 13
    assert all(path.stat().st_size > 0 for path in figuras)
    assert (ROOT / "relatorios" / "sprint_10_piloto_biologia.md").exists()
