"""Pipeline determinístico dos contrastes e benchmarks da Fase 9A."""

from __future__ import annotations

from hashlib import sha256

import numpy as np
import pandas as pd

from src.analise.associacoes_ecologicas import correlacao_spearman_ecologica
from src.analise.benchmarks_fase_9a import construir_benchmark_amplo, construir_benchmark_comparavel
from src.analise.contratos_fase_9a import (
    NIVEIS_RELAXAMENTO_BENCHMARK,
    ConfiguracaoBootstrap,
    EstadoElegibilidade,
    PoliticaElegibilidade,
    PoliticaTamanhoBenchmark,
    StatusAnalise,
    Territorio,
    classificar_elegibilidade,
)
from src.analise.estimandos_fase_9a import hedges_g_cursos, resumo_contraste_foco_unico
from src.analise.incerteza_fase_9a import (
    bootstrap_ic_condicional_ao_foco,
    bootstrap_ic_dois_grupos,
    bootstrap_ic_multifoco,
)
from src.core.configuracao_area import ConfiguracaoArea
from src.core.grupos import aplicar_grupos_area


NOMES_ARTEFATOS = (
    "grupos_comparativos.csv",
    "benchmarks_definicoes.csv",
    "benchmarks_membros.csv",
    "contrastes.csv",
    "efeitos.csv",
    "incerteza.csv",
    "associacoes_ecologicas.csv",
    "exclusoes_fase_9a.csv",
    "metadados_fase_9a.json",
)

COLUNAS_PROVENIENCIA = (
    "edicao_origem",
    "arquivo_fonte",
    "variavel_oficial",
    "indicador_derivado",
    "regra_agregacao",
    "unidade_indicador",
    "denominador_indicador",
)

COLUNAS_MINIMAS_ARTEFATOS = {
    "benchmarks_definicoes.csv": (
        "benchmark_id", "alvo_analise", "CO_CURSO_ALVO", "indicador", "territorio",
        "tipo_benchmark", "ordem_relaxamento", "criterio_benchmark", "n_estrutural",
        "n_elegivel", "n_cursos", "status", "selecionado", "motivo", "politica_n",
    ),
    "benchmarks_membros.csv": (
        "benchmark_id", "alvo_analise", "CO_CURSO_ALVO", "indicador", "territorio",
        "tipo_benchmark", "ordem_relaxamento", "criterio_benchmark", "CO_CURSO", "valor",
        "n_valido", "n_total", "cobertura_valida", "n_ausente", *COLUNAS_PROVENIENCIA,
    ),
    "contrastes.csv": (
        "identificador", "benchmark_id", "alvo_analise", "CO_CURSO_ALVO", "tipo_foco",
        "papel_analise", "n_focos_elegiveis", "focos_elegiveis", "focos_excluidos",
        "indicador", "n_cursos", "status", "motivo", *COLUNAS_PROVENIENCIA,
    ),
    "efeitos.csv": (
        "identificador", "medida", "valor", "status", "motivo", "indicador", "tipo_foco",
        *COLUNAS_PROVENIENCIA,
    ),
    "incerteza.csv": (
        "identificador", "tipo_incerteza", "unidade_reamostragem", "foco_reamostrado",
        "numero_reamostragens", "seed", "status", "motivo",
    ),
    "associacoes_ecologicas.csv": (
        "identificador", "variavel_x", "variavel_y", "unidade_analise", "metodo",
        "n_estrutural", "n_elegivel", "n_pares_completos", "n_excluidos", "n_cursos",
        "tipo_associacao", "rho", "status", "motivo", "arquivo_fonte_x",
        "arquivo_fonte_y", "variavel_oficial_x", "variavel_oficial_y",
    ),
    "exclusoes_fase_9a.csv": (
        "tipo_exclusao", "identificador_analise", "CO_CURSO_ALVO", "CO_CURSO", "indicador",
        "variavel_x", "variavel_y", "benchmark", "estado", "motivo", "n_total", "n_valido",
        "cobertura_valida", "n_ausente", "arquivo_origem", "variavel_origem",
        *COLUNAS_PROVENIENCIA,
    ),
}


def _origem_padrao(indicador: str, tipo: str, area: ConfiguracaoArea) -> dict:
    return {
        "edicao_origem": area.edicao,
        "arquivo_fonte": "nao_informado",
        "variavel_oficial": indicador,
        "indicador_derivado": indicador,
        "regra_agregacao": "media_por_curso" if tipo == "continua" else "proporcao_por_curso",
        "unidade_indicador": "CO_CURSO",
        "denominador_indicador": "n_valido",
        "familia_indicador": "nao_classificada",
    }


