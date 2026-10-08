from __future__ import annotations

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.analise.contratos_fase_9a import ConfiguracaoBootstrap
from src.analise.pipeline_fase_9a import construir_fase_9a
from src.core.configuracao_area import ConfiguracaoArea
from src.validacao.validar_fase_9a import validar_artefatos_fase_9a


BOOTSTRAP_RAPIDO = ConfiguracaoBootstrap(numero_reamostragens=100)
FOCOS = ("1001", "1002", "1003")
AREA_MULTIFOCO = ConfiguracaoArea(
    "teste_multifoco",
    "Teste multifoco",
    999,
    co_ies_focal=569,
    edicao=2025,
    co_cursos_focais=FOCOS,
)


def _base(n: int = 30) -> pd.DataFrame:
    cursos = [str(1001 + i) for i in range(n)]
    indice = np.arange(n, dtype=float)
    return pd.DataFrame(
        {
            "CO_CURSO": cursos,
            "CO_IES": ["569"] * min(3, n) + [str(700 + i) for i in range(max(0, n - 3))],
            "CO_UF_CURSO": ["15"] * n,
            "CO_REGIAO_CURSO": ["1"] * n,
            "CO_MODALIDADE": ["1"] * n,
            "CO_CATEGAD": ["1"] * n,
            "CO_ORGACAD": ["10028"] * n,
            "PARTICIPANTES": 95 + (indice % 11),
            "CONCEITO_ENADE_NUM": [3] * n,
            "registros_microdados": [20] * n,
            "geral_mean": 40 + indice,
            "geral_n_valido": [20] * n,
            "perfil_pct": 0.2 + indice / 100,
            "perfil_n_total": [20] * n,
            "perfil_n_valido": [20] * n,
        }
    )


def _executar(
    base: pd.DataFrame | None = None,
    *,
    area: ConfiguracaoArea = AREA_MULTIFOCO,
    processo: pd.DataFrame | None = None,
    proveniencia: dict[str, dict] | None = None,
) -> dict:
    return construir_fase_9a(
        _base() if base is None else base,
        area,
        processo,
        proveniencia_indicadores=proveniencia,
        configuracao_bootstrap=BOOTSTRAP_RAPIDO,
    )


def _pacote(resultado: dict) -> dict:
    artefatos = resultado["artefatos"]
    grupos = artefatos["grupos_comparativos.csv"]
    referencias = {
        nome: {"arquivo": nome, "n_registros": len(artefatos[nome])}
        for nome in (
            "benchmarks_definicoes.csv",
            "benchmarks_membros.csv",
            "contrastes.csv",
            "efeitos.csv",
            "associacoes_ecologicas.csv",
            "exclusoes_fase_9a.csv",
        )
    }
    return {
        "universo": {
            "cursos": grupos["CO_CURSO"].astype(str).tolist(),
            "cursos_focais": grupos.loc[grupos["eh_focal"], "CO_CURSO"].astype(str).tolist(),
        },
        "area": {
            "co_ies_focal": AREA_MULTIFOCO.co_ies_focal,
            "co_cursos_focais": list(AREA_MULTIFOCO.co_cursos_focais),
        },
        "benchmarks": {
            "definicoes": referencias["benchmarks_definicoes.csv"],
            "membros": referencias["benchmarks_membros.csv"],
        },
        "efeitos": {"resultados": referencias["efeitos.csv"]},
        "associacoes_ecologicas": {
            "resultados": referencias["associacoes_ecologicas.csv"]
        },
        "fase_9a": {
            "metadados": resultado["metadados"],
            "contrastes": referencias["contrastes.csv"],
            "exclusoes": referencias["exclusoes_fase_9a.csv"],
        },
    }


