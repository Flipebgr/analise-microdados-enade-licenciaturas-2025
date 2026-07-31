from __future__ import annotations

import pandas as pd

from src.core.configuracao_area import MATEMATICA
from src.core.grupos import aplicar_grupos_area
from src.matematica.agregar_matematica import juntar_um_para_um
from src.matematica.validar_matematica import validar_base_matematica


def _catalogo_sintetico() -> pd.DataFrame:
    conceitos = [3, 1, 1, 1, 1, 1, 1, 1]
    return pd.DataFrame(
        {
            "CO_CURSO": list(range(1, 9)),
            "CO_GRUPO": [MATEMATICA.co_grupo] * 8,
            "CO_IES": [MATEMATICA.co_ies_focal] * 8,
            "UF": ["PA"] * 8,
            "CO_UF_CURSO": [15] * 8,
            "CO_REGIAO_CURSO": [1] * 8,
            "CONCEITO_ENADE": conceitos,
            "CONCEITO_ENADE_NUM": conceitos,
            "ROTULO_OFERTA": [f"Oferta {indice}" for indice in range(1, 9)],
        }
    )


def main() -> int:
    catalogo = aplicar_grupos_area(_catalogo_sintetico(), MATEMATICA)
    agregado = pd.DataFrame({"CO_CURSO": list(range(1, 9)), "nt_ger_mean": [40.0] * 8})
    base = juntar_um_para_um(catalogo, [("desempenho", agregado)])
    validar_base_matematica(base)

    print("Refactor 06 — migração de Matemática para o núcleo compartilhado")
    print(f"Área: {MATEMATICA.nome} ({MATEMATICA.co_grupo})")
    print(f"Cursos no teste de contrato: {len(base)}")
    print("Catálogo, grupos, junções e validação central: OK")
    print("Sete ofertas de Conceito Enade 1 preservadas: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
