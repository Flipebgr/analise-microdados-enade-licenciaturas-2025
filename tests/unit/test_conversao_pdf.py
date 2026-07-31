from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess

from src.relatorios import conversao_pdf
from src.relatorios.conversao_pdf import converter_docx_para_pdf


def test_docx_inexistente_retorna_resultado_estruturado(tmp_path: Path):
    resultado = converter_docx_para_pdf(tmp_path / "ausente.docx", executavel="soffice")

    assert resultado.gerado is False
    assert resultado.caminho_pdf is None
    assert resultado.returncode is None
    assert "não localizado" in resultado.mensagem


def test_libreoffice_ausente_nao_interrompe_pipeline(tmp_path: Path, monkeypatch):
    docx = tmp_path / "relatorio.docx"
    docx.write_bytes(b"docx")

    monkeypatch.setattr(conversao_pdf, "localizar_libreoffice", lambda: None)
    resultado = converter_docx_para_pdf(docx, executavel=None)

    assert resultado.gerado is False
    assert resultado.caminho_pdf is None
    assert "LibreOffice não localizado" in resultado.mensagem


def test_conversao_bem_sucedida(tmp_path: Path):
    docx = tmp_path / "relatorio.docx"
    docx.write_bytes(b"docx")

    def executor(comando, **kwargs):
        destino = Path(comando[comando.index("--outdir") + 1])
        (destino / "relatorio.pdf").write_bytes(b"pdf")
        return CompletedProcess(comando, 0, stdout="ok", stderr="")

    resultado = converter_docx_para_pdf(docx, executavel="soffice", executor=executor)

    assert resultado.gerado is True
    assert resultado.caminho_pdf == tmp_path / "relatorio.pdf"
    assert resultado.returncode == 0


def test_retorno_de_erro_preserva_stderr(tmp_path: Path):
    docx = tmp_path / "relatorio.docx"
    docx.write_bytes(b"docx")

    def executor(comando, **kwargs):
        return CompletedProcess(comando, 7, stdout="", stderr="falha simulada")

    resultado = converter_docx_para_pdf(docx, executavel="soffice", executor=executor)

    assert resultado.gerado is False
    assert resultado.returncode == 7
    assert resultado.stderr == "falha simulada"
    assert "retornou erro" in resultado.mensagem


def test_processo_sem_pdf_e_reportado(tmp_path: Path):
    docx = tmp_path / "relatorio.docx"
    docx.write_bytes(b"docx")

    def executor(comando, **kwargs):
        return CompletedProcess(comando, 0, stdout="ok", stderr="")

    resultado = converter_docx_para_pdf(docx, executavel="soffice", executor=executor)

    assert resultado.gerado is False
    assert resultado.returncode == 0
    assert "sem produzir um PDF válido" in resultado.mensagem


def test_falha_ao_iniciar_processo_e_reportada(tmp_path: Path):
    docx = tmp_path / "relatorio.docx"
    docx.write_bytes(b"docx")

    def executor(comando, **kwargs):
        raise OSError("executável indisponível")

    resultado = converter_docx_para_pdf(docx, executavel="soffice", executor=executor)

    assert resultado.gerado is False
    assert resultado.returncode is None
    assert resultado.stderr == "executável indisponível"