def test_multifoco_e_primario_media_nao_ponderada_e_individuais_secundarios():
    base = _base()
    base.loc[base["CO_CURSO"].eq("1001"), ["geral_mean", "geral_n_valido"]] = [30, 10]
    base.loc[base["CO_CURSO"].eq("1002"), ["geral_mean", "geral_n_valido"]] = [50, 20]
    base.loc[base["CO_CURSO"].eq("1003"), ["geral_mean", "geral_n_valido"]] = [70, 20]

    artefatos = _executar(base)["artefatos"]
    contrastes = artefatos["contrastes.csv"]
    multi = contrastes.loc[
        contrastes["identificador"].eq("multifoco:geral_mean:brasil:amplo")
    ].iloc[0]
    individuais = contrastes.loc[
        contrastes["tipo_foco"].eq("individual")
        & contrastes["indicador"].eq("geral_mean")
    ]

    assert multi["papel_analise"] == "primaria"
    assert multi["valor_focal"] == pytest.approx(50.0)
    assert multi["valor_focal_ponderado"] == pytest.approx(54.0)
    assert multi["focos_elegiveis"] == list(FOCOS)
    assert set(individuais["papel_analise"]) == {"secundaria"}
    membros = artefatos["benchmarks_membros.csv"]
    membros_multi = membros.loc[membros["benchmark_id"].eq(multi["benchmark_id"])]
    assert set(membros_multi["CO_CURSO"]).isdisjoint(FOCOS)


@pytest.mark.parametrize(
    ("n_elegiveis", "valor_esperado", "tipo_ic"),
    [
        (1, 40.0, "IC ecológico condicional ao foco"),
        (0, None, None),
    ],
)
def test_multifoco_trata_um_ou_nenhum_foco_elegivel(n_elegiveis, valor_esperado, tipo_ic):
    base = _base()
    base.loc[base["CO_CURSO"].isin(FOCOS), "geral_n_valido"] = 5
    if n_elegiveis:
        base.loc[base["CO_CURSO"].eq("1001"), "geral_n_valido"] = 20
    resultado = _executar(base)
    contrastes = resultado["artefatos"]["contrastes.csv"]
    multi = contrastes.loc[
        contrastes["tipo_foco"].eq("multifoco")
        & contrastes["indicador"].eq("geral_mean")
    ]

    if n_elegiveis:
        linha = multi.loc[multi["identificador"].eq("multifoco:geral_mean:brasil:amplo")].iloc[0]
        assert linha["valor_focal"] == valor_esperado
        ic = resultado["artefatos"]["incerteza.csv"]
        ic = ic.loc[ic["identificador"].eq(linha["identificador"])].iloc[0]
        assert ic["tipo_incerteza"] == tipo_ic
        assert not bool(ic["foco_reamostrado"])
    else:
        assert len(multi) == 1
        assert multi.iloc[0]["status"] == "insuficiente"
        assert multi.iloc[0]["motivo"] == "nenhum_foco_elegivel"


def test_multifoco_distingue_baixo_n_e_cobertura_insuficiente():
    base = _base()
    base.loc[base["CO_CURSO"].eq("1002"), "registros_microdados"] = 18
    base.loc[base["CO_CURSO"].eq("1002"), "geral_n_valido"] = 9
    base.loc[base["CO_CURSO"].eq("1003"), "geral_n_valido"] = 5
    contrastes = _executar(base)["artefatos"]["contrastes.csv"]
    linha = contrastes.loc[
        contrastes["identificador"].eq("multifoco:geral_mean:brasil:amplo")
    ].iloc[0]

    assert linha["focos_elegiveis"] == ["1001"]
    assert linha["focos_excluidos"] == ["1002", "1003"]
    assert linha["motivos_focos_excluidos"] == [
        "1002:n_valido_abaixo_do_minimo",
        "1003:cobertura_abaixo_do_minimo",
    ]


def test_todos_ausentes_e_denominador_zero_permanecem_auditaveis():
    base = _base()
    base["geral_mean"] = np.nan
    base["geral_registros_microdados"] = 20
    base.loc[base["CO_CURSO"].eq("1001"), "geral_registros_microdados"] = 0
    base.loc[base["CO_CURSO"].eq("1001"), "geral_n_valido"] = 0
    resultado = _executar(base)
    contrastes = resultado["artefatos"]["contrastes.csv"]
    exclusoes = resultado["artefatos"]["exclusoes_fase_9a.csv"]
    global_foco = exclusoes.loc[
        exclusoes["tipo_exclusao"].eq("indicador_global")
        & exclusoes["CO_CURSO"].eq("1001")
        & exclusoes["indicador"].eq("geral_mean")
    ].iloc[0]

    assert contrastes.loc[
        contrastes["identificador"].eq("multifoco:geral_mean:indisponivel"), "status"
    ].item() == "insuficiente"
    assert global_foco["estado"] == "insuficiente_cobertura"
    assert global_foco["motivo"] == "denominador_zero"
    assert pd.isna(global_foco["cobertura_valida"])


