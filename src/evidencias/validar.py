"""Contrato semântico do pacote; proporções são frações, contagens são inteiras."""
from __future__ import annotations

import math
import re

from src.edicoes.base import normalizar_conceito
from src.evidencias.proveniencia import fontes_utilizadas

SCHEMA_VERSION = "3.0"
SCHEMA_VERSION_HISTORICO = "2.0"
BLOCOS_V2 = {
    "schema_version", "edicao", "area", "universo", "ofertas_focais", "participacao",
    "desempenho", "perfil", "trajetoria", "processo_formativo", "benchmarks", "efeitos",
    "associacoes_ecologicas", "qualidade", "alertas", "achados_priorizados", "proveniencia",
}
BLOCOS = {*BLOCOS_V2, "fase_9a"}


def _exigir(condicao: bool, mensagem: str) -> None:
    if not condicao:
        raise ValueError(mensagem)


def _campos(objeto: dict, campos, *, exatos: bool = False) -> None:
    _exigir(isinstance(objeto, dict), "Objeto do schema deve ser um dicionário")
    esperados = set(campos)
    faltantes = esperados - objeto.keys()
    _exigir(not faltantes, f"Campos obrigatórios ausentes: {faltantes}")
    if exatos:
        extras = objeto.keys() - esperados
        _exigir(not extras, f"Campos incompatíveis com a versão do schema: {extras}")


def _contagem(valor, nome: str, *, nulo=False) -> None:
    if valor is None and nulo:
        return
    # Um left join pode representar contagens inteiras como 10.0; não arredondar.
    _exigir(type(valor) in (int, float) and math.isfinite(valor) and valor >= 0
            and valor == int(valor), f"Contagem inválida em {nome}")


def _razao(valor, numerador, denominador, nome: str) -> None:
    if denominador is None or numerador is None or denominador == 0:
        _exigir(valor is None, f"{nome} deve ser nulo sem denominador válido")
        return
    _exigir(type(valor) in (int, float) and math.isfinite(valor) and 0 <= valor <= 1,
            f"Proporção inválida em {nome}")
    _exigir(math.isclose(valor, numerador / denominador, rel_tol=1e-12, abs_tol=1e-14),
            f"{nome} incompatível com contagem/denominador (n_total ou n_valido)")


def _finitos(objeto) -> None:
    if isinstance(objeto, dict):
        for valor in objeto.values():
            _finitos(valor)
    elif isinstance(objeto, list):
        for valor in objeto:
            _finitos(valor)
    elif isinstance(objeto, float):
        _exigir(math.isfinite(objeto), "NaN/inf não são valores JSON analíticos válidos")


def _linhas(linhas, cursos: set[str], chave=("CO_CURSO",), *, completa=False) -> dict:
    _exigir(isinstance(linhas, list), "Tabela deve ser uma lista")
    index = {}
    for linha in linhas:
        _campos(linha, chave)
        _exigir(linha["CO_CURSO"] in cursos, "CO_CURSO inexistente no universo")
        k = tuple(linha[c] for c in chave)
        _exigir(k not in index, f"Chave lógica duplicada: {k}")
        index[k] = linha
    if completa:
        _exigir({k[0] for k in index} == cursos, "Cobertura incompleta de cursos")
    return index


def _conceito(linha) -> None:
    _campos(linha, ("CONCEITO_ENADE_ORIGINAL", "CONCEITO_ENADE_NUM", "SITUACAO_CONCEITO"))
    normalizado = normalizar_conceito(linha["CONCEITO_ENADE_ORIGINAL"])
    _contagem(linha["CONCEITO_ENADE_NUM"], "CONCEITO_ENADE_NUM", nulo=True)
    _exigir(linha["CONCEITO_ENADE_NUM"] == normalizado.conceito_numerico,
            "Conceito numérico diverge do original; SC/ausência não ocupa faixa numérica")
    situacao = linha["SITUACAO_CONCEITO"]
    # Cursos sem correspondência na planilha possuem os três campos nulos após left join.
    _exigir(situacao == normalizado.situacao or (
        situacao is None and linha["CONCEITO_ENADE_ORIGINAL"] is None
    ), "Situação do Conceito incompatível com o original")


