from __future__ import annotations

from pathlib import Path

import pytest

from src.core.configuracao_area import BIOLOGIA, BIOLOGIA_BACHARELADO_2017
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS
from src.evidencias import construir_evidencias, validar_evidencias
from src.orquestracao.area import analisar_area

pytestmark = pytest.mark.integration
ROOT = Path(__file__).resolve().parents[2]


def test_evidencias_piloto_2017_preservam_processo_e_proveniencia():
    microdados = ROOT / "dados_brutos" / "enade_2017" / "microdados_enade_2017_LGPD.zip"
    conceitos = ROOT / "dados_brutos" / "enade_2017" / "resultados_conceito_enade_2017.xlsx"
    if not microdados.exists() or not conceitos.exists():
        pytest.skip("Fontes locais de 2017 ausentes")

    resultado = analisar_area(microdados, conceitos, ENADE_2017, BIOLOGIA_BACHARELADO_2017)
    pacote = construir_evidencias(resultado, ENADE_2017, BIOLOGIA_BACHARELADO_2017, microdados)

    validar_evidencias(pacote)
    assert pacote["universo"]["n_cursos_base"] == 268
    assert pacote["ofertas_focais"][0]["CO_CURSO"] == "12027"
    assert pacote["ofertas_focais"][0]["CONCEITO_ENADE_NUM"] == 3
    assert pacote["ofertas_focais"][0]["INSCRITOS"] == 23
    assert pacote["ofertas_focais"][0]["PARTICIPANTES"] == 13
    assert pacote["area"]["aplicabilidade"]["questionario_licenciatura"] is False
    assert pacote["edicao"]["capacidades"]["proficiencia"] is False
    assert pacote["edicao"]["capacidades"]["recomendacao"] is False
    assert {"formacao_geral_total", "componente_especifico_total"} <= pacote["desempenho"]["mapa_canonico"].keys()
    assert pacote["edicao"]["itens_processo"] == [f"QE_I{i}" for i in range(27, 69)]
    assert set(pacote["proveniencia"]["fontes"][0]["arquivos_tematicos"]) == {
        f"microdados2017_arq{i}.txt" for i in (1, 3, 4, 10, 11, 14, 16, 18, 19, 21, 27, 29)
    }
    assert len(pacote["processo_formativo"]["itens_por_curso"]) == 268 * 42
    assert {linha["denominador_codigos_especiais"] for linha in pacote["processo_formativo"]["proveniencia"]} == {"n_total"}


def test_evidencias_2025_usam_contrato_proprio_da_edicao():
    microdados = ROOT / "dados_brutos" / "microdados_enade_licenciaturas_2025.zip"
    conceitos = ROOT / "dados_brutos" / "conceito_enade_licenciaturas.xlsx"
    if not microdados.exists() or not conceitos.exists():
        pytest.skip("Fontes locais de 2025 ausentes")

    resultado = analisar_area(microdados, conceitos, ENADE_2025_LICENCIATURAS, BIOLOGIA)
    pacote = construir_evidencias(resultado, ENADE_2025_LICENCIATURAS, BIOLOGIA, microdados)

    validar_evidencias(pacote)
    assert pacote["universo"]["n_cursos_base"] == 428
    assert len(pacote["processo_formativo"]["itens_por_curso"]) == 428 * 47
    assert "proficiencia" in pacote["desempenho"]["mapa_canonico"]
    assert "formacao_geral_total" not in pacote["desempenho"]["mapa_canonico"]
    assert set(pacote["proveniencia"]["fontes"][0]["arquivos_tematicos"]) == {
        f"microdados2025_arq{i}.txt" for i in (1, 3, 4, 11, 12, 13, 15, 16, 17, 21, 22, 23, 24)
    }
    sem_conceito = [r for r in pacote["participacao"]["por_curso"] if r["SITUACAO_CONCEITO"] == "sem_conceito"]
    assert sem_conceito
    assert all(r["CONCEITO_ENADE_NUM"] is None for r in sem_conceito)
