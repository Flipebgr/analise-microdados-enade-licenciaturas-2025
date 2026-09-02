from __future__ import annotations

from pathlib import Path

from docx import Document

from src.relatorios.validar_relatorio import validar_docx


def _salvar_docx(path: Path, paragrafos: list[str]) -> None:
    doc = Document()
    for texto in paragrafos:
        doc.add_paragraph(texto)
    doc.save(path)


def test_validador_nao_exige_nome_de_area_especifica(tmp_path: Path):
    caminho = tmp_path / "quimica.docx"
    capitulos = [
        "1 INTRODUÇÃO",
        "2 REFERENCIAL INSTITUCIONAL E METODOLÓGICO",
        "3 METODOLOGIA",
        "4 PANORAMA DA LICENCIATURA EM QUÍMICA",
        "5 RESULTADOS",
        "6 DISCUSSÃO",
        "7 CONCLUSÃO",
        "REFERÊNCIAS",
    ]
    _salvar_docx(caminho, capitulos)

    assert validar_docx(
        caminho,
        minimo_figuras=0,
        minimo_tabelas=0,
    ) == []


def test_validador_reporta_capitulo_ausente(tmp_path: Path):
    caminho = tmp_path / "incompleto.docx"
    _salvar_docx(caminho, ["1 INTRODUÇÃO"])

    erros = validar_docx(
        caminho,
        minimo_figuras=0,
        minimo_tabelas=0,
    )

    assert "Capítulo ausente: 3 METODOLOGIA" in erros
    assert any("4 PANORAMA" in erro for erro in erros)


def test_validador_rejeita_caminho_absoluto_windows(tmp_path: Path):
    caminho = tmp_path / "caminho.docx"
    _salvar_docx(
        caminho,
        [
            "1 INTRODUÇÃO",
            r"Arquivo temporário em C:\Users\usuario\relatorio.csv",
        ],
    )

    erros = validar_docx(
        caminho,
        capitulos_esperados=("1 INTRODUÇÃO",),
        minimo_figuras=0,
        minimo_tabelas=0,
    )

    assert "Caminho absoluto encontrado no relatório" in erros


def test_validador_rejeita_caminho_absoluto_sandbox(tmp_path: Path):
    caminho = tmp_path / "sandbox.docx"
    _salvar_docx(
        caminho,
        [
            "1 INTRODUÇÃO",
            "Arquivo temporário em /mnt/data/relatorio.csv",
        ],
    )

    erros = validar_docx(
        caminho,
        capitulos_esperados=("1 INTRODUÇÃO",),
        minimo_figuras=0,
        minimo_tabelas=0,
    )

    assert "Caminho absoluto encontrado no relatório" in erros


def test_docx_inexistente_e_reportado(tmp_path: Path):
    erros = validar_docx(
        tmp_path / "ausente.docx",
        minimo_figuras=0,
        minimo_tabelas=0,
    )

    assert erros == ["DOCX não gerado ou vazio"]
