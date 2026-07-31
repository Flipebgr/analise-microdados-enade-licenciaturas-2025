from __future__ import annotations

import json
from pathlib import Path


def test_baseline_pre_refatoracao_tem_contratos_principais():
    raiz = Path(__file__).resolve().parents[2]
    caminho = raiz / "documentacao" / "refatoracao" / "baseline_pre_refatoracao.json"
    baseline = json.loads(caminho.read_text(encoding="utf-8"))

    assert baseline["matematica"]["total_cursos"] == 482
    assert baseline["fisica"]["total_cursos"] == 257
    assert baseline["fisica"]["ofertas_ufpa_localizadas"] == 5
    assert baseline["restricoes_metodologicas"]["unidade_principal"] == "CO_CURSO"
    assert baseline["restricoes_metodologicas"]["join_individual_entre_arquivos"] is False
    assert baseline["restricoes_metodologicas"]["ausencia_conceito_equivale_conceito_1"] is False
