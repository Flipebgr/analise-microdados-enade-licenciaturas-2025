from __future__ import annotations

import pytest

from src.configuracao.caminhos import ROOT
from src.relatorios.validar_relatorio_geografia import validar_relatorio

pytestmark = pytest.mark.integration


def test_relatorio_final_geografia_quando_disponivel() -> None:
    pasta_dados = ROOT / "dados_processados" / "geografia"
    base = pasta_dados / "base_analitica_cursos.csv"
    if not base.exists():
        pytest.skip("Produtos locais das Sprints 19 e 20 não disponíveis.")

    pasta = ROOT / "relatorios" / "geografia"
    docx = pasta / "relatorio_geografia_enade_2025_ufpa.docx"
    markdown = pasta / "relatorio_geografia_enade_2025_ufpa.md"
    if not docx.exists() or not markdown.exists():
        pytest.skip("Relatório final da Sprint 21 ainda não foi executado.")

    validar_relatorio(docx, markdown)
