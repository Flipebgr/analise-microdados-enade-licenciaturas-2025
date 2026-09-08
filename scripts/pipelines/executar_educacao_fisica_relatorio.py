from __future__ import annotations

# ruff: noqa: E402

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.relatorios.gerar_relatorio_educacao_fisica import gerar_relatorio


def main() -> int:
    resultado = gerar_relatorio(PROJECT_ROOT)
    print(f"DOCX: {resultado.docx}")
    print(f"Markdown: {resultado.markdown}")
    if resultado.conversao_pdf.gerado:
        print(f"PDF:  {resultado.pdf}")
    else:
        print(f"PDF não gerado: {resultado.conversao_pdf.mensagem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
