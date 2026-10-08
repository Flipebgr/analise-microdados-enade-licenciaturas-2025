"""Construção dos universos de referência da Fase 9A."""

from __future__ import annotations

import pandas as pd

from src.analise.contratos_fase_9a import (
    NIVEIS_RELAXAMENTO_BENCHMARK,
    NivelRelaxamentoBenchmark,
    PoliticaTamanhoBenchmark,
    StatusAnalise,
    Territorio,
)


COLUNAS_BENCHMARK = (
    "CO_CURSO",
    "CO_IES",
    "CO_MODALIDADE",
    "CO_CATEGAD",
    "CO_ORGACAD",
    "CO_UF_CURSO",
    "CO_REGIAO_CURSO",
    "PARTICIPANTES",
)


def _normalizar_codigo(serie: pd.Series) -> pd.Series:
    return serie.astype("string").str.strip().str.lstrip("0")


def _validar_base(cursos: pd.DataFrame, *, comparavel: bool = False) -> None:
    obrigatorias = set(COLUNAS_BENCHMARK if comparavel else ("CO_CURSO", "CO_UF_CURSO", "CO_REGIAO_CURSO"))
    ausentes = sorted(obrigatorias - set(cursos.columns))
    if ausentes:
        raise ValueError(f"Colunas ausentes para benchmark: {ausentes}")
    if cursos["CO_CURSO"].isna().any() or cursos["CO_CURSO"].duplicated().any():
        raise ValueError("Benchmark exige CO_CURSO presente e único")


def mascara_territorio(cursos: pd.DataFrame, territorio: Territorio) -> pd.Series:
    """Seleciona Pará, Região Norte ou Brasil sem ampliar o recorte."""

    uf = pd.to_numeric(cursos["CO_UF_CURSO"], errors="coerce")
    regiao = pd.to_numeric(cursos["CO_REGIAO_CURSO"], errors="coerce")
    if territorio == Territorio.PARA:
        return uf.eq(15)
    if territorio == Territorio.NORTE:
        return regiao.eq(1)
    if territorio == Territorio.BRASIL:
        return pd.Series(True, index=cursos.index)
    raise ValueError(f"Território de benchmark desconhecido: {territorio}")


def construir_benchmark_amplo(
    cursos: pd.DataFrame,
    co_curso_alvo: str,
    territorio: Territorio,
) -> pd.DataFrame:
    """Retorna cursos da mesma área no território, sem incluir o alvo."""

    _validar_base(cursos)
    alvo = str(co_curso_alvo).strip()
    mascara = mascara_territorio(cursos, territorio)
    mascara &= cursos["CO_CURSO"].astype("string").str.strip().ne(alvo)
    membros = cursos.loc[mascara].copy()
    return membros.sort_values("CO_CURSO", kind="stable").reset_index(drop=True)


def _nivel(candidatos: pd.DataFrame, alvo: pd.Series, regra: NivelRelaxamentoBenchmark) -> pd.DataFrame:
    modalidade = _normalizar_codigo(candidatos["CO_MODALIDADE"]).eq(
        _normalizar_codigo(pd.Series([alvo["CO_MODALIDADE"]])).iloc[0]
    )
    mascara = modalidade
    if regra.exige_categoria:
        mascara &= _normalizar_codigo(candidatos["CO_CATEGAD"]).eq(
            _normalizar_codigo(pd.Series([alvo["CO_CATEGAD"]])).iloc[0]
        )
    if regra.exige_organizacao:
        mascara &= _normalizar_codigo(candidatos["CO_ORGACAD"]).eq(
            _normalizar_codigo(pd.Series([alvo["CO_ORGACAD"]])).iloc[0]
        )
    porte_alvo = pd.to_numeric(pd.Series([alvo["PARTICIPANTES"]]), errors="coerce").iloc[0]
    porte_candidatos = pd.to_numeric(candidatos["PARTICIPANTES"], errors="coerce")
    if pd.isna(porte_alvo) or porte_alvo <= 0:
        return candidatos.iloc[0:0].copy()
    mascara &= porte_candidatos.between(
        porte_alvo * regra.limite_inferior_porte,
        porte_alvo * regra.limite_superior_porte,
        inclusive="both",
    )
    return candidatos.loc[mascara].sort_values("CO_CURSO", kind="stable").reset_index(drop=True)


