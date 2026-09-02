from __future__ import annotations

import logging

from src.configuracao.caminhos import ROOT
from src.relatorios.gerar_relatorio_biologia import gerar_relatorio
from src.relatorios.utilitarios_relatorio import registrar_resultado_pdf
from src.relatorios.validar_relatorio_biologia import validar_relatorio


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger = logging.getLogger("sprint_12")
    logger.info("Carregando produtos validados das Sprints 10 e 11")

    pasta = ROOT / "relatorios" / "biologia"
    docx = pasta / "relatorio_ciencias_biologicas_enade_2025_soure.docx"
    markdown = pasta / "relatorio_ciencias_biologicas_enade_2025_soure.md"

    saidas = gerar_relatorio(ROOT, docx, markdown)
    validar_relatorio(docx, markdown)

    logger.info("DOCX gerado: %s", saidas["docx"])
    logger.info("Markdown gerado: %s", saidas["markdown"])
    registrar_resultado_pdf(logger, saidas["conversao_pdf"])
    logger.info("Sprint 12 concluída")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
