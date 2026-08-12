from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT
from src.pedagogia import CO_CURSO_CASTANHAL

pytestmark = pytest.mark.integration


def test_produtos_sprint_14_pedagogia_quando_disponiveis() -> None:
    pasta = ROOT / "dados_processados" / "pedagogia"
    base_path = pasta / "base_analitica_cursos.csv"
    sens_path = pasta / "sensibilidade_benchmarks_sprint14.csv"
    if not base_path.exists() or not sens_path.exists():
        pytest.skip("Produtos locais da Sprint 14 de Pedagogia ainda não foram gerados.")

    base = pd.read_csv(base_path)
    sens = pd.read_csv(sens_path)
    assert len(base) == 1200
    assert base["CO_CURSO"].is_unique
    ufpa = base.loc[base["CO_IES"].eq(569)]
    assert len(ufpa) == 7
    assert not ufpa["CONCEITO_ENADE_NUM"].eq(1).any()

    castanhal = ufpa.loc[
        pd.to_numeric(ufpa["CO_CURSO"], errors="coerce").eq(CO_CURSO_CASTANHAL)
    ]
    assert len(castanhal) == 1
    assert int(castanhal.iloc[0]["CONCEITO_ENADE_NUM"]) == 5

    assert len(sens) == 35
    assert sens["CO_CURSO_ALVO"].nunique() == 7
    principal = sens.loc[sens["CENARIO"].eq("estrutura_porte_0_5_2_0")]
    assert len(principal) == 7
    assert (principal["N_CURSOS"] > 0).all()

    itens = pd.read_csv(pasta / "processo_formativo_castanhal_validado.csv")
    assert itens["ITEM"].nunique() == 47

    figuras = list((ROOT / "figuras" / "pedagogia").glob("validada_*.png"))
    assert len(figuras) >= 6
    assert all(path.stat().st_size > 0 for path in figuras)
    assert (ROOT / "relatorios" / "sprint_14_validacao_pedagogia.md").exists()