def construir_benchmark_comparavel(
    cursos: pd.DataFrame,
    co_curso_alvo: str,
    *,
    territorio: Territorio,
    cursos_elegiveis: set[str] | None = None,
    politica: PoliticaTamanhoBenchmark = PoliticaTamanhoBenchmark(),
    niveis: tuple[NivelRelaxamentoBenchmark, ...] = NIVEIS_RELAXAMENTO_BENCHMARK,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Retorna membros de cada nível tentado, resumo e decisão selecionada.

    ``cursos_elegiveis`` permite aplicar elegibilidade indicador a indicador.
    Se nenhum degrau atingir N completo, escolhe-se para descrição o degrau
    com mais membros, desempate pelo nível mais estrito.
    """

    _validar_base(cursos, comparavel=True)
    alvo_id = str(co_curso_alvo).strip()
    candidatos = cursos.loc[mascara_territorio(cursos, territorio)].copy()
    candidatos = candidatos.loc[candidatos["CO_CURSO"].astype("string").str.strip().ne(alvo_id)]
    if cursos_elegiveis is not None:
        elegiveis = set(map(str, cursos_elegiveis))
        candidatos = candidatos.loc[candidatos["CO_CURSO"].astype("string").isin(elegiveis)]
    alvo_mask = cursos["CO_CURSO"].astype("string").str.strip().eq(alvo_id)
    if not alvo_mask.any():
        raise ValueError(f"Curso focal ausente no universo: {alvo_id}")
    alvo = cursos.loc[alvo_mask].iloc[0]

    membros_nivel: list[pd.DataFrame] = []
    tentativas: list[dict] = []
    for regra in niveis:
        membros = _nivel(candidatos, alvo, regra)
        membros.insert(0, "ordem_relaxamento", regra.ordem)
        membros.insert(1, "criterio_benchmark", regra.criterio.value)
        membros.insert(2, "CO_CURSO_ALVO", alvo_id)
        membros.insert(3, "territorio", territorio.value)
        membros_nivel.append(membros)
        n = len(membros)
        tentativas.append({
            "CO_CURSO_ALVO": alvo_id,
            "territorio": territorio.value,
            "ordem_relaxamento": regra.ordem,
            "criterio_benchmark": regra.criterio.value,
            "n_cursos": n,
            "status": (
                StatusAnalise.DISPONIVEL.value if n >= politica.n_minimo_completo
                else StatusAnalise.DESCRITIVO_APENAS.value if n >= politica.n_minimo_sintese
                else StatusAnalise.INSUFICIENTE.value
            ),
            "selecionado": False,
        })

    elegiveis_completos = [r for r in tentativas if r["n_cursos"] >= politica.n_minimo_completo]
    if elegiveis_completos:
        escolhido = min(elegiveis_completos, key=lambda r: r["ordem_relaxamento"])
    elif tentativas:
        escolhido = max(tentativas, key=lambda r: (r["n_cursos"], -r["ordem_relaxamento"]))
    else:
        raise ValueError("A cascata de relaxamento precisa ter ao menos um nível")
    escolhido["selecionado"] = True
    escolhido["motivo"] = (
        None if escolhido["n_cursos"] >= politica.n_minimo_completo
        else "nenhum_nivel_atingiu_n_minimo_completo"
    )
    resumo = pd.DataFrame(tentativas)
    todos_membros = pd.concat(membros_nivel, ignore_index=True) if membros_nivel else pd.DataFrame()
    if not todos_membros.empty:
        todos_membros = todos_membros.sort_values(
            ["ordem_relaxamento", "CO_CURSO"], kind="stable"
        ).reset_index(drop=True)
    return todos_membros, resumo, escolhido.copy()
