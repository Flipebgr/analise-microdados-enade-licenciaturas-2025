from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_produtos_sprint20_geografia_quando_disponiveis() -> None:
    pasta = ROOT / "dados_processados" / "geografia"
    base_path = pasta / "base_analitica_cursos.csv"
    if not base_path.exists():
        pytest.skip("Produtos locais da Sprint 19 não disponíveis.")

    base = pd.read_csv(base_path, low_memory=False)
    assert len(base) == 254
    assert base["CO_CURSO"].is_unique

    ufpa = base.loc[base["CO_IES"].eq(569)]
    assert len(ufpa) == 4
    assert set(ufpa["CONCEITO_ENADE_NUM"].astype(int)) == {3, 4}

    pasta20 = [
        "auditoria_desempenho_sprint20.csv",
        "auditoria_indicadores_sprint20.csv",
        "comparacoes_regionais_validadas_sprint20.csv",
        "sensibilidade_benchmarks_sprint20.csv",
        "membros_benchmarks_sprint20.csv",
        "contraste_interno_ufpa_validado_sprint20.csv",
        "perfil_recortes_validado_sprint20.csv",
        "processo_formativo_grupos_validado_sprint20.csv",
        "recomendacao_recortes_validada_sprint20.csv",
        "diagnostico_outliers_sprint20.csv",
        "associacoes_ecologicas_sprint20.csv",
    ]
    for nome in pasta20:
        assert (pasta / nome).exists(), nome

    sens = pd.read_csv(
        pasta / "sensibilidade_benchmarks_sprint20.csv",
        low_memory=False,
    )
    assert len(sens) == 20

    processo = pd.read_csv(
        pasta / "processo_formativo_grupos_validado_sprint20.csv",
        low_memory=False,
    )
    assert processo["ITEM"].nunique() == 47

    figuras = ROOT / "figuras" / "geografia"
    for n in range(14, 20):
        assert list(figuras.glob(f"validada_{n:02d}_*.png"))

