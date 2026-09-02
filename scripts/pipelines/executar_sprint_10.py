from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analise.estatisticas_descritivas import adicionar_posicoes, resumo_por_grupo
from src.biologia import BIOLOGIA, CO_CURSO_SOURE
from src.biologia.agregar_biologia import agregar_temas_biologia, juntar_um_para_um
from src.biologia.analise_soure import (
    construir_benchmark_soure,
    construir_comparacao_focal,
    construir_perfil_diferencial_soure,
    resumir_percentis_soure,
)
from src.biologia.comparacoes_regionais import construir_comparacoes_regionais
from src.biologia.gerar_figuras import (
    benchmark_soure,
    comparacao_regional,
    desempenho_ufpa,
    distribuicao_notas_focal,
    painel_ufpa,
    percentis_soure,
    perfil_diferencial,
    perfil_socioeconomico_focal,
    posicao_relativa,
    processo_formativo_focal,
    recomendacao_focal,
)
from src.biologia.preparar_catalogo import preparar_catalogo_biologia
from src.biologia.validar_biologia import validar_base_biologia
from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo, garantir_pastas
from src.extracao.extrair_zip import extrair_e_manifestar
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")


def gerar_relatorio_piloto(
    base: pd.DataFrame,
    comparacoes: pd.DataFrame,
    benchmark_resumo: pd.DataFrame,
    comparacao_focal: pd.DataFrame,
    diferencas: pd.DataFrame,
    caminho: Path,
) -> None:
    ufpa = base[base["CO_IES"].eq(BIOLOGIA.co_ies_focal)].copy()
    soure = ufpa[pd.to_numeric(ufpa["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)]
    colunas = [
        "CO_CURSO", "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "INSCRITOS_NUM",
        "PARTICIPANTES_NUM", "TAXA_PARTICIPACAO_OFICIAL", "nt_ger_count",
        "nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "nt_ger_percentil_brasil",
        "nt_ger_percentil_norte", "nt_ger_percentil_para",
    ]
    linhas = [
        "# Sprint 10 — Ciências Biológicas com estudo focal de Soure",
        "",
        "## Síntese",
        "",
        f"A base analítica reúne **{len(base)} cursos** de Ciências Biológicas. "
        f"Foram localizadas **{len(ufpa)} ofertas da UFPA**. Não há oferta da UFPA "
        "com Conceito Enade 1; por isso, o contraste principal não reproduz o desenho "
        "usado nas áreas com Conceito 1.",
        "",
        "A oferta de **Soure (CO_CURSO 104640)** é o caso focal. A análise geral da área "
        "é preservada, mas Soure é contrastada com as demais ofertas da UFPA, outras IES "
        "do Pará, Norte sem Pará, Brasil sem Norte e benchmark estruturalmente comparável.",
        "",
        "A unidade de análise principal é `CO_CURSO`. Arquivos temáticos são tratados e "
        "agregados separadamente antes de qualquer junção. Não há join individual entre "
        "arquivos distintos.",
        "",
        "## Ofertas da UFPA",
        "",
        ufpa[colunas].sort_values("ROTULO_OFERTA").to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Oferta focal de Soure",
        "",
        soure[colunas].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Comparações regionais e nacionais",
        "",
        comparacoes[comparacoes["INDICADOR"].eq("nt_ger_mean")].to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Benchmark comparável de Soure",
        "",
        benchmark_resumo.to_markdown(index=False),
        "",
        "## Comparação focal",
        "",
        comparacao_focal.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Perfil diferencial de Soure",
        "",
        diferencas.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Limitações",
        "",
        "- não há identificação comum de estudante entre arquivos temáticos;",
        "- relações entre indicadores de arquivos diferentes são ecológicas;",
        "- o estudo focal de Soure é descritivo e comparativo, não causal;",
        "- cursos pequenos podem apresentar estimativas instáveis;",
        "- o benchmark é descritivo e sua composição será submetida à análise de sensibilidade;",
        "- itens de processo formativo não são condensados em índice único sem validação.",
    ]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    garantir_pastas()
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "sprint_10_biologia.log")
    zip_path = caminho_relativo(cfg["arquivos"]["zip_microdados"])
    conceito_path = caminho_relativo(cfg["arquivos"]["conceito_enade"])
    extraida = caminho_relativo(cfg["arquivos"]["pasta_extraida"])
    if not zip_path.exists() or not conceito_path.exists():
        logger.error("Arquivos brutos ausentes em dados_brutos/")
        return 2
    if not extraida.exists() or not list(extraida.rglob("microdados2025_arq1.txt")):
        logger.info("Extraindo pacote de microdados")
        extrair_e_manifestar(zip_path, extraida)

    pasta_dados = encontrar_arquivo(extraida, "microdados2025_arq1.txt").parent
    logger.info("Preparando catálogo nacional de Ciências Biológicas")
    cursos = preparar_catalogo_biologia(extraida, conceito_path)
    codigos = cursos["CO_CURSO"].astype(int).tolist()

    logger.info("Agregando desempenho, perfil, trajetória, processo formativo e recomendação")
    temas = agregar_temas_biologia(pasta_dados, codigos)
    base = juntar_um_para_um(cursos, [
        ("desempenho", temas["desempenho"]),
        ("demografia", temas["demografia"]),
        ("trajetoria", temas["trajetoria"]),
        ("socioeconomico", temas["socioeconomico"]),
        ("processo_formativo", temas["processo_formativo"]),
        ("recomendacao", temas["recomendacao"]),
    ])
    base = adicionar_posicoes(base)
    validar_base_biologia(base)

    comparacoes = construir_comparacoes_regionais(base)
    benchmark_cursos, benchmark_resumo = construir_benchmark_soure(base)
    comparacao_focal = construir_comparacao_focal(base)
    diferencas = construir_perfil_diferencial_soure(base, benchmark_cursos)
    percentis = resumir_percentis_soure(base)

    indicadores = [
        "nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "taxa_presenca_microdados",
        "renda_ate_3sm_pct", "trabalha_pct", "acao_afirmativa_pct",
        "auxilio_permanencia_pct", "qe_i68_media", "qe_i69_media",
    ]
    benchmarks_amplos = resumo_por_grupo(base, indicadores)

    out = ROOT / "dados_processados" / "biologia"
    produtos = {
        "cursos_biologia.csv": cursos,
        "agregado_desempenho.csv": temas["desempenho"],
        "agregado_demografia.csv": temas["demografia"],
        "agregado_trajetoria.csv": temas["trajetoria"],
        "agregado_socioeconomico.csv": temas["socioeconomico"],
        "agregado_processo_formativo.csv": temas["processo_formativo"],
        "agregado_recomendacao.csv": temas["recomendacao"],
        "base_analitica_cursos.csv": base,
        "benchmarks_amplos.csv": benchmarks_amplos,
        "benchmark_soure_cursos.csv": benchmark_cursos,
        "benchmark_soure_resumo.csv": benchmark_resumo,
        "comparacoes_regionais_nacionais.csv": comparacoes,
        "comparacao_focal_soure.csv": comparacao_focal,
        "perfil_diferencial_soure.csv": diferencas,
        "percentis_soure.csv": percentis,
        "distribuicao_sexo.csv": temas["distribuicao_sexo"],
        "distribuicao_turno.csv": temas["distribuicao_turno"],
        "distribuicao_socioeconomica.csv": temas["distribuicao_socioeconomica"],
        "regras_indicadores_socioeconomicos.csv": temas["regras_socioeconomicos"],
        "itens_processo_formativo.csv": temas["itens_processo_formativo"],
        "diagnostico_consistencia_processo.csv": temas["diagnostico_processo"],
        "distribuicao_recomendacao.csv": temas["distribuicao_recomendacao"],
        "desempenho_individual_soure.csv": temas["desempenho_individual"][
            pd.to_numeric(temas["desempenho_individual"]["CO_CURSO"], errors="coerce").eq(CO_CURSO_SOURE)
        ],
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, out / nome)

    figdir = ROOT / "figuras" / "biologia"
    painel_ufpa(base, figdir / "01_painel_ofertas_ufpa.png")
    posicao_relativa(base, figdir / "02_posicao_relativa_nt_ger.png")
    distribuicao_notas_focal(
        temas["desempenho_individual"],
        cursos,
        "NT_GER",
        figdir / "03_distribuicao_nt_ger_foco_soure.png",
    )
    distribuicao_notas_focal(
        temas["desempenho_individual"],
        cursos,
        "NT_OBJ",
        figdir / "04_distribuicao_nt_obj_foco_soure.png",
    )
    distribuicao_notas_focal(
        temas["desempenho_individual"],
        cursos,
        "NT_DIS",
        figdir / "05_distribuicao_nt_dis_foco_soure.png",
    )
    perfil_socioeconomico_focal(base, figdir / "06_perfil_socioeconomico_foco_soure.png")
    processo_formativo_focal(
        temas["itens_processo_formativo"],
        cursos,
        figdir / "07_processo_formativo_foco_soure.png",
    )
    comparacao_regional(comparacoes, figdir / "08_comparacao_regional_nacional.png")
    desempenho_ufpa(base, figdir / "09_desempenho_ofertas_ufpa.png")
    percentis_soure(percentis, figdir / "10_percentis_soure.png")
    benchmark_soure(base, benchmark_cursos, figdir / "11_benchmark_soure.png")
    recomendacao_focal(base, figdir / "12_recomendacao_foco_soure.png")
    perfil_diferencial(diferencas, figdir / "13_perfil_diferencial_soure.png")

    gerar_relatorio_piloto(
        base, comparacoes, benchmark_resumo, comparacao_focal, diferencas,
        ROOT / "relatorios" / "sprint_10_piloto_biologia.md",
    )
    logger.info(
        "Sprint 10 concluída: %s cursos de Ciências Biológicas, %s ofertas da UFPA, "
        "Soure focal e 13 figuras",
        len(base), int(base["CO_IES"].eq(BIOLOGIA.co_ies_focal).sum()),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
