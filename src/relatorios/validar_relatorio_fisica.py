from __future__ import annotations

from pathlib import Path

SECOES = [
    "1 INTRODUÇÃO", "2 REFERENCIAL INSTITUCIONAL E METODOLÓGICO", "3 METODOLOGIA",
    "4 PANORAMA DA LICENCIATURA EM FÍSICA", "5 RESULTADOS", "5.1 Desempenho",
    "5.2 Perfil demográfico e socioeconômico", "5.3 Trajetória e condições acadêmicas",
    "5.4 Processo formativo", "5.5 Recomendação", "5.6 Benchmark comparável",
    "5.7 Associações ecológicas", "6 DISCUSSÃO", "7 CONCLUSÃO", "REFERÊNCIAS",
    "APÊNDICES",
]


def validar_relatorio(docx: Path, md: Path) -> None:
    if not docx.exists() or docx.stat().st_size < 20_000:
        raise ValueError("Relatório DOCX ausente ou vazio")
    if not md.exists() or md.stat().st_size < 5_000:
        raise ValueError("Relatório Markdown ausente ou vazio")
    texto = md.read_text(encoding="utf-8")
    ausentes = [secao for secao in SECOES if secao not in texto]
    if ausentes:
        raise ValueError(f"Seções ausentes: {ausentes}")
    if "Tucuruí" not in texto or "não foi" not in texto:
        raise ValueError("Situação de Tucuruí não documentada")
    if "CO_CURSO" not in texto or "ecológica" not in texto:
        raise ValueError("Restrições metodológicas não documentadas")
