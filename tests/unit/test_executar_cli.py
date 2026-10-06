from __future__ import annotations

from pathlib import Path

import executar
import src.orquestracao.area as orquestracao


def test_normalizar_aceita_acentos() -> None:
    assert executar.normalizar("Validação") == "validacao"


def test_fontes_sem_etapa_usa_validacao(monkeypatch) -> None:
    monkeypatch.setattr(executar, "ROOT", Path("/projeto"))
    scripts = executar.resolver_scripts("fontes", None)
    assert scripts == [Path("/projeto/scripts/pipelines/executar_sprint_00.py")]


def test_area_aposentada_nao_e_pipeline_operacional() -> None:
    assert executar.etapas_disponiveis("matematica") == []
    assert executar.main(["matematica", "base"]) == 2


def test_quimica_ainda_nao_esta_registrada() -> None:
    assert executar.etapas_disponiveis("quimica") == []


def test_script_ausente_retorna_codigo_2(tmp_path) -> None:
    assert executar.executar_scripts([tmp_path / "ausente.py"]) == 2


def test_listar_mostra_somente_pipelines_operacionais(capsys) -> None:
    assert executar.main(["--listar"]) == 0
    saida = capsys.readouterr().out
    assert "fontes" in saida
    assert "matematica" not in saida
    assert "geografia" not in saida


def test_comando_area_despacha_por_edicao_e_slug(monkeypatch, tmp_path, capsys) -> None:
    chamadas = []

    def preparar(microdados, conceitos, edicao, area):
        chamadas.append((microdados, conceitos, edicao.ano, area.slug))
        return object()

    monkeypatch.setattr(orquestracao, "preparar_area", preparar)
    monkeypatch.setattr(orquestracao, "salvar_resultado_area", lambda resultado, pasta: [pasta / "base_cursos.csv"])

    assert executar.main([
        "area", "--ano", "2017", "--slug", "biologia_bacharelado",
        "--microdados", "micro.zip", "--conceitos", "conceito.xlsx",
        "--etapa", "validacao", "--saida", str(tmp_path),
    ]) == 0
    assert chamadas == [
        (Path("micro.zip"), Path("conceito.xlsx"), 2017, "biologia_bacharelado")
    ]
    assert str(tmp_path / "validacao" / "base_cursos.csv") in capsys.readouterr().out


def test_comando_area_rejeita_slug_de_outra_edicao(capsys) -> None:
    assert executar.main([
        "area", "--ano", "2017", "--slug", "matematica",
        "--microdados", "micro.zip", "--conceitos", "conceito.xlsx",
    ]) == 2
    assert "Área desconhecida" in capsys.readouterr().err
