from __future__ import annotations

import logging

from src.relatorios.resultado_relatorio import ResultadoConversaoPDF


def registrar_resultado_pdf(logger: logging.Logger, resultado: ResultadoConversaoPDF) -> None:
    if resultado.gerado and resultado.caminho_pdf is not None:
        logger.info("PDF gerado: %s", resultado.caminho_pdf)
        return

    if resultado.stderr:
        logger.warning("%s stderr=%s", resultado.mensagem, resultado.stderr)
    else:
        logger.warning(resultado.mensagem)
