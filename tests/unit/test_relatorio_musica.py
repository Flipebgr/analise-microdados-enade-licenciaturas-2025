from __future__ import annotations

from pathlib import Path


def test_gerador_relatorio_musica_existe() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / "src" / "relatorios" / "gerar_relatorio_musica.py").exists()
    assert (root / "scripts" / "pipelines" / "executar_musica_relatorio.py").exists()
