from __future__ import annotations

import json
import math
from hashlib import sha256
from pathlib import Path
from typing import Any

import pandas as pd

from src.core.configuracao_area import ConfiguracaoArea
from src.edicoes.base import ContratoEdicao
from src.orquestracao.area import ResultadoArea


SCHEMA_VERSION = "1.0"
COLUNAS_PROCESSO = (
    "edicao", "CO_CURSO", "ITEM", "n_total", "n_valido", "n_ausente", "n_invalido",
    "n_nao_sabe_responder", "n_nao_se_aplica", "media", "mediana", "dp",
    "concordancia_n", "concordancia_pct", "ausencia_analitica_pct",
    "nao_sabe_responder_pct", "nao_se_aplica_pct",
)


def _sha256(arquivo: Path) -> str:
    resumo = sha256()
    with arquivo.open("rb") as entrada:
        for bloco in iter(lambda: entrada.read(1024 * 1024), b""):
            resumo.update(bloco)
    return resumo.hexdigest()


def _registros(tabela: pd.DataFrame, colunas: tuple[str, ...] | None = None) -> list[dict[str, Any]]:
    if colunas is not None:
        ausentes = sorted(set(colunas) - set(tabela.columns))
        if ausentes:
            raise ValueError(f"Colunas ausentes no pacote de evidências: {ausentes}")
        tabela = tabela.loc[:, list(colunas)]
    # to_json lida de forma estável com pd.NA, NaN e tipos numpy sem propagar NaN ao JSON.
    return json.loads(tabela.to_json(orient="records", force_ascii=False))


def _campos_com_prefixo(tabela: pd.DataFrame, prefixos: tuple[str, ...]) -> list[str]:
    return [coluna for coluna in tabela.columns if coluna.startswith(prefixos)]


def _cobertura(auditoria: pd.DataFrame) -> dict[str, int]:
    resultado = {"n_cursos_auditoria": len(auditoria)}
    for coluna in ("em_microdados", "em_conceito", "em_desempenho"):
        if coluna in auditoria:
            resultado[coluna] = int(auditoria[coluna].fillna(False).sum())
    return resultado


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

    if resultado.processo_itens is None or resultado.proveniencia_processo is None:
        raise ValueError("A análise da área deve incluir processo formativo para gerar evidências")
    if resultado.distribuicoes_questionario is None or resultado.regras_indicadores is None:
        raise ValueError("A análise da área deve incluir indicadores para gerar evidências")
    if not fonte_microdados.is_file():
        raise FileNotFoundError(f"Fonte de microdados ausente: {fonte_microdados}")

    base = resultado.base_cursos.copy()
    if not base["CO_CURSO"].is_unique:
        raise ValueError("base_cursos deve conter uma linha por CO_CURSO")
    if not base["edicao"].eq(edicao.ano).all() or not base["area"].eq(area.slug).all():
        raise ValueError("A base não corresponde à edição e área informadas")

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
    ofertas_focais = base.loc[base["CO_IES"].eq(str(area.co_ies_focal)), colunas_focal]

    pacote: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "edicao": {
            "ano": edicao.ano,
            "nome": edicao.nome,
            "capacidades": {
                "proficiencia": edicao.capacidades.proficiencia,
                "recomendacao": edicao.capacidades.recomendacao,
                "questionario_licenciatura": edicao.capacidades.questionario_licenciatura,
            },
        },
        "area": {
            "slug": area.slug,
            "nome": area.nome,
            "co_grupo": area.co_grupo,
            "co_ies_focal": area.co_ies_focal,
            "grau": area.grau,
        },
        "universo": {
            "n_cursos_base": len(base),
            "cobertura": _cobertura(resultado.auditoria_cobertura),
            "cobertura_por_curso": _registros(resultado.auditoria_cobertura),
        },
        "ofertas_focais": _registros(ofertas_focais),
        "participacao": {"por_curso": _registros(base, tuple(colunas_desempenho[:4]))},
        "desempenho": {
            "por_curso": _registros(base, tuple(colunas_desempenho)),
            "mapa_canonico": edicao.desempenho.mapa_canonico,
        },
        "perfil": {
            "indicadores_por_curso": _registros(base, tuple(colunas_perfil)),
            "distribuicoes": _registros(resultado.distribuicoes_questionario),
            "regras": _registros(resultado.regras_indicadores),
        },
        "trajetoria": {"disponivel": False, "motivo": "Ainda não integrada à orquestração."},
        "processo_formativo": {
            "itens_por_curso": _registros(resultado.processo_itens, COLUNAS_PROCESSO),
            "proveniencia": _registros(resultado.proveniencia_processo),
            "unidade": "CO_CURSO e item; códigos 7 e 8 não integram a escala analítica.",
        },
        "benchmarks": {"disponivel": False, "motivo": "Contrato de contraste focal pendente."},
        "efeitos": {"disponivel": False, "motivo": "Depende de benchmarks validados."},
        "associacoes_ecologicas": {"disponivel": False, "motivo": "Não especificadas para esta fase."},
        "qualidade": {"base_por_curso_unica": True},
        "alertas": [],
        "achados_priorizados": [],
        "proveniencia": {
            "fontes": [
                {
                    "tipo": "microdados",
                    "caminho": str(fonte_microdados),
                    "sha256": _sha256(fonte_microdados),
                    "arquivos_tematicos": [
                        edicao.nome_arquivo(numero) for numero in (1, 3, 4)
                    ],
                },
                *_registros(resultado.proveniencia_conceito),
            ],
            "processo_formativo": _registros(resultado.proveniencia_processo),
            "indicadores": _registros(resultado.regras_indicadores),
            "tabelas_auditaveis": [
                "base_cursos.csv", "auditoria_cobertura.csv", "proveniencia_conceito.csv",
                "processo_itens.csv", "proveniencia_processo.csv",
                "distribuicoes_questionario.csv", "regras_indicadores.csv",
            ],
        },
    }
    validar_evidencias(pacote)
    return pacote


