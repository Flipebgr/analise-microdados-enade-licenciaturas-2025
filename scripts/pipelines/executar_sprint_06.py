from __future__ import annotations

import logging
from pathlib import Path

from src.relatorios.gerar_relatorio_fisica import gerar_relatorio
from src.relatorios.utilitarios_relatorio import registrar_resultado_pdf

ROOT = Path(__file__).resolve().parent


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    logger = logging.getLogger("sprint_06")
    logger.info("Carregando produtos validados das Sprints 4 e 5")
    saidas = gerar_relatorio(
        ROOT,
        ROOT / "relatorios" / "fisica" / "relatorio_fisica_enade_2025.docx",
        ROOT / "relatorios" / "fisica" / "relatorio_fisica_enade_2025.md",
    )
    logger.info("DOCX gerado: %s", saidas["docx"])
    logger.info("Markdown gerado: %s", saidas["markdown"])
    registrar_resultado_pdf(logger, saidas["conversao_pdf"])
    logger.info("Sprint 6 concluída")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
