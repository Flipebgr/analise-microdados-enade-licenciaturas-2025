from __future__ import annotations

import json
import locale
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUALIDADE = ROOT / "dados_processados" / "qualidade"

AREAS_APOSENTADAS = (
    "matematica",
    "fisica",
    "ingles",
    "biologia",
    "pedagogia",
    "portugues",
    "geografia",
)

PASTAS_SRC_ESPERADAS = {
    "agregacao",
    "analise",
    "configuracao",
    "core",
    "extracao",
    "qualidade",
    "relatorios",
    "utilitarios",
    "validacao",
}

EXTENSOES_BINARIAS_NAO_OPERACIONAIS = {
    ".docx",
    ".pdf",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}

PREFIXOS_DADOS_DERIVADOS = (
    "dados_processados/",
    "dados_extraidos/",
)

ARQUIVOS_FONTE_BRUTA_PROIBIDOS = (
    "microdados_enade_licenciaturas_2025.zip",
    "conceito_enade_licenciaturas.xlsx",
)


@dataclass
class Check:
    nome: str
    status: str
    detalhe: str


def _decode(data: bytes) -> str:
    enc = locale.getpreferredencoding(False) or "utf-8"
    try:
        return data.decode(enc)
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")


def run(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        list(args),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, _decode(proc.stdout).strip()


def git(*args: str) -> tuple[int, str]:
    return run("git", *args)


def registrar(
    checks: list[Check],
    nome: str,
    condicao: bool,
    ok: str,
    erro: str,
    *,
    warn: bool = False,
) -> None:
    if condicao:
        checks.append(Check(nome, "PASS", ok))
    else:
        checks.append(Check(nome, "WARN" if warn else "FAIL", erro))


def arquivos_versionados() -> list[str]:
    code, out = git("ls-files")
    if code != 0:
        return []
    return [linha.strip().replace("\\", "/") for linha in out.splitlines() if linha.strip()]


def tamanho(path_rel: str) -> int:
    path = ROOT / path_rel
    try:
        return path.stat().st_size
    except OSError:
        return 0


def fmt_bytes(valor: int) -> str:
    unidades = ("B", "KB", "MB", "GB")
    num = float(valor)
    for unidade in unidades:
        if num < 1024 or unidade == unidades[-1]:
            return f"{num:.1f} {unidade}"
        num /= 1024
    return f"{valor} B"


def main() -> int:
    checks: list[Check] = []
    detalhes: dict[str, object] = {}

    # ------------------------------------------------------------------
    # Git e estrutura
    # ------------------------------------------------------------------
    code, branch = git("branch", "--show-current")
    registrar(
        checks,
        "Git disponível",
        code == 0 and bool(branch),
        f"Branch atual: {branch}",
        f"Falha ao identificar branch: {branch}",
    )
    detalhes["branch"] = branch

    code, status = git("status", "--short")
    registrar(
        checks,
        "Working tree limpo",
        code == 0 and not status,
        "Nenhuma alteração pendente.",
        f"Há alterações pendentes:\n{status}" if status else "Falha ao ler git status.",
    )
    detalhes["git_status"] = status

    code, upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if code == 0:
        code2, divergencia = git(
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...{upstream}",
        )
        if code2 == 0:
            partes = divergencia.split()
            ahead = int(partes[0]) if len(partes) >= 1 else -1
            behind = int(partes[1]) if len(partes) >= 2 else -1
            registrar(
                checks,
                "Sincronização com upstream",
                ahead == 0 and behind == 0,
                f"HEAD sincronizado com {upstream}.",
                f"Divergência em relação a {upstream}: ahead={ahead}, behind={behind}.",
                warn=True,
            )
            detalhes["upstream"] = {
                "nome": upstream,
                "ahead": ahead,
                "behind": behind,
            }
    else:
        checks.append(
            Check(
                "Sincronização com upstream",
                "WARN",
                "Branch atual não possui upstream configurado.",
            )
        )

    code, tags = git("tag", "--list", "archive/pre-aposentadoria-areas")
    registrar(
        checks,
        "Tag de arquivamento",
        code == 0 and "archive/pre-aposentadoria-areas" in tags.splitlines(),
        "Tag archive/pre-aposentadoria-areas encontrada.",
        "Tag archive/pre-aposentadoria-areas não encontrada.",
    )

    src_dirs = {
        p.name
        for p in (ROOT / "src").iterdir()
        if p.is_dir() and p.name != "__pycache__"
    }
    registrar(
        checks,
        "Estrutura src",
        src_dirs == PASTAS_SRC_ESPERADAS,
        "Somente as nove famílias compartilhadas permanecem em src/.",
        "Estrutura inesperada em src/: "
        f"encontrado={sorted(src_dirs)}; esperado={sorted(PASTAS_SRC_ESPERADAS)}",
    )
    detalhes["src_dirs"] = sorted(src_dirs)

    aposentadas_presentes = [
        area for area in AREAS_APOSENTADAS if (ROOT / "src" / area).exists()
    ]
    registrar(
        checks,
        "Pacotes de áreas aposentadas",
        not aposentadas_presentes,
        "Nenhum pacote aposentado permanece em src/.",
        f"Pacotes ainda presentes: {', '.join(aposentadas_presentes)}",
    )

    pipeline_dir = ROOT / "scripts" / "pipelines"
    pipelines = sorted(
        p.name
        for p in pipeline_dir.glob("*.py")
        if p.name != "__init__.py"
    )
    registrar(
        checks,
        "Executores operacionais",
        pipelines == ["executar_sprint_00.py"],
        "Somente executar_sprint_00.py permanece em scripts/pipelines/.",
        f"Executores encontrados: {pipelines}",
    )
    detalhes["pipelines"] = pipelines

    # ------------------------------------------------------------------
    # Inventário versionado
    # ------------------------------------------------------------------
    tracked = arquivos_versionados()
    detalhes["tracked_count"] = len(tracked)

    area_path_pattern = re.compile(
        r"(^|/)(matematica|fisica|ingles|biologia|pedagogia|portugues|geografia)(/|$)",
        re.IGNORECASE,
    )
    area_paths = [
        p for p in tracked
        if (
            p.startswith("src/")
            or p.startswith("tests/")
            or p.startswith("scripts/pipelines/")
        )
        and area_path_pattern.search(p)
    ]
    registrar(
        checks,
        "Código operacional de áreas aposentadas",
        not area_paths,
        "Nenhum arquivo operacional aposentado está versionado.",
        "Arquivos operacionais aposentados ainda versionados:\n"
        + "\n".join(area_paths),
    )
    detalhes["retired_operational_paths"] = area_paths

    binarios = [
        p for p in tracked
        if Path(p).suffix.lower() in EXTENSOES_BINARIAS_NAO_OPERACIONAIS
    ]
    registrar(
        checks,
        "Binários de entrega no Git",
        not binarios,
        "Nenhum DOCX/PDF/PPTX/imagem de entrega está versionado.",
        "Binários ainda versionados:\n" + "\n".join(binarios),
    )
    detalhes["tracked_delivery_binaries"] = binarios

    derivados = [
        p for p in tracked
        if p.startswith(PREFIXOS_DADOS_DERIVADOS)
        and not p.endswith(".gitkeep")
    ]
    registrar(
        checks,
        "Dados derivados no Git",
        not derivados,
        "Nenhum dado derivado está versionado.",
        "Dados derivados ainda versionados:\n" + "\n".join(derivados),
    )
    detalhes["tracked_derived_data"] = derivados

    fontes_brutas = [
        p for p in tracked
        if Path(p).name in ARQUIVOS_FONTE_BRUTA_PROIBIDOS
    ]
    registrar(
        checks,
        "Fontes brutas no Git",
        not fontes_brutas,
        "Microdados ZIP e planilha de conceito não estão versionados.",
        "Fontes brutas versionadas:\n" + "\n".join(fontes_brutas),
    )
    detalhes["tracked_raw_sources"] = fontes_brutas

    grandes = [
        {"arquivo": p, "bytes": tamanho(p), "tamanho": fmt_bytes(tamanho(p))}
        for p in tracked
        if tamanho(p) >= 5 * 1024 * 1024
    ]
    registrar(
        checks,
        "Arquivos versionados >= 5 MB",
        not grandes,
        "Nenhum arquivo versionado possui 5 MB ou mais.",
        "Arquivos grandes encontrados:\n"
        + "\n".join(f"{x['arquivo']} ({x['tamanho']})" for x in grandes),
        warn=True,
    )
    detalhes["large_tracked_files"] = grandes

    # ------------------------------------------------------------------
    # Referências e qualidade estática
    # ------------------------------------------------------------------
    referencias_aposentadas: list[str] = []
    padrao_import = re.compile(
        r"src\.(matematica|fisica|ingles|biologia|pedagogia|portugues|geografia)"
    )
    for arquivo in tracked:
        if not arquivo.endswith((".py", ".md", ".yaml", ".yml", ".toml")):
            continue
        if arquivo.startswith("documentacao/"):
            continue
        path = ROOT / arquivo
        try:
            texto = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if padrao_import.search(texto):
            referencias_aposentadas.append(arquivo)

    registrar(
        checks,
        "Imports/referências operacionais aposentadas",
        not referencias_aposentadas,
        "Nenhuma referência operacional src.<area aposentada> encontrada.",
        "Referências encontradas:\n" + "\n".join(referencias_aposentadas),
    )
    detalhes["retired_import_references"] = referencias_aposentadas

    code, diff_check = git("diff", "--check", "HEAD")
    registrar(
        checks,
        "Whitespace Git",
        code == 0 and not diff_check,
        "git diff --check sem problemas.",
        diff_check or "git diff --check falhou.",
    )

    code, compile_out = run(
        sys.executable,
        "-m",
        "compileall",
        "-q",
        "src",
        "scripts",
        "executar.py",
    )
    registrar(
        checks,
        "Compilação Python",
        code == 0,
        "Todos os módulos Python compilam.",
        compile_out or "compileall retornou erro.",
    )

    code, executor_out = run(sys.executable, "executar.py", "--listar")
    executor_ok = (
        code == 0
        and "fontes" in executor_out
        and all(area not in executor_out.lower() for area in AREAS_APOSENTADAS)
    )
    registrar(
        checks,
        "Executor unificado",
        executor_ok,
        "executar.py --listar expõe apenas o pipeline operacional.",
        executor_out or "Falha ao executar executar.py --listar.",
    )
    detalhes["executor_listar"] = executor_out

    # ------------------------------------------------------------------
    # Ambiente e testes
    # ------------------------------------------------------------------
    code, pip_check = run(sys.executable, "-m", "pip", "check")
    registrar(
        checks,
        "Integridade do ambiente Python",
        code == 0,
        pip_check or "pip check sem conflitos.",
        pip_check or "pip check retornou erro.",
        warn=True,
    )

    code, pytest_out = run(sys.executable, "-m", "pytest", "-q")
    registrar(
        checks,
        "Pytest completo",
        code == 0,
        pytest_out.splitlines()[-1] if pytest_out else "Suíte passou.",
        pytest_out or "pytest retornou erro.",
    )
    detalhes["pytest"] = pytest_out

    code, ruff_out = run(sys.executable, "-m", "ruff", "check", ".")
    registrar(
        checks,
        "Ruff",
        code == 0,
        ruff_out or "Ruff sem problemas.",
        ruff_out or "Ruff retornou erro.",
    )
    detalhes["ruff"] = ruff_out

    # ------------------------------------------------------------------
    # Resultado
    # ------------------------------------------------------------------
    totais = {
        "PASS": sum(c.status == "PASS" for c in checks),
        "WARN": sum(c.status == "WARN" for c in checks),
        "FAIL": sum(c.status == "FAIL" for c in checks),
    }

    QUALIDADE.mkdir(parents=True, exist_ok=True)
    json_path = QUALIDADE / "auditoria_final_repositorio.json"
    md_path = QUALIDADE / "auditoria_final_repositorio.md"

    payload = {
        "totais": totais,
        "checks": [asdict(c) for c in checks],
        "detalhes": detalhes,
    }
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    linhas = [
        "# Auditoria final do repositório",
        "",
        f"- PASS: **{totais['PASS']}**",
        f"- WARN: **{totais['WARN']}**",
        f"- FAIL: **{totais['FAIL']}**",
        "",
        "## Checks",
        "",
        "| Status | Verificação | Resultado |",
        "|---|---|---|",
    ]

    for check in checks:
        detalhe = check.detalhe.replace("\n", "<br>")
        linhas.append(f"| {check.status} | {check.nome} | {detalhe} |")

    linhas.extend(
        [
            "",
            "## Critério para merge",
            "",
            "A branch pode avançar para o fluxo de merge quando:",
            "",
            "- `FAIL = 0`;",
            "- warnings restantes forem compreendidos e aceitos;",
            "- working tree estiver limpo;",
            "- branch estiver sincronizada com o remoto;",
            "- snapshot/tag de arquivamento estiver preservado.",
            "",
            "## Observação",
            "",
            "Referências históricas às áreas aposentadas em `documentacao/` são permitidas. "
            "O bloqueio se aplica a dependências operacionais do código atual.",
            "",
        ]
    )

    md_path.write_text("\n".join(linhas), encoding="utf-8")

    print("=" * 78)
    print("AUDITORIA FINAL DO REPOSITÓRIO")
    print("=" * 78)
    print(f"PASS: {totais['PASS']} | WARN: {totais['WARN']} | FAIL: {totais['FAIL']}")
    print(f"Relatório: {md_path}")
    print(f"JSON:      {json_path}")

    for check in checks:
        if check.status != "PASS":
            print(f"\n[{check.status}] {check.nome}")
            print(check.detalhe)

    return 1 if totais["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
