from __future__ import annotations

from pathlib import Path

from docx import Document

SECOES_OBRIGATORIAS = (
    "1 INTRODUÇÃO",
    "2 REFERENCIAL INSTITUCIONAL E METODOLÓGICO",
    "3 METODOLOGIA",
    "4 PANORAMA DA LICENCIATURA EM LETRAS–INGLÊS",
    "5 RESULTADOS",
    "5.1 Desempenho",
    "5.2 Perfil demográfico e socioeconômico",
    "5.3 Trajetória e condições acadêmicas",
    "5.4 Processo formativo",
    "5.5 Recomendação",
    "5.6 Benchmark comparável",
    "5.7 Associações ecológicas",
    "5.8 Comparação regional e nacional",
    "6 DISCUSSÃO",
    "7 CONCLUSÃO",
    "REFERÊNCIAS",
    "APÊNDICE A – REGRAS DE INTEGRIDADE",
    "APÊNDICE B – APROFUNDAMENTOS SUGERIDOS",
)


def validar_relatorio(docx: Path, markdown: Path) -> None:
    if not docx.exists() or docx.stat().st_size == 0:
        raise ValueError("DOCX final de Letras–Inglês ausente ou vazio.")
    if not markdown.exists() or markdown.stat().st_size == 0:
        raise ValueError("Markdown final de Letras–Inglês ausente ou vazio.")

    doc = Document(docx)
    texto_docx = "\n".join(p.text for p in doc.paragraphs)
    texto_md = markdown.read_text(encoding="utf-8")
    for secao in SECOES_OBRIGATORIAS:
        if secao not in texto_docx:
            raise ValueError(f"Seção obrigatória ausente no DOCX: {secao}")
        marcador_md = secao.replace("–", "–")
        if marcador_md not in texto_md:
            raise ValueError(f"Seção obrigatória ausente no Markdown: {secao}")

    termos = (
        "CO_CURSO",
        "Conceito Enade 1",
        "one-to-one",
        "ecológica",
        "média ponderada",
        "Norte",
        "Brasil",
    )
    for termo in termos:
        if termo not in texto_md:
            raise ValueError(f"Restrição ou conceito metodológico ausente no Markdown: {termo}")
