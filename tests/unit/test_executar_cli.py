from __future__ import annotations

from pathlib import Path

import executar


def test_normalizar_aceita_acentos() -> None:
    assert executar.normalizar("Física") == "fisica"
    assert executar.normalizar("Português") == "portugues"
    assert executar.normalizar("Matemática") == "matematica"


def test_resolver_tudo_preserva_ordem_do_pipeline(monkeypatch) -> None:
    monkeypatch.setattr(executar, "ROOT", Path("/projeto"))
    scripts = executar.resolver_scripts("geografia", "tudo")
    assert [path.name for path in scripts] == [
        "executar_sprint_19.py",
        "executar_sprint_20.py",
        "executar_sprint_21.py",
    ]


def test_fisica_regional_e_etapa_separada(monkeypatch) -> None:
    monkeypatch.setattr(executar, "ROOT", Path("/projeto"))
    scripts = executar.resolver_scripts("fisica", "regional")
    assert [path.name for path in scripts] == ["executar_relatorio_regional_fisica.py"]


def test_fontes_sem_etapa_usa_validacao(monkeypatch) -> None:
    monkeypatch.setattr(executar, "ROOT", Path("/projeto"))
    scripts = executar.resolver_scripts("fontes", None)
    assert [path.name for path in scripts] == ["executar_sprint_00.py"]


def test_area_invalida_retorna_erro() -> None:
    assert executar.main(["quimica", "base"]) == 2


def test_script_ausente_retorna_codigo_2(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(executar, "ROOT", tmp_path)
    script = tmp_path / "nao_existe.py"
    assert executar.executar_scripts([script]) == 2
