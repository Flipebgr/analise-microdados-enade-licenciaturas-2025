from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.core.configuracao_area import MATEMATICA
from src.core.juncoes import validar_unicidade_por_curso
from src.core.validacao import validar_base_area

ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "dados_processados" / "matematica" / "base_analitica_cursos.csv"

COLUNAS_CRITICAS = {
    "CO_CURSO",
    "CO_IES",
    "CO_GRUPO",
    "ROTULO_OFERTA",
    "CONCEITO_ENADE_NUM",
    "GRUPO_CODIGO",
    "nt_ger_mean",
    "nt_obj_mean",
    "nt_dis_mean",
}


def carregar_base() -> pd.DataFrame:
    return pd.read_csv(BASE_PATH, encoding="utf-8-sig")


def test_base_matematica_preserva_contrato_do_core() -> None:
    base = carregar_base()
    resultado = validar_base_area(
        base,
        MATEMATICA,
        colunas_obrigatorias=COLUNAS_CRITICAS,
        total_cursos_esperado=482,
        ofertas_ies_esperadas=8,
    )
    resultado.exigir_valido()
    validar_unicidade_por_curso(base, nome="base analítica de Matemática")


def test_base_matematica_preserva_grupos_e_conceitos_ufpa() -> None:
    base = carregar_base()
    ufpa = base[base["CO_IES"].eq(MATEMATICA.co_ies_focal)].copy()
    conceito = pd.to_numeric(ufpa["CONCEITO_ENADE_NUM"], errors="coerce")

    assert len(ufpa) == 8
    assert int(conceito.eq(1).sum()) == 7
    assert int(conceito.gt(1).sum()) == 1
    assert set(ufpa.loc[conceito.eq(1), "GRUPO_CODIGO"]) == {"A"}
    assert set(ufpa.loc[conceito.gt(1), "GRUPO_CODIGO"]) == {"B"}


def test_figuras_principais_de_matematica_foram_preservadas() -> None:
    figuras = sorted((ROOT / "figuras" / "matematica").glob("0[1-7]_*.png"))
    assert len(figuras) == 7
