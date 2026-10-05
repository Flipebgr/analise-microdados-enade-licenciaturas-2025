from __future__ import annotations
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config.yaml"


def carregar_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def carregar_config_edicao(ano: int) -> dict:
    """Retorna a configuração de arquivos de uma edição conhecida."""

    config = carregar_config()
    try:
        edicao = config["edicoes"][ano]
    except KeyError as exc:
        disponiveis = ", ".join(str(valor) for valor in sorted(config.get("edicoes", {})))
        raise KeyError(f"Edição não configurada: {ano}. Disponíveis: {disponiveis}") from exc
    return edicao.copy()


def carregar_config_area(edicao: int, slug: str) -> dict:
    """Resolve configuração de área pela edição e pelo slug."""

    config = carregar_config()
    chave = slug.strip().lower()
    try:
        area = config["areas_por_edicao"][edicao][chave]
    except KeyError as exc:
        raise KeyError(f"Área não configurada na edição {edicao}: {slug!r}") from exc
    return area.copy()


def caminho_relativo(valor: str) -> Path:
    return ROOT / valor


def garantir_pastas() -> None:
    for nome in ["dados_extraidos", "dados_intermediarios", "dados_processados", "documentacao", "logs", "relatorios", "tabelas", "figuras"]:
        (ROOT / nome).mkdir(parents=True, exist_ok=True)