def _metricas(
    base: pd.DataFrame,
    processo: pd.DataFrame | None,
    area: ConfiguracaoArea,
    proveniencia_indicadores: dict[str, dict] | None,
) -> pd.DataFrame:
    if base["CO_CURSO"].isna().any() or base["CO_CURSO"].astype("string").duplicated().any():
        raise ValueError("Métricas da Fase 9A exigem CO_CURSO presente e único na base")
    if processo is not None and not processo.empty:
        if processo[["CO_CURSO", "ITEM"]].isna().any().any():
            raise ValueError("Processo formativo exige CO_CURSO e ITEM presentes")
        chaves_processo = processo[["CO_CURSO", "ITEM"]].astype("string")
        if chaves_processo.duplicated().any():
            raise ValueError("Processo formativo repete a chave CO_CURSO/ITEM")

    origens = proveniencia_indicadores or {}
    linhas: list[pd.DataFrame] = []

    def anexar(tabela: pd.DataFrame, indicador: str, tipo: str) -> None:
        origem = {**_origem_padrao(indicador, tipo, area), **origens.get(indicador, {})}
        for chave, valor in origem.items():
            tabela[chave] = valor
        linhas.append(tabela)

    for coluna in base.columns:
        if coluna.endswith("_mean"):
            componente = coluna.removesuffix("_mean")
            coluna_n = f"{componente}_n_valido"
            coluna_total = f"{componente}_registros_microdados"
            if coluna_total not in base and "registros_microdados" in base:
                coluna_total = "registros_microdados"
            if coluna_n in base:
                anexar(
                    pd.DataFrame({
                        "CO_CURSO": base["CO_CURSO"].astype("string"),
                        "indicador": coluna,
                        "valor": pd.to_numeric(base[coluna], errors="coerce"),
                        "n_total": pd.to_numeric(base.get(coluna_total, base[coluna_n]), errors="coerce"),
                        "n_valido": pd.to_numeric(base[coluna_n], errors="coerce"),
                        "tipo": "continua",
                        "arquivo_origem": "base_cursos.csv",
                        "variavel_origem": coluna,
                    }),
                    coluna,
                    "continua",
                )
        elif coluna.endswith("_pct") and coluna != "taxa_presenca_microdados":
            prefixo = coluna.removesuffix("pct")
            coluna_n = f"{prefixo}n_valido"
            coluna_total = f"{prefixo}n_total"
            if coluna_n in base and coluna_total in base:
                anexar(
                    pd.DataFrame({
                        "CO_CURSO": base["CO_CURSO"].astype("string"),
                        "indicador": coluna,
                        "valor": pd.to_numeric(base[coluna], errors="coerce"),
                        "n_total": pd.to_numeric(base[coluna_total], errors="coerce"),
                        "n_valido": pd.to_numeric(base[coluna_n], errors="coerce"),
                        "tipo": "proporcao",
                        "arquivo_origem": "base_cursos.csv",
                        "variavel_origem": coluna,
                    }),
                    coluna,
                    "proporcao",
                )
    if processo is not None and not processo.empty:
        processo = processo.copy()
        processo["CO_CURSO"] = processo["CO_CURSO"].astype("string")
        processo["ITEM"] = processo["ITEM"].astype("string")
        for coluna, tipo in (("media", "continua"), ("concordancia_pct", "proporcao")):
            if coluna not in processo:
                continue
            for item, subset in processo.groupby("ITEM", sort=True):
                indicador = f"processo:{item}:{coluna}"
                tabela = subset[["CO_CURSO", coluna, "n_total", "n_valido"]].rename(
                    columns={coluna: "valor"}
                )
                tabela["indicador"] = indicador
                tabela["tipo"] = tipo
                tabela["arquivo_origem"] = "processo_itens.csv"
                tabela["variavel_origem"] = f"{item}:{coluna}"
                anexar(tabela, indicador, tipo)
    if not linhas:
        raise ValueError("Nenhum indicador elegível ao contrato da Fase 9A foi encontrado")
    metricas = pd.concat(linhas, ignore_index=True)
    duplicadas = metricas.duplicated(["CO_CURSO", "indicador"], keep=False)
    if duplicadas.any():
        exemplos = metricas.loc[duplicadas, ["CO_CURSO", "indicador"]].head(5).to_dict("records")
        raise ValueError(f"Métricas repetem a chave CO_CURSO/indicador: {exemplos}")
    if metricas[["n_total", "n_valido"]].isna().any().any():
        raise ValueError("Denominadores ausentes nas métricas da Fase 9A")
    invalidos = metricas["n_total"].lt(0) | metricas["n_valido"].lt(0) | metricas["n_valido"].gt(
        metricas["n_total"]
    )
    if invalidos.any():
        raise ValueError("Denominadores inválidos nas métricas da Fase 9A")
    metricas["n_ausente"] = (metricas["n_total"] - metricas["n_valido"]).astype(int)
    metricas["cobertura_valida"] = metricas["n_valido"].div(
        metricas["n_total"].where(metricas["n_total"].gt(0))
    )
    return metricas.sort_values(["indicador", "CO_CURSO"], kind="stable").reset_index(drop=True)


def _classificar_metricas(metricas: pd.DataFrame, politica: PoliticaElegibilidade) -> pd.DataFrame:
    resultado = metricas.copy()
    estados: list[str] = []
    motivos: list[str | None] = []
    incluidos: list[bool] = []
    for linha in resultado.itertuples(index=False):
        elegibilidade = classificar_elegibilidade(int(linha.n_total), int(linha.n_valido), politica)
        motivo = elegibilidade.motivo
        if elegibilidade.estado == EstadoElegibilidade.ELEGIVEL and pd.isna(linha.valor):
            motivo = "valor_indicador_ausente"
        estados.append(elegibilidade.estado.value)
        motivos.append(motivo)
        incluidos.append(elegibilidade.estado == EstadoElegibilidade.ELEGIVEL and motivo is None)
    resultado["estado_elegibilidade"] = estados
    resultado["motivo_exclusao"] = motivos
    resultado["incluido"] = incluidos
    return resultado


def _geracao_id(area: ConfiguracaoArea, grupos: pd.DataFrame, metricas: pd.DataFrame) -> str:
    cabecalho = f"{area.edicao}|{area.slug}|{area.co_grupo}|{area.co_ies_focal}\n"
    cursos = grupos.sort_values("CO_CURSO", kind="stable")[[
        "CO_CURSO", "CO_IES", "CO_MODALIDADE", "CO_CATEGAD", "CO_ORGACAD", "PARTICIPANTES",
    ]]
    valores = metricas.sort_values(["indicador", "CO_CURSO"], kind="stable")[[
        "CO_CURSO", "indicador", "valor", "n_total", "n_valido",
    ]]
    payload = cabecalho + cursos.to_csv(index=False) + valores.to_csv(index=False)
    return sha256(payload.encode("utf-8")).hexdigest()


def _territorios_foco(focal: pd.Series) -> list[Territorio]:
    uf = pd.to_numeric(pd.Series([focal["CO_UF_CURSO"]]), errors="coerce").iloc[0]
    regiao = pd.to_numeric(pd.Series([focal["CO_REGIAO_CURSO"]]), errors="coerce").iloc[0]
    territorios = [Territorio.BRASIL]
    if regiao == 1:
        territorios.insert(0, Territorio.NORTE)
    if uf == 15:
        territorios.insert(0, Territorio.PARA)
    return territorios


def _territorios_multifoco(focais: pd.DataFrame) -> list[Territorio]:
    conjuntos = [set(_territorios_foco(linha)) for _, linha in focais.iterrows()]
    comuns = set.intersection(*conjuntos) if conjuntos else set()
    return [t for t in (Territorio.PARA, Territorio.NORTE, Territorio.BRASIL) if t in comuns]


def _status_n(n: int, politica: PoliticaTamanhoBenchmark) -> str:
    if n >= politica.n_minimo_completo:
        return StatusAnalise.DISPONIVEL.value
    if n >= politica.n_minimo_sintese:
        return StatusAnalise.DESCRITIVO_APENAS.value
    return StatusAnalise.INSUFICIENTE.value


def _proveniencia_linha(linha) -> dict:
    return {campo: getattr(linha, campo, None) for campo in COLUNAS_PROVENIENCIA}


def _registrar_exclusao(
    exclusoes: list[dict],
    linha,
    *,
    tipo_exclusao: str,
    identificador_analise: str,
    co_curso_alvo: str | None = None,
    benchmark: str | None = None,
    variavel_x: str | None = None,
    variavel_y: str | None = None,
    motivo: str | None = None,
    estado: str | None = None,
) -> None:
    exclusoes.append({
        "tipo_exclusao": tipo_exclusao,
        "identificador_analise": identificador_analise,
        "CO_CURSO_ALVO": co_curso_alvo,
        "CO_CURSO": str(linha.CO_CURSO),
        "indicador": str(linha.indicador),
        "variavel_x": variavel_x,
        "variavel_y": variavel_y,
        "benchmark": benchmark,
        "estado": estado or str(linha.estado_elegibilidade),
        "motivo": motivo or str(linha.motivo_exclusao),
        "n_total": int(linha.n_total),
        "n_valido": int(linha.n_valido),
        "cobertura_valida": float(linha.n_valido / linha.n_total) if int(linha.n_total) else None,
        "n_ausente": int(linha.n_ausente),
        "arquivo_origem": linha.arquivo_origem,
        "variavel_origem": linha.variavel_origem,
        **_proveniencia_linha(linha),
    })


