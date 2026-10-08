"""Publicação de uma geração completa com staging e restauração em falhas."""
from __future__ import annotations

import json
import os
import shutil
import tempfile
import warnings
from pathlib import Path

from src.evidencias.construir import COLUNAS_PROCESSO, _registros, salvar_evidencias
from src.evidencias.validar import validar_evidencias
from src.orquestracao.area import ResultadoArea, salvar_resultado_area
from src.validacao.validar_fase_9a import validar_artefatos_fase_9a


def validar_staging(pasta: Path, resultado: ResultadoArea, pacote: dict) -> None:
    carregado = json.loads((pasta / "evidencias.json").read_text(encoding="utf-8"))
    validar_evidencias(carregado)
    if pacote["schema_version"] == "3.0":
        validar_artefatos_fase_9a(resultado.artefatos_fase_9a or {}, pacote)
    if carregado != pacote:
        raise ValueError("JSON gravado diverge das evidências em memória")
    # O JSON também precisa corresponder aos CSVs da mesma geração, não basta
    # cada representação passar isoladamente por suas validações.
    base = resultado.base_cursos
    for linhas, tabela in (
        (pacote["participacao"]["por_curso"], base),
        (pacote["desempenho"]["por_curso"], base),
        (pacote["perfil"]["indicadores_por_curso"], base),
        (
            pacote["ofertas_focais"],
            base.loc[base["CO_CURSO"].isin(pacote["universo"]["cursos_focais"])].sort_values(
                "CO_CURSO", kind="stable"
            ),
        ),
    ):
        if linhas and linhas != _registros(tabela, tuple(linhas[0])):
            raise ValueError("Evidências divergem da base agregada da geração")
        if not linhas and not tabela.empty:
            raise ValueError("Evidências omitiram linhas da base agregada")
    for linhas, tabela, colunas in (
        (pacote["universo"]["cobertura_por_curso"], resultado.auditoria_cobertura, None),
        (pacote["perfil"]["regras"], resultado.regras_indicadores, None),
        (pacote["perfil"]["distribuicoes"], resultado.distribuicoes_questionario, None),
        (pacote["processo_formativo"]["itens_por_curso"], resultado.processo_itens, COLUNAS_PROCESSO),
        (pacote["processo_formativo"]["proveniencia"], resultado.proveniencia_processo, None),
    ):
        if linhas != (_registros(tabela, colunas) if tabela is not None else []):
            raise ValueError("Evidências divergem das tabelas temáticas da geração")
    esperados = set(pacote["proveniencia"]["tabelas_auditaveis"])
    if {p.name for p in pasta.iterdir()} != esperados | {"evidencias.json"}:
        raise ValueError("Staging contém conjunto incompleto ou inesperado de artefatos")
    # Compara a representação efetivamente publicada; preserva zeros à esquerda,
    # nulidade e precisão, sem coerções de uma segunda importação CSV.
    for nome in esperados:
        if nome in (resultado.artefatos_fase_9a or {}):
            tabela = resultado.artefatos_fase_9a[nome]
        else:
            tabela = getattr(resultado, Path(nome).stem)
        if isinstance(tabela, dict):
            esperado = json.dumps(tabela, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
            gravado = (pasta / nome).read_text(encoding="utf-8")
        else:
            esperado = tabela.to_csv(index=False, sep=";", lineterminator="\n")
            gravado = (pasta / nome).read_text(encoding="utf-8-sig")
        if gravado != esperado:
            raise ValueError(f"Artefato gravado diverge do agregado validado: {nome}")


def publicar_analise(resultado: ResultadoArea, pacote: dict, destino: Path) -> list[Path]:
    """Troca o diretório completo, restaurando a geração anterior se a troca falhar.

    Staging e backup ficam no mesmo volume. Um lock exclusivo impede dois
    escritores. Não há substituição arquivo a arquivo no destino publicado.
    """
    validar_evidencias(pacote)
    destino = destino.resolve()
    fontes = [Path(pacote["proveniencia"]["fontes"][0]["caminho"]).resolve()]
    fontes.extend(Path(f["fonte"]).resolve() for f in pacote["proveniencia"]["fontes"][1:])
    if any(destino == f or f.is_relative_to(destino) or destino.is_relative_to(f) for f in fontes):
        raise ValueError("Destino de publicação sobrepõe uma fonte oficial")
    destino.parent.mkdir(parents=True, exist_ok=True)
    lock = destino.parent / f".{destino.name}.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ValueError(f"Publicação já em andamento ou lock pendente: {lock}") from exc
    os.close(fd)
    transacao = None
    preservar_backup = False
    try:
        transacao = Path(tempfile.mkdtemp(prefix=f".{destino.name}-staging-", dir=destino.parent))
        novo = transacao / "novo"
        antigo = transacao / "anterior"
        salvar_resultado_area(resultado, novo)
        salvar_evidencias(pacote, novo / "evidencias.json")
        validar_staging(novo, resultado, pacote)
        havia_anterior = destino.exists()
        if havia_anterior:
            destino.rename(antigo)
        try:
            novo.rename(destino)
        except (OSError, KeyboardInterrupt, SystemExit):
            if havia_anterior:
                try:
                    antigo.rename(destino)
                except OSError as exc:
                    preservar_backup = True
                    raise OSError(f"Restauração falhou; última saída válida preservada em {antigo}") from exc
            raise
        return [destino / nome for nome in (*pacote["proveniencia"]["tabelas_auditaveis"], "evidencias.json")]
    finally:
        try:
            if transacao is not None and not preservar_backup:
                try:
                    shutil.rmtree(transacao)
                except OSError as exc:
                    warnings.warn(f"Resíduo temporário preservado em {transacao}: {exc}", stacklevel=2)
        finally:
            lock.unlink()
