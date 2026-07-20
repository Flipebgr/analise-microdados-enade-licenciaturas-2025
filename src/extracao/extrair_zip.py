from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile
import hashlib
import pandas as pd


def sha256_arquivo(path: Path, bloco: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for parte in iter(lambda: f.read(bloco), b""):
            h.update(parte)
    return h.hexdigest()


def extrair_e_manifestar(zip_path: Path, destino: Path) -> pd.DataFrame:
    destino.mkdir(parents=True, exist_ok=True)
    linhas: list[dict] = []
    with ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            nome = info.filename
            temporario = Path(nome).name.startswith("~$")
            linhas.append({
                "caminho_no_zip": nome,
                "nome": Path(nome).name,
                "extensao": Path(nome).suffix.lower(),
                "tamanho_bytes": info.file_size,
                "temporario_office": temporario,
                "categoria": "temporario" if temporario else ("microdados" if nome.endswith(".txt") else "documentacao"),
            })
            if not temporario:
                zf.extract(info, destino)
    return pd.DataFrame(linhas)
