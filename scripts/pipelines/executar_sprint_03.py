from __future__ import annotations

from src.configuracao.caminhos import ROOT
from src.relatorios.conversao_pdf import converter_docx_para_pdf
from src.relatorios.gerar_relatorio_matematica import gerar_relatorio
from src.relatorios.utilitarios_relatorio import registrar_resultado_pdf
from src.relatorios.validar_relatorio import validar_docx
from src.utilitarios.logs import configurar_logger



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
    resultado_pdf = converter_docx_para_pdf(docx, saida)
    registrar_resultado_pdf(logger, resultado_pdf)
    logger.info("Sprint 3 concluída: DOCX, Markdown e PDF (quando LibreOffice disponível)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
