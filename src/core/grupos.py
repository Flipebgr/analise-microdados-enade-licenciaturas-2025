from __future__ import annotations

import pandas as pd

from src.analise.definir_grupos import aplicar_grupos
from src.core.configuracao_area import ConfiguracaoArea
from src.core.juncoes import validar_unicidade_por_curso


def aplicar_grupos_area(
    cursos: pd.DataFrame,
    configuracao: ConfiguracaoArea,
) -> pd.DataFrame:
    """Classifica cursos nos grupos comparativos exclusivos da área.

    A função preserva cursos sem Conceito Enade no cadastro, mas não os
    classifica como Conceito 1.
    """

    validar_unicidade_por_curso(cursos, nome=f"catálogo de {configuracao.nome}")
    resultado = aplicar_grupos(cursos, configuracao.co_ies_focal)
    validar_unicidade_por_curso(resultado, nome=f"catálogo classificado de {configuracao.nome}")
    return resultado
