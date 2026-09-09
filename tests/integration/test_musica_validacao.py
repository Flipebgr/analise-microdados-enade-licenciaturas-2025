from __future__ import annotations

import pandas as pd
import pytest

from src.configuracao.caminhos import ROOT

pytestmark = pytest.mark.integration


def test_produtos_validacao_musica() -> None:
    pasta = ROOT / "dados_processados" / "musica"
    esperado = [
        "base_analitica_validada.csv",
        "catalogo_itens_processo_formativo.csv",
        "consistencia_dimensoes_processo.csv",
        "benchmark_sensibilidade_resumo.csv",
        "associacoes_ecologicas.csv",
        "associacoes_ecologicas_diagnostico.csv",
        "validacao_analitica.csv",
    ]
    ausentes = [nome for nome in esperado if not (pasta / nome).exists()]
    if ausentes:
        pytest.skip(
            "Produtos locais da validação ainda não foram gerados: "
            + ", ".join(ausentes)
        )

    base = pd.read_csv(pasta / "base_analitica_validada.csv")
    assert len(base) == 107
    assert base["CO_CURSO"].is_unique

    ufpa = base[base["CO_IES"].eq(569)]
    assert len(ufpa) == 1
    assert set(ufpa["CO_CURSO"].astype(int)) == {114950}
    assert set(ufpa["CONCEITO_ENADE_NUM"].astype(int)) == {1}
    assert set(ufpa["GRUPO_CODIGO"]) == {"A"}

    validacao = pd.read_csv(pasta / "validacao_analitica.csv")
    assert validacao["APROVADO"].all()

    figuras = list((ROOT / "figuras" / "musica").glob("*.png"))
    assert len(figuras) >= 10
