from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PASTAS_NUCLEO = {
    "src/agregacao",
    "src/analise",
    "src/configuracao",
    "src/core",
    "src/extracao",
    "src/qualidade",
    "src/relatorios",
    "src/utilitarios",
    "src/validacao",
}

ARQUIVOS_IGNORADOS = {
    ".venv",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "dados_extraidos",
    "dados_processados",
}


def ignorado(path: Path) -> bool:
    return any(parte in ARQUIVOS_IGNORADOS for parte in path.parts)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def modulo_de_path(path: Path) -> str | None:
    if path.suffix != ".py":
        return None
    try:
        relativo = path.relative_to(ROOT)
    except ValueError:
        return None
    partes = list(relativo.with_suffix("").parts)
    if partes[-1] == "__init__":
        partes = partes[:-1]
    return ".".join(partes)


def ler_ast(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return None


def imports_do_arquivo(path: Path) -> set[str]:
    tree = ler_ast(path)
    if tree is None:
        return set()

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def simbolos_publicos(path: Path) -> list[dict]:
    tree = ler_ast(path)
    if tree is None:
        return []

    simbolos = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_"):
                continue
            simbolos.append(
                {
                    "nome": node.name,
                    "tipo": "classe" if isinstance(node, ast.ClassDef) else "funcao",
                    "linha": node.lineno,
                }
            )
    return simbolos


def todos_python() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*.py")
        if not ignorado(p)
    )


def modulo_projeto_para_path() -> dict[str, Path]:
    resultado = {}
    for path in todos_python():
        modulo = modulo_de_path(path)
        if modulo:
            resultado[modulo] = path
    return resultado


def resolver_import(importado: str, modulos: dict[str, Path]) -> set[str]:
    encontrados = set()
    for modulo in modulos:
        if (
            importado == modulo
            or importado.startswith(modulo + ".")
            or modulo.startswith(importado + ".")
        ):
            encontrados.add(modulo)
    return encontrados


def contar_referencias_textuais(nome: str, arquivos: list[Path], excluir: Path) -> list[str]:
    padrao = re.compile(rf"\b{re.escape(nome)}\b")
    refs = []
    for path in arquivos:
        if path == excluir:
            continue
        try:
            texto = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if padrao.search(texto):
            refs.append(rel(path))
    return refs


def requisitos() -> list[str]:
    arquivo = ROOT / "requirements.txt"
    if not arquivo.exists():
        return []

    deps = []
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        nome = re.split(r"[<>=!~\[]", linha, maxsplit=1)[0].strip()
        if nome:
            deps.append(nome)
    return deps


def imports_top_level() -> Counter:
    contador = Counter()
    for path in todos_python():
        for imp in imports_do_arquivo(path):
            top = imp.split(".", 1)[0]
            contador[top] += 1
    return contador