def test_associacao_aplica_elegibilidade_antes_dos_pares_e_audita_exclusoes():
    base = _base()
    base.loc[base["CO_CURSO"].eq("1004"), "geral_n_valido"] = 5
    base.loc[base["CO_CURSO"].eq("1005"), "perfil_n_valido"] = 5
    base.loc[base["CO_CURSO"].eq("1006"), "perfil_pct"] = np.nan
    resultado = _executar(base)
    associacao = resultado["artefatos"]["associacoes_ecologicas.csv"].iloc[0]
    exclusoes = resultado["artefatos"]["exclusoes_fase_9a.csv"]
    exclusoes_assoc = exclusoes.loc[exclusoes["tipo_exclusao"].eq("associacao")]

    assert associacao["n_estrutural"] == 30
    assert associacao["n_elegivel"] == 27
    assert associacao["n_pares_completos"] == 27
    assert associacao["n_excluidos"] == 3
    assert set(exclusoes_assoc["CO_CURSO"]) == {"1004", "1005", "1006"}
    chave = [
        "tipo_exclusao",
        "identificador_analise",
        "CO_CURSO_ALVO",
        "CO_CURSO",
        "indicador",
        "variavel_x",
        "variavel_y",
    ]
    assert not exclusoes[chave].fillna("<NULO>").duplicated().any()


def test_associacao_mecanica_e_n_abaixo_de_vinte_sao_explicitos():
    origem = {
        indicador: {
            "familia_indicador": "desempenho",
            "arquivo_fonte": "arquivo_oficial.txt",
            "variavel_oficial": variavel,
        }
        for indicador, variavel in (("geral_mean", "NT_GER"), ("perfil_pct", "NT_PERFIL"))
    }
    associacao = _executar(_base(15), proveniencia=origem)["artefatos"][
        "associacoes_ecologicas.csv"
    ].iloc[0]

    assert associacao["tipo_associacao"] == "mecanica_desempenho"
    assert associacao["n_pares_completos"] == 15
    assert associacao["status"] == "insuficiente"
    assert pd.isna(associacao["rho"])
    assert associacao["motivo"] == "n_cursos_abaixo_do_minimo_20"


def test_resultado_independe_da_ordem_das_linhas():
    base = _base()
    original = _executar(base)
    embaralhado = _executar(base.sample(frac=1, random_state=17).reset_index(drop=True))

    assert original["metadados"] == embaralhado["metadados"]
    for nome, tabela in original["artefatos"].items():
        if nome.endswith(".csv"):
            assert_frame_equal(tabela, embaralhado["artefatos"][nome])


def test_processo_formativo_duplicado_e_rejeitado():
    processo = pd.DataFrame(
        {
            "CO_CURSO": ["1001", "1001"],
            "ITEM": ["QE_I01", "QE_I01"],
            "media": [4.0, 4.0],
            "concordancia_pct": [0.8, 0.8],
            "n_total": [20, 20],
            "n_valido": [20, 20],
        }
    )

    with pytest.raises(ValueError, match="repete a chave CO_CURSO/ITEM"):
        _executar(processo=processo)


def test_curso_duplicado_na_base_e_rejeitado_sem_desduplicacao_silenciosa():
    base = pd.concat([_base(), _base().iloc[[0]]], ignore_index=True)

    with pytest.raises(ValueError, match="Cursos duplicados"):
        _executar(base)


def test_grupos_sem_a_nao_geram_contrastes_de_grupo():
    contrastes = _executar()["artefatos"]["contrastes.csv"]

    assert not contrastes["tipo_foco"].eq("grupo").any()


