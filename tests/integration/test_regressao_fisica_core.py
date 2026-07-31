from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.core.configuracao_area import FISICA
from src.core.juncoes import validar_unicidade_por_curso
from src.core.validacao import validar_base_area

ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "dados_processados" / "fisica" / "base_analitica_cursos.csv"

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
    return pd.read_csv(BASE_PATH)


def test_base_fisica_preserva_contrato_do_core() -> None:
    base = carregar_base()
    resultado = validar_base_area(
        base,
        FISICA,
        colunas_obrigatorias=COLUNAS_CRITICAS,
        total_cursos_esperado=257,
        ofertas_ies_esperadas=5,
    )
    resultado.exigir_valido()
    validar_unicidade_por_curso(base, nome="base analítica de Física")


def test_base_fisica_preserva_grupos_e_conceitos_ufpa() -> None:
    base = carregar_base()
    ufpa = base[base["CO_IES"].eq(FISICA.co_ies_focal)].copy()
    conceito = pd.to_numeric(ufpa["CONCEITO_ENADE_NUM"], errors="coerce")

    assert len(ufpa) == 5
    assert int(conceito.eq(1).sum()) == 4
    assert int(conceito.gt(1).sum()) == 1
    assert set(ufpa.loc[conceito.eq(1), "GRUPO_CODIGO"]) == {"A"}
    assert set(ufpa.loc[conceito.gt(1), "GRUPO_CODIGO"]) == {"B"}


def test_tucurui_nao_foi_artificialmente_inserido() -> None:
    base = carregar_base()
    assert not base["CO_CURSO"].astype(str).eq("1627581").any()