def _processo(pacote, cursos):
    bloco = pacote["processo_formativo"]
    _campos(bloco, ("disponivel", "status", "itens_por_curso", "proveniencia", "unidade"))
    aplica = (pacote["edicao"]["capacidades"]["processo_formativo"]
              and pacote["area"]["aplicabilidade"]["processo_formativo"])
    _exigir(bloco["disponivel"] is aplica, "Disponibilidade do processo diverge da aplicabilidade")
    if not aplica:
        _exigir(bloco["status"] == "nao_aplicavel" and bloco["itens_por_curso"] == []
                and bloco["proveniencia"] == [], "Processo não aplicável deve estar explicitamente vazio")
        return
    _exigir(bloco["status"] == "disponivel", "Processo aplicável deve estar disponível")
    itens = pacote["edicao"]["itens_processo"]
    _exigir(bool(itens) and len(itens) == len(set(itens)), "Itens declarados inválidos")
    index = _linhas(bloco["itens_por_curso"], cursos, ("CO_CURSO", "ITEM"))
    _exigir(set(index) == {(curso, item) for curso in cursos for item in itens},
            "Processo aplicável incompleto: esperado todo curso/item")
    proveniencia = bloco["proveniencia"]
    _exigir(len(proveniencia) == len(itens) and {r["item"] for r in proveniencia} == set(itens),
            "Proveniência de processo incompleta ou duplicada")
    for r in proveniencia:
        _campos(r, ("edicao", "arquivo", "item", "codigos_validos", "codigos_concordancia",
                    "codigos_especiais", "escala", "denominador_concordancia", "denominador_codigos_especiais"))
        _exigir(r["edicao"] == pacote["edicao"]["ano"] and r["denominador_concordancia"] == "n_valido"
                and r["denominador_codigos_especiais"] == "n_total", "Regra de processo incompatível")
    escala = pacote["edicao"]["escala_processo"]
    _exigir(bool(escala), "Escala do processo ausente")
    contagens = ("n_total", "n_valido", "n_ausente", "n_invalido", "n_nao_sabe_responder", "n_nao_se_aplica")
    for r in index.values():
        _campos(r, (*contagens, "edicao", "concordancia_n", "concordancia_pct", "ausencia_analitica_pct",
                    "nao_sabe_responder_pct", "nao_se_aplica_pct", "media", "mediana", "dp"))
        _exigir(r["edicao"] == pacote["edicao"]["ano"], "Edição do item incompatível")
        for nome in (*contagens, "concordancia_n"):
            _contagem(r[nome], nome)
        _exigir(r["n_total"] == sum(r[n] for n in contagens[1:]), "Contagens de processo não reconciliam")
        _exigir(r["concordancia_n"] <= r["n_valido"], "Concordância excede n_valido")
        for campo, num, den in (
            ("concordancia_pct", r["concordancia_n"], r["n_valido"]),
            ("ausencia_analitica_pct", r["n_total"] - r["n_valido"], r["n_total"]),
            ("nao_sabe_responder_pct", r["n_nao_sabe_responder"], r["n_total"]),
            ("nao_se_aplica_pct", r["n_nao_se_aplica"], r["n_total"]),
        ):
            _razao(r[campo], num, den, campo)
        for campo in ("media", "mediana"):
            v = r[campo]
            _exigir(v is None if r["n_valido"] == 0 else type(v) in (int, float)
                    and min(escala) <= v <= max(escala), f"{campo} incompatível com escala/n_valido")
        _exigir(r["dp"] is None if r["n_valido"] < 2 else type(r["dp"]) in (int, float)
                and r["dp"] >= 0, "Desvio-padrão incompatível com n_valido")