def _registrar_definicao(
    definicoes: list[dict],
    *,
    alvo_analise: str,
    co_curso_alvo: str | None,
    indicador: str,
    territorio: str,
    tipo_benchmark: str,
    ordem_relaxamento: int | None,
    criterio: str | None,
    n_estrutural: int,
    n_elegivel: int,
    selecionado: bool,
    politica: PoliticaTamanhoBenchmark,
    benchmark_id: str,
    motivo: str | None = None,
) -> None:
    definicoes.append({
        "benchmark_id": benchmark_id,
        "alvo_analise": alvo_analise,
        "CO_CURSO_ALVO": co_curso_alvo,
        "indicador": indicador,
        "territorio": territorio,
        "tipo_benchmark": tipo_benchmark,
        "ordem_relaxamento": ordem_relaxamento,
        "criterio_benchmark": criterio,
        "n_estrutural": int(n_estrutural),
        "n_elegivel": int(n_elegivel),
        "n_cursos": int(n_elegivel),
        "status": _status_n(int(n_elegivel), politica),
        "selecionado": bool(selecionado),
        "motivo": motivo,
        "politica_n": politica.versao,
    })


def _registrar_membros(
    membros_saida: list[dict],
    membros: pd.DataFrame,
    *,
    benchmark_id: str,
    alvo_analise: str,
    co_curso_alvo: str | None,
    indicador: str,
    territorio: str,
    tipo_benchmark: str,
    criterio: str | None,
    ordem_relaxamento: int | None,
) -> None:
    for row in membros.sort_values("CO_CURSO", kind="stable").itertuples(index=False):
        membros_saida.append({
            "benchmark_id": benchmark_id,
            "alvo_analise": alvo_analise,
            "CO_CURSO_ALVO": co_curso_alvo,
            "indicador": indicador,
            "territorio": territorio,
            "tipo_benchmark": tipo_benchmark,
            "criterio_benchmark": criterio,
            "ordem_relaxamento": ordem_relaxamento,
            "CO_CURSO": str(row.CO_CURSO),
            "valor": row.valor,
            "n_valido": int(row.n_valido),
            "n_total": int(row.n_total),
            "cobertura_valida": row.cobertura_valida,
            "n_ausente": int(row.n_ausente),
            "arquivo_origem": row.arquivo_origem,
            "variavel_origem": row.variavel_origem,
            **_proveniencia_linha(row),
        })


def _efeito_focal(
    resumo: dict,
    tipo_indicador: str,
    status_contraste: str,
    valor_focal: float | None,
) -> tuple[str, float | None, str | None, float | None]:
    medida = "diferenca_proporcoes" if tipo_indicador == "proporcao" else "z_ref"
    if status_contraste == StatusAnalise.INSUFICIENTE.value or valor_focal is None:
        return medida, None, "n_benchmark_abaixo_minimo_sintese", None
    if tipo_indicador == "proporcao":
        media = resumo["media_benchmark"]
        valor = float(valor_focal - media) if media is not None else None
        razao = float(valor_focal / media) if media is not None and media > 0 else None
        return medida, valor, None if valor is not None else "estimativa_indefinida", razao
    if resumo["z_ref"] is None:
        return medida, None, "variancia_benchmark_nula_ou_indefinida", None
    return medida, float(resumo["z_ref"]), None, None


def _registrar_estimativas(
    contrastes: list[dict],
    efeitos: list[dict],
    incertezas: list[dict],
    focal: dict,
    membros: pd.DataFrame,
    *,
    benchmark_id: str | None,
    identificador: str,
    indicador: str,
    benchmark: str,
    tipo_benchmark: str,
    tipo_foco: str,
    papel_analise: str,
    focos_elegiveis: list[str],
    focos_excluidos: list[str],
    motivos_focos_excluidos: list[str],
    bootstrap: ConfiguracaoBootstrap,
    politica: PoliticaTamanhoBenchmark,
) -> None:
    membros = membros.sort_values("CO_CURSO", kind="stable").reset_index(drop=True)
    valores = pd.to_numeric(membros.get("valor", pd.Series(dtype=float)), errors="coerce")
    pesos = pd.to_numeric(membros.get("n_valido", pd.Series(dtype=float)), errors="coerce")
    resumo = resumo_contraste_foco_unico(focal.get("valor_focal"), valores, n_valido_benchmark=pesos)
    n_cursos = int(valores.notna().sum())
    status = _status_n(n_cursos, politica)
    suficiente = n_cursos >= politica.n_minimo_sintese and focal.get("valor_focal") is not None
    validos = membros.loc[valores.notna()].copy()
    if not validos.empty:
        valores_validos = pd.to_numeric(validos["valor"], errors="coerce")
        q1, q3 = valores_validos.quantile([0.25, 0.75])
        amplitude = q3 - q1
        outlier = valores_validos.lt(q1 - 1.5 * amplitude) | valores_validos.gt(q3 + 1.5 * amplitude)
        cursos_outlier = sorted(validos.loc[outlier, "CO_CURSO"].astype(str).tolist())
        sem_outliers = valores_validos.loc[~outlier]
    else:
        cursos_outlier = []
        sem_outliers = pd.Series(dtype=float)
    medida, valor_efeito, motivo_efeito, razao = _efeito_focal(
        resumo, focal["tipo"], status, focal.get("valor_focal")
    )
    motivo_contraste = None if suficiente else (
        "nenhum_foco_elegivel" if not focos_elegiveis else "n_benchmark_abaixo_minimo_sintese"
    )
    media_ponderada = resumo["media_benchmark_ponderada"] if suficiente else None
    alvo_analise = "multifoco" if tipo_foco == "multifoco" else f"curso:{focos_elegiveis[0]}"
    contrastes.append({
        "identificador": identificador,
        "benchmark_id": benchmark_id,
        "alvo_analise": alvo_analise,
        "CO_CURSO_ALVO": focos_elegiveis[0] if tipo_foco == "individual" else None,
        "tipo_foco": tipo_foco,
        "papel_analise": papel_analise,
        "n_focos_elegiveis": len(focos_elegiveis),
        "focos_elegiveis": sorted(focos_elegiveis),
        "focos_excluidos": sorted(focos_excluidos),
        "motivos_focos_excluidos": sorted(motivos_focos_excluidos),
        "indicador": indicador,
        "benchmark": benchmark,
        "tipo_benchmark": tipo_benchmark,
        "n_cursos": n_cursos,
        "valor_focal": focal.get("valor_focal"),
        "valor_focal_ponderado": focal.get("valor_focal_ponderado"),
        "n_total_focal": focal.get("n_total_focal"),
        "n_valido_focal": focal.get("n_valido_focal"),
        "cobertura_focal": focal.get("cobertura_focal"),
        "arquivo_origem": focal.get("arquivo_origem"),
        "variavel_origem": focal.get("variavel_origem"),
        **{campo: focal.get(campo) for campo in COLUNAS_PROVENIENCIA},
        "media_benchmark": resumo["media_benchmark"] if suficiente else None,
        "media_benchmark_ponderada": media_ponderada,
        "diferenca_media_ponderada": (
            float(focal["valor_focal"] - media_ponderada)
            if suficiente and media_ponderada is not None else None
        ),
        "tipo_estimando_principal": resumo["tipo_estimando_principal"],
        "tipo_estimando_secundario": resumo["tipo_estimando_secundario"],
        "mediana_benchmark": resumo["mediana_benchmark"] if suficiente else None,
        "diferenca_media": resumo["diferenca_media"] if suficiente else None,
        "diferenca_mediana": resumo["diferenca_mediana"] if suficiente else None,
        "percentil_focal": resumo["percentil_focal"] if suficiente else None,
        "diferenca_proporcoes": valor_efeito if focal["tipo"] == "proporcao" else None,
        "razao_proporcoes": razao,
        "n_outliers_sinalizados": len(cursos_outlier),
        "cursos_outlier_sinalizados": cursos_outlier,
        "n_cursos_sensibilidade_sem_outliers": int(len(sem_outliers)),
        "media_benchmark_sem_outliers": float(sem_outliers.mean()) if len(sem_outliers) >= 10 else None,
        "diferenca_media_sem_outliers": (
            float(focal["valor_focal"] - sem_outliers.mean())
            if focal.get("valor_focal") is not None and len(sem_outliers) >= 10 else None
        ),
        "status": status if focal.get("valor_focal") is not None else StatusAnalise.INSUFICIENTE.value,
        "motivo": motivo_contraste,
    })
    efeitos.append({
        "identificador": identificador,
        "medida": medida,
        "valor": valor_efeito,
        "interpretacao": (
            "diferenca_de_proporcoes"
            if focal["tipo"] == "proporcao" else "distancia_padronizada_de_referencia"
        ),
        "razao_proporcoes": razao,
        "status": status if valor_efeito is not None else StatusAnalise.INSUFICIENTE.value,
        "motivo": motivo_efeito,
        "indicador": indicador,
        "tipo_foco": tipo_foco,
        **{campo: focal.get(campo) for campo in COLUNAS_PROVENIENCIA},
    })
    if n_cursos < politica.n_minimo_completo or focal.get("valor_focal") is None:
        return
    if tipo_foco == "multifoco" and len(focos_elegiveis) >= 2:
        incerteza = bootstrap_ic_multifoco(
            focal["valores_focais"],
            valores,
            identificador=identificador,
            cursos_focais=focal["cursos_focais"],
            cursos_benchmark=membros["CO_CURSO"],
            configuracao=bootstrap,
        )
    else:
        incerteza = bootstrap_ic_condicional_ao_foco(
            float(focal["valor_focal"]),
            valores,
            identificador=identificador,
            cursos_benchmark=membros["CO_CURSO"],
            configuracao=bootstrap,
        )
    incertezas.append({"identificador": identificador, **incerteza})


