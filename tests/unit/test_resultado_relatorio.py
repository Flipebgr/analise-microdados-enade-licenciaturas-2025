from pathlib import Path

from src.relatorios.resultado_relatorio import ResultadoConversaoPDF, ResultadoRelatorio


def test_resultado_relatorio_mantem_compatibilidade_com_dict(tmp_path: Path):
    pdf = tmp_path / "relatorio.pdf"
    conversao = ResultadoConversaoPDF(True, pdf, 0, "PDF gerado com sucesso.")
    resultado = ResultadoRelatorio(
        docx=tmp_path / "relatorio.docx",
        markdown=tmp_path / "relatorio.md",
        conversao_pdf=conversao,
    )

    saidas = resultado.como_dict()

    assert saidas["docx"] == resultado.docx
    assert saidas["markdown"] == resultado.markdown
    assert saidas["pdf"] == pdf
    assert saidas["conversao_pdf"] == conversao
