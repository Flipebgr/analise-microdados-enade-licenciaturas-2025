from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_produtos_sprint_07_quando_disponiveis() -> None:
    base_path = ROOT / "dados_processados" / "ingles" / "base_analitica_cursos.csv"
    if not base_path.exists():
        pytest.skip("Produtos locais da Sprint 07 ainda não foram gerados.")
    base = pd.read_csv(base_path)
    assert base["CO_CURSO"].is_unique
    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 5
    assert ufpa["CONCEITO_ENADE_NUM"].eq(1).sum() == 4
    figuras = list((ROOT / "figuras" / "ingles").glob("*.png"))
    assert len(figuras) >= 8
    assert all(path.stat().st_size > 0 for path in figuras)