def test_hedges_g_e_publicado_e_variancia_nula_fica_indisponivel():
    base = _base(20)
    base.loc[:4, ["CO_IES", "CONCEITO_ENADE_NUM"]] = ["569", 1]
    base.loc[5:9, "CONCEITO_ENADE_NUM"] = 1
    area = ConfiguracaoArea("grupos", "Grupos", 999, co_ies_focal=569, edicao=2025)
    efeitos = _executar(base, area=area)["artefatos"]["efeitos.csv"]
    efeito = efeitos.loc[
        efeitos["identificador"].eq("2025:grupos:geral_mean:grupo:A_vs_C")
    ].iloc[0]
    assert efeito["medida"] == "hedges_g"
    assert efeito["status"] == "descritivo_apenas"
    assert pd.notna(efeito["valor"])

    base.loc[:4, "geral_mean"] = 50.0
    base.loc[5:, "geral_mean"] = 50.0
    efeitos = _executar(base, area=area)["artefatos"]["efeitos.csv"]
    efeito = efeitos.loc[
        efeitos["identificador"].eq("2025:grupos:geral_mean:grupo:A_vs_C")
    ].iloc[0]
    assert efeito["status"] == "insuficiente"
    assert pd.isna(efeito["valor"])
    assert efeito["motivo"] == "variancia_combinada_nula_ou_indefinida"


def test_sem_comparaveis_publica_insuficiencia_sem_estimativa():
    base = _base()
    base.loc[~base["CO_CURSO"].eq("1001"), "CO_MODALIDADE"] = "2"
    contrastes = _executar(base)["artefatos"]["contrastes.csv"]
    linha = contrastes.loc[
        contrastes["identificador"].str.startswith("curso:1001:geral_mean:brasil:comparavel")
    ].iloc[0]

    assert linha["n_cursos"] == 0
    assert linha["status"] == "insuficiente"
    assert pd.isna(linha["diferenca_media"])
    efeitos = _executar(base)["artefatos"]["efeitos.csv"]
    efeito = efeitos.loc[efeitos["identificador"].eq(linha["identificador"])].iloc[0]
    assert efeito["status"] == "insuficiente"
    assert pd.isna(efeito["valor"])
    assert efeito["motivo"] == "n_benchmark_abaixo_minimo_sintese"


def test_validador_cruza_contagens_geracao_e_exclusoes():
    resultado = _executar()
    pacote = _pacote(resultado)
    validar_artefatos_fase_9a(resultado["artefatos"], pacote)

    artefatos = deepcopy(resultado["artefatos"])
    artefatos["benchmarks_definicoes.csv"].loc[0, "n_elegivel"] += 1
    with pytest.raises(ValueError, match="N declarado diverge"):
        validar_artefatos_fase_9a(artefatos, pacote)

    artefatos = deepcopy(resultado["artefatos"])
    artefatos["contrastes.csv"].loc[0, "geracao_id"] = "outra-geracao"
    with pytest.raises(ValueError, match="outra geração"):
        validar_artefatos_fase_9a(artefatos, pacote)

    base = _base()
    base.loc[0, "geral_n_valido"] = 5
    resultado_exclusoes = _executar(base)
    pacote_exclusoes = _pacote(resultado_exclusoes)
    validar_artefatos_fase_9a(resultado_exclusoes["artefatos"], pacote_exclusoes)

    artefatos = deepcopy(resultado_exclusoes["artefatos"])
    artefatos["associacoes_ecologicas.csv"].loc[0, "n_excluidos"] += 1
    with pytest.raises(ValueError, match="Exclusões da associação não reconciliam"):
        validar_artefatos_fase_9a(artefatos, pacote_exclusoes)

    artefatos = deepcopy(resultado_exclusoes["artefatos"])
    exclusoes = artefatos["exclusoes_fase_9a.csv"]
    artefatos["exclusoes_fase_9a.csv"] = pd.concat(
        [exclusoes, exclusoes.iloc[[0]]], ignore_index=True
    )
    pacote_exclusoes["fase_9a"]["exclusoes"]["n_registros"] += 1
    with pytest.raises(ValueError, match="chave lógica"):
        validar_artefatos_fase_9a(artefatos, pacote_exclusoes)
