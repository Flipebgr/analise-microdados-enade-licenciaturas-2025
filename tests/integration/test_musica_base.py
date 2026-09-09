from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_base_musica_quando_disponivel() -> None:
    pasta = ROOT / "dados_processados" / "musica"
    base_path = pasta / "base_analitica_cursos.csv"

    if not base_path.exists():
        pytest.skip("Base local de Música ainda não foi gerada.")

    base = pd.read_csv(base_path, low_memory=False)

    assert len(base) == 107
    assert base["CO_CURSO"].is_unique

    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 1
    assert set(ufpa["CO_CURSO"].astype(int)) == {114950}
    assert set(ufpa["CONCEITO_ENADE_NUM"].astype(int)) == {1}
    assert set(ufpa["GRUPO_CODIGO"]) == {"A"}

    contagem = base["GRUPO_CODIGO"].value_counts().to_dict()
    assert contagem == {"E": 98, "D": 8, "A": 1}

    auditoria = pd.read_csv(pasta / "auditoria_fontes_ufpa.csv")
    assert len(auditoria) == 1
    assert auditoria["STATUS_FONTES"].eq("Localizada nas duas fontes").all()

    benchmark = pd.read_csv(pasta / "benchmark_comparavel_resumo.csv")
    assert benchmark["CO_CURSO_ALVO"].astype(int).tolist() == [114950]
