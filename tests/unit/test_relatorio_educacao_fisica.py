from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.relatorios.gerar_relatorio_educacao_fisica import (
    carregar_produtos,
    tabela_benchmark,
    tabela_ofertas,
)

ROOT = Path(__file__).resolve().parents[2]


def test_ofertas_ufpa_contrato():
    pasta = ROOT / "dados_processados" / "educacao_fisica"
    if not (pasta / "base_analitica_validada.csv").exists():
        return
    produtos = carregar_produtos(ROOT)
    ofertas = tabela_ofertas(produtos["base"])
    assert len(ofertas) == 2
    assert set(ofertas["Conceito"].dropna().astype(int)) == {4}


def test_benchmark_principal_duas_ofertas():
    pasta = ROOT / "dados_processados" / "educacao_fisica"
    if not (pasta / "benchmark_sensibilidade_resumo.csv").exists():
        return
    produtos = carregar_produtos(ROOT)
    tab = tabela_benchmark(produtos["benchmark"])
    assert len(tab) == 2
    assert set(pd.to_numeric(tab["N comparáveis"])) == {9, 24}
