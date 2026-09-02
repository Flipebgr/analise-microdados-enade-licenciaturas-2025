from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.configuracao.caminhos import ROOT
from src.geografia.gerar_figuras_validadas import (
    contraste_interno_validado,
    participacao_ufpa_validada,
    perfil_interno_validado,
    processo_grupos_validado,
    regional_validada,
    sensibilidade_benchmarks_validada,
)
from src.geografia.validacao_analitica import (
    associacoes_ecologicas,
    auditar_participacao_desempenho,
    comparar_itens_processo_grupos,
    diagnosticar_outliers,
    perfil_validado,
    recomendacao_validada,
    resumo_contraste_interno,
    sensibilidade_benchmarks_geografia,
    validar_comparacoes_regionais,
)
from src.geografia.validar_resultados_sprint20 import (
    validar_resultados_sprint20,
)
from src.utilitarios.logs import configurar_logger


def carregar_csv(pasta: Path, nome: str) -> pd.DataFrame:
    caminho = pasta / nome
    if not caminho.exists():
        raise FileNotFoundError(
            f"Produto da Sprint 19 ausente: {caminho}. "
            "Execute python executar_sprint_19.py antes da Sprint 20."
        )
    return pd.read_csv(caminho, low_memory=False)


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")


def gerar_relatorio_validacao(
    base: pd.DataFrame,
    auditoria_desempenho: pd.DataFrame,
    comparacoes: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    contraste: pd.DataFrame,
    perfil: pd.DataFrame,
    processo: pd.DataFrame,
    recomendacao: pd.DataFrame,
    associacoes: pd.DataFrame,
    outliers: pd.DataFrame,
    caminho: Path,
) -> None:
    ufpa = base.loc[base["CO_IES"].eq(569)].copy()
    principal = sensibilidade.loc[
        sensibilidade["CENARIO"].eq("estrutura_porte_0_5_2_0")
    ].copy()
    processo_destaque = processo.copy()
    processo_destaque["ABS_DIF"] = pd.to_numeric(
        processo_destaque["DIFERENCA_C3_C4"],
        errors="coerce",
    ).abs()
    processo_destaque = processo_destaque.nlargest(
        12,
        "ABS_DIF",
    ).drop(columns=["ABS_DIF"])

    linhas = [
        "# Sprint 20 — Validação analítica de Geografia",
        "",
        "## Escopo",
        "",
        f"Foram auditados **{len(base)} cursos de Geografia**, incluindo "
        f"**{len(ufpa)} ofertas da UFPA**. Não existe oferta UFPA com "
        "Conceito Enade 1; o Grupo A permanece vazio.",
        "",
        "O contraste institucional principal é entre as duas ofertas UFPA "
        "Conceito 3 e as duas ofertas UFPA Conceito 4. Conceito 3 não é "
        "tratado como insuficiência e o contraste não é causal.",
        "",
        "A unidade principal permanece `CO_CURSO`; não há junções individuais "
        "entre arquivos temáticos. Relações entre temas distintos são ecológicas.",
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
        ].sort_values("ROTULO_OFERTA").to_markdown(
            index=False,
            floatfmt=".3f",
        ),
        "",
        "## Auditoria de N e participação",
        "",
        auditoria_desempenho.loc[
            auditoria_desempenho["CO_CURSO"].isin(ufpa["CO_CURSO"])
        ].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Contraste interno UFPA — Conceito 3 × Conceito 4",
        "",
        contraste.to_markdown(index=False, floatfmt=".3f"),
        "",
        "As diferenças são calculadas como média Conceito 3 menos média "
        "Conceito 4. Com apenas duas ofertas em cada estrato, tamanhos "
        "padronizados são exclusivamente descritivos.",
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
        "Foram avaliados cinco cenários por oferta, totalizando 20 "
        "combinações oferta-cenário. O benchmark reduz heterogeneidade "
        "observável, mas não constitui desenho causal.",
        "",
        "## Perfil demográfico, socioeconômico e trajetória",
        "",
        perfil.loc[
            perfil["RECORTE_GEOGRAFIA"].isin(
                ["UFPA — Conceito 3", "UFPA — Conceito 4"]
            )
        ].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Processo formativo",
        "",
        processo_destaque.to_markdown(index=False, floatfmt=".3f"),
        "",
        "QE_I20–QE_I66 permanecem item a item. A interpretação substantiva "
        "dos códigos exige vínculo com o texto oficial e não é criado índice único.",
        "",
        "## Recomendação",
        "",
        recomendacao.to_markdown(index=False, floatfmt=".3f"),
        "",
        "QE_I68, QE_I69 e QE_I70 permanecem conceitualmente separados e "
        "não são automaticamente denominados satisfação.",
        "",
        "## Comparações regionais e nacionais",
        "",
        comparacoes.loc[
            comparacoes["INDICADOR"].eq("nt_ger_mean")
        ].to_markdown(index=False, floatfmt=".3f"),
        "",
        "Pará, Norte e Brasil completos são benchmarks descritivos "
        "sobrepostos, não grupos independentes em testes.",
        "",
        "## Associações ecológicas",
        "",
        associacoes.sort_values(
            "SPEARMAN_RHO",
            key=lambda s: s.abs(),
            ascending=False,
        ).to_markdown(index=False, floatfmt=".4f"),
        "",
        "As correlações de Spearman usam cursos como unidades. Não representam "
        "associações individuais e não sustentam causalidade.",
        "",
        "## Outliers",
        "",
        (
            outliers.loc[outliers["OUTLIER_IQR"]]
            .to_markdown(index=False, floatfmt=".3f")
            if outliers["OUTLIER_IQR"].any()
            else "Nenhum outlier sinalizado pela regra exploratória de 1,5×IQR."
        ),
        "",
        "Outliers são sinalizados e preservados, não excluídos automaticamente.",
        "",
        "## Decisões para o relatório final",
        "",
        "- preservar o contraste Conceito 3 × Conceito 4 como descritivo;",
        "- informar N, dispersão e participação para cada oferta;",
        "- usar cinco cenários de benchmark por oferta;",
        "- interpretar processo formativo somente com rótulos oficiais;",
        "- manter QE_I68, QE_I69 e QE_I70 separados;",
        "- manter associações entre temas no nível ecológico do curso.",
    ]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    logger = configurar_logger(
        ROOT / "logs" / "sprint_20_validacao_geografia.log"
    )
    pasta = ROOT / "dados_processados" / "geografia"

    logger.info("Carregando produtos da Sprint 19")
    base = carregar_csv(pasta, "base_analitica_cursos.csv")
    comparacoes = carregar_csv(
        pasta,
        "comparacoes_regionais_nacionais.csv",
    )
    itens_processo = carregar_csv(
        pasta,
        "itens_processo_formativo.csv",
    )

    logger.info(
        "Auditando participação, desempenho e indicadores percentuais"
    )
    auditoria_desempenho, auditoria_indicadores = (
        auditar_participacao_desempenho(base)
    )
    comparacoes_validadas = validar_comparacoes_regionais(comparacoes)

    logger.info(
        "Executando sensibilidade dos benchmarks das quatro ofertas da UFPA"
    )
    sensibilidade, membros = sensibilidade_benchmarks_geografia(base)

    logger.info(
        "Validando contraste interno, perfil, processo formativo e recomendação"
    )
    contraste = resumo_contraste_interno(base)
    perfil = perfil_validado(base)
    processo = comparar_itens_processo_grupos(itens_processo, base)
    recomendacao = recomendacao_validada(base)

    logger.info("Diagnosticando outliers e associações ecológicas")
    outliers = diagnosticar_outliers(base)
    associacoes = associacoes_ecologicas(base)

    produtos = {
        "auditoria_desempenho_sprint20.csv": auditoria_desempenho,
        "auditoria_indicadores_sprint20.csv": auditoria_indicadores,
        "comparacoes_regionais_validadas_sprint20.csv": comparacoes_validadas,
        "sensibilidade_benchmarks_sprint20.csv": sensibilidade,
        "membros_benchmarks_sprint20.csv": membros,
        "contraste_interno_ufpa_validado_sprint20.csv": contraste,
        "perfil_recortes_validado_sprint20.csv": perfil,
        "processo_formativo_grupos_validado_sprint20.csv": processo,
        "recomendacao_recortes_validada_sprint20.csv": recomendacao,
        "diagnostico_outliers_sprint20.csv": outliers,
        "associacoes_ecologicas_sprint20.csv": associacoes,
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, pasta / nome)

    figdir = ROOT / "figuras" / "geografia"
    figuras = [
        figdir / "validada_14_participacao_ufpa.png",
        figdir / "validada_15_contraste_interno_ufpa.png",
        figdir / "validada_16_benchmarks_por_oferta.png",
        figdir / "validada_17_processo_formativo.png",
        figdir / "validada_18_perfil_interno_ufpa.png",
        figdir / "validada_19_comparacao_regional.png",
    ]

    participacao_ufpa_validada(base, figuras[0])
    contraste_interno_validado(contraste, figuras[1])
    sensibilidade_benchmarks_validada(sensibilidade, figuras[2])
    processo_grupos_validado(processo, figuras[3])
    perfil_interno_validado(perfil, figuras[4])
    regional_validada(comparacoes_validadas, figuras[5])

    gerar_relatorio_validacao(
        base,
        auditoria_desempenho,
        comparacoes_validadas,
        sensibilidade,
        contraste,
        perfil,
        processo,
        recomendacao,
        associacoes,
        outliers,
        ROOT / "relatorios" / "sprint_20_validacao_geografia.md",
    )

    validar_resultados_sprint20(
        base,
        auditoria_desempenho,
        auditoria_indicadores,
        comparacoes_validadas,
        sensibilidade,
        contraste,
        processo,
        figuras,
    )

    logger.info(
        "Sprint 20 concluída: %d cursos auditados, "
        "%d cenários-oferta e %d figuras validadas",
        len(base),
        len(sensibilidade),
        len(figuras),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
