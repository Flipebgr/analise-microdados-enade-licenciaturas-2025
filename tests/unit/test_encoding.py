from __future__ import annotations

from pathlib import Path

from src.qualidade.auditar_encoding import (
    auditar_encoding,
    corrigir_substituicoes_seguras,
    detectar_mojibake_texto,
)


def test_detectar_mojibake_texto_identifica_linha():
    texto = "Linha correta\nRelatÃ³rio com problema\n"
    assert detectar_mojibake_texto(texto) == [(2, "RelatÃ³rio com problema")]

def test_correcao_conservadora_em_diretorio_temporario(tmp_path: Path):
    arquivo = tmp_path / "exemplo.md"
    arquivo.write_text("RelatÃ³rio ecolÃ³gico de FÃ­sica\n", encoding="utf-8")

    alterados = corrigir_substituicoes_seguras(tmp_path)

    assert alterados == ["exemplo.md"]
    assert arquivo.read_text(encoding="utf-8") == "Relatório ecológico de Física\n"
    assert auditar_encoding(tmp_path) == []

def test_detectar_mojibake_nao_marca_acentos_legitimos():
    texto = "SÃO CARLOS\nUBERLÂNDIA\nCOMPOSIÇÃO\nINTRODUÇÃO\n"
    assert detectar_mojibake_texto(texto) == []

def test_auditoria_ignora_pastas_derivadas(tmp_path: Path):
    pasta = tmp_path / "dados_processados" / "fisica"
    pasta.mkdir(parents=True)
    (pasta / "base.csv").write_text("RelatÃ³rio\n", encoding="utf-8")
    assert auditar_encoding(tmp_path) == []
