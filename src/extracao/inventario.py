from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from src.edicoes.base import ContratoEdicao


@dataclass(frozen=True, slots=True)
class ArquivoTematico:
    """Localização de um arquivo oficial, extraído ou dentro do ZIP."""

    numero: int
    fonte: Path
    membro_zip: str | None = None

    @property
    def nome(self) -> str:
        return self.fonte.name if self.membro_zip is None else PurePosixPath(self.membro_zip).name


def inventariar_arquivos(fonte: Path, edicao: ContratoEdicao) -> dict[int, ArquivoTematico]:
    """Confere o inventário completo da edição sem extrair ou alterar a fonte."""

    fonte = Path(fonte)
    if not fonte.exists():
        raise FileNotFoundError(f"Fonte de microdados não encontrada: {fonte}")

    padrao = re.compile(rf"^{re.escape(edicao.prefixo_arquivos)}(\d+)\.txt$")
    encontrados: dict[int, ArquivoTematico] = {}

    if fonte.is_file() and fonte.suffix.lower() == ".zip":
        with ZipFile(fonte) as arquivo_zip:
            candidatos = (
                (PurePosixPath(info.filename).name, info.filename)
                for info in arquivo_zip.infolist()
                if not info.is_dir()
            )
            entradas = list(candidatos)
    elif fonte.is_dir():
        entradas = [(path.name, path) for path in fonte.rglob("*.txt") if path.is_file()]
    else:
        raise ValueError(f"A fonte deve ser um ZIP ou diretório extraído: {fonte}")

    for nome, local in entradas:
        correspondencia = padrao.fullmatch(nome)
        if correspondencia is None:
            continue
        numero = int(correspondencia.group(1))
        if numero < 1 or numero > edicao.quantidade_arquivos:
            raise ValueError(f"Arquivo fora do inventário de {edicao.ano}: {nome}")
        if numero in encontrados:
            raise ValueError(f"Arquivo temático duplicado em {fonte}: {nome}")
        if nome != edicao.nome_arquivo(numero):
            raise ValueError(f"Nome inesperado para o arquivo {numero}: {nome}")
        encontrados[numero] = ArquivoTematico(
            numero=numero,
            fonte=fonte if isinstance(local, str) else local,
            membro_zip=local if isinstance(local, str) else None,
        )

    faltantes = sorted(set(range(1, edicao.quantidade_arquivos + 1)) - encontrados.keys())
    if faltantes:
        raise ValueError(f"Arquivos ausentes na edição {edicao.ano}: {faltantes}")
    return dict(sorted(encontrados.items()))