def _perfil(pacote, cursos):
    perfil = pacote["perfil"]
    _campos(perfil, ("indicadores_por_curso", "distribuicoes", "regras"))
    index = _linhas(perfil["indicadores_por_curso"], cursos, completa=True)
    regras = perfil["regras"]
    nomes = [r["indicador"] for r in regras]
    _exigir(bool(nomes) and len(nomes) == len(set(nomes)), "Regras de perfil ausentes ou duplicadas")
    for regra in regras:
        _campos(regra, ("edicao", "arquivo", "item", "indicador", "rotulo", "positivas", "validas",
                        "excluidas", "nao_aplicaveis", "multipla_escolha", "exclusivas", "denominador", "ausencias"))
        _exigir(regra["edicao"] == pacote["edicao"]["ano"] and regra["denominador"] == "n_valido",
                "Regra de perfil incompatível")
        nome = regra["indicador"]
        prefixo = nome.removesuffix("pct")
        categorias = ("n_valido", "n_ausente", "n_excluida", "n_nao_aplicavel", "n_invalida")
        for linha in index.values():
            _campos(linha, (nome, *(prefixo + c for c in (*categorias, "n_total", "n_positivo"))))
            r = {c: linha[prefixo + c] for c in (*categorias, "n_total", "n_positivo")}
            for c, v in r.items():
                _contagem(v, prefixo + c)
            _exigir(sum(r[c] for c in categorias) == r["n_total"] and r["n_positivo"] <= r["n_valido"],
                    "Contagens de perfil não reconciliam")
            _razao(linha[nome], r["n_positivo"], r["n_valido"], nome)
    dist = _linhas(perfil["distribuicoes"], cursos, ("CO_CURSO", "item", "RESPOSTA"))
    totais = {}
    arquivos = {r["item"]: r["arquivo"] for r in regras}
    for (curso, item, _), r in dist.items():
        _campos(r, ("edicao", "arquivo", "n", "pct_total"))
        _exigir(item in arquivos and r["arquivo"] == arquivos[item] and r["edicao"] == pacote["edicao"]["ano"],
                "Distribuição fora das regras de perfil")
        _contagem(r["n"], "distribuicao.n")
        totais[curso, item] = totais.get((curso, item), 0) + r["n"]
    for (curso, item, _), r in dist.items():
        _razao(r["pct_total"], r["n"], totais[curso, item], "pct_total")
    for r in index.values():
        for regra in regras:
            _exigir(totais.get((r["CO_CURSO"], regra["item"]), 0)
                    == r[regra["indicador"].removesuffix("pct") + "n_total"],
                    "Distribuições não reconciliam com n_total do perfil")


