from __future__ import annotations

from pathlib import Path

import pytest

from src.configuracao.caminhos import ROOT
from src.relatorios.gerar_relatorio_pedagogia import gerar_relatorio
from src.relatorios.validar_relatorio_pedagogia import validar_relatorio


@pytest.mark.integration
def test_sprint_15_gera_relatorio_final_pedagogia(tmp_path: Path):
    base = ROOT / "dados_processados" / "pedagogia" / "base_analitica_cursos.csv"
    if not base.exists():
        pytest.skip("Produtos locais das Sprints 13 e 14 não disponíveis.")

    pasta = tmp_path / "pedagogia"
    docx = pasta / "relatorio_pedagogia_enade_2025_ufpa.docx"
    md = pasta / "relatorio_pedagogia_enade_2025_ufpa.md"

    saidas = gerar_relatorio(ROOT, docx, md)
    validar_relatorio(docx, md)

    assert saidas["docx"].exists()
    assert saidas["markdown"].exists()
    texto = md.read_text(encoding="utf-8")
    assert "1200 cursos" in texto
    assert "7 ofertas" in texto
    assert "Castanhal" in texto
    assert "Conceito Enade 1" in texto
    assert "APÊNDICE B – APROFUNDAMENTOS SUGERIDOS" in texto
