from __future__ import annotations

import pandas as pd
import pytest

from src.biologia import CO_CURSO_SOURE
from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_produtos_sprint_11_biologia_quando_disponiveis() -> None:
    pasta = ROOT / "dados_processados" / "biologia"
    base_path = pasta / "base_analitica_cursos.csv"
    sensibilidade_path = pasta / "sensibilidade_benchmark_soure.csv"
    itens_path = pasta / "processo_formativo_soure_itens_validado.csv"
    if not base_path.exists() or not sensibilidade_path.exists() or not itens_path.exists():
        pytest.skip("Produtos locais da Sprint 11 de Biologia ainda não foram gerados.")

    base = pd.read_csv(base_path)
    sensibilidade = pd.read_csv(sensibilidade_path)
    itens = pd.read_csv(itens_path)
    assert len(base) == 428
    assert base["CO_CURSO"].is_unique
    ufpa = base.loc[base["CO_IES"].eq(569)]
    assert len(ufpa) == 5
    assert int(pd.to_numeric(ufpa["CONCEITO_ENADE_NUM"], errors="coerce").eq(1).sum()) == 0
    soure = base.loc[pd.to_numeric(base["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)]
    assert len(soure) == 1
    assert soure.iloc[0]["RECORTE_FOCAL"] == "Soure"
    assert len(sensibilidade) == 5
    assert (sensibilidade["N_CURSOS"] > 0).all()
    assert itens["ITEM"].nunique() == 47

    figuras = [
        ROOT / "figuras" / "biologia" / "validada_14_participacao_ufpa.png",
        ROOT / "figuras" / "biologia" / "validada_15_componentes_soure.png",
        ROOT / "figuras" / "biologia" / "validada_16_sensibilidade_benchmark_soure.png",
        ROOT / "figuras" / "biologia" / "validada_17_processo_itens_soure.png",
        ROOT / "figuras" / "biologia" / "validada_18_perfil_focal_soure.png",
        ROOT / "figuras" / "biologia" / "validada_19_recomendacao_soure.png",
    ]
    assert all(path.exists() and path.stat().st_size > 0 for path in figuras)
    assert (ROOT / "relatorios" / "sprint_11_validacao_biologia_soure.md").exists()