def _validar(p):
    versao = p.get("schema_version")
    if versao == SCHEMA_VERSION_HISTORICO:
        _campos(p, BLOCOS_V2, exatos=True)
    elif versao == SCHEMA_VERSION:
        _campos(p, BLOCOS, exatos=True)
    else:
        raise ValueError("Versão do schema de evidências não suportada")
    _finitos(p)
    _campos(p["edicao"], ("ano", "nome", "capacidades", "itens_processo", "escala_processo"))
    _campos(p["area"], ("slug", "nome", "co_grupo", "co_ies_focal", "grau", "aplicabilidade"))
    recursos = ("proficiencia", "recomendacao", "questionario_licenciatura", "processo_formativo")
    for nome in recursos:
        for bloco in (p["edicao"]["capacidades"], p["area"]["aplicabilidade"]):
            _campos(bloco, (nome,))
            _exigir(type(bloco[nome]) is bool, "Capacidade/aplicabilidade deve ser booleana")
        _exigir(not p["area"]["aplicabilidade"][nome] or p["edicao"]["capacidades"][nome],
                "Área solicita capacidade inexistente")
    universo = p["universo"]
    _campos(universo, ("cursos", "cursos_focais", "n_cursos_base", "cobertura", "cobertura_por_curso", "arquivo_caracterizacao"))
    _contagem(universo["n_cursos_base"], "n_cursos_base")
    cursos = universo["cursos"]
    _exigir(isinstance(cursos, list) and all(isinstance(c, str) and re.fullmatch(r"[0-9]+", c) for c in cursos),
            "CO_CURSO deve preservar identificador oficial textual")
    _exigir(len(cursos) == len(set(cursos)) == universo["n_cursos_base"] > 0, "Universo vazio ou duplicado")
    cursos = set(cursos)
    _exigir(len(universo["cursos_focais"]) == len(set(universo["cursos_focais"]))
            and set(universo["cursos_focais"]) <= cursos, "Universo focal inválido")
    configurados = set(map(str, p["area"].get("co_cursos_focais", ())))
    if configurados:
        _exigir(set(universo["cursos_focais"]) == configurados,
                "Universo focal diverge dos cursos configurados")
    cobertura = universo["cobertura_por_curso"]
    # A auditoria pode incluir cursos somente da planilha, fora da base ancorada nos microdados.
    _linhas(cobertura, {r["CO_CURSO"] for r in cobertura})
    for r in cobertura:
        for c in ("em_microdados", "em_conceito", "em_desempenho"):
            _exigir(type(r[c]) is bool, "Cobertura deve ser booleana")
    _exigir({r["CO_CURSO"] for r in cobertura if r["em_microdados"]} == cursos, "Universo diverge da cobertura")
    resumo = {"n_cursos_auditoria": len(cobertura)}
    resumo.update({c: sum(r[c] for r in cobertura) for c in ("em_microdados", "em_conceito", "em_desempenho")})
    _exigir(universo["cobertura"] == resumo, "Resumo de cobertura inconsistente")
    participacao = _linhas(p["participacao"]["por_curso"], cursos, completa=True)
    for r in participacao.values():
        _campos(r, ("INSCRITOS", "PARTICIPANTES", "registros_microdados", "presentes_validos", "taxa_presenca_microdados"))
        for c in ("INSCRITOS", "PARTICIPANTES", "registros_microdados", "presentes_validos"):
            _contagem(r[c], c, nulo=True)
        for total, validos in (("INSCRITOS", "PARTICIPANTES"), ("registros_microdados", "presentes_validos")):
            if r[total] is not None and r[validos] is not None:
                _exigir(r[validos] <= r[total], "Participantes/presentes excedem total da própria fonte")
        _exigir((r["registros_microdados"] is None) == (r["presentes_validos"] is None),
                "Presença sem total de microdados")
        _razao(r["taxa_presenca_microdados"], r["presentes_validos"], r["registros_microdados"], "taxa_presenca_microdados")
        _conceito(r)
    desempenho = p["desempenho"]
    _campos(desempenho, ("por_curso", "mapa_canonico", "arquivo"))
    _exigir(isinstance(desempenho["mapa_canonico"], dict) and bool(desempenho["mapa_canonico"]),
            "Mapa canônico ausente")
    for r in _linhas(desempenho["por_curso"], cursos, completa=True).values():
        part = participacao[(r["CO_CURSO"],)]
        for campo in ("registros_microdados", "presentes_validos", "taxa_presenca_microdados"):
            _exigir(r[campo] == part[campo], "Participação diverge entre blocos")
        for componente in desempenho["mapa_canonico"]:
            cols = ("n_valido", "n_ausente", "n_presente_sem_nota", "n_nota_fora_presenca_valida")
            for c in cols:
                _contagem(r[f"{componente}_{c}"], f"{componente}_{c}", nulo=part["registros_microdados"] is None)
            n = r[f"{componente}_n_valido"]
            if part["registros_microdados"] is not None:
                _exigir(n <= part["presentes_validos"] <= part["registros_microdados"], "N de desempenho inconsistente")
                _exigir(r[f"{componente}_n_ausente"] == part["registros_microdados"] - n
                        and r[f"{componente}_n_presente_sem_nota"] == part["presentes_validos"] - n,
                        "Ausências de desempenho não reconciliam")
            estatisticas = ("mean", "median", "std", "min", "max", "p10", "p25", "p75", "p90",
                            "iqr", "erro_padrao", "ic95_inf", "ic95_sup")
            _campos(r, (f"{componente}_{c}" for c in estatisticas))
            for c in estatisticas:
                valor = r[f"{componente}_{c}"]
                precisa_dois = c in {"std", "erro_padrao", "ic95_inf", "ic95_sup"}
                tem_amostra = n is not None and n >= (2 if precisa_dois else 1)
                _exigir(type(valor) in (int, float) if tem_amostra else valor is None,
                        f"Estatística {componente}_{c} incompatível com N válido")
    focais = _linhas(p["ofertas_focais"], cursos)
    _exigir({k[0] for k in focais} == set(universo["cursos_focais"]), "Ofertas focais incompletas")
    for r in focais.values():
        _campos(r, ("CO_MUNIC_CURSO", "CO_UF_CURSO", "CO_REGIAO_CURSO", "CO_MODALIDADE", "CONCEITO_ENADE_CONTINUO"))
        _exigir(r["CO_IES"] == str(p["area"]["co_ies_focal"]) and r["CO_GRUPO"] == str(p["area"]["co_grupo"]),
                "Oferta focal fora da área/IES")
        _conceito(r)
        for c, v in participacao[(r["CO_CURSO"],)].items():
            _exigir(r[c] == v, "Oferta focal diverge da participação")
    _processo(p, cursos)
    _perfil(p, cursos)
    for bloco, tabela in (("desempenho", "por_curso"), ("perfil", "indicadores_por_curso")):
        for r in p[bloco][tabela]:
            focal = focais.get((r["CO_CURSO"],))
            if focal:
                _exigir(all(focal[c] == v for c, v in r.items()), "Oferta focal diverge dos indicadores")
    _campos(p["trajetoria"], ("disponivel", "motivo"))
    _exigir(p["trajetoria"]["disponivel"] is False and bool(p["trajetoria"]["motivo"]),
            "trajetoria ainda sem contrato implementado")
    if versao == SCHEMA_VERSION_HISTORICO:
        for nome in ("benchmarks", "efeitos", "associacoes_ecologicas"):
            _campos(p[nome], ("disponivel", "motivo"))
            _exigir(p[nome]["disponivel"] is False and bool(p[nome]["motivo"]),
                    f"{nome} incompatível com o schema histórico 2.0")
    else:
        _validar_fase_9a(p)
    _exigir(p["alertas"] == [] and p["achados_priorizados"] == [], "Alertas/achados ainda não implementados")
    _exigir(p["qualidade"] == {"base_por_curso_unica": True}, "Qualidade incompatível")
    _campos(p["proveniencia"], ("fontes", "tabelas_auditaveis"))
    tabelas = {"base_cursos.csv", "auditoria_cobertura.csv", "proveniencia_conceito.csv",
               "distribuicoes_questionario.csv", "regras_indicadores.csv"}
    if versao == SCHEMA_VERSION:
        tabelas |= {
            "grupos_comparativos.csv", "benchmarks_definicoes.csv", "benchmarks_membros.csv",
            "contrastes.csv", "efeitos.csv", "incerteza.csv", "associacoes_ecologicas.csv",
            "exclusoes_fase_9a.csv", "metadados_fase_9a.json",
        }
    if p["processo_formativo"]["disponivel"]:
        tabelas |= {"processo_itens.csv", "proveniencia_processo.csv"}
    _exigir(len(p["proveniencia"]["tabelas_auditaveis"]) == len(tabelas)
            and set(p["proveniencia"]["tabelas_auditaveis"]) == tabelas, "Lista de tabelas auditáveis inconsistente")
    fontes = p["proveniencia"]["fontes"]
    _exigir(len(fontes) >= 2, "Proveniência deve incluir microdados e Conceito")
    micro = fontes[0]
    _campos(micro, ("tipo", "armazenamento", "caminho", "arquivos_tematicos", "arquivos"))
    _exigir(micro["tipo"] == "microdados" and micro["armazenamento"] in {"zip", "diretorio"}, "Fonte inválida")
    esperadas = fontes_utilizadas(p)
    _exigir(micro["arquivos_tematicos"] == sorted(esperadas), "Proveniência incompleta ou com arquivos não utilizados")
    _exigir([r["nome"] for r in micro["arquivos"]] == sorted(esperadas), "Manifesto de arquivos incompleto")
    for r in micro["arquivos"]:
        _campos(r, ("nome", "caminho_relativo", "tamanho_bytes", "sha256"))
        _contagem(r["tamanho_bytes"], "tamanho_bytes")
        _exigir(isinstance(r["sha256"], str) and re.fullmatch("[0-9a-f]{64}", r["sha256"]) is not None,
                "SHA256 inválido")
    for r in fontes[1:]:
        _campos(r, ("edicao", "fonte", "sha256", "aba", "n_linhas_fonte", "n_linhas_nao_dados", "n_ofertas"))
        _exigir(r["edicao"] == p["edicao"]["ano"] and re.fullmatch("[0-9a-f]{64}", r["sha256"]) is not None,
                "Proveniência de Conceito incompatível")


