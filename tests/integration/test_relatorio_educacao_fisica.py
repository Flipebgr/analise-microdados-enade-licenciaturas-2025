from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration
ROOT = Path(__file__).resolve().parents[2]


def test_relatorio_final_educacao_fisica():
    pasta = ROOT / "relatorios" / "educacao_fisica"
    docx = pasta / "relatorio_educacao_fisica_enade_2025_ufpa.docx"
    md = pasta / "relatorio_educacao_fisica_enade_2025_ufpa.md"
    if not docx.exists() or not md.exists():
        pytest.skip("Relatório final local ainda não foi gerado.")
    assert docx.stat().st_size > 100_000
    texto = md.read_text(encoding="utf-8")
    assert "406 cursos" in texto
    assert "Conceito Enade 4" in texto
    assert "Conceito Enade 1" in texto
