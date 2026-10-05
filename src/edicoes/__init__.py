from __future__ import annotations

from src.edicoes.base import (
    ConceitoNormalizado,
    ContratoEdicao,
    SituacaoConceito,
    normalizar_conceito,
)
from src.edicoes.enade_2017 import ENADE_2017
from src.edicoes.enade_2025_licenciaturas import ENADE_2025_LICENCIATURAS

EDICOES: dict[int, ContratoEdicao] = {
    ENADE_2017.ano: ENADE_2017,
    ENADE_2025_LICENCIATURAS.ano: ENADE_2025_LICENCIATURAS,
}


def obter_edicao(ano: int) -> ContratoEdicao:
    try:
        return EDICOES[ano]
    except KeyError as exc:
        disponiveis = ", ".join(str(valor) for valor in sorted(EDICOES))
        raise KeyError(f"Edição desconhecida: {ano}. Disponíveis: {disponiveis}") from exc


__all__ = [
    "ConceitoNormalizado",
    "ContratoEdicao",
    "EDICOES",
    "ENADE_2017",
    "ENADE_2025_LICENCIATURAS",
    "SituacaoConceito",
    "normalizar_conceito",
    "obter_edicao",
]
