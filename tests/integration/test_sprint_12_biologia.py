from __future__ import annotations

from pathlib import Path

from src.relatorios.gerar_relatorio_biologia import gerar_relatorio
from src.relatorios.validar_relatorio_biologia import validar_relatorio

ROOT = Path(__file__).resolve().parents[2]


def test_produtos_sprints_10_11_disponiveis():
    pasta = ROOT / "dados_processados" / "biologia"
    obrigatorios = [
        "cursos_biologia.csv",
        "base_analitica_cursos.csv",
        "comparacoes_regionais_validadas_sprint11.csv",
        "benchmark_soure_cursos.csv",
        "benchmark_soure_resumo.csv",
        "sensibilidade_benchmark_soure.csv",
        "percentis_soure.csv",
        "perfil_focal_soure_validado.csv",
        "processo_formativo_soure_itens_validado.csv",
        "desempenho_individual_soure_descritivas.csv",
        "desempenho_individual_soure_correlacoes.csv",
        "associacoes_ecologicas_sprint11.csv",
        "auditoria_desempenho_sprint11.csv",
    ]
    for nome in obrigatorios:
        assert (pasta / nome).exists(), nome


def test_relatorio_final_biologia_gerado(tmp_path):
    docx = tmp_path / "relatorio.docx"
    markdown = tmp_path / "relatorio.md"
    saidas = gerar_relatorio(ROOT, docx, markdown)
    assert saidas["docx"].exists()
    assert saidas["markdown"].exists()
    validar_relatorio(docx, markdown)


def test_markdown_preserva_estudo_focal_e_restricoes(tmp_path):
    docx = tmp_path / "relatorio.docx"
    markdown = tmp_path / "relatorio.md"
    gerar_relatorio(ROOT, docx, markdown)
    texto = markdown.read_text(encoding="utf-8")
    assert "CO_CURSO" in texto
    assert "one-to-one" in texto
    assert "Soure" in texto
    assert "104640" in texto
    assert "não existe oferta da UFPA com Conceito Enade 1" in texto
    assert "5.9 Estudo focal da oferta de Soure" in texto
    assert "5.9.7 Síntese dos pontos distintivos" in texto
    assert "média ponderada" in texto
    assert "associação ecológica" in texto
    assert "APÊNDICE C" in texto
    assert "extensão universitária" in texto
