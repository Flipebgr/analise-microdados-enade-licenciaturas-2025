from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO, Iterator, Iterable
from zipfile import ZipFile

from charset_normalizer import from_path
import pandas as pd

from src.configuracao.caminhos import carregar_config_edicao
from src.edicoes.base import ConfiguracaoLeitura, ContratoEdicao
from src.extracao.inventario import ArquivoTematico, inventariar_arquivos


def detectar_encoding(path: Path) -> str:
    resultado = from_path(path).best()
    return resultado.encoding if resultado and resultado.encoding else "utf-8-sig"


def ler_txt(
    path: Path,
    *,
    encoding: str | None = None,
    nrows: int | None = None,
    usecols=None,
    leitura: ConfiguracaoLeitura | None = None,
) -> pd.DataFrame:
    enc = encoding or detectar_encoding(path)
    return pd.read_csv(
        path,
        sep=leitura.separador if leitura else ";",
        decimal=leitura.decimal if leitura else ",",
        quotechar=leitura.quotechar if leitura else '"',
        encoding=enc,
        dtype="string",
        nrows=nrows,
        usecols=usecols,
        low_memory=False,
    )


def encontrar_arquivo(base: Path, nome: str) -> Path:
    candidatos = list(base.rglob(nome))
    if not candidatos:
        raise FileNotFoundError(f"Arquivo não encontrado: {nome}")
    if len(candidatos) > 1:
        candidatos.sort(key=lambda p: len(str(p)))
    return candidatos[0]


@contextmanager
def _abrir_arquivo(arquivo: ArquivoTematico) -> Iterator[BinaryIO]:
    """Abre o TXT no ZIP ou no diretório, sem extrair fontes oficiais."""

    if arquivo.membro_zip is None:
        with arquivo.fonte.open("rb") as entrada:
            yield entrada
    else:
        with ZipFile(arquivo.fonte) as arquivo_zip:
            with arquivo_zip.open(arquivo.membro_zip) as entrada:
                yield entrada


def _chunksize_edicao(edicao: ContratoEdicao) -> int:
    tamanho = carregar_config_edicao(edicao.ano)["leitura_txt"]["chunksize"]
    if not isinstance(tamanho, int) or isinstance(tamanho, bool) or tamanho <= 0:
        raise ValueError(f"chunksize inválido para a edição {edicao.ano}: {tamanho!r}")
    return tamanho


def _carregar_com_encoding(
    arquivo: ArquivoTematico,
    edicao: ContratoEdicao,
    colunas_lidas: list[str],
    colunas_saida: list[str],
    cursos: set[str] | None,
    co_grupo: str | None,
    chunksize: int,
    encoding: str,
) -> pd.DataFrame:
    parametros = {
        "sep": edicao.leitura.separador,
        "decimal": edicao.leitura.decimal,
        "quotechar": edicao.leitura.quotechar,
        "encoding": encoding,
        "dtype": "string",
    }
    with _abrir_arquivo(arquivo) as entrada:
        cabecalho = set(pd.read_csv(entrada, nrows=0, **parametros).columns)
    obrigatorias = set(edicao.schema_arquivo(arquivo.numero).colunas_obrigatorias)
    ausentes = sorted((obrigatorias | set(colunas_lidas)) - cabecalho)
    if ausentes:
        raise ValueError(f"Colunas ausentes em {arquivo.nome}: {ausentes}")

    partes: list[pd.DataFrame] = []
    with _abrir_arquivo(arquivo) as entrada:
        blocos = pd.read_csv(
            entrada,
            usecols=colunas_lidas,
            chunksize=chunksize,
            low_memory=False,
            **parametros,
        )
        for bloco in blocos:
            if co_grupo is not None:
                bloco = bloco.loc[bloco["CO_GRUPO"].str.strip().eq(co_grupo)]
            if cursos is not None:
                bloco = bloco.loc[bloco["CO_CURSO"].str.strip().isin(cursos)]
            if not bloco.empty:
                partes.append(bloco.loc[:, colunas_saida].copy())

    if not partes:
        return pd.DataFrame(columns=colunas_saida).astype("string")
    return pd.concat(partes, ignore_index=True)


def carregar_filtrado_edicao(
    fonte: Path,
    edicao: ContratoEdicao,
    numero: int,
    *,
    usecols: Iterable[str],
    cursos: Iterable[int | str] | None = None,
    co_grupo: int | str | None = None,
    chunksize: int | None = None,
) -> pd.DataFrame:
    """Lê somente as colunas e linhas pedidas, filtrando cada chunk por curso.

    O filtro por CO_GRUPO é permitido apenas no arq1. Nos demais arquivos,
    passa-se o conjunto de CO_CURSO obtido do arq1; não há junção individual.
    """

    if co_grupo is not None and numero != 1:
        raise ValueError("O filtro CO_GRUPO só pode ser usado no arq1")
    edicao.schema_arquivo(numero)
    if cursos is None and co_grupo is None:
        raise ValueError("Informe cursos ou CO_GRUPO para limitar a leitura")
    if chunksize is None:
        chunksize = _chunksize_edicao(edicao)
    if not isinstance(chunksize, int) or isinstance(chunksize, bool) or chunksize <= 0:
        raise ValueError("chunksize deve ser um inteiro positivo")

    colunas_saida = list(dict.fromkeys(["CO_CURSO", *usecols]))
    colunas_lidas = list(dict.fromkeys([*colunas_saida, *(["CO_GRUPO"] if co_grupo is not None else [])]))
    codigos = None if cursos is None else {str(codigo).strip() for codigo in cursos}
    arquivo = inventariar_arquivos(fonte, edicao)[numero]
    erro_encoding: UnicodeDecodeError | None = None
    for encoding in edicao.leitura.encodings:
        try:
            return _carregar_com_encoding(
                arquivo,
                edicao,
                colunas_lidas,
                colunas_saida,
                codigos,
                str(co_grupo).strip() if co_grupo is not None else None,
                chunksize,
                encoding,
            )
        except UnicodeDecodeError as exc:
            erro_encoding = exc
    raise ValueError(f"Nenhum encoding declarado conseguiu ler {arquivo.nome}") from erro_encoding


def obter_cursos_area(
    fonte: Path,
    edicao: ContratoEdicao,
    co_grupo: int | str,
    *,
    chunksize: int | None = None,
) -> set[str]:
    """Descobre os cursos da área pelo arq1, preservando os códigos oficiais."""

    dados = carregar_filtrado_edicao(
        fonte, edicao, 1, usecols=["CO_CURSO"], co_grupo=co_grupo, chunksize=chunksize
    )
    return set(dados["CO_CURSO"].dropna().str.strip())
