from __future__ import annotations

import pandas as pd
import pytest

from src.ingles.comparacoes_regionais import construir_comparacoes_regionais
from src.ingles.validar_ingles import validar_base_ingles


def base_ufpa_valida() -> pd.DataFrame:
    municipios = ["Belém", "Altamira", "Bragança", "Cametá", "Soure"]
    conceitos = [3, 1, 1, 1, 1]
    return pd.DataFrame({
        "CO_CURSO": [1, 2, 3, 4, 5],
        "CO_IES": [569] * 5,
        "CO_GRUPO": [6407] * 5,
        "MUNICIPIO": municipios,
        "CONCEITO_ENADE_NUM": conceitos,
        "GRUPO_CODIGO": ["B", "A", "A", "A", "A"],
        "GRUPO": ["UFPA conceito superior"] + ["UFPA conceito 1"] * 4,
    })


def test_validacao_ingles_aceita_relacao_inicial() -> None:
    validar_base_ingles(base_ufpa_valida())


def test_validacao_ingles_rejeita_quinta_oferta_conceito_1() -> None:
    base = base_ufpa_valida()
    base.loc[0, "CONCEITO_ENADE_NUM"] = 1
    base.loc[0, "GRUPO_CODIGO"] = "A"
    with pytest.raises(ValueError, match="4 ofertas"):
        validar_base_ingles(base)


def test_comparacoes_regionais_incluem_medias_simples_e_ponderadas() -> None:
    base = pd.DataFrame({
        "CO_CURSO": [1, 2, 3],
        "CO_IES": [569, 100, 200],
        "CO_REGIAO_CURSO": [1, 1, 2],
        "CO_UF_CURSO": [15, 13, 29],
        "ROTULO_OFERTA": ["Belém", "Manaus", "Salvador"],
        "nt_ger_mean": [40.0, 50.0, 60.0],
        "nt_obj_mean": [38.0, 48.0, 58.0],
        "nt_dis_mean": [42.0, 52.0, 62.0],
        "nt_ger_count": [10, 20, 30],
    })
    resultado = construir_comparacoes_regionais(base)
    brasil = resultado[
        resultado["RECORTE"].eq("Brasil geral")
        & resultado["INDICADOR"].eq("nt_ger_mean")
    ].iloc[0]
    assert brasil["MEDIA_CURSOS"] == pytest.approx(50.0)
    assert brasil["MEDIA_PONDERADA_PARTICIPANTES"] == pytest.approx(53.333333)
