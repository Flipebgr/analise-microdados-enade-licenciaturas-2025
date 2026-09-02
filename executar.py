from __future__ import annotations

import argparse
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def pasta_pipelines() -> Path:
    return ROOT / "scripts" / "pipelines"

PIPELINES: dict[str, dict[str, str]] = {
    "fontes": {
        "validacao": "executar_sprint_00.py",
    },
    "matematica": {
        "base": "executar_sprint_01.py",
        "validacao": "executar_sprint_02.py",
        "relatorio": "executar_sprint_03.py",
    },
    "fisica": {
        "base": "executar_sprint_04.py",
        "validacao": "executar_sprint_05.py",
        "relatorio": "executar_sprint_06.py",
        "regional": "executar_relatorio_regional_fisica.py",
    },
    "ingles": {
        "base": "executar_sprint_07.py",
        "validacao": "executar_sprint_08.py",
        "relatorio": "executar_sprint_09.py",
    },
    "biologia": {
        "base": "executar_sprint_10.py",
        "validacao": "executar_sprint_11.py",
        "relatorio": "executar_sprint_12.py",
    },
    "pedagogia": {
        "base": "executar_sprint_13.py",
        "validacao": "executar_sprint_14.py",
        "relatorio": "executar_sprint_15.py",
    },
    "portugues": {
        "base": "executar_sprint_16.py",
        "validacao": "executar_sprint_17.py",
        "relatorio": "executar_sprint_18.py",
    },
    "geografia": {
        "base": "executar_sprint_19.py",
        "validacao": "executar_sprint_20.py",
        "relatorio": "executar_sprint_21.py",
    },
}

ORDEM_TUDO = ("base", "validacao", "relatorio")


def normalizar(valor: str) -> str:
    texto = unicodedata.normalize("NFKD", valor.strip().lower())
    return "".join(char for char in texto if not unicodedata.combining(char))


def etapas_disponiveis(area: str) -> list[str]:
    area_normalizada = normalizar(area)
    if area_normalizada not in PIPELINES:
        return []
    return list(PIPELINES[area_normalizada])


def resolver_scripts(area: str, etapa: str | None) -> list[Path]:
    area_normalizada = normalizar(area)
    if area_normalizada not in PIPELINES:
        validas = ", ".join(sorted(PIPELINES))
        raise ValueError(f"Área desconhecida: {area}. Opções: {validas}")

    registro = PIPELINES[area_normalizada]

    if area_normalizada == "fontes" and etapa is None:
        etapa = "validacao"

    if etapa is None:
        raise ValueError("Informe a etapa: base, validacao, relatorio, regional ou tudo.")

    etapa_normalizada = normalizar(etapa)

    if etapa_normalizada == "tudo":
        selecionadas = [nome for nome in ORDEM_TUDO if nome in registro]
    elif etapa_normalizada in registro:
        selecionadas = [etapa_normalizada]
    else:
        opcoes = ", ".join([*registro, "tudo"])
        raise ValueError(
            f"Etapa '{etapa}' não disponível para {area_normalizada}. Opções: {opcoes}"
        )

    return [pasta_pipelines() / registro[nome] for nome in selecionadas]


def executar_scripts(scripts: list[Path]) -> int:
    for script in scripts:
        if not script.exists():
            print(
                f"ERRO: executor não encontrado: {script.name}. "
                "A etapa pode ainda não estar integrada nesta branch.",
                file=sys.stderr,
            )
            return 2

        print(f"\n=== Executando {script.name} ===")
        resultado = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            check=False,
        )
        if resultado.returncode != 0:
            print(
                f"ERRO: {script.name} terminou com código {resultado.returncode}.",
                file=sys.stderr,
            )
            return resultado.returncode

    return 0


def listar() -> None:
    print("Pipelines registrados:\n")
    for area, etapas in PIPELINES.items():
        print(area)
        for etapa, arquivo in etapas.items():
            status = "disponível" if (pasta_pipelines() / arquivo).exists() else "ausente nesta branch"
            print(f"  {etapa:<10} -> {arquivo} [{status}]")


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Executor unificado dos pipelines do ENADE Licenciaturas 2025."
    )
    parser.add_argument("area", nargs="?", help="Área: matematica, fisica, ingles, etc.")
    parser.add_argument(
        "etapa",
        nargs="?",
        help="Etapa: base, validacao, relatorio, regional ou tudo.",
    )
    parser.add_argument(
        "--listar",
        action="store_true",
        help="Lista áreas, etapas e executores disponíveis na branch atual.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)

    if args.listar:
        listar()
        return 0

    if not args.area:
        criar_parser().print_help()
        return 2

    try:
        scripts = resolver_scripts(args.area, args.etapa)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    return executar_scripts(scripts)


if __name__ == "__main__":
    raise SystemExit(main())
