from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

EXTENSOES_TEXTO = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".csv",
}

PASTAS_IGNORADAS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "dados_brutos",
    "dados_intermediarios",
    "dados_processados",
    "figuras",
    "relatorios",
    "entregas",
}

ARQUIVOS_IGNORADOS = {
    Path("src/qualidade/auditar_encoding.py"),
    Path("tests/test_refactor_01.py"),
    Path("documentacao/refatoracao/resultado_auditoria_encoding.json"),
}

# Sequências típicas de texto UTF-8 interpretado incorretamente como Windows-1252.
# Não usar caracteres isolados como "Ã" ou "Â": eles aparecem legitimamente em
# palavras portuguesas como "SÃO" e "UBERLÂNDIA".
MARCADORES_MOJIBAKE = (
    "Ã¡", "Ã¢", "Ã£", "Ã¤", "Ã©", "Ãª", "Ã­", "Ã³", "Ã´", "Ãµ",
    "Ãº", "Ã¼", "Ã§", "Ã€", "Ã", "Ã‚", "Ãƒ", "Ã‰", "ÃŠ", "Ã",
    "Ã“", "Ã”", "Ã•", "Ãš", "Ã‡", "Â ", "Â ", "Â°", "Âº", "Âª", "�",
)

# Substituições conservadoras e recorrentes em textos em português.
# O modo de correção não tenta reinterpretar o arquivo inteiro: apenas troca
# sequências conhecidas, preservando qualquer ocorrência não mapeada para revisão.
SUBSTITUICOES_SEGURAS = {
    "ecolÃ³gica": "ecológica",
    "ecolÃ³gico": "ecológico",
    "TucuruÃ­": "Tucuruí",
    "RelatÃ³rio": "Relatório",
    "relatÃ³rio": "relatório",
    "FÃ­sica": "Física",
    "MatemÃ¡tica": "Matemática",
    "InglÃªs": "Inglês",
    "RegiÃ£o": "Região",
    "regiÃ£o": "região",
    "anÃ¡lise": "análise",
    "validaÃ§Ã£o": "validação",
    "comparaÃ§Ã£o": "comparação",
    "instituiÃ§Ã£o": "instituição",
    "participaÃ§Ã£o": "participação",
    "informaÃ§Ã£o": "informação",
    "conclusÃ£o": "conclusão",
}


@dataclass(frozen=True)
class OcorrenciaEncoding:
    arquivo: str
    linha: int
    trecho: str


def iterar_arquivos_texto(raiz: Path) -> Iterable[Path]:
    for caminho in raiz.rglob("*"):
        if not caminho.is_file() or caminho.suffix.lower() not in EXTENSOES_TEXTO:
            continue
        if any(parte in PASTAS_IGNORADAS for parte in caminho.parts):
            continue
        relativo = caminho.relative_to(raiz)
        if relativo in ARQUIVOS_IGNORADOS:
            continue
        yield caminho


def detectar_mojibake_texto(texto: str) -> list[tuple[int, str]]:
    ocorrencias: list[tuple[int, str]] = []
    for numero, linha in enumerate(texto.splitlines(), start=1):
        if any(marcador in linha for marcador in MARCADORES_MOJIBAKE):
            ocorrencias.append((numero, linha.strip()[:240]))
    return ocorrencias


def auditar_encoding(raiz: Path) -> list[OcorrenciaEncoding]:
    ocorrencias: list[OcorrenciaEncoding] = []
    for arquivo in iterar_arquivos_texto(raiz):
        try:
            texto = arquivo.read_text(encoding="utf-8")
        except UnicodeDecodeError as erro:
            ocorrencias.append(
                OcorrenciaEncoding(
                    arquivo=str(arquivo.relative_to(raiz)),
                    linha=erro.start,
                    trecho="Arquivo não decodificável como UTF-8",
                )
            )
            continue

        for linha, trecho in detectar_mojibake_texto(texto):
            ocorrencias.append(
                OcorrenciaEncoding(
                    arquivo=str(arquivo.relative_to(raiz)),
                    linha=linha,
                    trecho=trecho,
                )
            )
    return ocorrencias


def corrigir_substituicoes_seguras(raiz: Path) -> list[str]:
    alterados: list[str] = []
    for arquivo in iterar_arquivos_texto(raiz):
        try:
            original = arquivo.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        corrigido = original
        for incorreto, correto in SUBSTITUICOES_SEGURAS.items():
            corrigido = corrigido.replace(incorreto, correto)
        if corrigido != original:
            arquivo.write_text(corrigido, encoding="utf-8", newline="\n")
            alterados.append(str(arquivo.relative_to(raiz)))
    return alterados


def salvar_relatorio(
    destino: Path,
    ocorrencias: list[OcorrenciaEncoding],
    alterados: list[str],
) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "arquivos_corrigidos": alterados,
        "quantidade_ocorrencias_pendentes": len(ocorrencias),
        "ocorrencias_pendentes": [asdict(item) for item in ocorrencias],
    }
    destino.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audita arquivos textuais do projeto em busca de mojibake e UTF-8 inválido."
    )
    parser.add_argument("--raiz", type=Path, default=Path.cwd())
    parser.add_argument(
        "--corrigir",
        action="store_true",
        help="Aplica apenas substituições conservadoras conhecidas.",
    )
    parser.add_argument(
        "--relatorio",
        type=Path,
        default=Path("documentacao/refatoracao/resultado_auditoria_encoding.json"),
    )
    return parser


def main() -> int:
    args = construir_parser().parse_args()
    raiz = args.raiz.resolve()

    alterados: list[str] = []
    if args.corrigir:
        alterados = corrigir_substituicoes_seguras(raiz)

    ocorrencias = auditar_encoding(raiz)
    destino = args.relatorio
    if not destino.is_absolute():
        destino = raiz / destino
    salvar_relatorio(destino, ocorrencias, alterados)

    print(f"Arquivos corrigidos: {len(alterados)}")
    print(f"Ocorrências pendentes: {len(ocorrencias)}")
    print(f"Relatório: {destino}")
    return 1 if ocorrencias else 0


if __name__ == "__main__":
    raise SystemExit(main())
