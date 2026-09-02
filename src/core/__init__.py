"""Núcleo compartilhado para processamento por área do Enade."""

from src.core.catalogo import preparar_catalogo_area
from src.core.configuracao_area import (
    AREAS,
    BIOLOGIA,
    FISICA,
    GEOGRAFIA,
    INGLES,
    MATEMATICA,
    PEDAGOGIA,
    PORTUGUES,
    QUIMICA,
    ConfiguracaoArea,
    obter_area,
)
from src.core.juncoes import juntar_por_curso, validar_unicidade_por_curso
from src.core.validacao import ResultadoValidacao, validar_base_area

__all__ = [
    "AREAS",
    "BIOLOGIA",
    "FISICA",
    "GEOGRAFIA",
    "INGLES",
    "MATEMATICA",
    "PEDAGOGIA",
    "PORTUGUES",
    "QUIMICA",
    "ConfiguracaoArea",
    "ResultadoValidacao",
    "juntar_por_curso",
    "obter_area",
    "preparar_catalogo_area",
    "validar_base_area",
    "validar_unicidade_por_curso",
]
