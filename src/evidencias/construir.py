from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd

from src.analise.pipeline_fase_9a import construir_fase_9a
from src.core.configuracao_area import ConfiguracaoArea, validar_compatibilidade_area
from src.core.juncoes import validar_unicidade_por_curso
from src.edicoes.base import ContratoEdicao
from src.orquestracao.area import COLUNAS_CARACTERIZACAO, ResultadoArea
from src.evidencias.proveniencia import arquivo_das_variaveis, fontes_utilizadas, manifesto_microdados
from src.evidencias.validar import SCHEMA_VERSION, validar_evidencias


COLUNAS_PROCESSO = (
    "edicao", "CO_CURSO", "ITEM", "n_total", "n_valido", "n_ausente", "n_invalido",
    "n_nao_sabe_responder", "n_nao_se_aplica", "media", "mediana", "dp",
    "concordancia_n", "concordancia_pct", "ausencia_analitica_pct",
    "nao_sabe_responder_pct", "nao_se_aplica_pct",
)


def _registros(tabela: pd.DataFrame, colunas: tuple[str, ...] | None = None) -> list[dict[str, Any]]:
    if colunas is not None:
        ausentes = sorted(set(colunas) - set(tabela.columns))
        if ausentes:
            raise ValueError(f"Colunas ausentes no pacote de evidências: {ausentes}")
        tabela = tabela.loc[:, list(colunas)]
    # to_json lida de forma estável com pd.NA, NaN e tipos numpy sem propagar NaN ao JSON.
    if tabela.isin([float("inf"), float("-inf")]).any().any():
        raise ValueError("Infinito não pode ser convertido silenciosamente em ausência")
    return json.loads(tabela.to_json(orient="records", force_ascii=False, double_precision=15))


def _campos_com_prefixo(tabela: pd.DataFrame, prefixos: tuple[str, ...]) -> list[str]:
    return [coluna for coluna in tabela.columns if coluna.startswith(prefixos)]


def _cobertura(auditoria: pd.DataFrame) -> dict[str, int]:
    resultado = {"n_cursos_auditoria": len(auditoria)}
    for coluna in ("em_microdados", "em_conceito", "em_desempenho"):
        if coluna in auditoria:
            resultado[coluna] = int(auditoria[coluna].fillna(False).sum())
    return resultado


def _proveniencia_indicadores(
    resultado: ResultadoArea,
    edicao: ContratoEdicao,
) -> dict[str, dict[str, Any]]:
    """Explicita a linhagem oficial consumida pelos artefatos da Fase 9A."""

    origens: dict[str, dict[str, Any]] = {}
    for componente, variavel in edicao.desempenho.mapa_canonico.items():
        indicador = f"{componente}_mean"
        origens[indicador] = {
            "edicao_origem": edicao.ano,
            "arquivo_fonte": arquivo_das_variaveis(edicao, (variavel,)),
            "variavel_oficial": variavel,
            "indicador_derivado": indicador,
            "regra_agregacao": "media_dos_presentes_validos_por_curso",
            "unidade_indicador": "CO_CURSO",
            "denominador_indicador": f"{componente}_n_valido",
            "familia_indicador": "desempenho",
        }
    regras_indicadores = (
        resultado.regras_indicadores
        if resultado.regras_indicadores is not None else pd.DataFrame()
    )
    for regra in regras_indicadores.to_dict("records"):
        indicador = regra["indicador"]
        origens[indicador] = {
            "edicao_origem": regra["edicao"],
            "arquivo_fonte": regra["arquivo"],
            "variavel_oficial": regra["item"],
            "indicador_derivado": indicador,
            "regra_agregacao": "proporcao_de_respostas_positivas_por_curso",
            "unidade_indicador": "CO_CURSO",
            "denominador_indicador": regra["denominador"],
            "familia_indicador": "perfil_socioeconomico",
        }
    proveniencia_processo = (
        resultado.proveniencia_processo
        if resultado.proveniencia_processo is not None else pd.DataFrame()
    )
    for regra in proveniencia_processo.to_dict("records"):
        for sufixo, agregacao in (
            ("media", "media_das_respostas_validas_por_curso"),
            ("concordancia_pct", "proporcao_de_concordancia_por_curso"),
        ):
            indicador = f"processo:{regra['item']}:{sufixo}"
            origens[indicador] = {
                "edicao_origem": regra["edicao"],
                "arquivo_fonte": regra["arquivo"],
                "variavel_oficial": regra["item"],
                "indicador_derivado": indicador,
                "regra_agregacao": agregacao,
                "unidade_indicador": "CO_CURSO",
                "denominador_indicador": "n_valido",
                "familia_indicador": "processo_formativo",
            }
    return origens