def _focal_dict(linha) -> dict:
    return {
        "valor_focal": float(linha.valor),
        "valor_focal_ponderado": float(linha.valor),
        "n_total_focal": int(linha.n_total),
        "n_valido_focal": int(linha.n_valido),
        "cobertura_focal": float(linha.n_valido / linha.n_total) if int(linha.n_total) else None,
        "tipo": linha.tipo,
        "arquivo_origem": linha.arquivo_origem,
        "variavel_origem": linha.variavel_origem,
        **_proveniencia_linha(linha),
    }


def _focal_multifoco(incluidos: pd.DataFrame) -> dict:
    valores = pd.to_numeric(incluidos["valor"], errors="coerce")
    pesos = pd.to_numeric(incluidos["n_valido"], errors="coerce")
    primeira = incluidos.iloc[0]
    return {
        "valor_focal": float(valores.mean()),
        "valor_focal_ponderado": float(np.average(valores, weights=pesos)) if pesos.sum() > 0 else None,
        "n_total_focal": int(incluidos["n_total"].sum()),
        "n_valido_focal": int(incluidos["n_valido"].sum()),
        "cobertura_focal": (
            float(incluidos["n_valido"].sum() / incluidos["n_total"].sum())
            if incluidos["n_total"].sum() else None
        ),
        "tipo": primeira["tipo"],
        "arquivo_origem": primeira["arquivo_origem"],
        "variavel_origem": primeira["variavel_origem"],
        "valores_focais": valores.reset_index(drop=True),
        "cursos_focais": incluidos["CO_CURSO"].astype("string").reset_index(drop=True),
        **{campo: primeira[campo] for campo in COLUNAS_PROVENIENCIA},
    }


def _merge_metricas(membros: pd.DataFrame, metricas_indicador: pd.DataFrame) -> pd.DataFrame:
    colunas = [
        "CO_CURSO", "valor", "n_valido", "n_total", "cobertura_valida", "n_ausente",
        "arquivo_origem", "variavel_origem", *COLUNAS_PROVENIENCIA,
    ]
    return membros.merge(
        metricas_indicador[colunas], on="CO_CURSO", how="inner", validate="many_to_one"
    ).sort_values("CO_CURSO", kind="stable").reset_index(drop=True)


