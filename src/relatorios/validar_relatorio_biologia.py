from __future__ import annotations

from pathlib import Path

from docx import Document

SECOES_OBRIGATORIAS = (
    "1 INTRODUÇÃO",
    "2 REFERENCIAL INSTITUCIONAL E METODOLÓGICO",
    "3 METODOLOGIA",
    "4 PANORAMA DE CIÊNCIAS BIOLÓGICAS",
    "5 RESULTADOS",
    "5.1 Desempenho",
    "5.2 Perfil demográfico e socioeconômico",
    "5.3 Trajetória e condições acadêmicas",
    "5.4 Processo formativo",
    "5.5 Recomendação",
    "5.6 Benchmark comparável",
    "5.7 Associações ecológicas",
    "5.8 Comparação regional e nacional",
    "5.9 Estudo focal da oferta de Soure",
    "5.9.1 Participação e desempenho",
    "5.9.2 Perfil discente",
    "5.9.3 Trajetória acadêmica",
    "5.9.4 Processo formativo",
    "5.9.5 Recomendação",
    "5.9.6 Benchmark comparável",
    "5.9.7 Síntese dos pontos distintivos",
    "6 DISCUSSÃO",
    "7 CONCLUSÃO",
    "REFERÊNCIAS",
    "APÊNDICE A – REGRAS DE INTEGRIDADE",
    "APÊNDICE B – APROFUNDAMENTOS SUGERIDOS",
    "APÊNDICE C – RÓTULOS OFICIAIS DOS ITENS QE_I20–QE_I66",
)


def validar_relatorio(docx: Path, markdown: Path) -> None:
    if not docx.exists() or docx.stat().st_size == 0:
        raise ValueError("DOCX final de Ciências Biológicas ausente ou vazio.")
    if not markdown.exists() or markdown.stat().st_size == 0:
        raise ValueError("Markdown final de Ciências Biológicas ausente ou vazio.")

    doc = Document(docx)
    texto_docx = "\n".join(p.text for p in doc.paragraphs)
    texto_md = markdown.read_text(encoding="utf-8")

    for secao in SECOES_OBRIGATORIAS:
        if secao not in texto_docx:
            raise ValueError(f"Seção obrigatória ausente no DOCX: {secao}")
        if secao not in texto_md:
            raise ValueError(f"Seção obrigatória ausente no Markdown: {secao}")

    termos = (
    "CO_CURSO",
    "one-to-one",
    "Soure",
    "104640",
    "associação ecológica",
    "média ponderada",
    "Norte",
    "Brasil",
    "não existe oferta da UFPA com Conceito Enade 1",
    "QE_I20",
    "textos oficiais",
    "não causal",
    )
    for termo in termos:
        if termo.lower() not in texto_md.lower():
            raise ValueError(
                f"Restrição ou conceito metodológico ausente no Markdown: {termo}"
            )
