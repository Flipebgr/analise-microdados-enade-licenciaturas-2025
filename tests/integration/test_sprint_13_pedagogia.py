from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT
from src.pedagogia import CO_CURSO_CASTANHAL

pytestmark = pytest.mark.integration


def test_produtos_sprint_13_pedagogia_quando_disponiveis() -> None:
    pasta = ROOT / "dados_processados" / "pedagogia"
    base_path = pasta / "base_analitica_cursos.csv"
    if not base_path.exists():
        pytest.skip("Produtos locais da Sprint 13 de Pedagogia ainda não foram gerados.")

    base = pd.read_csv(base_path)
    assert base["CO_CURSO"].is_unique
    assert len(base) == 1200

    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 7
    assert int(ufpa["CONCEITO_ENADE_NUM"].eq(1).sum()) == 0
    assert set(ufpa["CONCEITO_ENADE_NUM"].astype(int)) == {4, 5}

    castanhal = ufpa[
        pd.to_numeric(ufpa["CO_CURSO"], errors="coerce").eq(CO_CURSO_CASTANHAL)
    ]
    assert len(castanhal) == 1
    assert int(castanhal.iloc[0]["CONCEITO_ENADE_NUM"]) == 5
    assert castanhal.iloc[0]["RECORTE_PEDAGOGIA"] == "UFPA — Conceito 5"

    resumo = pd.read_csv(pasta / "benchmark_comparavel_resumo.csv")
    assert len(resumo) == 7
    assert (resumo["N_CURSOS_COMPARAVEIS"] > 0).all()

    assert (pasta / "comparacao_interna_ufpa.csv").exists()
    assert (pasta / "comparacoes_regionais_nacionais.csv").exists()

    figuras = list((ROOT / "figuras" / "pedagogia").glob("*.png"))
    assert len(figuras) >= 13
    assert all(path.stat().st_size > 0 for path in figuras)
    assert (ROOT / "relatorios" / "sprint_13_piloto_pedagogia.md").exists()
