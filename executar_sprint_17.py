from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.configuracao.caminhos import ROOT
from src.portugues.gerar_figuras_validadas import (
    benchmark_conceito1_validado,
    participacao_ufpa_validada,
    perfil_ab_validado,
    processo_conceito1_validado,
    regional_validada,
    sensibilidade_desempenho_validada,
)
from src.portugues.validacao_analitica import (
    associacoes_ecologicas,
    auditar_participacao_desempenho,
    comparar_itens_processo_conceito1,
    construir_sensibilidades,
    diagnosticar_outliers,
    obter_belem_ead,
    perfil_grupos_validado,
    recomendacao_grupos,
    validar_comparacoes_regionais,
)
from src.portugues.validar_resultados_sprint17 import validar_resultados_sprint17
from src.utilitarios.logs import configurar_logger


def carregar_csv(pasta: Path, nome: str) -> pd.DataFrame:
    caminho = pasta / nome
    if not caminho.exists():
        raise FileNotFoundError(
            f"Produto da Sprint 16 ausente: {caminho}. "
            "Execute python executar_sprint_16.py antes da Sprint 17."
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
    benchmarks: pd.DataFrame,
    perfil: pd.DataFrame,
    processo: pd.DataFrame,
    recomendacao: pd.DataFrame,
    associacoes: pd.DataFrame,
    outliers: pd.DataFrame,
    caminho: Path,
) -> None:
    alvo = obter_belem_ead(base)
    ufpa = base.loc[base["CO_IES"].eq(569)].copy()
    processo_ufpa = processo.loc[
        processo["REFERENCIA"].eq("UFPA — conceitos superiores")
    ].copy()
    processo_ufpa["ABS_DIF"] = pd.to_numeric(
        processo_ufpa["DIFERENCA_CONCEITO1_REFERENCIA"], errors="coerce"
    ).abs()
    processo_destaque = processo_ufpa.nlargest(12, "ABS_DIF").drop(
        columns=["ABS_DIF"]
    )

    linhas = [
        "# Sprint 17 — Validação analítica de Letras–Português",
        "",
        "## Escopo",
        "",
        f"Foram auditados **{len(base)} cursos de Letras–Português**, incluindo "
        f"**{len(ufpa)} ofertas localizadas da UFPA**. O Grupo A contém apenas "
        f"Belém EaD (`CO_CURSO={int(alvo['CO_CURSO'])}`), Conceito Enade 1.",
        "",
        "A oferta inicialmente informada de Soure permanece como não localizada nas fontes "
        "de 2025 e não recebe CO_CURSO, conceito, participação ou desempenho artificiais.",
        "",
        "A unidade principal permanece `CO_CURSO`; não há junções individuais entre temas. "
        "Relações entre perfil, processo formativo, recomendação e desempenho são ecológicas.",
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
                "nt_ger_percentil_brasil",
                "nt_ger_percentil_norte",
                "nt_ger_percentil_para",
            ]
        ].sort_values("ROTULO_OFERTA").to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Auditoria de N e participação",
        "",
        auditoria_desempenho.loc[
            auditoria_desempenho["CO_CURSO"].isin(ufpa["CO_CURSO"])
        ].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Comparações regionais e nacionais",
        "",
        comparacoes.loc[
            comparacoes["INDICADOR"].eq("nt_ger_mean")
        ].to_markdown(index=False, floatfmt=".3f"),
        "",
        "Pará, Norte e Brasil completos permanecem benchmarks descritivos sobrepostos e "
        "não são usados como grupos independentes em testes.",
        "",
        "## Sensibilidade dos grupos A–E",
        "",
        sensibilidade.to_markdown(index=False, floatfmt=".3f"),
        "",
        "O cenário presencial pode excluir a única oferta do Grupo A, pois Belém EaD é "
        "educação a distância. Essa ausência é informativa sobre comparabilidade e não é "
        "preenchida artificialmente.",
        "",
        "## Sensibilidade do benchmark da oferta Conceito 1",
        "",
        benchmarks.to_markdown(index=False, floatfmt=".3f"),
        "",
        "Os critérios de porte ±25%, ±50% e até 2x preservam modalidade, categoria "
        "administrativa e organização acadêmica. O benchmark reduz heterogeneidade "
        "observável, mas não constitui desenho causal.",
        "",
        "## Perfil demográfico, socioeconômico e trajetória",
        "",
        perfil.loc[
            perfil["GRUPO_CODIGO"].isin(["A", "B"])
        ].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Processo formativo",
        "",
        processo_destaque.to_markdown(index=False, floatfmt=".3f"),
        "",
        "QE_I20–QE_I66 são mantidos item a item. As diferenças acima ainda devem ser "
        "vinculadas aos textos oficiais no relatório final; não é criado índice único.",
        "",
        "## Recomendação",
        "",
        recomendacao.to_markdown(index=False, floatfmt=".3f"),
        "",
        "QE_I68, QE_I69 e QE_I70 são mantidos com seus significados próprios; não são "
        "automaticamente denominados satisfação.",
        "",
        "## Associações ecológicas",
        "",
        associacoes.sort_values(
            "SPEARMAN_RHO",
            key=lambda s: s.abs(),
            ascending=False,
        ).to_markdown(index=False, floatfmt=".4f"),
        "",
        "As correlações de Spearman usam cursos como unidades e não representam relações "
        "individuais nem sustentam causalidade.",
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
        "- tratar Belém EaD como a única oferta UFPA Conceito 1, sem generalizar uma unidade para um grupo populacional;",
        "- contrastar a oferta focal com as sete ofertas UFPA de conceito superior e com benchmarks estruturais;",
        "- preservar Soure como não localizada nas fontes de 2025;",
        "- informar N, dispersão, percentis e participação em todas as comparações de desempenho;",
        "- interpretar QE_I20–QE_I66 somente após associação aos rótulos oficiais;",
        "- manter QE_I68, QE_I69 e QE_I70 separados;",
        "- manter todas as relações entre temas distintos no nível ecológico do curso.",
    ]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    logger = configurar_logger(ROOT / "logs" / "sprint_17_validacao_portugues.log")
    pasta = ROOT / "dados_processados" / "portugues"

    logger.info("Carregando produtos da Sprint 16")
    base = carregar_csv(pasta, "base_analitica_cursos.csv")
    comparacoes = carregar_csv(pasta, "comparacoes_regionais_nacionais.csv")
    itens = carregar_csv(pasta, "itens_processo_formativo.csv")

    logger.info("Auditando participação, desempenho e indicadores percentuais")
    auditoria_desempenho, auditoria_indicadores = auditar_participacao_desempenho(base)
    comparacoes_validadas = validar_comparacoes_regionais(comparacoes)

    logger.info("Executando sensibilidade dos grupos A-E e do benchmark Conceito 1")
    sensibilidade, benchmarks, membros = construir_sensibilidades(base)

    logger.info("Validando perfil, processo formativo e recomendação")
    perfil = perfil_grupos_validado(base)
    processo = comparar_itens_processo_conceito1(itens, base, membros)
    recomendacao = recomendacao_grupos(base)

    logger.info("Diagnosticando outliers e associações ecológicas")
    outliers = diagnosticar_outliers(base)
    associacoes = associacoes_ecologicas(base)

    produtos = {
        "auditoria_desempenho_sprint17.csv": auditoria_desempenho,
        "auditoria_indicadores_sprint17.csv": auditoria_indicadores,
        "comparacoes_regionais_validadas_sprint17.csv": comparacoes_validadas,
        "sensibilidade_desempenho_sprint17.csv": sensibilidade,
        "sensibilidade_benchmarks_sprint17.csv": benchmarks,
        "membros_benchmarks_sprint17.csv": membros,
        "perfil_grupos_validado_sprint17.csv": perfil,
        "processo_formativo_conceito1_validado.csv": processo,
        "recomendacao_grupos_validada_sprint17.csv": recomendacao,
        "diagnostico_outliers_sprint17.csv": outliers,
        "associacoes_ecologicas_sprint17.csv": associacoes,
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, pasta / nome)

    figdir = ROOT / "figuras" / "portugues"
    figuras = [
        figdir / "validada_14_participacao_ufpa.png",
        figdir / "validada_15_sensibilidade_desempenho.png",
        figdir / "validada_16_benchmark_conceito1.png",
        figdir / "validada_17_processo_conceito1.png",
        figdir / "validada_18_perfil_ab.png",
        figdir / "validada_19_comparacao_regional.png",
    ]
    participacao_ufpa_validada(base, figuras[0])
    sensibilidade_desempenho_validada(sensibilidade, figuras[1])
    benchmark_conceito1_validado(benchmarks, figuras[2])
    processo_conceito1_validado(processo, figuras[3])
    perfil_ab_validado(perfil, figuras[4])
    regional_validada(comparacoes_validadas, figuras[5])

    gerar_relatorio_validacao(
        base,
        auditoria_desempenho,
        comparacoes_validadas,
        sensibilidade,
        benchmarks,
        perfil,
        processo,
        recomendacao,
        associacoes,
        outliers,
        ROOT / "relatorios" / "sprint_17_validacao_letras_portugues.md",
    )

    validar_resultados_sprint17(
        base,
        auditoria_desempenho,
        auditoria_indicadores,
        comparacoes_validadas,
        sensibilidade,
        benchmarks,
        processo,
        figuras,
    )
    logger.info(
        "Sprint 17 concluída: %d cursos auditados, %d benchmarks e %d figuras validadas",
        len(base),
        len(benchmarks),
        len(figuras),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
