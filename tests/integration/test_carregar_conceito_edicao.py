from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.edicoes import (
    ENADE_2017,
    ENADE_2025_LICENCIATURAS,
    carregar_conceitos_edicao,
)

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]


def test_conceito_2017_reconcilia_piloto_ufpa_e_preserva_sc():
    fonte = ROOT / "dados_brutos" / "enade_2017" / "resultados_conceito_enade_2017.xlsx"
    if not fonte.exists():
        pytest.skip(f"Fonte local ausente: {fonte}")

    normalizado, original, proveniencia = carregar_conceitos_edicao(fonte, ENADE_2017)
    piloto = normalizado.set_index("CO_CURSO").loc["12027"]

    assert len(normalizado) == len(original) == 10_570
    assert normalizado["CO_CURSO"].is_unique
    assert piloto["CO_GRUPO"] == "1601"
    assert piloto["CO_IES"] == "569"
    assert piloto["INSCRITOS"] == 23
    assert piloto["PARTICIPANTES"] == 13
    assert piloto["CONCEITO_ENADE_ORIGINAL"] == "3"
    assert piloto["CONCEITO_ENADE_NUM"] == 3
    assert piloto["SITUACAO_CONCEITO"] == "com_conceito"
    assert piloto["CONCEITO_ENADE_CONTINUO"] == pytest.approx(2.549786457357)
    assert (normalizado["SITUACAO_CONCEITO"] == "sem_conceito").sum() == 360
    assert normalizado.loc[
        normalizado["SITUACAO_CONCEITO"].eq("sem_conceito"), "CONCEITO_ENADE_NUM"
    ].isna().all()
    assert proveniencia.loc[0, "n_linhas_nao_dados"] == 0


def test_conceito_2025_separa_tres_linhas_de_notas_e_preserva_sc():
    fonte = ROOT / "dados_brutos" / "conceito_enade_licenciaturas.xlsx"
    if not fonte.exists():
        pytest.skip(f"Fonte local ausente: {fonte}")

    normalizado, original, proveniencia = carregar_conceitos_edicao(
        fonte, ENADE_2025_LICENCIATURAS
    )
    piloto = normalizado.set_index("CO_CURSO").loc["100148"]

    assert len(original) == 4_951
    assert len(normalizado) == 4_948
    assert normalizado["CO_CURSO"].is_unique
    assert piloto["CONCEITO_ENADE_ORIGINAL"] == "2"
    assert piloto["CONCEITO_ENADE_NUM"] == 2
    assert pd.isna(piloto["CONCEITO_ENADE_CONTINUO"])
    assert (normalizado["SITUACAO_CONCEITO"] == "sem_conceito").sum() == 401
    assert normalizado.loc[
        normalizado["SITUACAO_CONCEITO"].eq("sem_conceito"), "CONCEITO_ENADE_NUM"
    ].isna().all()
    assert proveniencia.loc[0, "n_linhas_nao_dados"] == 3
    assert proveniencia.loc[0, "n_ofertas"] == 4_948
