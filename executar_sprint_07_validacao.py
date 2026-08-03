from __future__ import annotations

from src.core.configuracao_area import INGLES


def main() -> int:
    assert INGLES.co_grupo == 6407
    assert INGLES.co_ies_focal == 569
    print("Sprint 07 — Letras–Inglês")
    print("Área: Letras–Inglês (6407)")
    print("Unidade de análise: CO_CURSO")
    print("Grupos exclusivos e comparações regionais: configurados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
