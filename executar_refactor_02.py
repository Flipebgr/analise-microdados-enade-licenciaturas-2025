from __future__ import annotations

import pandas as pd

from src.core import INGLES, juntar_por_curso, preparar_catalogo_area, validar_base_area


def main() -> None:
    cadastro = pd.DataFrame(
        {
            "CO_CURSO": [10, 20, 30],
            "CO_IES": [569, 569, 999],
            "CO_GRUPO": [6407, 6407, 702],
            "CO_MODALIDADE": [1, 1, 0],
        }
    )
    catalogo = preparar_catalogo_area(
        cadastro,
        INGLES,
        colunas_adicionais=("CO_MODALIDADE",),
    )
    desempenho = pd.DataFrame(
        {"CO_CURSO": [10, 20], "NT_GER_MEDIA": [48.2, 52.1]}
    )
    base = juntar_por_curso(catalogo, desempenho)
    resultado = validar_base_area(
        base,
        INGLES,
        colunas_obrigatorias=("NT_GER_MEDIA",),
        total_cursos_esperado=2,
        ofertas_ies_esperadas=2,
    )
    resultado.exigir_valido()

    print("Refactor 02 — núcleo compartilhado")
    print(f"Área validada: {INGLES.nome} ({INGLES.co_grupo})")
    print(f"Cursos no teste de contrato: {resultado.total_cursos}")
    print(f"Ofertas da IES focal: {resultado.total_ofertas_ies_focal}")
    print("Contratos de catálogo, junção e validação: OK")


if __name__ == "__main__":
    main()