def main() -> int:
    py_files = todos_python()
    modulos = modulo_projeto_para_path()

    inbound: dict[str, set[str]] = defaultdict(set)
    outbound: dict[str, set[str]] = defaultdict(set)

    for origem in py_files:
        origem_modulo = modulo_de_path(origem)
        if not origem_modulo:
            continue

        for imp in imports_do_arquivo(origem):
            for destino_modulo in resolver_import(imp, modulos):
                if destino_modulo == origem_modulo:
                    continue
                inbound[destino_modulo].add(rel(origem))
                outbound[origem_modulo].add(destino_modulo)

    modulos_src = {
        modulo: path
        for modulo, path in modulos.items()
        if rel(path).startswith("src/")
    }

    sem_importadores = []
    for modulo, path in sorted(modulos_src.items()):
        refs = sorted(inbound.get(modulo, set()))
        sem_importadores.append(
            {
                "modulo": modulo,
                "arquivo": rel(path),
                "importadores": refs,
                "quantidade_importadores": len(refs),
                "pasta_nucleo": "/".join(rel(path).split("/")[:2]) in PASTAS_NUCLEO,
            }
        )

    candidatos_simbolos = []
    for modulo, path in sorted(modulos_src.items()):
        for simbolo in simbolos_publicos(path):
            refs = contar_referencias_textuais(simbolo["nome"], py_files, path)
            if not refs:
                candidatos_simbolos.append(
                    {
                        "arquivo": rel(path),
                        "modulo": modulo,
                        **simbolo,
                    }
                )

    reqs = requisitos()
    imports = imports_top_level()

    aliases = {
        "PyYAML": "yaml",
        "python-docx": "docx",
        "Pillow": "PIL",
        "scikit-learn": "sklearn",
        "beautifulsoup4": "bs4",
    }

    deps_sem_import = []
    for dep in reqs:
        import_name = aliases.get(dep, dep.replace("-", "_"))
        if imports[import_name] == 0:
            deps_sem_import.append(
                {
                    "dependencia": dep,
                    "import_esperado": import_name,
                }
            )

    # Arquivos Python por família.
    familias = Counter()
    for path in py_files:
        r = rel(path)
        if r.startswith("src/"):
            familia = "/".join(r.split("/")[:2])
        elif r.startswith("tests/"):
            familia = "/".join(r.split("/")[:2])
        elif r.startswith("scripts/"):
            familia = "/".join(r.split("/")[:2])
        else:
            familia = r.split("/", 1)[0]
        familias[familia] += 1

    payload = {
        "resumo": {
            "arquivos_python": len(py_files),
            "modulos_src": len(modulos_src),
            "modulos_src_sem_importadores": sum(
                1 for item in sem_importadores if item["quantidade_importadores"] == 0
            ),
            "simbolos_publicos_sem_referencia_textual": len(candidatos_simbolos),
            "dependencias_requirements_sem_import_estatico": len(deps_sem_import),
        },
        "familias_python": dict(sorted(familias.items())),
        "modulos_src": sem_importadores,
        "simbolos_sem_referencia_textual": candidatos_simbolos,
        "requirements_sem_import_estatico": deps_sem_import,
        "imports_top_level": dict(sorted(imports.items())),
    }

    destino = ROOT / "dados_processados" / "qualidade"
    destino.mkdir(parents=True, exist_ok=True)

    json_path = destino / "auditoria_nucleo_pos_aposentadoria.json"
    md_path = destino / "auditoria_nucleo_pos_aposentadoria.md"

    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    linhas = [
        "# Auditoria do núcleo após aposentadoria das áreas",
        "",
        "Esta auditoria é conservadora: ausência de import estático não significa, sozinha, que um módulo pode ser apagado.",
        "",
        "## Resumo",
        "",
        f"- Arquivos Python analisados: **{payload['resumo']['arquivos_python']}**",
        f"- Módulos em `src/`: **{payload['resumo']['modulos_src']}**",
        f"- Módulos `src` sem importadores detectados: **{payload['resumo']['modulos_src_sem_importadores']}**",
        f"- Símbolos públicos sem referência textual externa: **{payload['resumo']['simbolos_publicos_sem_referencia_textual']}**",
        f"- Dependências de `requirements.txt` sem import estático detectado: **{payload['resumo']['dependencias_requirements_sem_import_estatico']}**",
        "",
        "## Arquivos Python por família",
        "",
    ]

    for familia, quantidade in payload["familias_python"].items():
        linhas.append(f"- `{familia}`: {quantidade}")

    linhas.extend(
        [
            "",
            "## Módulos em src sem importadores detectados",
            "",
        ]
    )

    sem_refs = [
        item for item in sem_importadores
        if item["quantidade_importadores"] == 0
    ]
    if not sem_refs:
        linhas.append("- Nenhum.")
    else:
        for item in sem_refs:
            linhas.append(f"- `{item['arquivo']}` (`{item['modulo']}`)")

    linhas.extend(
        [
            "",
            "## Símbolos públicos sem referência textual externa",
            "",
            "Estes itens são somente candidatos à revisão. Funções chamadas dinamicamente ou via callback podem aparecer aqui.",
            "",
        ]
    )

    if not candidatos_simbolos:
        linhas.append("- Nenhum.")
    else:
        for item in candidatos_simbolos:
            linhas.append(
                f"- `{item['arquivo']}:{item['linha']}` — "
                f"{item['tipo']} `{item['nome']}`"
            )

    linhas.extend(
        [
            "",
            "## Dependências de requirements sem import estático",
            "",
            "Também são somente candidatas: uma dependência pode ser usada por ferramenta externa, notebook, conversão ou fluxo não importado diretamente.",
            "",
        ]
    )

    if not deps_sem_import:
        linhas.append("- Nenhuma.")
    else:
        for item in deps_sem_import:
            linhas.append(
                f"- `{item['dependencia']}` "
                f"(import esperado: `{item['import_esperado']}`)"
            )

    linhas.extend(
        [
            "",
            "## Próxima decisão",
            "",
            "A limpeza final deve classificar os itens acima em:",
            "",
            "- **MANTER** — infraestrutura reutilizável para novas áreas;",
            "- **REMOVER** — legado órfão sem função operacional futura;",
            "- **COBRIR COM TESTE** — componente útil, mas sem proteção atual;",
            "- **REVISAR REQUIREMENTS** — dependência potencialmente desnecessária.",
            "",
        ]
    )

    md_path.write_text("\n".join(linhas), encoding="utf-8")

    print("Auditoria concluída.")
    print(f"Arquivos Python: {payload['resumo']['arquivos_python']}")
    print(f"Módulos src: {payload['resumo']['modulos_src']}")
    print(
        "Módulos src sem importadores:",
        payload["resumo"]["modulos_src_sem_importadores"],
    )
    print(
        "Símbolos públicos sem referência:",
        payload["resumo"]["simbolos_publicos_sem_referencia_textual"],
    )
    print(
        "Dependências sem import estático:",
        payload["resumo"]["dependencias_requirements_sem_import_estatico"],
    )
    print(f"Markdown: {md_path}")
    print(f"JSON: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
