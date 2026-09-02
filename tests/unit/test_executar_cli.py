from __future__ import annotations

from pathlib import Path

import executar


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
