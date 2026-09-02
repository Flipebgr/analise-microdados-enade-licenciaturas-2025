from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.configuracao.caminhos import ROOT
from src.ingles.gerar_figuras_validadas import (
    benchmark_validado,
    participacao_validada,
    regional_validado,
    sensibilidade_validada,
)
from src.ingles.validacao_analitica import (
    associacoes_ecologicas,
    auditar_participacao_desempenho,
    construir_sensibilidades,
    diagnosticar_outliers,
    sintetizar_socioeconomico_ufpa,
    validar_comparacoes_regionais,
)
from src.ingles.validar_resultados import validar_resultados_sprint08
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def gerar_relatorio(
    base: pd.DataFrame,
    auditoria_desempenho: pd.DataFrame,
    comparacoes: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    benchmarks: pd.DataFrame,
    outliers: pd.DataFrame,
    associacoes: pd.DataFrame,
    socio_ufpa: pd.DataFrame,
    path: Path,
) -> None:
    ufpa = base[base["CO_IES"].eq(569)]
    linhas = [
        "# Sprint 08 — Validação analítica de Letras–Inglês",
        "",
        "## Resumo executivo",
        "",
        f"Foram auditados **{len(base)} cursos de Letras–Inglês**, incluindo "
        f"**{len(ufpa)} ofertas da UFPA**. A unidade de análise permanece `CO_CURSO`.",
        "",
        "## Participação e desempenho",
        "",
        auditoria_desempenho[auditoria_desempenho["CO_CURSO"].isin(ufpa["CO_CURSO"])].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Comparações regionais e nacionais",
        "",
        comparacoes[comparacoes["INDICADOR"].eq("nt_ger_mean")].to_markdown(index=False, floatfmt=".3f"),
        "",
        "As referências Norte e Brasil são benchmarks descritivos sobrepostos e não são tratadas como grupos independentes em testes.",
        "",
        "## Sensibilidade do desempenho",
        "",
        sensibilidade.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Sensibilidade do benchmark comparável",
        "",
        benchmarks.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Perfil socioeconômico das ofertas da UFPA",
        "",
        socio_ufpa.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Diagnóstico de outliers",
        "",
        outliers[outliers["OUTLIER_IQR"]].to_markdown(index=False, floatfmt=".3f") if outliers["OUTLIER_IQR"].any() else "Nenhum outlier de NT_GER pela regra exploratória de 1,5×IQR.",
        "",
        "Os outliers não são excluídos automaticamente; são apenas sinalizados para análise de sensibilidade.",
        "",
        "## Associações ecológicas",
        "",
        associacoes.to_markdown(index=False, floatfmt=".4f"),
        "",
        "As correlações são ecológicas, calculadas entre indicadores agregados por curso. Não representam associações individuais e não sustentam inferência causal.",
        "",
        "## Processo formativo",
        "",
        "A Sprint 07 preservou `QE_I20–QE_I66` em nível agregado por curso e item e não formou índice único. A validação mantém essa decisão até confirmação teórica dos itens e da escala.",
        "",
        "## Decisões para o relatório final",
        "",
        "- manter N válido, dispersão e ausências junto aos indicadores;",
        "- apresentar média simples e média ponderada por participantes nas comparações territoriais;",
        "- manter grupos A–E exclusivos para comparações independentes;",
        "- apresentar benchmarks comparáveis com análise de sensibilidade de porte;",
        "- tratar relações entre perfil, processo formativo e desempenho apenas no nível ecológico do curso;",
        "- não interpretar modalidade, interiorização ou baixo N como explicação causal sem desenho apropriado.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    logger = configurar_logger(ROOT / "logs" / "sprint_08.log")
    pasta = ROOT / "dados_processados" / "ingles"
    base_path = pasta / "base_analitica_cursos.csv"
    comparacoes_path = pasta / "comparacoes_regionais_nacionais.csv"
    if not base_path.exists() or not comparacoes_path.exists():
        logger.error("Produtos da Sprint 07 ausentes. Execute python executar_sprint_07.py")
        return 2

    logger.info("Carregando produtos da Sprint 07")
    base = pd.read_csv(base_path)
    comparacoes = pd.read_csv(comparacoes_path)

    logger.info("Auditando participação, desempenho e indicadores percentuais")
    auditoria_desempenho, auditoria_indicadores = auditar_participacao_desempenho(base)
    comparacoes_validadas = validar_comparacoes_regionais(comparacoes)

    logger.info("Executando sensibilidade de desempenho e benchmarks")
    sensibilidade, benchmarks, membros = construir_sensibilidades(base)

    logger.info("Diagnosticando outliers e associações ecológicas")
    outliers = diagnosticar_outliers(base)
    associacoes = associacoes_ecologicas(base)
    socio_ufpa = sintetizar_socioeconomico_ufpa(base)

    produtos = {
        "auditoria_desempenho_sprint08.csv": auditoria_desempenho,
        "auditoria_indicadores_sprint08.csv": auditoria_indicadores,
        "comparacoes_regionais_validadas.csv": comparacoes_validadas,
        "sensibilidade_desempenho.csv": sensibilidade,
        "sensibilidade_benchmarks.csv": benchmarks,
        "sensibilidade_benchmark_membros.csv": membros,
        "diagnostico_outliers_nt_ger.csv": outliers,
        "associacoes_ecologicas.csv": associacoes,
        "tabela_socioeconomica_ufpa.csv": socio_ufpa,
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, pasta / nome)

    figdir = ROOT / "figuras" / "ingles"
    figuras = [
        figdir / "validada_09_participacao_ufpa.png",
        figdir / "validada_10_sensibilidade_desempenho.png",
        figdir / "validada_11_benchmark_comparavel.png",
        figdir / "validada_12_comparacao_regional.png",
    ]
    participacao_validada(base, figuras[0])
    sensibilidade_validada(sensibilidade, figuras[1])
    benchmark_validado(benchmarks, figuras[2])
    regional_validado(comparacoes_validadas, figuras[3])

    gerar_relatorio(
        base,
        auditoria_desempenho,
        comparacoes_validadas,
        sensibilidade,
        benchmarks,
        outliers,
        associacoes,
        socio_ufpa,
        ROOT / "relatorios" / "sprint_08_validacao_letras_ingles.md",
    )
    validar_resultados_sprint08(
        base,
        auditoria_desempenho,
        auditoria_indicadores,
        comparacoes_validadas,
        sensibilidade,
        benchmarks,
        figuras,
    )
    logger.info(
        "Sprint 8 concluída: %d cursos auditados, %d benchmarks e %d figuras validadas",
        len(base), len(benchmarks), len(figuras),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
