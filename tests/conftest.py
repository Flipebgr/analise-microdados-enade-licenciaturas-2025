from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def catalogo_minimo() -> pd.DataFrame:
    """Catálogo sintético, sem vínculo com registros reais do Enade."""
    return pd.DataFrame(
        {
            "CO_CURSO": [101, 102, 103],
            "CO_GRUPO": [6407, 6407, 6407],
            "CO_IES": [569, 569, 999],
            "UF": ["PA", "PA", "AM"],
            "CO_UF_CURSO": [15, 15, 13],
            "CO_REGIAO_CURSO": [1, 1, 1],
            "CONCEITO_ENADE": [1, pd.NA, 3],
        }
    )


@pytest.fixture
def tabela_agregada_valida() -> pd.DataFrame:
    """Tabela sintética já agregada, com uma linha por curso."""
    return pd.DataFrame(
        {
            "CO_CURSO": [101, 102, 103],
            "nt_ger_mean": [40.0, 50.0, 60.0],
            "nt_ger_count": [10, 20, 30],
        }
    )


@pytest.fixture
def pasta_raiz_projeto() -> Path:
    return Path(__file__).resolve().parents[1]


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Marca automaticamente testes localizados em tests/integration."""
    for item in items:
        caminho = Path(str(item.path))
        if "integration" in caminho.parts:
            item.add_marker(pytest.mark.integration)
