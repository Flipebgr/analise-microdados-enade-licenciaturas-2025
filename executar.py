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
    }
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
        raise ValueError(f"Pipeline não registrado: {area}. Disponíveis: {validas}")

    registro = PIPELINES[area_normalizada]

    if area_normalizada == "fontes" and etapa is None:
        etapa = "validacao"

    if etapa is None:
        raise ValueError("Informe a etapa do pipeline.")

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
                f"ERRO: executor não encontrado: {script}.",
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
    print("Pipelines operacionais registrados:\n")
    for area, etapas in PIPELINES.items():
        print(area)
        for etapa, arquivo in etapas.items():
            caminho = pasta_pipelines() / arquivo
            status = "disponível" if caminho.exists() else "ausente nesta branch"
            print(f"  {etapa:<10} -> {arquivo} [{status}]")

    print(
        "\nÁreas já entregues foram aposentadas do branch operacional. "
        "Consulte o histórico Git/tag de arquivamento para reproduzi-las."
    )


def executar_area_cli(argv: list[str]) -> int:
    """Despacha o pipeline multi-edição sem alterar os comandos legados."""

    from src.core.configuracao_area import obter_area
    from src.edicoes import obter_edicao
    from src.evidencias import construir_evidencias
    from src.evidencias.publicar import publicar_analise
    from src.orquestracao.area import analisar_area, preparar_area, salvar_resultado_area

    parser = argparse.ArgumentParser(description="Pipeline genérico do Enade por área.")
    parser.add_argument("--ano", type=int, required=True)
    parser.add_argument("--slug", required=True, help="Slug da área na edição informada.")
    parser.add_argument("--microdados", type=Path, required=True)
    parser.add_argument("--conceitos", type=Path, required=True)
    parser.add_argument("--etapa", choices=("validacao", "analise", "tudo"), default="tudo")
    parser.add_argument("--saida", type=Path)
    args = parser.parse_args(argv)
    try:
        edicao = obter_edicao(args.ano)
        area = obter_area(args.ano, args.slug)
        executar = preparar_area if args.etapa == "validacao" else analisar_area
        resultado = executar(args.microdados, args.conceitos, edicao, area)
        raiz = args.saida or ROOT / "dados_processados" / str(args.ano) / area.slug
        pasta = raiz / ("validacao" if args.etapa == "validacao" else "analise")
        if args.etapa == "validacao":
            arquivos = salvar_resultado_area(resultado, pasta)
        else:
            evidencias = construir_evidencias(resultado, edicao, area, args.microdados)
            arquivos = publicar_analise(resultado, evidencias, pasta)
    except (ValueError, KeyError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2
    for arquivo in arquivos:
        print(arquivo)
    return 0


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Executor dos pipelines operacionais do ENADE Licenciaturas 2025."
    )
    parser.add_argument(
        "area",
        nargs="?",
        help="Pipeline operacional registrado, por exemplo: fontes.",
    )
    parser.add_argument(
        "etapa",
        nargs="?",
        help="Etapa registrada para o pipeline.",
    )
    parser.add_argument(
        "--listar",
        action="store_true",
        help="Lista os pipelines operacionais disponíveis na branch atual.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "area":
        return executar_area_cli(argv[1:])
    parser = criar_parser()
    args = parser.parse_args(argv)

    if args.listar:
        listar()
        return 0

    if not args.area:
        parser.print_help()
        return 2

    try:
        scripts = resolver_scripts(args.area, args.etapa)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    return executar_scripts(scripts)


if __name__ == "__main__":
    raise SystemExit(main())
