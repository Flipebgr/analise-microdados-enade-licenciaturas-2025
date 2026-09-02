from __future__ import annotations

from pathlib import Path

import pytest

from executar import resolver_scripts

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]


def test_executor_de_validacao_de_fontes_permanece_operacional() -> None:
    scripts = resolver_scripts("fontes", None)
    assert len(scripts) == 1
    assert scripts[0].name == "executar_sprint_00.py"
    assert scripts[0].exists()


def test_fontes_brutas_quando_disponiveis() -> None:
    zip_microdados = ROOT / "dados_brutos" / "microdados_enade_licenciaturas_2025.zip"
    conceito = ROOT / "dados_brutos" / "conceito_enade_licenciaturas.xlsx"

    if not zip_microdados.exists() or not conceito.exists():
        pytest.skip("Fontes brutas locais não estão disponíveis neste computador.")

    assert zip_microdados.stat().st_size > 0
    assert conceito.stat().st_size > 0
