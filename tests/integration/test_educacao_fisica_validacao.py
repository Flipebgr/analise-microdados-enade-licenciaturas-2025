from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]


def test_produtos_validacao_educacao_fisica():
    pasta = ROOT / "dados_processados" / "educacao_fisica"
    esperado = [
        "base_analitica_validada.csv",
        "catalogo_itens_processo_formativo.csv",
        "consistencia_dimensoes_processo.csv",
        "benchmark_sensibilidade_resumo.csv",
        "associacoes_ecologicas.csv",
        "validacao_analitica.csv",
    ]
    ausentes = [nome for nome in esperado if not (pasta / nome).exists()]
    if ausentes:
        pytest.skip(
            "Produtos locais da validação ainda não foram gerados: "
            + ", ".join(ausentes)
        )

    base = pd.read_csv(pasta / "base_analitica_validada.csv")
    assert len(base) == 406
    assert base["CO_CURSO"].is_unique
    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 2
    assert set(ufpa["CONCEITO_ENADE_NUM"].dropna()) == {4.0}

    validacao = pd.read_csv(pasta / "validacao_analitica.csv")
    assert validacao["APROVADO"].all()

    figuras = list((ROOT / "figuras" / "educacao_fisica").glob("*.png"))
    assert len(figuras) >= 10
