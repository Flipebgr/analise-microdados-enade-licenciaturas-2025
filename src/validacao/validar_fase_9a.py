"""Validação semântica cruzada dos artefatos da Fase 9A."""

from __future__ import annotations

import math

import pandas as pd

from src.analise.benchmarks_fase_9a import construir_benchmark_comparavel, mascara_territorio
from src.analise.contratos_fase_9a import (
    EstadoElegibilidade,
    PoliticaElegibilidade,
    Territorio,
    classificar_elegibilidade,
)
from src.analise.definir_grupos import definir_grupo
from src.analise.pipeline_fase_9a import COLUNAS_PROVENIENCIA, NOMES_ARTEFATOS


def _exigir_colunas(tabela: pd.DataFrame, colunas: set[str], nome: str) -> None:
    ausentes = sorted(colunas - set(tabela.columns))
    if ausentes:
        raise ValueError(f"{nome} não possui as colunas requeridas: {ausentes}")


def _booleano(valor) -> bool:
    if isinstance(valor, bool):
        return valor
    if str(valor).strip().lower() in {"true", "1"}:
        return True
    if str(valor).strip().lower() in {"false", "0"}:
        return False
    raise ValueError(f"Valor booleano inválido: {valor!r}")


def _texto_nulo(valor) -> str | None:
    return None if pd.isna(valor) or str(valor).strip() == "" else str(valor)


def _inteiro(valor, nome: str) -> int:
    numero = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]
    if pd.isna(numero) or not math.isfinite(float(numero)) or numero < 0 or numero != int(numero):
        raise ValueError(f"Contagem inválida em {nome}: {valor!r}")
    return int(numero)


def _status_esperado(n: int) -> str:
    return "disponivel" if n >= 10 else "descritivo_apenas" if n >= 5 else "insuficiente"


def _validar_geracao(artefatos: dict, pacote: dict) -> str:
    geracao = pacote["fase_9a"]["metadados"]["geracao_id"]
    if artefatos["metadados_fase_9a.json"].get("geracao_id") != geracao:
        raise ValueError("Metadados da Fase 9A pertencem a outra geração")
    for nome, tabela in artefatos.items():
        if not nome.endswith(".csv"):
            continue
        _exigir_colunas(tabela, {"geracao_id"}, nome)
        if not tabela.empty and set(tabela["geracao_id"].astype(str)) != {geracao}:
            raise ValueError(f"Artefato pertence a outra geração: {nome}")
    return geracao


def _validar_referencias_json(artefatos: dict, pacote: dict) -> None:
    referencias = {
        "benchmarks_definicoes.csv": pacote["benchmarks"]["definicoes"],
        "benchmarks_membros.csv": pacote["benchmarks"]["membros"],
        "efeitos.csv": pacote["efeitos"]["resultados"],
        "associacoes_ecologicas.csv": pacote["associacoes_ecologicas"]["resultados"],
        "contrastes.csv": pacote["fase_9a"]["contrastes"],
        "exclusoes_fase_9a.csv": pacote["fase_9a"]["exclusoes"],
    }
    for nome, referencia in referencias.items():
        if referencia != {"arquivo": nome, "n_registros": len(artefatos[nome])}:
            raise ValueError(f"Referência de {nome} diverge do artefato da geração")


