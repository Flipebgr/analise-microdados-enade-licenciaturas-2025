from __future__ import annotations
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config.yaml"


def carregar_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def caminho_relativo(valor: str) -> Path:
    return ROOT / valor


def garantir_pastas() -> None:
    for nome in ["dados_extraidos", "dados_intermediarios", "dados_processados", "documentacao", "logs", "relatorios", "tabelas", "figuras"]:
        (ROOT / nome).mkdir(parents=True, exist_ok=True)
