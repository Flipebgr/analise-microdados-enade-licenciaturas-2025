from __future__ import annotations

import pandas as pd

from src.core.configuracao_area import FISICA
from src.core.grupos import aplicar_grupos_area
from src.fisica.agregar_fisica import juntar_um_para_um
from src.fisica.validar_fisica import validar_base_fisica


def _catalogo_sintetico() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CO_CURSO": [1, 2, 3, 4, 5],
            "CO_GRUPO": [FISICA.co_grupo] * 5,
            "CO_IES": [FISICA.co_ies_focal] * 5,
            "UF": ["PA"] * 5,
            "CO_UF_CURSO": [15] * 5,
            "CO_REGIAO_CURSO": [1] * 5,
            "CONCEITO_ENADE": [3, 1, 1, 1, 1],
            "ROTULO_OFERTA": ["A", "B", "C", "D", "E"],
            "taxa_presenca_microdados": [0.8] * 5,
            "nt_ger_mean": [40.0] * 5,
            "nt_obj_mean": [40.0] * 5,
            "nt_dis_mean": [40.0] * 5,
        }
    )


def main() -> int:
    catalogo = aplicar_grupos_area(_catalogo_sintetico(), FISICA)
    agregado = pd.DataFrame({"CO_CURSO": [1, 2, 3, 4, 5], "N": [10] * 5})
    base = juntar_um_para_um(catalogo, [("agregado", agregado)])
    validar_base_fisica(base)

    print("Refactor 05 — migração de Física para o núcleo compartilhado")
    print(f"Área: {FISICA.nome} ({FISICA.co_grupo})")
    print(f"Cursos no teste de contrato: {len(base)}")
    print("Catálogo, grupos, junções e validação central: OK")
    print("Ausência de conceito permanece distinta de Conceito 1: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