def _validar_grupos(artefatos: dict, pacote: dict) -> tuple[pd.DataFrame, set[str], set[str]]:
    grupos = artefatos["grupos_comparativos.csv"]
    obrigatorias = {
        "CO_CURSO", "CO_IES", "CO_UF_CURSO", "CO_REGIAO_CURSO", "CO_MODALIDADE",
        "CO_CATEGAD", "CO_ORGACAD", "PARTICIPANTES", "CONCEITO_ENADE_NUM",
        "GRUPO_CODIGO", "GRUPO", "eh_focal",
    }
    _exigir_colunas(grupos, obrigatorias, "grupos_comparativos.csv")
    grupos = grupos.copy()
    grupos["CO_CURSO"] = grupos["CO_CURSO"].astype("string")
    cursos = set(pacote["universo"]["cursos"])
    focais = set(pacote["universo"]["cursos_focais"])
    if grupos["CO_CURSO"].duplicated().any() or set(grupos["CO_CURSO"]) != cursos:
        raise ValueError("Tabela de grupos diverge do universo ou repete CO_CURSO")
    co_ies_focal = pacote["area"]["co_ies_focal"]
    configurados = tuple(map(str, pacote["area"].get("co_cursos_focais", ())))
    for linha in grupos.to_dict("records"):
        if linha["GRUPO_CODIGO"] != definir_grupo(pd.Series(linha), co_ies_focal):
            raise ValueError(f"Classificação comparativa incorreta para {linha['CO_CURSO']}")
        esperado_foco = (
            str(linha["CO_CURSO"]) in configurados
            if configurados else str(linha["CO_IES"]).lstrip("0") == str(co_ies_focal).lstrip("0")
        )
        if _booleano(linha["eh_focal"]) != esperado_foco:
            raise ValueError(f"Camada focal incorreta para {linha['CO_CURSO']}")
    observados = set(grupos.loc[grupos["eh_focal"].map(_booleano), "CO_CURSO"])
    if observados != focais:
        raise ValueError("Focos na tabela de grupos divergem do universo")
    return grupos, cursos, focais


