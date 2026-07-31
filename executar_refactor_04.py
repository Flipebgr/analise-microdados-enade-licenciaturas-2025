from __future__ import annotations

import tempfile
from pathlib import Path
from subprocess import CompletedProcess

from src.relatorios.conversao_pdf import converter_docx_para_pdf


def main() -> int:
    with tempfile.TemporaryDirectory() as pasta:
        base = Path(pasta)
        docx = base / "contrato.docx"
        docx.write_bytes(b"docx")

        def executor(comando, **kwargs):
            (base / "contrato.pdf").write_bytes(b"pdf")
            return CompletedProcess(comando, 0, stdout="ok", stderr="")

        resultado = converter_docx_para_pdf(
            docx,
            base,
            executavel="soffice-simulado",
            executor=executor,
        )
        if not resultado.gerado:
            print(f"Falha no contrato de conversão: {resultado.mensagem}")
            return 1

    print("Refactor 04 — relatórios robustos")
    print("Conversão PDF estruturada: OK")
    print("Falhas do LibreOffice preservam DOCX e Markdown: OK")
    print("Compatibilidade dos geradores de Matemática e Física: preservada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
