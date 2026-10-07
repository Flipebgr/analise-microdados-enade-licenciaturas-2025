from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

import executar
import src.evidencias.publicar as publicacao
from src.core.configuracao_area import BIOLOGIA, BIOLOGIA_BACHARELADO_2017
from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS
from src.edicoes.base import RegraIndicadorQuestionario
from src.evidencias import construir_evidencias
from src.orquestracao.area import analisar_area
from tests.suporte_evidencias import fontes_sinteticas, resultado_sintetico


@pytest.fixture(scope="module")
def analise(tmp_path_factory):
    r, fonte, _, _ = resultado_sintetico(tmp_path_factory.mktemp("publicacao"))
    return r, construir_evidencias(r, ENADE_2017, BIOLOGIA_BACHARELADO_2017, fonte)


def snapshot(pasta):
    return {p.name: p.read_bytes() for p in pasta.iterdir()}


@pytest.mark.parametrize("edicao,area", [(ENADE_2017, BIOLOGIA_BACHARELADO_2017), (ENADE_2025_LICENCIATURAS, BIOLOGIA)])
def test_zip_diretorio_equivalentes_ate_publicacao(tmp_path, edicao, area):
    fonte, diretorio, conceito = fontes_sinteticas(tmp_path / "fontes", edicao, area)
    pacotes = []
    for i, origem in enumerate((fonte, diretorio)):
        resultado = analisar_area(origem, conceito, edicao, area, chunksize=3)
        pacote = construir_evidencias(resultado, edicao, area, origem)
        publicacao.publicar_analise(resultado, pacote, tmp_path / f"publicado{i}")
        manifesto = pacote["proveniencia"]["fontes"][0]
        assert manifesto["armazenamento"] == ("zip" if i == 0 else "diretorio")
        # Origem física varia; conteúdo e hashes individuais são idênticos.
        manifesto.pop("armazenamento")
        manifesto.pop("caminho")
        pacotes.append(pacote)
    assert pacotes[0] == pacotes[1]
    usados = pacotes[0]["proveniencia"]["fontes"][0]["arquivos_tematicos"]
    assert edicao.nome_arquivo(2) not in usados
    assert edicao.nome_arquivo(5) not in usados
    assert {r["arquivo"] for r in pacotes[0]["perfil"]["regras"]} <= set(usados)


def test_novo_indicador_inclui_automaticamente_sua_fonte(tmp_path):
    regra = RegraIndicadorQuestionario("novo_pct", "QE_I01", frozenset("B"), frozenset("AB"), "Indicador sintético")
    edicao = replace(ENADE_2017, questionario=replace(ENADE_2017.questionario,
        regras_indicadores=(*ENADE_2017.questionario.regras_indicadores, regra)))
    r, fonte, _, _ = resultado_sintetico(tmp_path, edicao)
    novo = construir_evidencias(r, edicao, BIOLOGIA_BACHARELADO_2017, fonte)
    anterior = analisar_area(fonte, tmp_path / "conceito.xlsx", ENADE_2017, BIOLOGIA_BACHARELADO_2017)
    antigo = construir_evidencias(anterior, ENADE_2017, BIOLOGIA_BACHARELADO_2017, fonte)
    antes = set(antigo["proveniencia"]["fontes"][0]["arquivos_tematicos"])
    depois = set(novo["proveniencia"]["fontes"][0]["arquivos_tematicos"])
    assert depois - antes == {"microdados2017_arq7.txt"}


