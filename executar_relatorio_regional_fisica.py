from __future__ import annotations

import logging
from pathlib import Path

from src.relatorios.gerar_relatorio_regional_fisica import executar


ROOT = Path(__file__).resolve().parent


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    logger = logging.getLogger("relatorio_regional_fisica")
    logger.info("Carregando base analítica de Física")
    saidas = executar(ROOT)
    logger.info("DOCX gerado: %s", saidas["docx"])
    logger.info("Markdown gerado: %s", saidas["markdown"])
    logger.info("Relatório regional concluído: 6 figuras e 4 tabelas derivadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