def construir_fase_9a(
    base: pd.DataFrame,
    area: ConfiguracaoArea,
    processo: pd.DataFrame | None = None,
    *,
    proveniencia_indicadores: dict[str, dict] | None = None,
    configuracao_bootstrap: ConfiguracaoBootstrap | None = None,
) -> dict:
    """Calcula grupos, benchmarks, contrastes, efeitos, IC e associações."""

    cursos = base.copy()
    cursos["CO_CURSO"] = cursos["CO_CURSO"].astype("string")
    cursos = cursos.sort_values("CO_CURSO", kind="stable").reset_index(drop=True)
    processo_ordenado = processo
    if processo is not None and not processo.empty:
        processo_ordenado = processo.copy()
        processo_ordenado["CO_CURSO"] = processo_ordenado["CO_CURSO"].astype("string")
        processo_ordenado = processo_ordenado.sort_values(
            ["CO_CURSO", "ITEM"], kind="stable"
        ).reset_index(drop=True)
    grupos = aplicar_grupos_area(cursos, area)
    politica_elegibilidade = PoliticaElegibilidade()
    politica_tamanho = PoliticaTamanhoBenchmark()
    bootstrap = configuracao_bootstrap or ConfiguracaoBootstrap()
    metricas = _classificar_metricas(
        _metricas(cursos, processo_ordenado, area, proveniencia_indicadores),
        politica_elegibilidade,
    )
    geracao_id = _geracao_id(area, grupos, metricas)

    cursos_focais = sorted(grupos.loc[grupos["eh_focal"], "CO_CURSO"].astype(str).tolist())
    focais_df = grupos.loc[grupos["eh_focal"]].copy()
    papel_individual = "secundaria" if len(cursos_focais) > 1 else "primaria"
    grupos_saida = grupos[[
        "CO_CURSO", "CO_IES", "CO_UF_CURSO", "CO_REGIAO_CURSO", "CO_MODALIDADE",
        "CO_CATEGAD", "CO_ORGACAD", "PARTICIPANTES", "CONCEITO_ENADE_NUM",
        "GRUPO_CODIGO", "GRUPO", "eh_focal",
    ]].copy()

    definicoes: list[dict] = []
    membros_saida: list[dict] = []
    contrastes: list[dict] = []
    efeitos: list[dict] = []
    incertezas: list[dict] = []
    exclusoes: list[dict] = []
    selecoes_comparaveis: dict[tuple[str, str, Territorio], tuple[pd.DataFrame, pd.DataFrame]] = {}

    for linha in metricas.loc[~metricas["incluido"]].itertuples(index=False):
        _registrar_exclusao(
            exclusoes,
            linha,
            tipo_exclusao="indicador_global",
            identificador_analise=f"indicador:{linha.indicador}",
        )

    cursos_idx = grupos.set_index("CO_CURSO", drop=False)
    for focal_id in cursos_focais:
        focal_curso = cursos_idx.loc[focal_id]
        focal_metrics = metricas.loc[metricas["CO_CURSO"].eq(focal_id)]
        territorios = _territorios_foco(focal_curso)
        estruturas = {}
        for territorio in territorios:
            amplo = construir_benchmark_amplo(grupos, focal_id, territorio)
            comparavel, _, _ = construir_benchmark_comparavel(
                grupos, focal_id, territorio=territorio, politica=politica_tamanho
            )
            estruturas[territorio] = (amplo, comparavel)

        for linha in focal_metrics.itertuples(index=False):
            if not linha.incluido:
                _registrar_exclusao(
                    exclusoes,
                    linha,
                    tipo_exclusao="foco",
                    identificador_analise=f"curso:{focal_id}:{linha.indicador}",
                    co_curso_alvo=focal_id,
                    benchmark="foco",
                )
                continue
            indicador_metricas = metricas.loc[metricas["indicador"].eq(linha.indicador)].copy()
            elegiveis = indicador_metricas.loc[indicador_metricas["incluido"]].copy()
            focal = _focal_dict(linha)
            for territorio in territorios:
                amplo_estrutural, comp_estrutural = estruturas[territorio]
                amplo = _merge_metricas(amplo_estrutural, elegiveis)
                amplo_id = f"curso:{focal_id}:{linha.indicador}:{territorio.value}:amplo"
                _registrar_definicao(
                    definicoes,
                    alvo_analise=f"curso:{focal_id}",
                    co_curso_alvo=focal_id,
                    indicador=linha.indicador,
                    territorio=territorio.value,
                    tipo_benchmark="amplo",
                    ordem_relaxamento=None,
                    criterio=None,
                    n_estrutural=len(amplo_estrutural),
                    n_elegivel=len(amplo),
                    selecionado=True,
                    politica=politica_tamanho,
                    benchmark_id=amplo_id,
                )
                _registrar_membros(
                    membros_saida,
                    amplo,
                    benchmark_id=amplo_id,
                    alvo_analise=f"curso:{focal_id}",
                    co_curso_alvo=focal_id,
                    indicador=linha.indicador,
                    territorio=territorio.value,
                    tipo_benchmark="amplo",
                    criterio=None,
                    ordem_relaxamento=None,
                )
                _registrar_estimativas(
                    contrastes,
                    efeitos,
                    incertezas,
                    focal,
                    amplo,
                    benchmark_id=amplo_id,
                    identificador=amplo_id,
                    indicador=linha.indicador,
                    benchmark=territorio.value,
                    tipo_benchmark="amplo",
                    tipo_foco="individual",
                    papel_analise=papel_individual,
                    focos_elegiveis=[focal_id],
                    focos_excluidos=[],
                    motivos_focos_excluidos=[],
                    bootstrap=bootstrap,
                    politica=politica_tamanho,
                )

                comp_elegivel = _merge_metricas(comp_estrutural, elegiveis)
                contagens_estruturais = comp_estrutural.groupby("ordem_relaxamento").size().to_dict()
                contagens_elegiveis = comp_elegivel.groupby("ordem_relaxamento").size().to_dict()
                completos = [
                    regra.ordem for regra in NIVEIS_RELAXAMENTO_BENCHMARK
                    if contagens_elegiveis.get(regra.ordem, 0) >= politica_tamanho.n_minimo_completo
                ]
                if completos:
                    nivel_escolhido = min(completos)
                else:
                    nivel_escolhido = min(
                        NIVEIS_RELAXAMENTO_BENCHMARK,
                        key=lambda regra: (-contagens_elegiveis.get(regra.ordem, 0), regra.ordem),
                    ).ordem
                for regra in NIVEIS_RELAXAMENTO_BENCHMARK:
                    benchmark_id = (
                        f"curso:{focal_id}:{linha.indicador}:{territorio.value}:comparavel:{regra.ordem}"
                    )
                    n_elegivel = int(contagens_elegiveis.get(regra.ordem, 0))
                    selecionado = regra.ordem == nivel_escolhido
                    _registrar_definicao(
                        definicoes,
                        alvo_analise=f"curso:{focal_id}",
                        co_curso_alvo=focal_id,
                        indicador=linha.indicador,
                        territorio=territorio.value,
                        tipo_benchmark="comparavel",
                        ordem_relaxamento=regra.ordem,
                        criterio=regra.criterio.value,
                        n_estrutural=int(contagens_estruturais.get(regra.ordem, 0)),
                        n_elegivel=n_elegivel,
                        selecionado=selecionado,
                        politica=politica_tamanho,
                        benchmark_id=benchmark_id,
                        motivo=(
                            None
                            if n_elegivel >= politica_tamanho.n_minimo_completo
                            else "nenhum_nivel_atingiu_n_minimo_completo" if selecionado else None
                        ),
                    )
                    membros_nivel = comp_elegivel.loc[
                        comp_elegivel["ordem_relaxamento"].eq(regra.ordem)
                    ].copy()
                    _registrar_membros(
                        membros_saida,
                        membros_nivel,
                        benchmark_id=benchmark_id,
                        alvo_analise=f"curso:{focal_id}",
                        co_curso_alvo=focal_id,
                        indicador=linha.indicador,
                        territorio=territorio.value,
                        tipo_benchmark="comparavel",
                        criterio=regra.criterio.value,
                        ordem_relaxamento=regra.ordem,
                    )
                escolhidos_elegiveis = comp_elegivel.loc[
                    comp_elegivel["ordem_relaxamento"].eq(nivel_escolhido)
                ].copy()
                escolhidos_estruturais = comp_estrutural.loc[
                    comp_estrutural["ordem_relaxamento"].eq(nivel_escolhido)
                ].copy()
                selecoes_comparaveis[(focal_id, linha.indicador, territorio)] = (
                    escolhidos_estruturais,
                    escolhidos_elegiveis,
                )
                comp_id = (
                    f"curso:{focal_id}:{linha.indicador}:{territorio.value}:comparavel:{nivel_escolhido}"
                )
                _registrar_estimativas(
                    contrastes,
                    efeitos,
                    incertezas,
                    focal,
                    escolhidos_elegiveis,
                    benchmark_id=comp_id,
                    identificador=comp_id,
                    indicador=linha.indicador,
                    benchmark=f"{territorio.value}:comparavel:{nivel_escolhido}",
                    tipo_benchmark="comparavel",
                    tipo_foco="individual",
                    papel_analise=papel_individual,
                    focos_elegiveis=[focal_id],
                    focos_excluidos=[],
                    motivos_focos_excluidos=[],
                    bootstrap=bootstrap,
                    politica=politica_tamanho,
                )

    if len(cursos_focais) > 1:
        _registrar_multifoco(
            area,
            grupos,
            focais_df,
            cursos_focais,
            metricas,
            selecoes_comparaveis,
            definicoes,
            membros_saida,
            contrastes,
            efeitos,
            incertezas,
            bootstrap,
            politica_tamanho,
        )

    _registrar_grupos(
        area,
        grupos,
        metricas,
        contrastes,
        efeitos,
        incertezas,
        bootstrap,
        politica_tamanho,
    )
    associacoes = _registrar_associacoes(
        area,
        grupos,
        metricas,
        exclusoes,
        bootstrap,
    )

    artefatos = {
        "grupos_comparativos.csv": grupos_saida,
        "benchmarks_definicoes.csv": pd.DataFrame(definicoes),
        "benchmarks_membros.csv": pd.DataFrame(membros_saida),
        "contrastes.csv": pd.DataFrame(contrastes),
        "efeitos.csv": pd.DataFrame(efeitos),
        "incerteza.csv": pd.DataFrame(incertezas),
        "associacoes_ecologicas.csv": pd.DataFrame(associacoes),
        "exclusoes_fase_9a.csv": pd.DataFrame(exclusoes),
    }
    _finalizar_artefatos(artefatos, geracao_id)
    metadados = {
        "geracao_id": geracao_id,
        "versao_politica_n": politica_tamanho.versao,
        "n_minimo_contraste_completo": politica_tamanho.n_minimo_completo,
        "n_minimo_sintese": politica_tamanho.n_minimo_sintese,
        "n_minimo_correlacao": 20,
        "cobertura_minima_indicador": politica_elegibilidade.cobertura_minima,
        "n_minimo_valido_indicador": politica_elegibilidade.n_minimo,
        "seed_base": bootstrap.seed_base,
        "numero_reamostragens": bootstrap.numero_reamostragens,
        "nivel_confianca": bootstrap.nivel_confianca,
        "unidade_reamostragem": bootstrap.unidade_reamostragem,
        "tipo_foco": "CO_CURSO_CONFIGURADO" if area.co_cursos_focais else "IES_FOCAL",
        "contrato_multifoco": "media_nao_ponderada_focos_elegiveis:v1",
        "cursos_focais": cursos_focais,
        "unidade_analise": "CO_CURSO",
        "edicao": area.edicao,
        "area": area.slug,
        "politica_elegibilidade": politica_elegibilidade.versao,
        "correlacao_ponderada": "nao_implementada",
        "politica_pares_correlacao": "geral_mean_vs_demais_indicadores_elegiveis:v2",
        "associacoes_tentadas": sorted(a["identificador"] for a in associacoes),
    }
    artefatos["metadados_fase_9a.json"] = metadados
    return {"artefatos": artefatos, "metadados": metadados}


