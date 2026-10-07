"""Manifesto dos arquivos que contribuíram para a análise, sem extrair fontes."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from src.edicoes.base import ContratoEdicao
from src.extracao.inventario import inventariar_arquivos
from src.utilitarios.leitura import _abrir_arquivo


def arquivo_das_variaveis(edicao: ContratoEdicao, variaveis) -> str:
    candidatos = [s.numero for s in edicao.arquivos if set(variaveis) <= set(s.colunas_obrigatorias)]
    if len(candidatos) != 1:
        raise ValueError("Variáveis devem identificar exatamente um arquivo de origem")
    return edicao.nome_arquivo(candidatos[0])


def fontes_utilizadas(pacote: dict) -> set[str]:
    """União da proveniência dos produtos efetivamente presentes no pacote."""
    return {
        pacote["universo"]["arquivo_caracterizacao"],
        pacote["desempenho"]["arquivo"],
        *(r["arquivo"] for r in pacote["perfil"]["regras"]),
        *(r["arquivo"] for r in pacote["processo_formativo"]["proveniencia"]),
    }


def manifesto_microdados(fonte: Path, edicao: ContratoEdicao, nomes: set[str]) -> dict:
    inventario = inventariar_arquivos(fonte, edicao)
    por_nome = {arquivo.nome: arquivo for arquivo in inventario.values()}
    if not nomes <= por_nome.keys():
        raise ValueError("Proveniência referencia arquivo fora do inventário")
    arquivos = []
    for nome in sorted(nomes):
        arquivo = por_nome[nome]
        digest = sha256()
        tamanho = 0
        with _abrir_arquivo(arquivo) as entrada:
            for bloco in iter(lambda: entrada.read(1024 * 1024), b""):
                tamanho += len(bloco)
                digest.update(bloco)
        relativo = arquivo.membro_zip or arquivo.fonte.relative_to(fonte).as_posix()
        arquivos.append({"nome": nome, "caminho_relativo": relativo,
                         "tamanho_bytes": tamanho, "sha256": digest.hexdigest()})
    # Hashes são dos bytes dos TXT consumidos, nunca um suposto hash de diretório.
    return {"tipo": "microdados", "armazenamento": "diretorio" if fonte.is_dir() else "zip",
            "caminho": str(fonte), "arquivos_tematicos": sorted(nomes), "arquivos": arquivos}
