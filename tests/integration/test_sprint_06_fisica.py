from pathlib import Path

from src.relatorios.gerar_relatorio_fisica import gerar_relatorio
from src.relatorios.validar_relatorio_fisica import validar_relatorio

ROOT = Path(__file__).resolve().parents[2]


def test_produtos_sprint_05_disponiveis():
    p = ROOT / "dados_processados" / "fisica"
    for nome in [
        "base_analitica_cursos.csv", "auditoria_presenca_validada.csv",
        "comparacao_territorial_validada.csv", "sensibilidade_benchmarks.csv",
        "diagnostico_dimensoes_processo.csv", "associacoes_ecologicas.csv",
        "tabela_socioeconomica_ufpa.csv",
    ]:
        assert (p / nome).exists()


def test_relatorio_fisica_gerado(tmp_path):
    docx = tmp_path / "relatorio.docx"
    md = tmp_path / "relatorio.md"
    saidas = gerar_relatorio(ROOT, docx, md)
    assert saidas["docx"].exists()
    assert saidas["markdown"].exists()
    validar_relatorio(docx, md)


def test_markdown_preserva_restricoes(tmp_path):
    docx = tmp_path / "relatorio.docx"
    md = tmp_path / "relatorio.md"
    gerar_relatorio(ROOT, docx, md)
    texto = md.read_text(encoding="utf-8")
    assert "CO_CURSO" in texto
    assert "ecológica" in texto
    assert "Tucuruí" in texto
    assert "1627581" in texto
    assert "não foi localizada na planilha" in texto
    assert "não foi interpretada como valor zero nem como Conceito Enade 1" in texto
    assert "5.1 Desempenho" in texto
    assert "5.7 Associações ecológicas" in texto
