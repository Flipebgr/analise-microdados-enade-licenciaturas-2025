from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path
from subprocess import CompletedProcess

from src.relatorios.resultado_relatorio import ResultadoConversaoPDF

ExecutorProcesso = Callable[..., CompletedProcess[str]]


def localizar_libreoffice() -> str | None:
    return shutil.which("libreoffice") or shutil.which("soffice")


def converter_docx_para_pdf(
    docx: Path,
    destino: Path | None = None,
    *,
    executavel: str | None = None,
    executor: ExecutorProcesso = subprocess.run,
    argumentos_adicionais: Sequence[str] = (),
) -> ResultadoConversaoPDF:
    docx = Path(docx)
    destino = Path(destino) if destino is not None else docx.parent

    if not docx.exists():
        return ResultadoConversaoPDF(
            gerado=False,
            caminho_pdf=None,
            returncode=None,
            mensagem=f"DOCX de origem não localizado: {docx}",
        )

    executavel = executavel or localizar_libreoffice()
    if not executavel:
        return ResultadoConversaoPDF(
            gerado=False,
            caminho_pdf=None,
            returncode=None,
            mensagem="LibreOffice não localizado; PDF não foi gerado.",
        )

    destino.mkdir(parents=True, exist_ok=True)
    comando = [
        executavel,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(destino),
        str(docx),
        *argumentos_adicionais,
    ]
    try:
        processo = executor(
            comando,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return ResultadoConversaoPDF(
            gerado=False,
            caminho_pdf=None,
            returncode=None,
            mensagem=f"Falha ao iniciar a conversão para PDF: {exc}",
            stderr=str(exc),
        )

    stderr = (processo.stderr or "").strip() or None
    candidato = destino / f"{docx.stem}.pdf"

    if processo.returncode != 0:
        return ResultadoConversaoPDF(
            gerado=False,
            caminho_pdf=None,
            returncode=processo.returncode,
            mensagem="LibreOffice retornou erro durante a conversão para PDF.",
            stderr=stderr,
        )

    if not candidato.exists() or candidato.stat().st_size == 0:
        return ResultadoConversaoPDF(
            gerado=False,
            caminho_pdf=None,
            returncode=processo.returncode,
            mensagem="O processo terminou sem produzir um PDF válido.",
            stderr=stderr,
        )

    return ResultadoConversaoPDF(
        gerado=True,
        caminho_pdf=candidato,
        returncode=processo.returncode,
        mensagem="PDF gerado com sucesso.",
        stderr=stderr,
    )