def _registrar_multifoco(
    area,
    grupos,
    focais_df,
    cursos_focais,
    metricas,
    selecoes_comparaveis,
    definicoes,
    membros_saida,
    contrastes,
    efeitos,
    incertezas,
    bootstrap,
    politica,
) -> None:
    for indicador in sorted(metricas["indicador"].unique()):
        focal_metricas = metricas.loc[
            metricas["indicador"].eq(indicador) & metricas["CO_CURSO"].isin(cursos_focais)
        ].sort_values("CO_CURSO", kind="stable")
        incluidos = focal_metricas.loc[focal_metricas["incluido"]].copy()
        excluidos = focal_metricas.loc[~focal_metricas["incluido"]].copy()
        focos_incluidos = incluidos["CO_CURSO"].astype(str).tolist()
        focos_excluidos = excluidos["CO_CURSO"].astype(str).tolist()
        motivos_excluidos = [
            f"{row.CO_CURSO}:{row.motivo_exclusao}" for row in excluidos.itertuples(index=False)
        ]
        if incluidos.empty:
            primeira = focal_metricas.iloc[0]
            focal = {
                "valor_focal": None,
                "valor_focal_ponderado": None,
                "n_total_focal": int(focal_metricas["n_total"].sum()),
                "n_valido_focal": int(focal_metricas["n_valido"].sum()),
                "cobertura_focal": None,
                "tipo": primeira["tipo"],
                "arquivo_origem": primeira["arquivo_origem"],
                "variavel_origem": primeira["variavel_origem"],
                **{campo: primeira[campo] for campo in COLUNAS_PROVENIENCIA},
            }
            _registrar_estimativas(
                contrastes,
                efeitos,
                incertezas,
                focal,
                pd.DataFrame(columns=["CO_CURSO", "valor", "n_valido"]),
                benchmark_id=None,
                identificador=f"multifoco:{indicador}:indisponivel",
                indicador=indicador,
                benchmark="nao_aplicavel",
                tipo_benchmark="nao_aplicavel",
                tipo_foco="multifoco",
                papel_analise="primaria",
                focos_elegiveis=[],
                focos_excluidos=focos_excluidos,
                motivos_focos_excluidos=motivos_excluidos,
                bootstrap=bootstrap,
                politica=politica,
            )
            continue
        focal = _focal_multifoco(incluidos)
        elegiveis = metricas.loc[metricas["indicador"].eq(indicador) & metricas["incluido"]]
        for territorio in _territorios_multifoco(focais_df):
            amplo_estrutural = construir_benchmark_amplo(grupos, cursos_focais[0], territorio)
            amplo_estrutural = amplo_estrutural.loc[
                ~amplo_estrutural["CO_CURSO"].astype(str).isin(cursos_focais)
            ]
            amplo = _merge_metricas(amplo_estrutural, elegiveis)
            amplo_id = f"multifoco:{indicador}:{territorio.value}:amplo"
            _registrar_definicao(
                definicoes,
                alvo_analise="multifoco",
                co_curso_alvo=None,
                indicador=indicador,
                territorio=territorio.value,
                tipo_benchmark="amplo",
                ordem_relaxamento=None,
                criterio="exclui_todos_os_focos",
                n_estrutural=len(amplo_estrutural),
                n_elegivel=len(amplo),
                selecionado=True,
                politica=politica,
                benchmark_id=amplo_id,
            )
            _registrar_membros(
                membros_saida,
                amplo,
                benchmark_id=amplo_id,
                alvo_analise="multifoco",
                co_curso_alvo=None,
                indicador=indicador,
                territorio=territorio.value,
                tipo_benchmark="amplo",
                criterio="exclui_todos_os_focos",
                ordem_relaxamento=None,
            )
            _registrar_estimativas(
                contrastes,
                efeitos,
                incertezas,
                focal,
                amplo,
                benchmark_id=amplo_id,
                identificador=amplo_id,
                indicador=indicador,
                benchmark=territorio.value,
                tipo_benchmark="amplo",
                tipo_foco="multifoco",
                papel_analise="primaria",
                focos_elegiveis=focos_incluidos,
                focos_excluidos=focos_excluidos,
                motivos_focos_excluidos=motivos_excluidos,
                bootstrap=bootstrap,
                politica=politica,
            )

            pares_selecao = [
                selecoes_comparaveis[(foco, indicador, territorio)]
                for foco in focos_incluidos
                if (foco, indicador, territorio) in selecoes_comparaveis
            ]
            estrutural_ids = sorted({
                str(curso)
                for estrutural, _ in pares_selecao for curso in estrutural["CO_CURSO"]
                if str(curso) not in cursos_focais
            })
            elegivel_ids = sorted({
                str(curso)
                for _, elegivel in pares_selecao for curso in elegivel["CO_CURSO"]
                if str(curso) not in cursos_focais
            })
            comparavel = elegiveis.loc[elegiveis["CO_CURSO"].isin(elegivel_ids)].copy()
            comp_id = f"multifoco:{indicador}:{territorio.value}:comparavel:uniao"
            _registrar_definicao(
                definicoes,
                alvo_analise="multifoco",
                co_curso_alvo=None,
                indicador=indicador,
                territorio=territorio.value,
                tipo_benchmark="comparavel",
                ordem_relaxamento=None,
                criterio="uniao_comparaveis_individuais_selecionados",
                n_estrutural=len(estrutural_ids),
                n_elegivel=len(comparavel),
                selecionado=True,
                politica=politica,
                benchmark_id=comp_id,
                motivo=(
                    None
                    if len(comparavel) >= politica.n_minimo_completo
                    else "uniao_comparavel_abaixo_do_minimo_completo"
                ),
            )
            _registrar_membros(
                membros_saida,
                comparavel,
                benchmark_id=comp_id,
                alvo_analise="multifoco",
                co_curso_alvo=None,
                indicador=indicador,
                territorio=territorio.value,
                tipo_benchmark="comparavel",
                criterio="uniao_comparaveis_individuais_selecionados",
                ordem_relaxamento=None,
            )
            _registrar_estimativas(
                contrastes,
                efeitos,
                incertezas,
                focal,
                comparavel,
                benchmark_id=comp_id,
                identificador=comp_id,
                indicador=indicador,
                benchmark=f"{territorio.value}:comparavel:uniao",
                tipo_benchmark="comparavel",
                tipo_foco="multifoco",
                papel_analise="primaria",
                focos_elegiveis=focos_incluidos,
                focos_excluidos=focos_excluidos,
                motivos_focos_excluidos=motivos_excluidos,
                bootstrap=bootstrap,
                politica=politica,
            )