@pytest.mark.parametrize("falha", ["schema", "csv", "json", "validacao", "promocao"])
def test_falha_preserva_toda_geracao_anterior(analise, tmp_path, monkeypatch, falha):
    resultado, pacote = analise
    destino = tmp_path / "analise"
    publicacao.publicar_analise(resultado, pacote, destino)
    antes = snapshot(destino)
    novo = deepcopy(pacote)
    novo["area"]["nome"] = "Nova geração"

    def falhar(*args, **kwargs):
        raise ValueError("falha simulada")

    if falha == "schema":
        novo["processo_formativo"]["itens_por_curso"] = []
    elif falha == "csv":
        original = publicacao.salvar_resultado_area
        def escrever_parcial(*args):
            original(*args)
            falhar()
        monkeypatch.setattr(publicacao, "salvar_resultado_area", escrever_parcial)
    elif falha == "json":
        monkeypatch.setattr(publicacao, "salvar_evidencias", falhar)
    elif falha == "validacao":
        original = publicacao.salvar_evidencias
        def corromper(p, caminho):
            original(p, caminho)
            (caminho.parent / "base_cursos.csv").write_text("corrompido", encoding="utf-8")
        monkeypatch.setattr(publicacao, "salvar_evidencias", corromper)
    else:
        original_rename = Path.rename
        def rename(origem, alvo):
            if origem.name == "novo":
                raise OSError("falha simulada na promoção")
            return original_rename(origem, alvo)
        monkeypatch.setattr(Path, "rename", rename)
    with pytest.raises((ValueError, OSError)):
        publicacao.publicar_analise(resultado, novo, destino)
    assert snapshot(destino) == antes
    assert sorted(p.name for p in tmp_path.iterdir()) == ["analise"]


def test_publicacao_sucesso_substitui_conjunto_completo(analise, tmp_path):
    resultado, pacote = analise
    destino = tmp_path / "analise"
    publicacao.publicar_analise(resultado, pacote, destino)
    novo = deepcopy(pacote)
    novo["area"]["nome"] = "Nova geração"
    arquivos = publicacao.publicar_analise(resultado, novo, destino)
    assert all(p.is_file() for p in arquivos)
    assert json.loads((destino / "evidencias.json").read_text(encoding="utf-8")) == novo
    assert sorted(p.name for p in tmp_path.iterdir()) == ["analise"]


@pytest.mark.parametrize("etapa", ["analise", "tudo"])
def test_cli_erro_preserva_saida_e_sucesso_publica(tmp_path, monkeypatch, etapa):
    import src.evidencias as evidencias
    fonte, _, conceito = fontes_sinteticas(tmp_path / "fontes")
    args = ["area", "--ano", "2017", "--slug", "biologia_bacharelado", "--microdados", str(fonte),
            "--conceitos", str(conceito), "--etapa", etapa, "--saida", str(tmp_path / "saida")]
    assert executar.main(args) == 0
    antes = snapshot(tmp_path / "saida" / "analise")
    def falhar(*args):
        raise ValueError("falha antes da publicação")
    monkeypatch.setattr(evidencias, "construir_evidencias", falhar)
    assert executar.main(args) == 2
    assert snapshot(tmp_path / "saida" / "analise") == antes
    assert sorted(p.name for p in (tmp_path / "saida").iterdir()) == ["analise"]


def test_lock_rejeita_escritor_concorrente(analise, tmp_path):
    resultado, pacote = analise
    lock = tmp_path / ".analise.lock"
    lock.write_text("outra execução", encoding="utf-8")
    with pytest.raises(ValueError, match="lock"):
        publicacao.publicar_analise(resultado, pacote, tmp_path / "analise")
    assert lock.read_text(encoding="utf-8") == "outra execução"


def test_json_valido_mas_divergente_do_csv_nao_publica(analise, tmp_path):
    resultado, pacote = analise
    destino = tmp_path / "analise"
    publicacao.publicar_analise(resultado, pacote, destino)
    antes = snapshot(destino)
    outro = deepcopy(pacote)
    # Mudança internamente válida no JSON, mas ausente na tabela de processo.
    outro["processo_formativo"]["itens_por_curso"][0]["media"] = 4.1
    with pytest.raises(ValueError, match="tabelas temáticas"):
        publicacao.publicar_analise(resultado, outro, destino)
    assert snapshot(destino) == antes