def _validar_fase_9a(p: dict) -> None:
    fase = p["fase_9a"]
    _campos(fase, ("contrastes", "exclusoes", "metadados"))
    metadados = fase["metadados"]
    _campos(metadados, (
        "geracao_id", "versao_politica_n", "n_minimo_contraste_completo", "n_minimo_sintese",
        "n_minimo_correlacao", "cobertura_minima_indicador", "n_minimo_valido_indicador",
        "seed_base", "numero_reamostragens", "nivel_confianca", "unidade_reamostragem",
        "cursos_focais", "unidade_analise", "edicao", "area", "politica_elegibilidade",
        "politica_pares_correlacao", "contrato_multifoco", "associacoes_tentadas",
    ))
    _exigir(metadados["versao_politica_n"] == "fase_9a_n_v1", "Política de N não versionada")
    _exigir(metadados["unidade_analise"] == "CO_CURSO", "Unidade da Fase 9A incompatível")
    _exigir(metadados["n_minimo_contraste_completo"] == 10
            and metadados["n_minimo_sintese"] == 5
            and metadados["n_minimo_correlacao"] == 20,
            "Limiares operacionais da Fase 9A incompatíveis")
    _exigir(metadados["seed_base"] == 20250901
            and metadados["numero_reamostragens"] == 5000
            and metadados["unidade_reamostragem"] == "CO_CURSO",
            "Configuração de bootstrap incompatível")
    _exigir(metadados["edicao"] == p["edicao"]["ano"] and metadados["area"] == p["area"]["slug"],
            "Metadados da Fase 9A divergem de edição/área")
    _exigir(isinstance(metadados["geracao_id"], str)
            and re.fullmatch("[0-9a-f]{64}", metadados["geracao_id"]) is not None,
            "Identificador de geração inválido")
    _exigir(metadados["cursos_focais"] == sorted(p["universo"]["cursos_focais"]),
            "Focos da Fase 9A divergem do universo")
    _exigir(metadados["contrato_multifoco"] == "media_nao_ponderada_focos_elegiveis:v1",
            "Contrato multifoco incompatível")
    for nome, chaves in (
        ("benchmarks", ("disponivel", "motivo", "definicoes", "membros")),
        ("efeitos", ("disponivel", "motivo", "resultados")),
        ("associacoes_ecologicas", ("disponivel", "motivo", "resultados")),
    ):
        _campos(p[nome], chaves)
        _exigir(p[nome]["disponivel"] is True and p[nome]["motivo"] is None,
                f"Bloco {nome} deve declarar o contrato 3.0 disponível")
    referencias = (
        (p["benchmarks"]["definicoes"], "benchmarks_definicoes.csv"),
        (p["benchmarks"]["membros"], "benchmarks_membros.csv"),
        (p["efeitos"]["resultados"], "efeitos.csv"),
        (p["associacoes_ecologicas"]["resultados"], "associacoes_ecologicas.csv"),
        (fase["contrastes"], "contrastes.csv"),
        (fase["exclusoes"], "exclusoes_fase_9a.csv"),
    )
    for referencia, arquivo in referencias:
        _campos(referencia, ("arquivo", "n_registros"))
        _exigir(referencia["arquivo"] == arquivo, f"Referência de artefato inválida: {arquivo}")
        _contagem(referencia["n_registros"], f"{arquivo}.n_registros")


def validar_evidencias(pacote: dict) -> None:
    """Rejeita schema incompleto e violações metodológicas com erro explícito."""
    try:
        _validar(pacote)
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError(f"Schema de evidências malformado: {exc}") from exc
