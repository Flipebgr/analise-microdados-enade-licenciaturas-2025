from __future__ import annotations

import logging

from src.configuracao.caminhos import ROOT
from src.relatorios.gerar_relatorio_ingles import gerar_relatorio
from src.relatorios.utilitarios_relatorio import registrar_resultado_pdf
from src.relatorios.validar_relatorio_ingles import validar_relatorio


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    logger = logging.getLogger("sprint_09")
    logger.info("Carregando produtos validados das Sprints 07 e 08")
    pasta = ROOT / "relatorios" / "ingles"
    docx = pasta / "relatorio_letras_ingles_enade_2025.docx"
    markdown = pasta / "relatorio_letras_ingles_enade_2025.md"
    saidas = gerar_relatorio(ROOT, docx, markdown)
    validar_relatorio(docx, markdown)
    logger.info("DOCX gerado: %s", saidas["docx"])
    logger.info("Markdown gerado: %s", saidas["markdown"])
    registrar_resultado_pdf(logger, saidas["conversao_pdf"])
    logger.info("Sprint 9 concluída")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
