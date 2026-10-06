from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.agregacao.agregar_desempenho import agregar_desempenho_edicao
from src.agregacao.agregar_processo_formativo import agregar_processo_formativo_edicao
from src.agregacao.agregar_socioeconomico import agregar_indicadores_questionario
from src.core.configuracao_area import ConfiguracaoArea, validar_compatibilidade_area
from src.core.juncoes import juntar_por_curso, validar_unicidade_por_curso
from src.edicoes.base import ContratoEdicao
from src.edicoes.conceito import carregar_conceitos_edicao
from src.utilitarios.leitura import carregar_filtrado_edicao


COLUNAS_CARACTERIZACAO = (
    "NU_ANO", "CO_GRUPO", "CO_IES", "CO_CATEGAD", "CO_ORGACAD",
    "CO_MODALIDADE", "CO_MUNIC_CURSO", "CO_UF_CURSO", "CO_REGIAO_CURSO",
)
COLUNAS_CONCEITO = (
    "CO_CURSO", "INSCRITOS", "PARTICIPANTES", "CONCEITO_ENADE_ORIGINAL",
    "CONCEITO_ENADE_NUM", "CONCEITO_ENADE_CONTINUO", "SITUACAO_CONCEITO",
    "OBSERVACAO_CONCEITO",
)
COLUNAS_CONFERENCIA = ("NU_ANO", "CO_GRUPO", "CO_IES", "CO_MUNIC_CURSO")


@dataclass(slots=True)
class ResultadoArea:
    base_cursos: pd.DataFrame
    auditoria_cobertura: pd.DataFrame
    proveniencia_conceito: pd.DataFrame
    processo_itens: pd.DataFrame | None = None
    proveniencia_processo: pd.DataFrame | None = None
    distribuicoes_questionario: pd.DataFrame | None = None
    regras_indicadores: pd.DataFrame | None = None


def caracterizar_cursos(
    microdados: Path,
    edicao: ContratoEdicao,
    area: ConfiguracaoArea,
    *,
    chunksize: int | None = None,
) -> pd.DataFrame:
    """Reduz o arq1 a uma linha por curso, sem usar posição de estudante."""

    validar_compatibilidade_area(edicao, area)
    dados = carregar_filtrado_edicao(
        microdados, edicao, 1, usecols=COLUNAS_CARACTERIZACAO,
        co_grupo=area.co_grupo, chunksize=chunksize,
    )
    if dados.empty:
        raise ValueError(f"Nenhum curso encontrado para CO_GRUPO={area.co_grupo}")
    dados = dados.astype("string").apply(lambda coluna: coluna.str.strip())
    if dados["CO_CURSO"].isna().any() or dados["CO_CURSO"].eq("").any():
        raise ValueError("CO_CURSO ausente no arq1")
    if dados["NU_ANO"].ne(str(edicao.ano)).fillna(True).any():
        raise ValueError("NU_ANO do arq1 não corresponde à edição")
    if dados["CO_GRUPO"].ne(str(area.co_grupo)).fillna(True).any():
        raise ValueError("CO_GRUPO do arq1 não corresponde à área")

    # A mesma oferta pode aparecer para muitos estudantes, mas seus atributos
    # estruturais precisam ser constantes antes de virar uma linha por curso.
    inconsistentes = (
        dados.groupby("CO_CURSO", dropna=False)[list(COLUNAS_CARACTERIZACAO)]
        .nunique(dropna=False).gt(1).any(axis=1)
    )
    if inconsistentes.any():
        exemplos = inconsistentes.index[inconsistentes].tolist()[:5]
        raise ValueError(f"Caracterização divergente no arq1: {exemplos}")
    cursos = dados.drop_duplicates("CO_CURSO").reset_index(drop=True)
    validar_unicidade_por_curso(cursos, nome="caracterização do arq1")
    return cursos


