from __future__ import annotations

from pathlib import Path
import pytest

pytestmark = pytest.mark.integration


def test_produtos_relatorio_musica_quando_disponiveis() -> None:
    root = Path(__file__).resolve().parents[2]
    pasta = root / "relatorios" / "musica"
    docx = pasta / "relatorio_musica_enade_2025_ufpa.docx"
    md = pasta / "relatorio_musica_enade_2025_ufpa.md"
    if not docx.exists() or not md.exists():
        pytest.skip("Relatório local de Música ainda não foi gerado.")
    assert docx.stat().st_size > 100_000
    texto = md.read_text(encoding="utf-8")
    assert "# 5 RESULTADOS" in texto
    assert "## 5.7 Associações ecológicas" in texto
    assert "# 7 CONCLUSÃO" in texto