def _registrar_grupos(
    area,
    grupos,
    metricas,
    contrastes,
    efeitos,
    incertezas,
    bootstrap,
    politica,
) -> None:
    metricas_grupo = metricas.merge(
        grupos[["CO_CURSO", "GRUPO_CODIGO"]], on="CO_CURSO", how="left", validate="many_to_one"
    )
    for indicador, subset in metricas_grupo.groupby("indicador", sort=True):
        elegiveis = subset.loc[subset["incluido"]].copy()
        grupo_a = elegiveis.loc[elegiveis["GRUPO_CODIGO"].eq("A")].copy()
        if grupo_a.empty:
            continue
        for grupo in "BCDE":
            grupo_b = elegiveis.loc[elegiveis["GRUPO_CODIGO"].eq(grupo)].copy()
            n_a, n_b = len(grupo_a), len(grupo_b)
            n_minimo = min(n_a, n_b)
            tipo = str(elegiveis["tipo"].iloc[0])
            status = _status_n(n_minimo, politica)
            motivo = None if n_minimo >= politica.n_minimo_sintese else "n_grupo_abaixo_minimo_sintese"
            identificador = f"{area.edicao}:{area.slug}:{indicador}:grupo:A_vs_{grupo}"
            valores_a = pd.to_numeric(grupo_a["valor"], errors="coerce")
            valores_b = pd.to_numeric(grupo_b["valor"], errors="coerce")
            pesos_a = pd.to_numeric(grupo_a["n_valido"], errors="coerce")
            pesos_b = pd.to_numeric(grupo_b["n_valido"], errors="coerce")
            suficiente = n_minimo >= politica.n_minimo_sintese
            media_a = float(valores_a.mean()) if suficiente else None
            media_b = float(valores_b.mean()) if suficiente else None
            media_a_p = float(np.average(valores_a, weights=pesos_a)) if suficiente else None
            media_b_p = float(np.average(valores_b, weights=pesos_b)) if suficiente else None
            primeira = grupo_a.iloc[0]
            contrastes.append({
                "identificador": identificador,
                "benchmark_id": None,
                "alvo_analise": "grupo:A",
                "CO_CURSO_ALVO": None,
                "tipo_foco": "grupo",
                "papel_analise": "secundaria",
                "n_focos_elegiveis": n_a,
                "focos_elegiveis": sorted(grupo_a["CO_CURSO"].astype(str).tolist()),
                "focos_excluidos": [],
                "motivos_focos_excluidos": [],
                "indicador": indicador,
                "benchmark": f"grupo:{grupo}",
                "tipo_benchmark": "grupo_exclusivo",
                "n_cursos": n_a + n_b,
                "n_cursos_a": n_a,
                "n_cursos_b": n_b,
                "media_a": media_a,
                "media_b": media_b,
                "media_a_ponderada": media_a_p,
                "media_b_ponderada": media_b_p,
                "diferenca_media": media_a - media_b if suficiente else None,
                "diferenca_media_ponderada": media_a_p - media_b_p if suficiente else None,
                "status": status,
                "motivo": motivo,
                **{campo: primeira[campo] for campo in COLUNAS_PROVENIENCIA},
            })
            if tipo == "proporcao" and suficiente:
                efeito = media_a - media_b
                motivo_efeito = None
                medida = "diferenca_proporcoes"
            elif tipo == "continua" and suficiente:
                efeito = hedges_g_cursos(valores_a, valores_b)
                motivo_efeito = None if efeito is not None else "variancia_combinada_nula_ou_indefinida"
                medida = "hedges_g"
            else:
                efeito = None
                motivo_efeito = motivo
                medida = "diferenca_proporcoes" if tipo == "proporcao" else "hedges_g"
            efeitos.append({
                "identificador": identificador,
                "medida": medida,
                "valor": efeito,
                "interpretacao": (
                    "diferenca_de_proporcoes"
                    if tipo == "proporcao" else "diferenca_padronizada_entre_grupos_de_cursos"
                ),
                "razao_proporcoes": (
                    float(media_a / media_b)
                    if tipo == "proporcao" and suficiente and media_b and media_b > 0 else None
                ),
                "status": status if efeito is not None else StatusAnalise.INSUFICIENTE.value,
                "motivo": motivo_efeito,
                "indicador": indicador,
                "tipo_foco": "grupo",
                **{campo: primeira[campo] for campo in COLUNAS_PROVENIENCIA},
            })
            if n_minimo >= politica.n_minimo_completo:
                incertezas.append({
                    "identificador": identificador,
                    **bootstrap_ic_dois_grupos(
                        valores_a,
                        valores_b,
                        identificador=identificador,
                        cursos_a=grupo_a["CO_CURSO"],
                        cursos_b=grupo_b["CO_CURSO"],
                        configuracao=bootstrap,
                    ),
                })