def preparar_area(
    microdados: Path,
    fonte_conceito: Path,
    edicao: ContratoEdicao,
    area: ConfiguracaoArea,
    *,
    chunksize: int | None = None,
) -> ResultadoArea:
    """Confere fontes e monta a base de cursos antes dos agregadores temáticos."""

    cursos = caracterizar_cursos(microdados, edicao, area, chunksize=chunksize)
    conceitos, _, proveniencia = carregar_conceitos_edicao(fonte_conceito, edicao)
    cursos_da_area = set(cursos["CO_CURSO"])
    grupo_incompativel = conceitos.loc[
        conceitos["CO_CURSO"].isin(cursos_da_area)
        & conceitos["CO_GRUPO"].ne(str(area.co_grupo)), "CO_CURSO"
    ]
    if not grupo_incompativel.empty:
        raise ValueError(
            f"CO_GRUPO diverge entre arq1 e Conceito Enade: {grupo_incompativel.head(5).tolist()}"
        )
    conceitos = conceitos.loc[conceitos["CO_GRUPO"].eq(str(area.co_grupo))].copy()
    validar_unicidade_por_curso(conceitos, nome="conceitos da área")

    conferidos = cursos[["CO_CURSO", *COLUNAS_CONFERENCIA]].merge(
        conceitos[["CO_CURSO", *COLUNAS_CONFERENCIA]], on="CO_CURSO", how="inner",
        validate="one_to_one", suffixes=("_microdados", "_conceito"),
    )
    for coluna in COLUNAS_CONFERENCIA:
        diferentes = conferidos[f"{coluna}_microdados"].ne(
            conferidos[f"{coluna}_conceito"]
        ).fillna(True)
        if diferentes.any():
            exemplos = conferidos.loc[diferentes, "CO_CURSO"].tolist()[:5]
            raise ValueError(f"{coluna} diverge entre arq1 e Conceito Enade: {exemplos}")

    codigos_microdados = cursos_da_area
    codigos_conceito = set(conceitos["CO_CURSO"])
    auditoria = pd.DataFrame({"CO_CURSO": sorted(codigos_microdados | codigos_conceito)})
    auditoria["em_microdados"] = auditoria["CO_CURSO"].isin(codigos_microdados)
    auditoria["em_conceito"] = auditoria["CO_CURSO"].isin(codigos_conceito)

    base = juntar_por_curso(cursos, conceitos[list(COLUNAS_CONCEITO)])
    base.insert(0, "edicao", edicao.ano)
    base.insert(1, "area", area.slug)
    return ResultadoArea(base, auditoria, proveniencia)


def analisar_area(
    microdados: Path,
    fonte_conceito: Path,
    edicao: ContratoEdicao,
    area: ConfiguracaoArea,
    *,
    chunksize: int | None = None,
) -> ResultadoArea:
    """Junta apenas agregados por curso; tabelas individuais ficam fora da base."""

    resultado = preparar_area(
        microdados, fonte_conceito, edicao, area, chunksize=chunksize
    )
    cursos = resultado.base_cursos["CO_CURSO"].tolist()
    desempenho, _ = agregar_desempenho_edicao(
        microdados, edicao, cursos, chunksize=chunksize
    )
    questionario, distribuicoes, regras = agregar_indicadores_questionario(
        microdados, edicao, cursos, chunksize=chunksize
    )
    processo, itens, proveniencia_processo = agregar_processo_formativo_edicao(
        microdados, edicao, cursos, chunksize=chunksize
    )
    base = resultado.base_cursos
    for nome, tabela in (
        ("desempenho", desempenho),
        ("indicadores do questionário", questionario),
        ("processo formativo", processo),
    ):
        validar_unicidade_por_curso(tabela, nome=nome)
        fora_da_area = set(tabela["CO_CURSO"]) - set(cursos)
        if fora_da_area:
            raise ValueError(f"Cursos fora da área no agregado {nome}: {sorted(fora_da_area)[:5]}")
        sobrepostas = (set(base.columns) & set(tabela.columns)) - {"CO_CURSO"}
        if sobrepostas:
            raise ValueError(f"Colunas sobrepostas no agregado {nome}: {sorted(sobrepostas)}")
        base = juntar_por_curso(base, tabela)
    resultado.auditoria_cobertura["em_desempenho"] = (
        resultado.auditoria_cobertura["CO_CURSO"].isin(set(desempenho["CO_CURSO"]))
    )
    resultado.base_cursos = base
    resultado.processo_itens = itens
    resultado.proveniencia_processo = proveniencia_processo
    resultado.distribuicoes_questionario = distribuicoes
    resultado.regras_indicadores = regras
    return resultado


def salvar_resultado_area(resultado: ResultadoArea, pasta: Path) -> list[Path]:
    """Grava somente tabelas derivadas, nunca fontes ou registros individuais."""

    pasta.mkdir(parents=True, exist_ok=True)
    arquivos: list[Path] = []
    for nome, tabela in (
        ("base_cursos", resultado.base_cursos),
        ("auditoria_cobertura", resultado.auditoria_cobertura),
        ("proveniencia_conceito", resultado.proveniencia_conceito),
        ("processo_itens", resultado.processo_itens),
        ("proveniencia_processo", resultado.proveniencia_processo),
        ("distribuicoes_questionario", resultado.distribuicoes_questionario),
        ("regras_indicadores", resultado.regras_indicadores),
    ):
        if tabela is not None:
            destino = pasta / f"{nome}.csv"
            tabela.to_csv(destino, index=False, sep=";", encoding="utf-8-sig")
            arquivos.append(destino)
    return arquivos
