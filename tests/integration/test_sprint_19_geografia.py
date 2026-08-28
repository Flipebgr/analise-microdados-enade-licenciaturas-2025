from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_produtos_sprint_19_geografia_quando_disponiveis() -> None:
    pasta = ROOT / "dados_processados" / "geografia"
    base_path = pasta / "base_analitica_cursos.csv"
    if not base_path.exists():
        pytest.skip("Produtos locais da Sprint 19 de Geografia ainda não foram gerados.")

    base = pd.read_csv(base_path, low_memory=False)
    assert base["CO_CURSO"].is_unique
    assert len(base) == 254

    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 4
    assert int(ufpa["CONCEITO_ENADE_NUM"].eq(1).sum()) == 0
    assert set(ufpa["CONCEITO_ENADE_NUM"].astype(int)) == {3, 4}

    esperados = {11991, 12052, 1194057, 1330343}
    assert set(ufpa["CO_CURSO"].astype(int)) == esperados

    auditoria = pd.read_csv(pasta / "auditoria_fontes_ufpa.csv")
    assert len(auditoria) == 4
    assert auditoria["STATUS_FONTES"].eq("Localizada nas duas fontes").all()

    resumo = pd.read_csv(pasta / "benchmark_comparavel_resumo.csv")
    assert len(resumo) == 4

    assert (pasta / "tabela_mestra_ufpa.csv").exists()
    assert (pasta / "comparacao_interna_ufpa.csv").exists()
    assert (pasta / "comparacoes_regionais_nacionais.csv").exists()

    figuras = list((ROOT / "figuras" / "geografia").glob("*.png"))
    assert len(figuras) >= 13
    assert all(path.stat().st_size > 0 for path in figuras)
    assert (ROOT / "relatorios" / "sprint_19_piloto_geografia.md").exists()