def _registrar_associacoes(area, grupos, metricas, exclusoes, bootstrap) -> list[dict]:
    associacoes: list[dict] = []
    indicadores = sorted(metricas["indicador"].unique())
    if "geral_mean" not in indicadores:
        return associacoes
    x_tab = metricas.loc[metricas["indicador"].eq("geral_mean")].copy()
    for y in (indicador for indicador in indicadores if indicador != "geral_mean"):
        y_tab = metricas.loc[metricas["indicador"].eq(y)].copy()
        combinado = x_tab.merge(
            y_tab, on="CO_CURSO", how="outer", suffixes=("_x", "_y"), validate="one_to_one"
        )
        identificador = f"{area.edicao}:{area.slug}:geral_mean:{y}"
        elegivel_x = combinado["incluido_x"].fillna(False)
        elegivel_y = combinado["incluido_y"].fillna(False)
        ambos_elegiveis = elegivel_x & elegivel_y
        pares_completos = ambos_elegiveis & combinado["valor_x"].notna() & combinado["valor_y"].notna()
        for row in combinado.loc[~pares_completos].itertuples(index=False):
            razoes = []
            causas: dict[str, str] = {}
            for sufixo, variavel in (("x", "geral_mean"), ("y", y)):
                incluido = bool(getattr(row, f"incluido_{sufixo}", False))
                valor = getattr(row, f"valor_{sufixo}", None)
                if not incluido:
                    motivo = getattr(row, f"motivo_exclusao_{sufixo}", "indicador_invalido")
                    causas[sufixo] = str(motivo)
                    razoes.append(f"{variavel}:{motivo}")
                elif pd.isna(valor):
                    causas[sufixo] = "valor_indicador_ausente"
                    razoes.append(f"{variavel}:valor_indicador_ausente")
            estado = (
                EstadoElegibilidade.INSUFICIENTE_COBERTURA.value
                if any("cobertura" in r or "denominador_zero" in r for r in razoes)
                else EstadoElegibilidade.BAIXO_N.value if any("n_valido" in r for r in razoes)
                else EstadoElegibilidade.ELEGIVEL.value
            )
            if estado == EstadoElegibilidade.INSUFICIENTE_COBERTURA.value:
                sufixo_proxy = next(
                    sufixo for sufixo, motivo in causas.items()
                    if "cobertura" in motivo or motivo == "denominador_zero"
                )
            elif estado == EstadoElegibilidade.BAIXO_N.value:
                sufixo_proxy = next(
                    sufixo for sufixo, motivo in causas.items()
                    if motivo == "n_valido_abaixo_do_minimo"
                )
            else:
                sufixo_proxy = next(iter(causas))
            origem_proxy = x_tab if sufixo_proxy == "x" else y_tab
            proxy = origem_proxy.loc[origem_proxy["CO_CURSO"].eq(str(row.CO_CURSO))]
            linha = type("LinhaExclusao", (), proxy.iloc[0].to_dict())()
            _registrar_exclusao(
                exclusoes,
                linha,
                tipo_exclusao="associacao",
                identificador_analise=identificador,
                variavel_x="geral_mean",
                variavel_y=y,
                motivo="|".join(sorted(razoes)),
                estado=estado,
            )
        dados = combinado.loc[pares_completos, ["CO_CURSO", "valor_x", "valor_y"]].rename(
            columns={"valor_x": "geral_mean", "valor_y": y}
        )
        associacao, sensibilidade = correlacao_spearman_ecologica(
            dados, "geral_mean", y, identificador=identificador, configuracao=bootstrap
        )
        origem_x = x_tab.iloc[0]
        origem_y = y_tab.iloc[0]
        associacao.update({
            "n_estrutural": int(len(grupos)),
            "n_elegivel": int(ambos_elegiveis.sum()),
            "n_pares_completos": int(pares_completos.sum()),
            "n_excluidos": int((~pares_completos).sum()),
            "tipo_associacao": (
                "mecanica_desempenho"
                if origem_x["familia_indicador"] == origem_y["familia_indicador"] == "desempenho"
                else "exploratoria"
            ),
            "edicao_origem_x": origem_x["edicao_origem"],
            "arquivo_fonte_x": origem_x["arquivo_fonte"],
            "variavel_oficial_x": origem_x["variavel_oficial"],
            "indicador_derivado_x": origem_x["indicador_derivado"],
            "regra_agregacao_x": origem_x["regra_agregacao"],
            "denominador_indicador_x": origem_x["denominador_indicador"],
            "edicao_origem_y": origem_y["edicao_origem"],
            "arquivo_fonte_y": origem_y["arquivo_fonte"],
            "variavel_oficial_y": origem_y["variavel_oficial"],
            "indicador_derivado_y": origem_y["indicador_derivado"],
            "regra_agregacao_y": origem_y["regra_agregacao"],
            "denominador_indicador_y": origem_y["denominador_indicador"],
        })
        if not sensibilidade.empty:
            associacao.update({
                f"sensibilidade_{chave}": valor
                for chave, valor in sensibilidade.iloc[0].to_dict().items()
                if chave not in {"identificador", "variavel_x", "variavel_y"}
            })
        associacoes.append(associacao)
    return associacoes


def _finalizar_artefatos(artefatos: dict[str, pd.DataFrame], geracao_id: str) -> None:
    chaves_ordenacao = {
        "grupos_comparativos.csv": ["CO_CURSO"],
        "benchmarks_definicoes.csv": [
            "alvo_analise", "indicador", "territorio", "tipo_benchmark", "ordem_relaxamento",
        ],
        "benchmarks_membros.csv": [
            "alvo_analise", "indicador", "territorio", "tipo_benchmark", "ordem_relaxamento", "CO_CURSO",
        ],
        "contrastes.csv": ["identificador"],
        "efeitos.csv": ["identificador"],
        "incerteza.csv": ["identificador"],
        "associacoes_ecologicas.csv": ["identificador"],
        "exclusoes_fase_9a.csv": [
            "tipo_exclusao", "identificador_analise", "CO_CURSO", "indicador",
        ],
    }
    for nome, tabela in tuple(artefatos.items()):
        for coluna in COLUNAS_MINIMAS_ARTEFATOS.get(nome, ()):
            if coluna not in tabela:
                tabela[coluna] = pd.Series(index=tabela.index, dtype="object")
        tabela["geracao_id"] = geracao_id
        chaves = [chave for chave in chaves_ordenacao[nome] if chave in tabela]
        artefatos[nome] = tabela.sort_values(
            chaves, kind="stable", na_position="first"
        ).reset_index(drop=True)
