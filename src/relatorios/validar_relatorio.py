from __future__ import annotations

from pathlib import Path

from docx import Document

CAPITULOS = ["1 INTRODUÇÃO", "2 REFERENCIAL INSTITUCIONAL E METODOLÓGICO", "3 METODOLOGIA", "4 PANORAMA DA LICENCIATURA EM MATEMÁTICA", "5 RESULTADOS", "6 DISCUSSÃO", "7 CONCLUSÃO", "REFERÊNCIAS"]


def validar_docx(caminho: Path) -> list[str]:
    erros: list[str] = []
    if not caminho.exists() or caminho.stat().st_size == 0:
        return ["DOCX não gerado ou vazio"]
    doc = Document(caminho)
    texto = "\n".join(p.text for p in doc.paragraphs)
    for cap in CAPITULOS:
        if cap not in texto:
            erros.append(f"Capítulo ausente: {cap}")
    if len(doc.inline_shapes) < 5:
        erros.append("Relatório contém menos de cinco figuras incorporadas")
    if len(doc.tables) < 4:
        erros.append("Relatório contém menos de quatro tabelas")
    if "C:\\Users\\" in texto or "/mnt/data/" in texto:
        erros.append("Caminho absoluto encontrado no relatório")
    return erros