def validar_evidencias(pacote: dict[str, Any]) -> None:
    """Falha quando o contrato metodológico mínimo do JSON não é satisfeito."""

    obrigatorios = {
        "schema_version", "edicao", "area", "universo", "ofertas_focais", "participacao",
        "desempenho", "perfil", "processo_formativo", "proveniencia",
    }
    faltantes = sorted(obrigatorios - set(pacote))
    if faltantes or pacote.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"Schema de evidências inválido; campos ausentes: {faltantes}")
    if pacote["universo"]["n_cursos_base"] < 1:
        raise ValueError("Pacote de evidências sem cursos")
    if not pacote["proveniencia"].get("fontes"):
        raise ValueError("Pacote de evidências sem proveniência de fontes")

    itens = pacote["processo_formativo"].get("itens_por_curso", [])
    for item in itens:
        faltantes_item = set(COLUNAS_PROCESSO) - set(item)
        if faltantes_item:
            raise ValueError(f"Item de processo incompleto: {sorted(faltantes_item)}")
        contagens = (
            item["n_valido"] + item["n_ausente"] + item["n_invalido"]
            + item["n_nao_sabe_responder"] + item["n_nao_se_aplica"]
        )
        if item["n_total"] != contagens:
            raise ValueError(f"Contagens de processo não reconciliam em {item['CO_CURSO']}/{item['ITEM']}")
        if item["n_total"] == 0:
            for coluna in ("ausencia_analitica_pct", "nao_sabe_responder_pct", "nao_se_aplica_pct"):
                if item[coluna] is not None:
                    raise ValueError(f"{coluna} deve ser nulo com n_total=0")
        else:
            for coluna, numerador in (
                ("nao_sabe_responder_pct", "n_nao_sabe_responder"),
                ("nao_se_aplica_pct", "n_nao_se_aplica"),
            ):
                valor = item[coluna]
                if valor is None or not math.isclose(
                    # pandas.to_json usa precisão decimal finita; esta margem
                    # cobre somente o arredondamento do formato serializado.
                    valor, item[numerador] / item["n_total"], rel_tol=3e-8, abs_tol=1e-10
                ):
                    raise ValueError(f"{coluna} não usa n_total como denominador")
        if item["n_valido"] == 0 and item["concordancia_pct"] is not None:
            raise ValueError("concordancia_pct deve ser nulo sem respostas válidas")

    for oferta in pacote["ofertas_focais"]:
        if oferta.get("SITUACAO_CONCEITO") in {"sem_conceito", "ausente"} and (
            oferta.get("CONCEITO_ENADE_NUM") is not None
        ):
            raise ValueError("SC ou ausência de conceito não pode ocupar a faixa numérica")


def salvar_evidencias(pacote: dict[str, Any], destino: Path) -> Path:
    """Valida e grava o JSON UTF-8 derivado; não modifica fontes oficiais."""

    validar_evidencias(pacote)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(pacote, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return destino
