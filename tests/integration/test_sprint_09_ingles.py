from __future__ import annotations

from pathlib import Path

from src.relatorios.gerar_relatorio_ingles import gerar_relatorio
from src.relatorios.validar_relatorio_ingles import validar_relatorio

ROOT = Path(__file__).resolve().parents[2]


def test_produtos_sprint_08_disponiveis():
    pasta = ROOT / "dados_processados" / "ingles"
    obrigatorios = [
        "cursos_ingles.csv",
        "base_analitica_cursos.csv",
        "comparacoes_regionais_validadas.csv",
        "sensibilidade_benchmarks.csv",
        "associacoes_ecologicas.csv",
        "tabela_socioeconomica_ufpa.csv",
        "itens_processo_formativo.csv",
        "diagnostico_consistencia_processo.csv",
        "distribuicao_recomendacao.csv",
        "auditoria_desempenho_sprint08.csv",
    ]
    for nome in obrigatorios:
        assert (pasta / nome).exists(), nome


def test_relatorio_final_ingles_gerado(tmp_path):
    docx = tmp_path / "relatorio.docx"
    markdown = tmp_path / "relatorio.md"
    saidas = gerar_relatorio(ROOT, docx, markdown)
    assert saidas["docx"].exists()
    assert saidas["markdown"].exists()
    validar_relatorio(docx, markdown)


def test_markdown_preserva_restricoes_metodologicas(tmp_path):
    docx = tmp_path / "relatorio.docx"
    markdown = tmp_path / "relatorio.md"
    gerar_relatorio(ROOT, docx, markdown)
    texto = markdown.read_text(encoding="utf-8")
    assert "CO_CURSO" in texto
    assert "one-to-one" in texto
    assert "Não foi usada posição de linha" in texto
    assert "ecológicas" in texto
    assert "Conceito 1" in texto
    assert "5.8 Comparação regional e nacional" in texto
    assert "média ponderada" in texto
    assert "aprofundamentos sugeridos" in texto.lower()
