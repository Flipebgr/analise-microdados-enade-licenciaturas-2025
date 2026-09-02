from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.biologia.gerar_figuras_validadas import (
    componentes_soure_validado,
    participacao_ufpa_validada,
    perfil_focal_validado,
    processo_itens_validado,
    recomendacao_validada,
    sensibilidade_benchmark_validada,
)
from src.biologia.validacao_analitica import (
    associacoes_ecologicas,
    auditar_participacao_desempenho,
    comparar_itens_processo_soure,
    desempenho_individual_soure,
    diagnosticar_dimensoes_exploratorias,
    diagnosticar_outliers,
    perfil_focal,
    sensibilidade_benchmark_soure,
    validar_comparacoes_regionais,
)
from src.biologia.validar_resultados import validar_resultados_sprint11
from src.configuracao.caminhos import ROOT
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def gerar_relatorio_validacao(
    base: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    descritas_individuais: pd.DataFrame,
    correlacoes_individuais: pd.DataFrame,
    perfil: pd.DataFrame,
    itens: pd.DataFrame,
    associacoes: pd.DataFrame,
    path: Path,
) -> None:
    soure = base.loc[base["RECORTE_FOCAL"].eq("Soure")].iloc[0]
    benchmark_cenario = sensibilidade.loc[sensibilidade["CENARIO"].eq("estrutura_porte_0_5_2_0")]
    linhas = [
        "# Sprint 11 — Validação analítica de Ciências Biológicas com foco em Soure",
        "",
        "## Resumo executivo",
        "",
        f"Foram auditados **{len(base)} cursos de Ciências Biológicas**, incluindo **5 ofertas da UFPA**. "
        "A oferta focal é Soure (`CO_CURSO=104640`). Não existe oferta UFPA com Conceito Enade 1; "
        "portanto, a validação preserva Soure como caso focal e usa referências territoriais e estruturais.",
        "",
        "## Soure — participação e desempenho",
        "",
        pd.DataFrame([{
            "CO_CURSO": soure["CO_CURSO"],
            "INSCRITOS": soure.get("INSCRITOS_NUM"),
            "PARTICIPANTES": soure.get("PARTICIPANTES_NUM"),
            "TAXA_PARTICIPACAO_OFICIAL": soure.get("TAXA_PARTICIPACAO_OFICIAL"),
            "NT_GER": soure.get("nt_ger_mean"),
            "NT_OBJ": soure.get("nt_obj_mean"),
            "NT_DIS": soure.get("nt_dis_mean"),
            "PERCENTIL_BRASIL": soure.get("nt_ger_percentil_brasil"),
            "PERCENTIL_NORTE": soure.get("nt_ger_percentil_norte"),
            "PERCENTIL_PARA": soure.get("nt_ger_percentil_para"),
        }]).to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Sensibilidade do benchmark de Soure",
        "",
        sensibilidade.to_markdown(index=False, floatfmt=".3f"),
        "",
        "O benchmark é recalculado sob filtros progressivos de modalidade, categoria administrativa, "
        "organização acadêmica e porte. A estabilidade das diferenças é usada como diagnóstico de robustez, não como prova causal.",
        "",
        "## Desempenho individual no mesmo arquivo temático",
        "",
        descritas_individuais.to_markdown(index=False, floatfmt=".3f"),
        "",
        correlacoes_individuais.to_markdown(index=False, floatfmt=".4f"),
        "",
        "As correlações individuais acima usam apenas variáveis do mesmo arquivo de desempenho. "
        "Relações entre nota, acertos e proficiência podem ser parcialmente mecânicas.",
        "",
        "## Perfil diferencial",
        "",
        perfil.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Processo formativo",
        "",
        itens.loc[itens["REFERENCIA"].eq("Benchmark comparável")].sort_values(
            "DIFERENCA_SOURE_REFERENCIA"
        ).to_markdown(index=False, floatfmt=".3f"),
        "",
        "Os códigos QE_I20–QE_I66 permanecem sem interpretação substantiva automática. "
        "Antes do relatório final, cada código deverá ser vinculado ao texto oficial do item, com conferência da direção da escala e de possíveis itens invertidos.",
        "",
        "## Associações ecológicas",
        "",
        associacoes.to_markdown(index=False, floatfmt=".4f"),
        "",
        "Essas associações são calculadas entre indicadores agregados por curso e não representam relações individuais.",
        "",
        "## Síntese preliminar a validar no relatório final",
        "",
        "A análise de sensibilidade permite verificar se a distância observada para Soure em NT_GER e, especialmente, NT_OBJ "
        "permanece quando a referência é restringida a cursos estruturalmente semelhantes. NT_DIS deve ser interpretada separadamente, "
        "pois pode apresentar padrão distinto. Nenhuma dessas diferenças é interpretada como efeito causal.",
    ]
    if not benchmark_cenario.empty:
        linhas.extend([
            "",
            "### Cenário estrutural principal",
            "",
            benchmark_cenario.to_markdown(index=False, floatfmt=".3f"),
        ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    logger = configurar_logger(ROOT / "logs" / "sprint_11_biologia.log")
    pasta = ROOT / "dados_processados" / "biologia"
    base_path = pasta / "base_analitica_cursos.csv"
    comparacoes_path = pasta / "comparacoes_regionais_nacionais.csv"
    benchmark_path = pasta / "benchmark_soure_cursos.csv"
    itens_path = pasta / "itens_processo_formativo.csv"
    individual_path = pasta / "desempenho_individual_soure.csv"
    obrigatorios = [base_path, comparacoes_path, benchmark_path, itens_path, individual_path]
    if any(not path.exists() for path in obrigatorios):
        logger.error("Produtos da Sprint 10 ausentes. Execute python executar_sprint_10.py")
        return 2

    logger.info("Carregando produtos da Sprint 10")
    base = pd.read_csv(base_path)
    comparacoes = pd.read_csv(comparacoes_path)
    benchmark = pd.read_csv(benchmark_path)
    itens = pd.read_csv(itens_path)
    individual = pd.read_csv(individual_path)

    logger.info("Auditando participação, desempenho e indicadores percentuais")
    auditoria_desempenho, auditoria_indicadores = auditar_participacao_desempenho(base)
    comparacoes_validadas = validar_comparacoes_regionais(comparacoes)

    logger.info("Executando sensibilidade do benchmark focal de Soure")
    sensibilidade, membros = sensibilidade_benchmark_soure(base)

    logger.info("Aprofundando desempenho, perfil e processo formativo de Soure")
    descritas_individuais, correlacoes_individuais = desempenho_individual_soure(individual)
    perfil = perfil_focal(base)
    comparacao_itens = comparar_itens_processo_soure(itens, base, benchmark)
    dimensoes_resumo, dimensoes_scores = diagnosticar_dimensoes_exploratorias(base)

    logger.info("Diagnosticando outliers e associações ecológicas")
    outliers = diagnosticar_outliers(base)
    associacoes = associacoes_ecologicas(base)

    produtos = {
        "auditoria_desempenho_sprint11.csv": auditoria_desempenho,
        "auditoria_indicadores_sprint11.csv": auditoria_indicadores,
        "comparacoes_regionais_validadas_sprint11.csv": comparacoes_validadas,
        "sensibilidade_benchmark_soure.csv": sensibilidade,
        "sensibilidade_benchmark_soure_membros.csv": membros,
        "desempenho_individual_soure_descritivas.csv": descritas_individuais,
        "desempenho_individual_soure_correlacoes.csv": correlacoes_individuais,
        "perfil_focal_soure_validado.csv": perfil,
        "processo_formativo_soure_itens_validado.csv": comparacao_itens,
        "dimensoes_processo_exploratorias.csv": dimensoes_resumo,
        "dimensoes_processo_scores_exploratorios.csv": dimensoes_scores,
        "diagnostico_outliers_sprint11.csv": outliers,
        "associacoes_ecologicas_sprint11.csv": associacoes,
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, pasta / nome)

    figdir = ROOT / "figuras" / "biologia"
    figuras = [
        figdir / "validada_14_participacao_ufpa.png",
        figdir / "validada_15_componentes_soure.png",
        figdir / "validada_16_sensibilidade_benchmark_soure.png",
        figdir / "validada_17_processo_itens_soure.png",
        figdir / "validada_18_perfil_focal_soure.png",
        figdir / "validada_19_recomendacao_soure.png",
    ]
    participacao_ufpa_validada(base, figuras[0])
    componentes_soure_validado(base, benchmark, figuras[1])
    sensibilidade_benchmark_validada(sensibilidade, figuras[2])
    processo_itens_validado(comparacao_itens, figuras[3])
    perfil_focal_validado(perfil, figuras[4])
    recomendacao_validada(perfil, figuras[5])

    gerar_relatorio_validacao(
        base,
        sensibilidade,
        descritas_individuais,
        correlacoes_individuais,
        perfil,
        comparacao_itens,
        associacoes,
        ROOT / "relatorios" / "sprint_11_validacao_biologia_soure.md",
    )
    validar_resultados_sprint11(
        base,
        auditoria_desempenho,
        auditoria_indicadores,
        sensibilidade,
        comparacao_itens,
        figuras,
    )
    logger.info(
        "Sprint 11 concluída: %d cursos auditados, %d cenários de benchmark e %d figuras validadas",
        len(base),
        len(sensibilidade),
        len(figuras),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
