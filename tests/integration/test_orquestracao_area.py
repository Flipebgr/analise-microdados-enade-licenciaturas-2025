from __future__ import annotations

from pathlib import Path

import pytest

from src.core.configuracao_area import BIOLOGIA, BIOLOGIA_BACHARELADO_2017
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS
from src.orquestracao.area import analisar_area

pytestmark = pytest.mark.integration
ROOT = Path(__file__).resolve().parents[2]


def test_piloto_2017_reconcilia_base_e_agregados():
    microdados = ROOT / "dados_brutos" / "enade_2017" / "microdados_enade_2017_LGPD.zip"
    conceitos = ROOT / "dados_brutos" / "enade_2017" / "resultados_conceito_enade_2017.xlsx"
    if not microdados.exists() or not conceitos.exists():
        pytest.skip("Fontes locais de 2017 ausentes")

    resultado = analisar_area(microdados, conceitos, ENADE_2017, BIOLOGIA_BACHARELADO_2017)
    piloto = resultado.base_cursos.set_index("CO_CURSO").loc["12027"]

    assert len(resultado.base_cursos) == 268
    assert resultado.base_cursos["CO_CURSO"].is_unique
    assert resultado.auditoria_cobertura["em_conceito"].all()
    assert piloto["CO_IES"] == "569"
    assert piloto["INSCRITOS"] == 23
    assert piloto["PARTICIPANTES"] == 13
    assert piloto["CONCEITO_ENADE_NUM"] == 3
    assert piloto["registros_microdados"] == 23
    assert resultado.processo_itens["ITEM"].nunique() == 42
    assert "nao_sabe_responder_pct" in resultado.processo_itens
    assert "nao_se_aplica_pct" in resultado.processo_itens


def test_biologia_2025_mantem_contrato_distinto():
    microdados = ROOT / "dados_brutos" / "microdados_enade_licenciaturas_2025.zip"
    conceitos = ROOT / "dados_brutos" / "conceito_enade_licenciaturas.xlsx"
    if not microdados.exists() or not conceitos.exists():
        pytest.skip("Fontes locais de 2025 ausentes")

    resultado = analisar_area(microdados, conceitos, ENADE_2025_LICENCIATURAS, BIOLOGIA)

    assert len(resultado.base_cursos) == 428
    assert resultado.base_cursos["CO_CURSO"].is_unique
    assert resultado.processo_itens["ITEM"].nunique() == 47
    assert "QE_I67" not in set(resultado.processo_itens["ITEM"])
    assert "proficiencia_mean" in resultado.base_cursos
    assert "formacao_geral_total_mean" not in resultado.base_cursos
