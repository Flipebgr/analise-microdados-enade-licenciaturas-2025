from __future__ import annotations

from pathlib import Path
import pandas as pd

from executar_sprint_01 import preparar_catalogo
from src.agregacao.comum import carregar_filtrado, converter_numerico
from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo, garantir_pastas
from src.extracao.extrair_zip import extrair_e_manifestar
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger
from src.analise.validar_indicadores import auditar_desempenho, auditar_indicadores
from src.analise.validar_benchmarks import sensibilidade_benchmarks
from src.analise.analise_sensibilidade import sensibilidade_desempenho
from src.analise.consistencia_dimensoes import diagnosticar_dimensoes, DIMENSOES
from src.validacao.validar_resultados_matematica import validar_resultados
from src.visualizacao.graficos_matematica_validados import (
    grafico_auditoria_participacao, grafico_sensibilidade, grafico_benchmarks,
)


def salvar(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def carregar_base_sprint1() -> pd.DataFrame:
    path = ROOT / "dados_processados" / "matematica" / "base_analitica_cursos.csv"
    if not path.exists():
        raise FileNotFoundError("Execute primeiro: python executar_sprint_01.py")
    return pd.read_csv(path)


def gerar_relatorio(
    auditoria: pd.DataFrame,
    indicadores: pd.DataFrame,
    benchmarks: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    dimensoes: pd.DataFrame,
    path: Path,
) -> None:
    ufpa = auditoria[auditoria["GRUPO_CODIGO"].isin(["A", "B"])]
    linhas = [
        "# Sprint 2 — Validação analítica de Matemática", "",
        "## Resumo executivo", "",
        "Esta sprint auditou indicadores, grupos, benchmarks e estabilidade dos resultados do piloto de Matemática.", "",
        f"Foram auditadas **{len(auditoria)} ofertas** e **{len(benchmarks)} combinações curso-alvo × critério de benchmark**.", "",
        "## Auditoria de participação — UFPA", "",
        ufpa[["CO_CURSO", "ROTULO_OFERTA", "PARTICIPANTES_NUM", "registros_microdados", "nt_ger_count", "diferenca_participantes_oficial_nt_ger", "alerta_diferenca_participantes"]].to_markdown(index=False), "",
        "## Indicadores percentuais", "",
        f"Foram verificados **{len(indicadores)} indicadores**. Indicadores fora do domínio 0–1: **{int(indicadores['fora_0_1'].sum())}**.", "",
        "## Sensibilidade dos benchmarks", "",
        benchmarks.to_markdown(index=False, floatfmt=".3f"), "",
        "As diferenças variam com o critério de porte. Resultados estáveis em direção entre critérios recebem maior confiança descritiva; mudanças de sinal devem ser tratadas como sensibilidade relevante.", "",
        "## Sensibilidade do desempenho", "",
        sensibilidade.to_markdown(index=False, floatfmt=".3f"), "",
        "## Dimensões do processo formativo", "",
        dimensoes.to_markdown(index=False, floatfmt=".3f"), "",
        "Os agrupamentos são diagnósticos preliminares. Nenhuma dimensão deve ser incorporada ao relatório final sem conferência textual dos itens no questionário oficial.", "",
        "## Decisões metodológicas", "",
        "- manter média e mediana em paralelo;",
        "- apresentar análises ponderadas e não ponderadas;",
        "- informar cursos excluídos por N mínimo;",
        "- usar benchmark amplo para contexto e benchmark comparável para contraste;",
        "- não interpretar associações agregadas como relações individuais;",
        "- não criar índice único de QE_I20–QE_I66.", "",
        "## Limitações", "",
        "- grupos A e B contêm poucos cursos da UFPA;",
        "- critérios determinísticos de comparabilidade não equivalem a desenho causal;",
        "- consistência interna não substitui validade de conteúdo;",
        "- diferenças entre participantes oficiais e notas válidas precisam aparecer nas figuras e tabelas.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    garantir_pastas()
    logger = configurar_logger(ROOT / "logs" / "sprint_02.log")
    cfg = carregar_config()
    zip_path = caminho_relativo(cfg["arquivos"]["zip_microdados"])
    conceito_path = caminho_relativo(cfg["arquivos"]["conceito_enade"])
    extraida = caminho_relativo(cfg["arquivos"]["pasta_extraida"])
    if not zip_path.exists() or not conceito_path.exists():
        logger.error("Arquivos brutos ausentes em dados_brutos/")
        return 2
    if not extraida.exists() or not list(extraida.rglob("microdados2025_arq1.txt")):
        extrair_e_manifestar(zip_path, extraida)

    logger.info("Carregando produtos da Sprint 1")
    base = carregar_base_sprint1()
    # Revalida o catálogo diretamente nas fontes para detectar divergências estruturais.
    catalogo = preparar_catalogo(extraida, conceito_path)
    if set(base["CO_CURSO"]) != set(catalogo["CO_CURSO"]):
        raise ValueError("A base da Sprint 1 não corresponde ao catálogo atual de Matemática.")

    logger.info("Auditando indicadores e participação")
    auditoria = auditar_desempenho(base)
    indicadores = auditar_indicadores(base)

    logger.info("Executando sensibilidade de benchmarks")
    benchmarks, membros = sensibilidade_benchmarks(base)
    sensibilidade = sensibilidade_desempenho(base)

    logger.info("Diagnosticando dimensões do processo formativo")
    pasta_dados = encontrar_arquivo(extraida, "microdados2025_arq1.txt").parent
    itens = sorted({item for valores in DIMENSOES.values() for item in valores})
    dados_qe = carregar_filtrado(pasta_dados / "microdados2025_arq4.txt", base["CO_CURSO"].astype(int).tolist(), usecols=["CO_CURSO", *itens])
    for item in itens:
        dados_qe[item] = converter_numerico(dados_qe[item]).where(lambda s: s.between(1, 6))
    dimensoes = diagnosticar_dimensoes(dados_qe)

    validar_resultados(auditoria, indicadores, benchmarks, sensibilidade)

    out = ROOT / "dados_processados" / "matematica"
    salvar(auditoria, out / "auditoria_desempenho.csv")
    salvar(indicadores, out / "auditoria_indicadores.csv")
    salvar(benchmarks, out / "sensibilidade_benchmarks.csv")
    salvar(membros, out / "benchmark_sensibilidade_membros.csv")
    salvar(sensibilidade, out / "sensibilidade_desempenho.csv")
    salvar(dimensoes, out / "diagnostico_dimensoes_processo.csv")

    figdir = ROOT / "figuras" / "matematica"
    grafico_auditoria_participacao(auditoria, figdir / "validada_04_participacao.png")
    grafico_sensibilidade(sensibilidade, figdir / "validada_03_sensibilidade_desempenho.png")
    grafico_benchmarks(benchmarks, figdir / "validada_08_benchmark_comparavel.png")

    gerar_relatorio(auditoria, indicadores, benchmarks, sensibilidade, dimensoes, ROOT / "relatorios" / "sprint_02_validacao_matematica.md")
    logger.info("Sprint 2 concluída: %s auditorias, %s benchmarks e 3 figuras", len(auditoria), len(benchmarks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
