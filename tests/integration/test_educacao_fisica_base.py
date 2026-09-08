from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_base_educacao_fisica_quando_disponivel() -> None:
    pasta = ROOT / "dados_processados" / "educacao_fisica"
    base_path = pasta / "base_analitica_cursos.csv"

    if not base_path.exists():
        pytest.skip(
            "Base local de Educação Física ainda não foi gerada."
        )

    base = pd.read_csv(base_path, low_memory=False)

    assert len(base) == 406
    assert base["CO_CURSO"].is_unique

    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 2
    assert set(ufpa["CO_CURSO"].astype(int)) == {21849, 104598}
    assert set(ufpa["CONCEITO_ENADE_NUM"].astype(int)) == {4}
    assert set(ufpa["GRUPO_CODIGO"]) == {"B"}

    contagem = base["GRUPO_CODIGO"].value_counts().to_dict()
    assert contagem == {
        "E": 382,
        "D": 17,
        "C": 5,
        "B": 2,
    }

    auditoria = pd.read_csv(
        pasta / "auditoria_fontes_ufpa.csv"
    )
    assert len(auditoria) == 2
    assert auditoria["STATUS_FONTES"].eq(
        "Localizada nas duas fontes"
    ).all()

    benchmark = pd.read_csv(
        pasta / "benchmark_comparavel_resumo.csv"
    )
    assert set(benchmark["CO_CURSO_ALVO"].astype(int)) == {
        21849,
        104598,
    }
    assert benchmark["N_CURSOS_COMPARAVEIS"].gt(0).all()
