from __future__ import annotations

from pathlib import Path


RAIZ = Path(__file__).resolve().parent


def _contar_testes(pasta: Path) -> int:
    return len(list(pasta.glob("test_*.py")))


def main() -> None:
    unitarios = RAIZ / "tests" / "unit"
    integracao = RAIZ / "tests" / "integration"
    pyproject = (RAIZ / "pyproject.toml").read_text(encoding="utf-8")

    if not unitarios.is_dir() or not integracao.is_dir():
        raise RuntimeError("Estrutura tests/unit e tests/integration não localizada.")
    if "integration: requer bases processadas" not in pyproject:
        raise RuntimeError("Marcador integration não foi registrado no pyproject.toml.")

    print("Refactor 03 — testes unitários e de integração")
    print(f"Arquivos de teste unitário: {_contar_testes(unitarios)}")
    print(f"Arquivos de teste de integração: {_contar_testes(integracao)}")
    print("Marcador pytest 'integration': configurado")
    print("Estrutura da suíte: OK")


if __name__ == "__main__":
    main()