def construir_evidencias(
    resultado: ResultadoArea,
    edicao: ContratoEdicao,
    area: ConfiguracaoArea,
    fonte_microdados: Path,
) -> dict[str, Any]:
    """Constrói evidências apenas a partir de agregados por ``CO_CURSO``.

    O pacote é uma interface resumida para a redação, não substitui os CSVs
    auditáveis e não incorpora tabelas individuais dos arquivos temáticos.
    """

    validar_compatibilidade_area(edicao, area)
    aplica_processo = edicao.capacidades.processo_formativo and area.aplicabilidade.processo_formativo
    if aplica_processo and (resultado.processo_itens is None or resultado.proveniencia_processo is None):
        raise ValueError("A análise da área deve incluir processo formativo para gerar evidências")
    if not aplica_processo and any(t is not None and not t.empty for t in (
        resultado.processo_itens, resultado.proveniencia_processo
    )):
        raise ValueError("Análise contém processo formativo não aplicável à área")
    if resultado.distribuicoes_questionario is None or resultado.regras_indicadores is None:
        raise ValueError("A análise da área deve incluir indicadores para gerar evidências")
    if not fonte_microdados.exists():
        raise FileNotFoundError(f"Fonte de microdados ausente: {fonte_microdados}")

    base = resultado.base_cursos.copy()
    validar_unicidade_por_curso(base, nome="base_cursos")
    if not base["edicao"].eq(edicao.ano).all() or not base["area"].eq(area.slug).all():
        raise ValueError("A base não corresponde à edição e área informadas")
    if not base["CO_GRUPO"].eq(str(area.co_grupo)).all():
        raise ValueError("A base não corresponde ao CO_GRUPO informado")

    resultado_fase_9a = construir_fase_9a(
        base,
        area,
        resultado.processo_itens,
        proveniencia_indicadores=_proveniencia_indicadores(resultado, edicao),
    )
    resultado.artefatos_fase_9a = resultado_fase_9a["artefatos"]

    indicadores = resultado.regras_indicadores["indicador"].tolist()
    colunas_perfil = ["CO_CURSO"]
    for indicador in indicadores:
        prefixo = indicador.removesuffix("pct")
        colunas_perfil.extend(
            coluna for coluna in base.columns if coluna == indicador or coluna.startswith(prefixo)
        )
    colunas_perfil = list(dict.fromkeys(colunas_perfil))
    colunas_desempenho = ["CO_CURSO", "registros_microdados", "presentes_validos", "taxa_presenca_microdados"]
    colunas_desempenho.extend(_campos_com_prefixo(base, tuple(edicao.desempenho.mapa_canonico)))
    colunas_desempenho = [coluna for coluna in dict.fromkeys(colunas_desempenho) if coluna in base]
    colunas_focal = list(dict.fromkeys([
        "CO_CURSO", "CO_GRUPO", "CO_IES", "CO_MUNIC_CURSO", "CO_UF_CURSO",
        "CO_REGIAO_CURSO", "CO_MODALIDADE", "INSCRITOS", "PARTICIPANTES",
        "CONCEITO_ENADE_ORIGINAL", "CONCEITO_ENADE_NUM", "CONCEITO_ENADE_CONTINUO",
        "SITUACAO_CONCEITO", *colunas_desempenho[1:], *colunas_perfil[1:],
    ]))
    colunas_focal = [coluna for coluna in colunas_focal if coluna in base]
    cursos_focais = set(resultado_fase_9a["metadados"]["cursos_focais"])
    ofertas_focais = base.loc[base["CO_CURSO"].isin(cursos_focais), colunas_focal].sort_values(
        "CO_CURSO", kind="stable"
    )

    pacote: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "edicao": {
            "ano": edicao.ano,
            "nome": edicao.nome,
            "capacidades": asdict(edicao.capacidades),
            "itens_processo": list(edicao.questionario.itens_processo_formativo),
            "escala_processo": sorted(edicao.questionario.codigos_validos_processo),
        },
        "area": {
            "slug": area.slug,
            "nome": area.nome,
            "co_grupo": area.co_grupo,
            "co_ies_focal": area.co_ies_focal,
            "grau": area.grau,
            "aplicabilidade": asdict(area.aplicabilidade),
            "co_cursos_focais": list(area.co_cursos_focais),
        },
        "universo": {
            "n_cursos_base": len(base),
            "cursos": base["CO_CURSO"].tolist(),
            "cursos_focais": ofertas_focais["CO_CURSO"].tolist(),
            "arquivo_caracterizacao": arquivo_das_variaveis(edicao, COLUNAS_CARACTERIZACAO),
            "cobertura": _cobertura(resultado.auditoria_cobertura),
            "cobertura_por_curso": _registros(resultado.auditoria_cobertura),
        },
        "ofertas_focais": _registros(ofertas_focais),
        "participacao": {"por_curso": _registros(base, (
            "CO_CURSO", "INSCRITOS", "PARTICIPANTES", "registros_microdados",
            "presentes_validos", "taxa_presenca_microdados",
            "CONCEITO_ENADE_ORIGINAL", "CONCEITO_ENADE_NUM", "SITUACAO_CONCEITO",
        ))},
        "desempenho": {
            "por_curso": _registros(base, tuple(colunas_desempenho)),
            "mapa_canonico": edicao.desempenho.mapa_canonico,
            "arquivo": arquivo_das_variaveis(edicao, edicao.desempenho.variaveis_numericas),
        },
        "perfil": {
            "indicadores_por_curso": _registros(base, tuple(colunas_perfil)),
            "distribuicoes": _registros(resultado.distribuicoes_questionario),
            "regras": _registros(resultado.regras_indicadores),
        },
        "trajetoria": {"disponivel": False, "motivo": "Ainda não integrada à orquestração."},
        "processo_formativo": {
            "disponivel": aplica_processo,
            "status": "disponivel" if aplica_processo else "nao_aplicavel",
            "itens_por_curso": _registros(resultado.processo_itens, COLUNAS_PROCESSO) if aplica_processo else [],
            "proveniencia": _registros(resultado.proveniencia_processo) if aplica_processo else [],
            "unidade": "CO_CURSO e item; códigos 7 e 8 não integram a escala analítica.",
        },
        "benchmarks": {
            "disponivel": True,
            "motivo": None,
            "definicoes": {
                "arquivo": "benchmarks_definicoes.csv",
                "n_registros": len(resultado.artefatos_fase_9a["benchmarks_definicoes.csv"]),
            },
            "membros": {
                "arquivo": "benchmarks_membros.csv",
                "n_registros": len(resultado.artefatos_fase_9a["benchmarks_membros.csv"]),
            },
        },
        "efeitos": {
            "disponivel": True,
            "motivo": None,
            "resultados": {
                "arquivo": "efeitos.csv",
                "n_registros": len(resultado.artefatos_fase_9a["efeitos.csv"]),
            },
        },
        "associacoes_ecologicas": {
            "disponivel": True,
            "motivo": None,
            "resultados": {
                "arquivo": "associacoes_ecologicas.csv",
                "n_registros": len(resultado.artefatos_fase_9a["associacoes_ecologicas.csv"]),
            },
        },
        "fase_9a": {
            "contrastes": {
                "arquivo": "contrastes.csv",
                "n_registros": len(resultado.artefatos_fase_9a["contrastes.csv"]),
            },
            "exclusoes": {
                "arquivo": "exclusoes_fase_9a.csv",
                "n_registros": len(resultado.artefatos_fase_9a["exclusoes_fase_9a.csv"]),
            },
            "metadados": resultado_fase_9a["metadados"],
        },
        "qualidade": {"base_por_curso_unica": True},
        "alertas": [],
        "achados_priorizados": [],
        "proveniencia": {
            "fontes": [
                *_registros(resultado.proveniencia_conceito),
            ],
            "tabelas_auditaveis": [
                "base_cursos.csv", "auditoria_cobertura.csv", "proveniencia_conceito.csv",
                "processo_itens.csv", "proveniencia_processo.csv",
                "distribuicoes_questionario.csv", "regras_indicadores.csv",
                *[nome for nome in resultado.artefatos_fase_9a if nome.endswith(".csv")],
                "metadados_fase_9a.json",
            ],
        },
    }
    pacote["proveniencia"]["fontes"].insert(
        0, manifesto_microdados(fonte_microdados, edicao, fontes_utilizadas(pacote))
    )
    if not aplica_processo:
        pacote["proveniencia"]["tabelas_auditaveis"] = [
            nome for nome in pacote["proveniencia"]["tabelas_auditaveis"]
            if nome not in {"processo_itens.csv", "proveniencia_processo.csv"}
        ]
    validar_evidencias(pacote)
    return pacote


def salvar_evidencias(pacote: dict[str, Any], destino: Path) -> Path:
    """Valida e grava o JSON UTF-8 derivado; não modifica fontes oficiais."""

    validar_evidencias(pacote)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(pacote, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return destino
