from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT
from src.portugues.validar_portugues import (
    validar_auditoria_relacao,
    validar_base_portugues,
)


@pytest.mark.integration
def test_produtos_sprint_16_portugues_quando_disponiveis():
    pasta = ROOT / "dados_processados" / "portugues"
    base_path = pasta / "base_analitica_cursos.csv"
    auditoria_path = pasta / "auditoria_relacao_ufpa.csv"
    if not base_path.exists() or not auditoria_path.exists():
        pytest.skip("Produtos locais da Sprint 16 ainda não foram executados.")

    base = pd.read_csv(base_path, low_memory=False)
    auditoria = pd.read_csv(auditoria_path, low_memory=False)
    validar_base_portugues(base)
    validar_auditoria_relacao(auditoria)

    assert len(base) == 340
    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 8
    assert int(ufpa["CONCEITO_ENADE_NUM"].eq(1).sum()) == 1
    assert not ufpa["MUNICIPIO"].astype("string").str.casefold().eq("soure").any()
