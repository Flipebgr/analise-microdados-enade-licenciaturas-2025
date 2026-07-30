from __future__ import annotations

import argparse
from pathlib import Path

from src.qualidade.auditar_encoding import (
    auditar_encoding,
    corrigir_substituicoes_seguras,
    salvar_relatorio,
)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Executa a auditoria de encoding da etapa Refactor 01."
    )
    parser.add_argument(
        "--corrigir",
        action="store_true",
        help="Aplica substituições conservadoras conhecidas antes da auditoria final.",
    )
    return parser


def main() -> int:
    args = construir_parser().parse_args()
    raiz = Path(__file__).resolve().parent
    alterados = corrigir_substituicoes_seguras(raiz) if args.corrigir else []
    ocorrencias = auditar_encoding(raiz)
    destino = raiz / "documentacao/refatoracao/resultado_auditoria_encoding.json"
    salvar_relatorio(destino, ocorrencias, alterados)

    print("Refactor 01 — auditoria de estrutura e encoding")
    print(f"Arquivos corrigidos automaticamente: {len(alterados)}")
    print(f"Ocorrências pendentes para revisão: {len(ocorrencias)}")
    print(f"Relatório gerado em: {destino.relative_to(raiz)}")
    return 1 if ocorrencias else 0


if __name__ == "__main__":
    raise SystemExit(main())
