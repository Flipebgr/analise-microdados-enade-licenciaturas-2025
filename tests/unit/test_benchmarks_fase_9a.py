from __future__ import annotations

import pandas as pd
import pytest

from src.analise.benchmarks_fase_9a import (
    construir_benchmark_amplo,
    construir_benchmark_comparavel,
)
from src.analise.contratos_fase_9a import Territorio
from src.analise.estimandos_fase_9a import (
    diferenca_proporcoes,
    hedges_g_cursos,
    media_cursos,
    media_ponderada,
    resumo_contraste_foco_unico,
)


def _cursos() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": ["focal", "pa1", "pa2", "am1", "sp1", "sp2", "sp3"],
            "CO_IES": ["569", "1", "2", "3", "4", "5", "6"],
            "CO_MODALIDADE": ["1"] * 7,
            "CO_CATEGAD": ["1", "1", "1", "1", "1", "2", "1"],
            "CO_ORGACAD": ["10028", "10028", "10028", "10028", "10028", "10028", "other"],
            "CO_UF_CURSO": ["15", "15", "15", "13", "35", "35", "35"],
            "CO_REGIAO_CURSO": ["1", "1", "1", "1", "3", "3", "3"],
            "PARTICIPANTES": [100, 95, 120, 90, 105, 100, 110],
            "x": [50.0, 40.0, 60.0, 55.0, 65.0, 70.0, 75.0],
        }
    )


def test_benchmark_amplo_respeita_territorio_e_remove_alvo():
    cursos = _cursos()

    para = construir_benchmark_amplo(cursos, "focal", Territorio.PARA)
    norte = construir_benchmark_amplo(cursos, "focal", Territorio.NORTE)
    brasil = construir_benchmark_amplo(cursos, "focal", Territorio.BRASIL)

    assert para["CO_CURSO"].tolist() == ["pa1", "pa2"]
    assert norte["CO_CURSO"].tolist() == ["am1", "pa1", "pa2"]
    assert "focal" not in brasil["CO_CURSO"].tolist()
    assert len(brasil) == 6


def test_benchmark_comparavel_audita_cascata_e_nao_relaxa_modalidade():
    cursos = _cursos()
    cursos.loc[cursos.CO_CURSO.eq("sp2"), "CO_MODALIDADE"] = "2"

    membros, resumo, escolhido = construir_benchmark_comparavel(
        cursos,
        "focal",
        territorio=Territorio.BRASIL,
    )

    assert resumo["ordem_relaxamento"].tolist() == [1, 2, 3, 4]
    assert escolhido["ordem_relaxamento"] == 3
    assert escolhido["status"] == "descritivo_apenas"
    assert resumo.loc[resumo.selecionado, "n_cursos"].item() == 5
    assert "sp2" not in membros.CO_CURSO.tolist()
    assert membros.loc[membros.ordem_relaxamento.eq(1), "CO_CURSO"].tolist() == [
        "am1",
        "pa1",
        "pa2",
        "sp1",
    ]


def test_benchmark_comparavel_restringe_cursos_elegiveis_por_indicador():
    cursos = _cursos()
    membros, resumo, escolhido = construir_benchmark_comparavel(
        cursos,
        "focal",
        territorio=Territorio.BRASIL,
        cursos_elegiveis={"pa1", "pa2", "am1"},
    )

    assert escolhido["n_cursos"] == 3
    assert escolhido["status"] == "insuficiente"
    assert resumo["n_cursos"].max() == 3
    assert set(membros.CO_CURSO) <= {"pa1", "pa2", "am1"}


def test_benchmark_comparavel_requer_alvo_e_reduz_territorio():
    cursos = _cursos()
    with pytest.raises(ValueError, match="ausente no universo"):
        construir_benchmark_comparavel(cursos, "inexistente", territorio=Territorio.BRASIL)
    membros, _, _ = construir_benchmark_comparavel(
        cursos, "focal", territorio=Territorio.PARA
    )
    assert set(membros.CO_CURSO).isdisjoint({"am1", "sp1", "sp2", "sp3"})


def test_estimandos_separam_curso_tipico_de_respondente_tipico():
    valores = pd.Series([40.0, 60.0])
    n_validos = pd.Series([1, 3])

    resultado = resumo_contraste_foco_unico(50.0, valores, n_valido_benchmark=n_validos)

    assert media_cursos(valores) == 50.0
    assert media_ponderada(valores, n_validos) == 55.0
    assert resultado["diferenca_media"] == 0.0
    assert resultado["percentil_focal"] == 50.0
    assert resultado["media_benchmark_ponderada"] == 55.0
    assert resultado["z_ref"] == 0.0


def test_estimandos_degenerados_e_proporcoes_sao_explicitos():
    resultado = resumo_contraste_foco_unico(2.0, pd.Series([1.0]))

    assert resultado["z_ref"] is None
    assert diferenca_proporcoes(0.4, 0.2) == {
        "diferenca_proporcoes": pytest.approx(0.2),
        "razao_proporcoes": pytest.approx(2.0),
    }
    assert diferenca_proporcoes(0.4, 0.0)["razao_proporcoes"] is None
    with pytest.raises(ValueError, match="intervalo"):
        diferenca_proporcoes(1.2, 0.4)


def test_efeitos_de_dois_grupos():
    assert hedges_g_cursos(pd.Series([2.0, 4.0]), pd.Series([1.0, 2.0])) is not None
    assert hedges_g_cursos(pd.Series([2.0]), pd.Series([1.0, 2.0])) is None
    assert hedges_g_cursos(pd.Series([1.0, 1.0]), pd.Series([2.0, 2.0])) is None


def test_percentil_focal_trata_empates_pelo_midrank():
    resultado = resumo_contraste_foco_unico(2.0, pd.Series([1.0, 2.0, 2.0, 3.0]))

    assert resultado["percentil_focal"] == 50.0
