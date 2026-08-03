from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_produtos_sprint_08_quando_disponiveis() -> None:
    pasta = ROOT / "dados_processados" / "ingles"
    base_path = pasta / "base_analitica_cursos.csv"
    sensibilidade_path = pasta / "sensibilidade_benchmarks.csv"
    if not base_path.exists() or not sensibilidade_path.exists():
        pytest.skip("Produtos locais das Sprints 07/08 ainda não foram gerados.")

    base = pd.read_csv(base_path)
    sensibilidade = pd.read_csv(sensibilidade_path)
    assert len(base) == 138
    assert base["CO_CURSO"].is_unique
    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 5
    assert ufpa["CONCEITO_ENADE_NUM"].eq(1).sum() == 4
    assert sensibilidade["CO_CURSO_ALVO"].nunique() == 4
    assert len(sensibilidade) == 12

    figuras = [
        ROOT / "figuras" / "ingles" / "validada_09_participacao_ufpa.png",
        ROOT / "figuras" / "ingles" / "validada_10_sensibilidade_desempenho.png",
        ROOT / "figuras" / "ingles" / "validada_11_benchmark_comparavel.png",
        ROOT / "figuras" / "ingles" / "validada_12_comparacao_regional.png",
    ]
    assert all(path.exists() and path.stat().st_size > 0 for path in figuras)
    assert (ROOT / "relatorios" / "sprint_08_validacao_letras_ingles.md").exists()
