from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ResultadoConversaoPDF:
    gerado: bool
    caminho_pdf: Path | None
    returncode: int | None
    mensagem: str
    stderr: str | None = None


@dataclass(frozen=True, slots=True)
class ResultadoRelatorio:
    docx: Path
    markdown: Path
    conversao_pdf: ResultadoConversaoPDF

    @property
    def pdf(self) -> Path | None:
        return self.conversao_pdf.caminho_pdf

    def como_dict(self) -> dict[str, Path | ResultadoConversaoPDF | None]:
        return {
            "docx": self.docx,
            "markdown": self.markdown,
            "pdf": self.pdf,
            "conversao_pdf": self.conversao_pdf,
        }
