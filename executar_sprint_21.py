from __future__ import annotations

import logging

from src.configuracao.caminhos import ROOT
from src.relatorios.gerar_relatorio_geografia import gerar_relatorio
from src.relatorios.utilitarios_relatorio import registrar_resultado_pdf
from src.relatorios.validar_relatorio_geografia import validar_relatorio


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger = logging.getLogger("sprint_21")
    logger.info("Carregando produtos validados das Sprints 19 e 20")

    pasta = ROOT / "relatorios" / "geografia"
    docx = pasta / "relatorio_geografia_enade_2025_ufpa.docx"
    markdown = pasta / "relatorio_geografia_enade_2025_ufpa.md"

    saidas = gerar_relatorio(ROOT, docx, markdown)
    validar_relatorio(docx, markdown)

    logger.info("DOCX gerado: %s", saidas["docx"])
    logger.info("Markdown gerado: %s", saidas["markdown"])
    registrar_resultado_pdf(logger, saidas["conversao_pdf"])
    logger.info("Sprint 21 concluída")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
