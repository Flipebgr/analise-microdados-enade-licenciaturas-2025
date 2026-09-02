from pathlib import Path

from src.relatorios.validar_relatorio import validar_docx


def test_relatorio_docx_gerado():
    caminho = Path("relatorios/matematica/relatorio_matematica_enade_2025.docx")
    if caminho.exists():
        assert validar_docx(caminho) == []


def test_arquivos_criticos_sprints_anteriores():
    assert Path("executar.py").exists()
    assert Path("scripts/pipelines/executar_sprint_00.py").exists()
    assert Path("scripts/pipelines/executar_sprint_01.py").exists()
    assert Path("scripts/pipelines/executar_sprint_02.py").exists()
    assert Path("src/validacao/validar_resultados_matematica.py").exists()
