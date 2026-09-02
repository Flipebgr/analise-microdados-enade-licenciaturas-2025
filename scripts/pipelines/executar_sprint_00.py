from __future__ import annotations
import shutil
from pathlib import Path
import pandas as pd

from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo, garantir_pastas
from src.extracao.extrair_zip import extrair_e_manifestar, sha256_arquivo
from src.qualidade.inspecionar_arquivos import inspecionar_todos
from src.qualidade.gerar_relatorio_qualidade import gerar_relatorio
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger
from src.validacao.validar_planilha_conceito import carregar_conceitos, localizar_ufpa
from src.validacao.validar_cursos_ufpa import carregar_caracterizacao, construir_tabela_mestra
from src.validacao.validar_relacionamentos import validar_unicidade_tabela_mestra
from src.validacao.validar_relacao_informada import comparar_relacao_informada


def salvar_csv(df: pd.DataFrame, path: Path, encoding: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding=encoding)


def main() -> int:
    garantir_pastas()
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "sprint_00.log")
    zip_path = caminho_relativo(cfg["arquivos"]["zip_microdados"])
    conceito_path = caminho_relativo(cfg["arquivos"]["conceito_enade"])
    extraida = caminho_relativo(cfg["arquivos"]["pasta_extraida"])
    encoding_saida = cfg["saida"]["csv_encoding"]

    for path in [zip_path, conceito_path]:
        if not path.exists():
            logger.error("Arquivo obrigatório ausente: %s", path)
            return 2

    logger.info("Iniciando Sprint 0")
    logger.info("SHA256 ZIP: %s", sha256_arquivo(zip_path))
    logger.info("SHA256 conceitos: %s", sha256_arquivo(conceito_path))

    if extraida.exists():
        shutil.rmtree(extraida)
    manifesto = extrair_e_manifestar(zip_path, extraida)
    salvar_csv(manifesto, ROOT / "dados_processados" / "manifesto_arquivos.csv", encoding_saida)

    conceitos = carregar_conceitos(conceito_path)
    conceitos_ufpa = localizar_ufpa(conceitos, cfg["ufpa"]["nome_oficial"], cfg["ufpa"]["sigla"])
    co_ies = int(conceitos_ufpa["CO_IES"].dropna().iloc[0])
    logger.info("UFPA localizada com CO_IES=%s", co_ies)

    inventario, ausencias = inspecionar_todos(extraida, co_ies)
    salvar_csv(inventario, ROOT / "dados_processados" / "inventario_microdados.csv", encoding_saida)
    salvar_csv(ausencias, ROOT / "dados_processados" / "ausencias_amostra.csv", encoding_saida)

    arq1 = encontrar_arquivo(extraida, "microdados2025_arq1.txt")
    caracterizacao = carregar_caracterizacao(arq1)
    areas = {int(k): v for k, v in cfg["areas"].items()}
    mestre, divergencias = construir_tabela_mestra(caracterizacao, conceitos_ufpa, areas)
    erros = validar_unicidade_tabela_mestra(mestre)

    salvar_csv(mestre, ROOT / "dados_processados" / "tabela_mestra_ufpa.csv", encoding_saida)
    salvar_csv(divergencias, ROOT / "dados_processados" / "divergencias_ufpa.csv", encoding_saida)
    validacao_informada = comparar_relacao_informada(mestre, cfg.get("ofertas_informadas", []), areas)
    salvar_csv(validacao_informada, ROOT / "dados_processados" / "validacao_relacao_informada.csv", encoding_saida)
    gerar_relatorio(ROOT / "relatorios" / "sprint_00_relatorio_qualidade.md", manifesto, inventario, mestre, divergencias, erros)

    logger.info("Sprint 0 concluída. Ofertas na tabela-mestra: %s", len(mestre))
    if erros:
        for erro in erros:
            logger.error(erro)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
