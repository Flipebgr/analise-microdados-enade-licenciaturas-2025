from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.configuracao.caminhos import ROOT
from src.pedagogia.gerar_figuras_validadas import (
    contraste_interno_validado,
    participacao_ufpa_validada,
    perfil_interno_validado,
    processo_castanhal_validado,
    regional_validada,
    sensibilidade_benchmarks_validada,
)
from src.pedagogia.validacao_analitica import (
    associacoes_ecologicas,
    auditar_participacao_desempenho,
    comparar_itens_processo_castanhal,
    diagnosticar_outliers,
    perfil_validado,
    resumo_contraste_interno,
    sensibilidade_benchmarks_pedagogia,
    validar_comparacoes_regionais,
)
from src.pedagogia.validar_resultados import validar_resultados_sprint14
from src.utilitarios.logs import configurar_logger


def carregar_csv(pasta: Path, nome: str) -> pd.DataFrame:
    caminho = pasta / nome
    if not caminho.exists():
        raise FileNotFoundError(
            f"Produto da Sprint 13 ausente: {caminho}. "
            "Execute python executar_sprint_13.py antes da Sprint 14."
        )
    return pd.read_csv(caminho)


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")


def gerar_relatorio_validacao(
    base: pd.DataFrame,
    auditoria_desempenho: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    contraste: pd.DataFrame,
    itens: pd.DataFrame,
    associacoes: pd.DataFrame,
    outliers: pd.DataFrame,
    caminho: Path,
) -> None:
    ufpa = base.loc[base["CO_IES"].eq(569)].copy()
    principal = sensibilidade.loc[
        sensibilidade["CENARIO"].eq("estrutura_porte_0_5_2_0")
    ].copy()
    itens_c4 = itens.loc[itens["REFERENCIA"].eq("UFPA — Conceito 4")].copy()
    itens_c4["ABS_DIF"] = pd.to_numeric(
        itens_c4["DIFERENCA_CASTANHAL_REFERENCIA"], errors="coerce"
    ).abs()
    itens_destaque = itens_c4.nlargest(12, "ABS_DIF").drop(columns=["ABS_DIF"])

    linhas = [
        "# Sprint 14 — Validação analítica de Pedagogia",
        "",
        "## Escopo",
        "",
        "A validação mantém `CO_CURSO` como unidade principal. Não há oferta da UFPA "
        "com Conceito Enade 1 em Pedagogia. O contraste interno é Castanhal, Conceito 5, "
        "versus as seis ofertas UFPA Conceito 4, sem interpretar Conceito 4 como insuficiência.",
        "",
        "As relações entre temas distintos são exclusivamente ecológicas no nível do curso. "
        "Não foram reconstruídos estudantes nem feitas junções individuais entre arquivos temáticos.",
        "",
        "## Ofertas UFPA auditadas",
        "",
        ufpa[
            [
                "CO_CURSO",
                "ROTULO_OFERTA",
                "CONCEITO_ENADE_NUM",
                "INSCRITOS_NUM",
                "PARTICIPANTES_NUM",
                "TAXA_PARTICIPACAO_OFICIAL",
                "taxa_presenca_microdados",
                "nt_ger_mean",
                "nt_obj_mean",
                "nt_dis_mean",
            ]
        ].sort_values("ROTULO_OFERTA").to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Auditoria de N e participação",
        "",
        auditoria_desempenho.loc[
            auditoria_desempenho["CO_CURSO"].isin(ufpa["CO_CURSO"])
        ].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Contraste interno UFPA",
        "",
        contraste.to_markdown(index=False, floatfmt=".3f"),
        "",
        "A diferença Castanhal menos média das ofertas Conceito 4 é apresentada como "
        "contraste descritivo entre cursos. O grupo Conceito 5 possui apenas uma oferta, "
        "portanto não é tratado como população independente para inferência estatística.",
        "",
        "## Sensibilidade dos benchmarks",
        "",
        principal[
            [
                "CO_CURSO_ALVO",
                "ROTULO_ALVO",
                "CONCEITO_ALVO",
                "N_CURSOS",
                "nt_ger_mean_ALVO",
                "nt_ger_mean_MEDIA_BENCHMARK",
                "nt_ger_mean_DIFERENCA",
                "nt_ger_mean_Z",
                "nt_obj_mean_DIFERENCA",
                "nt_dis_mean_DIFERENCA",
            ]
        ].to_markdown(index=False, floatfmt=".3f"),
        "",
        "Foram avaliados cinco cenários por oferta: modalidade; modalidade e categoria; "
        "modalidade, categoria e organização; estrutura com porte 0,5x–2x; e estrutura "
        "com porte 0,75x–1,5x. O benchmark reduz heterogeneidade observável, mas não é "
        "um desenho causal.",
        "",
        "## Processo formativo",
        "",
        "QE_I20–QE_I66 são mantidos item a item. Nesta sprint, a comparação identifica "
        "os códigos com maiores diferenças entre Castanhal e as ofertas UFPA Conceito 4. "
        "A interpretação substantiva exige vinculação ao texto oficial do item; não foi "
        "criado índice único.",
        "",
        itens_destaque.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Associações ecológicas",
        "",
        associacoes.sort_values(
            "SPEARMAN_RHO",
            key=lambda s: s.abs(),
            ascending=False,
        ).to_markdown(index=False, floatfmt=".3f"),
        "",
        "As correlações de Spearman acima usam cursos, não estudantes. Não representam "
        "associações individuais e não sustentam causalidade.",
        "",
        "## Outliers",
        "",
        outliers.loc[outliers["OUTLIER_IQR"]].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Decisões para o relatório final",
        "",
        "- preservar Castanhal como referência interna, não como prova de efeito do Conceito 5;",
        "- apresentar N, dispersão e participação para cada oferta da UFPA;",
        "- usar benchmarks estruturais por oferta e análise de sensibilidade;",
        "- manter comparações territoriais com média simples e ponderada por participantes;",
        "- interpretar processo formativo apenas com rótulos oficiais;",
        "- manter associações entre temas no nível ecológico.",
    ]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    logger = configurar_logger(ROOT / "logs" / "sprint_14_validacao_pedagogia.log")
    pasta = ROOT / "dados_processados" / "pedagogia"

    logger.info("Carregando produtos da Sprint 13")
    base = carregar_csv(pasta, "base_analitica_cursos.csv")
    comparacoes = carregar_csv(pasta, "comparacoes_regionais_nacionais.csv")
    itens_processo = carregar_csv(pasta, "itens_processo_formativo.csv")

    logger.info("Auditando participação, desempenho e indicadores percentuais")
    auditoria_desempenho, auditoria_indicadores = auditar_participacao_desempenho(base)
    comparacoes_validadas = validar_comparacoes_regionais(comparacoes)

    logger.info("Executando sensibilidade dos benchmarks das sete ofertas da UFPA")
    sensibilidade, membros = sensibilidade_benchmarks_pedagogia(base)

    logger.info("Validando contraste interno, perfil e processo formativo")
    contraste = resumo_contraste_interno(base)
    perfil = perfil_validado(base)
    itens = comparar_itens_processo_castanhal(itens_processo, base, membros)

    logger.info("Diagnosticando outliers e associações ecológicas")
    outliers = diagnosticar_outliers(base)
    associacoes = associacoes_ecologicas(base)

    produtos = {
        "auditoria_desempenho_sprint14.csv": auditoria_desempenho,
        "auditoria_indicadores_sprint14.csv": auditoria_indicadores,
        "comparacoes_regionais_validadas_sprint14.csv": comparacoes_validadas,
        "sensibilidade_benchmarks_sprint14.csv": sensibilidade,
        "membros_benchmarks_sprint14.csv": membros,
        "contraste_interno_ufpa_validado.csv": contraste,
        "perfil_recortes_validado.csv": perfil,
        "processo_formativo_castanhal_validado.csv": itens,
        "diagnostico_outliers_sprint14.csv": outliers,
        "associacoes_ecologicas_sprint14.csv": associacoes,
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, pasta / nome)

    figdir = ROOT / "figuras" / "pedagogia"
    figuras = [
        figdir / "validada_14_participacao_ufpa.png",
        figdir / "validada_15_contraste_interno_ufpa.png",
        figdir / "validada_16_benchmarks_por_oferta.png",
        figdir / "validada_17_processo_castanhal.png",
        figdir / "validada_18_perfil_interno_ufpa.png",
        figdir / "validada_19_comparacao_regional.png",
    ]
    participacao_ufpa_validada(base, figuras[0])
    contraste_interno_validado(contraste, figuras[1])
    sensibilidade_benchmarks_validada(sensibilidade, figuras[2])
    processo_castanhal_validado(itens, figuras[3])
    perfil_interno_validado(perfil, figuras[4])
    regional_validada(comparacoes_validadas, figuras[5])

    gerar_relatorio_validacao(
        base,
        auditoria_desempenho,
        sensibilidade,
        contraste,
        itens,
        associacoes,
        outliers,
        ROOT / "relatorios" / "sprint_14_validacao_pedagogia.md",
    )

    validar_resultados_sprint14(
        base,
        auditoria_desempenho,
        auditoria_indicadores,
        comparacoes_validadas,
        sensibilidade,
        contraste,
        itens,
        figuras,
    )
    logger.info(
        "Sprint 14 concluída: %d cursos auditados, %d cenários-oferta e %d figuras validadas",
        len(base),
        len(sensibilidade),
        len(figuras),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
