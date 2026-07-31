from __future__ import annotations

import pandas as pd

from src.core.juncoes import juntar_por_curso
from src.validacao.validar_agregacoes import validar_tabela_agregada


def juntar_um_para_um(
    base: pd.DataFrame,
    partes: list[tuple[str, pd.DataFrame]],
) -> pd.DataFrame:
    """Junta agregados de Matemática sob o contrato central one-to-one."""

    resultado = base.copy(deep=True)
    for nome, parte in partes:
        validar_tabela_agregada(parte, nome)
        resultado = juntar_por_curso(resultado, parte)
    return resultado
