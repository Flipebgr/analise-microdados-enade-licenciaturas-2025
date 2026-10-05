from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest

from src.edicoes import ENADE_2017, ENADE_2025_LICENCIATURAS
from src.edicoes.base import ContratoEdicao
from src.extracao.inventario import inventariar_arquivos
from src.qualidade.inspecionar_arquivos import inspecionar_todos
from src.utilitarios.leitura import carregar_filtrado_edicao, obter_cursos_area


def _conteudo(contrato: ContratoEdicao, numero: int) -> str:
    colunas = contrato.schema_arquivo(numero).colunas_obrigatorias
    linhas = []
    for curso, grupo, valor in (("12027", "1601", "primeiro"), ("900", "1602", "segundo"), ("12027", "1601", "terceiro")):
        campos = {coluna: "" for coluna in colunas}
        campos.update({"NU_ANO": str(contrato.ano), "CO_CURSO": curso})
        if "CO_GRUPO" in campos:
            campos["CO_GRUPO"] = grupo
        if "ANO_IN_GRAD" in campos:
            campos["ANO_IN_GRAD"] = valor
        linhas.append(";".join(campos[coluna] for coluna in colunas))
    return ";".join(colunas) + "\n" + "\n".join(linhas) + "\n"


def _criar_zip(path: Path, contrato: ContratoEdicao, *, omitir: int | None = None) -> None:
    with ZipFile(path, "w") as arquivo_zip:
        for numero in range(1, contrato.quantidade_arquivos + 1):
            if numero != omitir:
                arquivo_zip.writestr(
                    f"pasta/{contrato.nome_arquivo(numero)}", _conteudo(contrato, numero)
                )


@pytest.mark.parametrize("contrato", [ENADE_2017, ENADE_2025_LICENCIATURAS])
def test_inventario_encontra_arquivos_no_zip_e_no_diretorio(tmp_path: Path, contrato):
    zip_path = tmp_path / "fonte.zip"
    pasta = tmp_path / "extraidos"
    _criar_zip(zip_path, contrato)
    with ZipFile(zip_path) as arquivo_zip:
        arquivo_zip.extractall(pasta)

    inventario_zip = inventariar_arquivos(zip_path, contrato)
    inventario_pasta = inventariar_arquivos(pasta, contrato)

    assert len(inventario_zip) == len(inventario_pasta) == contrato.quantidade_arquivos
    assert inventario_zip[1].membro_zip == f"pasta/{contrato.nome_arquivo(1)}"
    assert inventario_pasta[1].fonte.name == contrato.nome_arquivo(1)


def test_inventario_rejeita_arquivo_ausente_e_duplicado(tmp_path: Path):
    zip_path = tmp_path / "fonte.zip"
    _criar_zip(zip_path, ENADE_2017, omitir=42)
    with pytest.raises(ValueError, match="Arquivos ausentes.*42"):
        inventariar_arquivos(zip_path, ENADE_2017)

    _criar_zip(zip_path, ENADE_2017)
    with ZipFile(zip_path, "a") as arquivo_zip:
        arquivo_zip.writestr("duplicata/microdados2017_arq1.txt", _conteudo(ENADE_2017, 1))
    with pytest.raises(ValueError, match="duplicado"):
        inventariar_arquivos(zip_path, ENADE_2017)


def test_filtragem_em_chunks_seleciona_cursos_sem_usar_posicao_de_linha(tmp_path: Path):
    zip_path = tmp_path / "fonte.zip"
    _criar_zip(zip_path, ENADE_2017)

    cursos = obter_cursos_area(zip_path, ENADE_2017, 1601, chunksize=1)
    trajetoria = carregar_filtrado_edicao(
        zip_path,
        ENADE_2017,
        2,
        usecols=["ANO_IN_GRAD"],
        cursos=cursos,
        chunksize=1,
    )

    assert cursos == {"12027"}
    assert trajetoria["CO_CURSO"].tolist() == ["12027", "12027"]
    assert trajetoria["ANO_IN_GRAD"].tolist() == ["primeiro", "terceiro"]
    assert "CO_GRUPO" not in trajetoria.columns


def test_leitura_rejeita_grupo_fora_do_arq1_e_coluna_ausente(tmp_path: Path):
    zip_path = tmp_path / "fonte.zip"
    _criar_zip(zip_path, ENADE_2017)

    with pytest.raises(ValueError, match="só pode ser usado no arq1"):
        carregar_filtrado_edicao(zip_path, ENADE_2017, 2, usecols=["CO_CURSO"], co_grupo=1601)
    with pytest.raises(ValueError, match="Colunas ausentes.*INEXISTENTE"):
        carregar_filtrado_edicao(
            zip_path, ENADE_2017, 1, usecols=["INEXISTENTE"], co_grupo=1601
        )


def test_leitura_2025_tambem_usa_contrato_e_chunks(tmp_path: Path):
    zip_path = tmp_path / "fonte.zip"
    _criar_zip(zip_path, ENADE_2025_LICENCIATURAS)

    selecionado = carregar_filtrado_edicao(
        zip_path,
        ENADE_2025_LICENCIATURAS,
        1,
        usecols=["CO_GRUPO"],
        co_grupo=1601,
        chunksize=1,
    )

    assert selecionado["CO_CURSO"].tolist() == ["12027", "12027"]
    assert selecionado["CO_GRUPO"].tolist() == ["1601", "1601"]


def test_inspecao_2017_usa_inventario_e_formato_da_edicao(tmp_path: Path):
    zip_path = tmp_path / "fonte.zip"
    pasta = tmp_path / "extraidos"
    _criar_zip(zip_path, ENADE_2017)
    with ZipFile(zip_path) as arquivo_zip:
        arquivo_zip.extractall(pasta)

    inventario, ausencias = inspecionar_todos(pasta, edicao=ENADE_2017)

    assert len(inventario) == 42
    assert inventario.iloc[0]["arquivo"] == "microdados2017_arq1.txt"
    assert set(inventario["decimal"]) == {"."}
    assert not ausencias.empty