def _validar_benchmarks(
    artefatos: dict,
    grupos: pd.DataFrame,
    cursos: set[str],
    focais: set[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    definicoes = artefatos["benchmarks_definicoes.csv"].copy()
    membros = artefatos["benchmarks_membros.csv"].copy()
    _exigir_colunas(definicoes, {
        "benchmark_id", "alvo_analise", "CO_CURSO_ALVO", "indicador", "territorio",
        "tipo_benchmark", "ordem_relaxamento", "criterio_benchmark", "n_estrutural",
        "n_elegivel", "n_cursos", "status", "selecionado", "motivo", "politica_n",
    }, "benchmarks_definicoes.csv")
    _exigir_colunas(membros, {
        "benchmark_id", "alvo_analise", "CO_CURSO_ALVO", "indicador", "territorio",
        "tipo_benchmark", "ordem_relaxamento", "criterio_benchmark", "CO_CURSO", "valor",
        "n_valido", "n_total", "cobertura_valida", "n_ausente", *COLUNAS_PROVENIENCIA,
    }, "benchmarks_membros.csv")
    if definicoes["benchmark_id"].astype(str).duplicated().any():
        raise ValueError("Definições de benchmark repetem benchmark_id")
    if membros.duplicated(["benchmark_id", "CO_CURSO"]).any():
        raise ValueError("Membros de benchmark repetem a chave benchmark_id/CO_CURSO")
    if not set(membros["benchmark_id"].astype(str)) <= set(definicoes["benchmark_id"].astype(str)):
        raise ValueError("Membro referencia benchmark inexistente")
    if not set(membros["CO_CURSO"].astype(str)) <= cursos:
        raise ValueError("Benchmark contém curso fora do universo")
    if membros["CO_CURSO"].astype(str).isin(focais).loc[
        membros["alvo_analise"].eq("multifoco")
    ].any():
        raise ValueError("Benchmark multifoco inclui uma oferta focal")

    contagens = membros.groupby("benchmark_id").size().to_dict()
    for linha in definicoes.itertuples(index=False):
        n = int(contagens.get(linha.benchmark_id, 0))
        if _inteiro(linha.n_elegivel, "n_elegivel") != n or _inteiro(linha.n_cursos, "n_cursos") != n:
            raise ValueError(f"N declarado diverge dos membros: {linha.benchmark_id}")
        n_estrutural = _inteiro(linha.n_estrutural, "n_estrutural")
        if n_estrutural < n:
            raise ValueError(f"N estrutural menor que N elegível: {linha.benchmark_id}")
        if linha.status != _status_esperado(n):
            raise ValueError(f"Status incompatível com N: {linha.benchmark_id}")
        if linha.politica_n != "fase_9a_n_v1":
            raise ValueError("Benchmark sem política de N versionada")
        alvo = _texto_nulo(linha.CO_CURSO_ALVO)
        membros_id = membros.loc[membros["benchmark_id"].eq(linha.benchmark_id)]
        if alvo is not None:
            if alvo not in focais or membros_id["CO_CURSO"].astype(str).eq(alvo).any():
                raise ValueError("Benchmark individual contém alvo inválido")
        territorio = Territorio(str(linha.territorio))
        if not membros_id.empty:
            candidatos = grupos.loc[grupos["CO_CURSO"].isin(membros_id["CO_CURSO"].astype(str))]
            if not mascara_territorio(candidatos, territorio).all():
                raise ValueError(f"Benchmark ampliou território: {linha.benchmark_id}")
            n_total = pd.to_numeric(membros_id["n_total"], errors="coerce")
            n_valido = pd.to_numeric(membros_id["n_valido"], errors="coerce")
            cobertura = pd.to_numeric(membros_id["cobertura_valida"], errors="coerce")
            if (n_total.le(0) | n_valido.lt(10) | cobertura.lt(0.5) | membros_id["valor"].isna()).any():
                raise ValueError(f"Benchmark contém membro inelegível: {linha.benchmark_id}")

        if alvo is not None and linha.tipo_benchmark == "comparavel":
            estruturais, _, _ = construir_benchmark_comparavel(grupos, alvo, territorio=territorio)
            nivel = _inteiro(linha.ordem_relaxamento, "ordem_relaxamento")
            esperados = set(
                estruturais.loc[estruturais["ordem_relaxamento"].eq(nivel), "CO_CURSO"].astype(str)
            )
            if len(esperados) != n_estrutural:
                raise ValueError(f"N estrutural comparável incorreto: {linha.benchmark_id}")
            if not set(membros_id["CO_CURSO"].astype(str)) <= esperados:
                raise ValueError(f"Membro viola critério comparável: {linha.benchmark_id}")
        elif alvo is not None and linha.tipo_benchmark == "amplo":
            esperados = set(
                grupos.loc[mascara_territorio(grupos, territorio), "CO_CURSO"].astype(str)
            ) - {alvo}
            if len(esperados) != n_estrutural:
                raise ValueError(f"N estrutural amplo incorreto: {linha.benchmark_id}")
        elif linha.alvo_analise == "multifoco" and linha.tipo_benchmark == "amplo":
            esperados = set(
                grupos.loc[mascara_territorio(grupos, territorio), "CO_CURSO"].astype(str)
            ) - focais
            if len(esperados) != n_estrutural:
                raise ValueError(f"N estrutural amplo multifoco incorreto: {linha.benchmark_id}")

    comparaveis = definicoes.loc[
        definicoes["tipo_benchmark"].eq("comparavel")
        & definicoes["alvo_analise"].astype(str).str.startswith("curso:")
    ]
    for _, tabela in comparaveis.groupby(["alvo_analise", "indicador", "territorio"], dropna=False):
        selecionados = tabela.loc[tabela["selecionado"].map(_booleano)]
        if len(selecionados) != 1:
            raise ValueError("Cascata comparável não possui exatamente um nível selecionado")
        completos = tabela.loc[pd.to_numeric(tabela["n_elegivel"]).ge(10)]
        if not completos.empty:
            esperado = int(pd.to_numeric(completos["ordem_relaxamento"]).min())
        else:
            esperado = int(
                tabela.assign(_n=pd.to_numeric(tabela["n_elegivel"]), _o=pd.to_numeric(tabela["ordem_relaxamento"]))
                .sort_values(["_n", "_o"], ascending=[False, True]).iloc[0]["_o"]
            )
        if int(pd.to_numeric(selecionados.iloc[0]["ordem_relaxamento"])) != esperado:
            raise ValueError("Nível comparável selecionado não é o primeiro elegível")

    multi_comp = definicoes.loc[
        definicoes["alvo_analise"].eq("multifoco") & definicoes["tipo_benchmark"].eq("comparavel")
    ]
    for linha in multi_comp.itertuples(index=False):
        individuais = definicoes.loc[
            definicoes["indicador"].eq(linha.indicador)
            & definicoes["territorio"].eq(linha.territorio)
            & definicoes["tipo_benchmark"].eq("comparavel")
            & definicoes["alvo_analise"].astype(str).str.startswith("curso:")
            & definicoes["selecionado"].map(_booleano)
        ]
        ids = set(individuais["benchmark_id"].astype(str))
        uniao = set(membros.loc[membros["benchmark_id"].isin(ids), "CO_CURSO"].astype(str)) - focais
        observados = set(membros.loc[membros["benchmark_id"].eq(linha.benchmark_id), "CO_CURSO"].astype(str))
        if observados != uniao:
            raise ValueError("Benchmark comparável multifoco diverge da união individual")
        uniao_estrutural: set[str] = set()
        territorio = Territorio(str(linha.territorio))
        for individual in individuais.itertuples(index=False):
            estruturais, _, _ = construir_benchmark_comparavel(
                grupos,
                str(individual.CO_CURSO_ALVO),
                territorio=territorio,
            )
            nivel = _inteiro(individual.ordem_relaxamento, "ordem_relaxamento")
            uniao_estrutural.update(
                estruturais.loc[
                    estruturais["ordem_relaxamento"].eq(nivel), "CO_CURSO"
                ].astype(str)
            )
        uniao_estrutural -= focais
        if _inteiro(linha.n_estrutural, "n_estrutural") != len(uniao_estrutural):
            raise ValueError("N estrutural comparável multifoco incorreto")
    return definicoes, membros


def _validar_exclusoes(artefatos: dict, cursos: set[str], focais: set[str]) -> None:
    exclusoes = artefatos["exclusoes_fase_9a.csv"]
    _exigir_colunas(exclusoes, {
        "tipo_exclusao", "identificador_analise", "CO_CURSO_ALVO", "CO_CURSO", "indicador",
        "variavel_x", "variavel_y", "estado", "motivo", "n_total", "n_valido",
        "cobertura_valida", "n_ausente",
    }, "exclusoes_fase_9a.csv")
    chave = [
        "tipo_exclusao", "identificador_analise", "CO_CURSO_ALVO", "CO_CURSO", "indicador",
        "variavel_x", "variavel_y",
    ]
    normalizada = exclusoes[chave].fillna("<NULO>").astype(str)
    if normalizada.duplicated().any():
        raise ValueError("Exclusões repetem a chave lógica")
    if not set(exclusoes["CO_CURSO"].astype(str)) <= cursos:
        raise ValueError("Exclusão referencia curso fora do universo")
    alvos = set(exclusoes["CO_CURSO_ALVO"].dropna().astype(str))
    if not alvos <= focais:
        raise ValueError("Exclusão específica referencia alvo não focal")
    estados = {estado.value for estado in EstadoElegibilidade}
    if not set(exclusoes["estado"].astype(str)) <= estados:
        raise ValueError("Estado de elegibilidade desconhecido")
    for linha in exclusoes.itertuples(index=False):
        n_total = _inteiro(linha.n_total, "exclusao.n_total")
        n_valido = _inteiro(linha.n_valido, "exclusao.n_valido")
        n_ausente = _inteiro(linha.n_ausente, "exclusao.n_ausente")
        if n_valido > n_total or n_ausente != n_total - n_valido:
            raise ValueError("Denominadores da exclusão não reconciliam")
        esperado = classificar_elegibilidade(n_total, n_valido, PoliticaElegibilidade())
        if linha.estado != esperado.estado.value:
            raise ValueError("Estado da exclusão diverge dos denominadores")
        cobertura = None if n_total == 0 else n_valido / n_total
        observada = pd.to_numeric(pd.Series([linha.cobertura_valida]), errors="coerce").iloc[0]
        if cobertura is None:
            if not pd.isna(observada):
                raise ValueError("Cobertura deve ser nula com denominador zero")
        elif pd.isna(observada) or not math.isclose(float(observada), cobertura):
            raise ValueError("Cobertura da exclusão diverge dos denominadores")
        if linha.estado == "baixo_n" and "n_valido_abaixo_do_minimo" not in str(linha.motivo):
            raise ValueError("Exclusão baixo_n sem motivo próprio")


def _validar_resultados(
    artefatos: dict,
    pacote: dict,
    definicoes: pd.DataFrame,
    membros: pd.DataFrame,
    focais: set[str],
) -> None:
    contrastes = artefatos["contrastes.csv"]
    efeitos = artefatos["efeitos.csv"]
    incerteza = artefatos["incerteza.csv"]
    associacoes = artefatos["associacoes_ecologicas.csv"]
    _exigir_colunas(contrastes, {
        "identificador", "benchmark_id", "alvo_analise", "CO_CURSO_ALVO", "tipo_foco",
        "papel_analise", "n_focos_elegiveis", "focos_elegiveis", "focos_excluidos",
        "indicador", "n_cursos", "status", "motivo", *COLUNAS_PROVENIENCIA,
    }, "contrastes.csv")
    _exigir_colunas(efeitos, {
        "identificador", "medida", "valor", "status", "motivo", "indicador", "tipo_foco",
        *COLUNAS_PROVENIENCIA,
    }, "efeitos.csv")
    if contrastes["identificador"].astype(str).duplicated().any():
        raise ValueError("Contrastes repetem identificador")
    if efeitos["identificador"].astype(str).duplicated().any():
        raise ValueError("Efeitos repetem identificador")
    if set(efeitos["identificador"].astype(str)) != set(contrastes["identificador"].astype(str)):
        raise ValueError("Efeitos e contrastes não têm correspondência um-para-um")
    ids_benchmarks = set(definicoes["benchmark_id"].astype(str))
    contagens = membros.groupby("benchmark_id").size().to_dict()
    for linha in contrastes.itertuples(index=False):
        alvo = _texto_nulo(linha.CO_CURSO_ALVO)
        if linha.tipo_foco == "individual" and alvo not in focais:
            raise ValueError("Contraste individual referencia alvo não focal")
        benchmark_id = _texto_nulo(linha.benchmark_id)
        if benchmark_id is not None:
            if benchmark_id not in ids_benchmarks:
                raise ValueError("Contraste referencia benchmark inexistente")
            if _inteiro(linha.n_cursos, "contraste.n_cursos") != contagens.get(benchmark_id, 0):
                raise ValueError("N do contraste diverge dos membros do benchmark")
        if linha.status not in {"disponivel", "descritivo_apenas", "insuficiente"}:
            raise ValueError("Status de contraste inválido")
    for linha in efeitos.itertuples(index=False):
        if linha.status in {"disponivel", "descritivo_apenas"} and pd.isna(linha.valor):
            raise ValueError("Efeito disponível sem valor")
        if linha.status == "insuficiente" and not pd.isna(linha.valor):
            raise ValueError("Efeito insuficiente publicou valor interpretável")
        if linha.status == "insuficiente" and not _texto_nulo(linha.motivo):
            raise ValueError("Efeito insuficiente sem motivo")
        for campo in COLUNAS_PROVENIENCIA:
            if not _texto_nulo(getattr(linha, campo)):
                raise ValueError("Efeito sem proveniência completa")

    if not incerteza.empty:
        _exigir_colunas(incerteza, {
            "identificador", "tipo_incerteza", "unidade_reamostragem", "foco_reamostrado",
            "numero_reamostragens", "seed", "status", "motivo",
        }, "incerteza.csv")
        if incerteza["identificador"].astype(str).duplicated().any():
            raise ValueError("Incerteza repete identificador")
        if not set(incerteza["identificador"].astype(str)) <= set(contrastes["identificador"].astype(str)):
            raise ValueError("Intervalo sem contraste correspondente")
        for linha in incerteza.itertuples(index=False):
            if linha.unidade_reamostragem != "CO_CURSO" or _inteiro(
                linha.numero_reamostragens, "numero_reamostragens"
            ) != pacote["fase_9a"]["metadados"]["numero_reamostragens"]:
                raise ValueError("Metadados do bootstrap incompatíveis")
            if linha.tipo_incerteza == "IC ecológico condicional ao foco" and _booleano(
                linha.foco_reamostrado
            ):
                raise ValueError("IC condicional reamostrou o foco")

    _exigir_colunas(associacoes, {
        "identificador", "variavel_x", "variavel_y", "unidade_analise", "metodo",
        "n_estrutural", "n_elegivel", "n_pares_completos", "n_excluidos", "n_cursos",
        "tipo_associacao", "rho", "status", "motivo", "arquivo_fonte_x", "arquivo_fonte_y",
        "variavel_oficial_x", "variavel_oficial_y",
    }, "associacoes_ecologicas.csv")
    if associacoes["identificador"].astype(str).duplicated().any():
        raise ValueError("Associações repetem identificador")
    tentadas = pacote["fase_9a"]["metadados"]["associacoes_tentadas"]
    if sorted(associacoes["identificador"].astype(str)) != tentadas:
        raise ValueError("Família de associações tentadas diverge dos metadados")
    for linha in associacoes.itertuples(index=False):
        n_estrutural = _inteiro(linha.n_estrutural, "associacao.n_estrutural")
        n_elegivel = _inteiro(linha.n_elegivel, "associacao.n_elegivel")
        n_pares = _inteiro(linha.n_pares_completos, "associacao.n_pares_completos")
        if not (n_pares <= n_elegivel <= n_estrutural):
            raise ValueError("N da associação não reconcilia")
        if _inteiro(linha.n_excluidos, "associacao.n_excluidos") != n_estrutural - n_pares:
            raise ValueError("Exclusões da associação não reconciliam")
        exclusoes = artefatos["exclusoes_fase_9a.csv"]
        n_exclusoes = exclusoes.loc[
            exclusoes["tipo_exclusao"].eq("associacao")
            & exclusoes["identificador_analise"].eq(linha.identificador)
        ]["CO_CURSO"].astype(str).nunique()
        if n_exclusoes != _inteiro(linha.n_excluidos, "associacao.n_excluidos"):
            raise ValueError("Exclusões publicadas da associação não reconciliam")
        if _inteiro(linha.n_cursos, "associacao.n_cursos") != n_pares:
            raise ValueError("N publicado da associação diverge dos pares completos")
        if linha.metodo != "spearman_nao_ponderado" or linha.unidade_analise != "CO_CURSO":
            raise ValueError("Contrato da associação ecológica incompatível")
        if n_pares < 20 and (not pd.isna(linha.rho) or linha.status != "insuficiente"):
            raise ValueError("Associação abaixo do N mínimo publicou resultado")
        if linha.tipo_associacao not in {"exploratoria", "mecanica_desempenho", "substantiva"}:
            raise ValueError("Tipo de associação desconhecido")
        for campo in ("arquivo_fonte_x", "arquivo_fonte_y", "variavel_oficial_x", "variavel_oficial_y"):
            if not _texto_nulo(getattr(linha, campo)):
                raise ValueError("Associação sem proveniência completa")


def validar_artefatos_fase_9a(artefatos: dict, pacote: dict) -> None:
    """Rejeita incoerências semânticas entre os CSVs e o schema 3.0."""

    esperados = set(NOMES_ARTEFATOS)
    if set(artefatos) != esperados:
        raise ValueError("Conjunto de artefatos da Fase 9A incompleto ou inesperado")
    for nome in NOMES_ARTEFATOS:
        if nome.endswith(".csv") and not isinstance(artefatos[nome], pd.DataFrame):
            raise ValueError(f"Artefato deve ser DataFrame: {nome}")
    if artefatos["metadados_fase_9a.json"] != pacote["fase_9a"]["metadados"]:
        raise ValueError("Metadados JSON e pacote da geração divergem")
    _validar_geracao(artefatos, pacote)
    _validar_referencias_json(artefatos, pacote)
    grupos, cursos, focais = _validar_grupos(artefatos, pacote)
    definicoes, membros = _validar_benchmarks(artefatos, grupos, cursos, focais)
    _validar_exclusoes(artefatos, cursos, focais)
    _validar_resultados(artefatos, pacote, definicoes, membros, focais)
