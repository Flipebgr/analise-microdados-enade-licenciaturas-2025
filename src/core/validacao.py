from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass

import pandas as pd

from src.core.configuracao_area import ConfiguracaoArea
from src.core.juncoes import validar_unicidade_por_curso
from src.utilitarios.normalizacao import normalizar_codigo


@dataclass(frozen=True, slots=True)
class ResultadoValidacao:
    valido: bool
    erros: tuple[str, ...]
    avisos: tuple[str, ...]
    total_cursos: int
    total_ofertas_ies_focal: int

    def exigir_valido(self) -> None:
        if not self.valido:
            detalhes = "; ".join(self.erros)
            raise ValueError(f"Base inválida: {detalhes}")


def validar_base_area(
    base: pd.DataFrame,
    configuracao: ConfiguracaoArea,
    *,
    colunas_obrigatorias: Collection[str] = (),
    total_cursos_esperado: int | None = None,
    ofertas_ies_esperadas: int | None = None,
) -> ResultadoValidacao:
    """Valida contratos estruturais de uma base agregada por curso."""

    erros: list[str] = []
    avisos: list[str] = []
    obrigatorias = {"CO_CURSO", "CO_IES", "CO_GRUPO", *colunas_obrigatorias}
    faltantes = sorted(obrigatorias - set(base.columns))
    if faltantes:
        erros.append(f"Colunas obrigatórias ausentes: {faltantes}")
        return ResultadoValidacao(False, tuple(erros), tuple(avisos), len(base), 0)

    trabalho = base.copy(deep=True)
    for coluna in ("CO_CURSO", "CO_IES", "CO_GRUPO"):
        trabalho[coluna] = normalizar_codigo(trabalho[coluna])

    try:
        validar_unicidade_por_curso(trabalho, nome=f"base de {configuracao.nome}")
    except ValueError as exc:
        erros.append(str(exc))

    grupos = set(trabalho["CO_GRUPO"].dropna().tolist())
    if grupos != {configuracao.co_grupo}:
        erros.append(
            f"CO_GRUPO incompatível com {configuracao.nome}: "
            f"esperado {configuracao.co_grupo}, encontrados {sorted(grupos)}"
        )

    total_cursos = len(trabalho)
    total_focal = int(trabalho["CO_IES"].eq(configuracao.co_ies_focal).sum())

    if total_cursos_esperado is not None and total_cursos != total_cursos_esperado:
        erros.append(
            f"Total de cursos divergente: esperado {total_cursos_esperado}, encontrado {total_cursos}"
        )
    if ofertas_ies_esperadas is not None and total_focal != ofertas_ies_esperadas:
        erros.append(
            "Ofertas da IES focal divergentes: "
            f"esperado {ofertas_ies_esperadas}, encontrado {total_focal}"
        )

    if "CONCEITO_ENADE" in trabalho.columns:
        ausentes = int(trabalho["CONCEITO_ENADE"].isna().sum())
        if ausentes:
            avisos.append(f"Há {ausentes} curso(s) sem Conceito Enade; ausência foi preservada")

    return ResultadoValidacao(
        valido=not erros,
        erros=tuple(erros),
        avisos=tuple(avisos),
        total_cursos=total_cursos,
        total_ofertas_ies_focal=total_focal,
    )
