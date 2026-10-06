from __future__ import annotations

from pathlib import Path

import pytest

from src.agregacao.agregar_processo_formativo import agregar_processo_formativo_edicao
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]


def test_piloto_2017_processa_qe_i27_ate_qe_i68_reais():
    fonte = ROOT / "dados_brutos" / "enade_2017" / "microdados_enade_2017_LGPD.zip"
    if not fonte.exists():
        pytest.skip(f"Fonte local ausente: {fonte}")

    agregado, resumo, proveniencia = agregar_processo_formativo_edicao(
        fonte, ENADE_2017, ["12027"]
    )
    primeiro = resumo.loc[resumo["ITEM"] == "QE_I27"].iloc[0]
    ultimo = resumo.loc[resumo["ITEM"] == "QE_I68"].iloc[0]

    assert agregado["CO_CURSO"].tolist() == ["12027"]
    assert len(resumo) == len(proveniencia) == 42
    assert primeiro["n_total"] == 23
    assert primeiro["n_valido"] == 16
    assert primeiro["n_ausente"] == 7
    assert primeiro["concordancia_n"] == 14
    assert ultimo["n_total"] == 23
    assert set(proveniencia["arquivo"]) == {"microdados2017_arq4.txt"}
    assert (
        resumo["n_total"] == resumo[[
            "n_valido", "n_ausente", "n_invalido", "n_nao_sabe_responder", "n_nao_se_aplica"
        ]].sum(axis=1)
    ).all()


def test_piloto_2025_nao_inventa_qe_i67_ausente_dos_microdados():
    fonte = ROOT / "dados_brutos" / "microdados_enade_licenciaturas_2025.zip"
    if not fonte.exists():
        pytest.skip(f"Fonte local ausente: {fonte}")

    agregado, resumo, proveniencia = agregar_processo_formativo_edicao(
        fonte, ENADE_2025_LICENCIATURAS, ["100148"]
    )
    primeiro = resumo.loc[resumo["ITEM"] == "QE_I20"].iloc[0]

    assert agregado["CO_CURSO"].tolist() == ["100148"]
    assert len(resumo) == len(proveniencia) == 47
    assert "QE_I67" not in set(resumo["ITEM"])
    assert primeiro["n_total"] == 12
    assert primeiro["n_valido"] == 10
    assert primeiro["n_ausente"] == 1
    assert primeiro["n_nao_sabe_responder"] == 1
    assert primeiro["concordancia_pct"] == 1
    assert set(proveniencia["arquivo"]) == {"microdados2025_arq4.txt"}
    assert (
        resumo["n_total"] == resumo[[
            "n_valido", "n_ausente", "n_invalido", "n_nao_sabe_responder", "n_nao_se_aplica"
        ]].sum(axis=1)
    ).all()
