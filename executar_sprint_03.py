from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from src.configuracao.caminhos import ROOT
from src.relatorios.gerar_relatorio_matematica import gerar_relatorio
from src.relatorios.validar_relatorio import validar_docx
from src.utilitarios.logs import configurar_logger


def converter_pdf(docx: Path, destino: Path, logger) -> None:
    exe = shutil.which("libreoffice") or shutil.which("soffice")
    if not exe:
        logger.warning("LibreOffice não localizado; PDF não foi gerado. O DOCX permanece disponível.")
        return
    destino.mkdir(parents=True, exist_ok=True)
    subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", str(destino), str(docx)], check=True)


def main() -> int:
    logger = configurar_logger(ROOT / "logs" / "sprint_03.log")
    logger.info("Gerando relatório técnico-científico de Matemática")
    saida = ROOT / "relatorios" / "matematica"
    docx = saida / "relatorio_matematica_enade_2025.docx"
    md = saida / "relatorio_matematica_enade_2025.md"
    gerar_relatorio(ROOT, docx, md, {"instituicao": "UNIVERSIDADE FEDERAL DO PARÁ", "cidade": "Belém"})
    erros = validar_docx(docx)
    if erros:
        for erro in erros:
            logger.error(erro)
        return 1
    converter_pdf(docx, saida, logger)
    logger.info("Sprint 3 concluída: DOCX, Markdown e PDF (quando LibreOffice disponível)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
