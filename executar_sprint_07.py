from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analise.construir_benchmarks import construir_benchmark_comparavel
from src.analise.estatisticas_descritivas import adicionar_posicoes, resumo_por_grupo
from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo, garantir_pastas
from src.core.configuracao_area import INGLES
from src.extracao.extrair_zip import extrair_e_manifestar
from src.ingles.agregar_ingles import agregar_temas_ingles, juntar_um_para_um
from src.ingles.comparacoes_regionais import construir_comparacoes_regionais
from src.ingles.gerar_figuras import (
    comparacao_regional,
    distribuicao_notas,
    painel_ufpa,
    perfil_socioeconomico,
    posicao_relativa,
    processo_formativo,
)
from src.ingles.preparar_catalogo import preparar_catalogo_ingles
from src.ingles.validar_ingles import validar_base_ingles
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")


def gerar_relatorio_piloto(
    base: pd.DataFrame,
    comparacoes: pd.DataFrame,
    benchmark_resumo: pd.DataFrame,
    caminho: Path,
) -> None:
    ufpa = base[base["CO_IES"].eq(INGLES.co_ies_focal)].copy()
    colunas = [
        "CO_CURSO", "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "INSCRITOS_NUM",
        "PARTICIPANTES_NUM", "TAXA_PARTICIPACAO_OFICIAL", "nt_ger_count",
        "nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "nt_ger_percentil_brasil",
    ]
    linhas = [
        "# Sprint 07 — Piloto de Letras–Inglês",
        "",
        "## Síntese",
        "",
        f"A base analítica reúne **{len(base)} cursos** de Letras–Inglês. "
        f"Foram localizadas **{len(ufpa)} ofertas da UFPA**, das quais "
        f"**{int(ufpa['CONCEITO_ENADE_NUM'].eq(1).sum())}** possuem Conceito Enade 1.",
        "",
        "A unidade de análise é `CO_CURSO`. As tabelas temáticas foram agregadas "
        "separadamente e unidas apenas após a redução para uma linha por curso.",
        "",
        "## Ofertas da UFPA",
        "",
        ufpa[colunas].sort_values("ROTULO_OFERTA").to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Comparações regionais e nacionais",
        "",
        comparacoes[comparacoes["INDICADOR"].eq("nt_ger_mean")].to_markdown(
            index=False, floatfmt=".3f"
        ),
        "",
        "As médias ponderadas usam o número de participantes válidos em `NT_GER`. "
        "As médias simples tratam cada curso com o mesmo peso.",
        "",
        "## Benchmark comparável",
        "",
        benchmark_resumo.to_markdown(index=False),
        "",
        "## Limitações",
        "",
        "- não há identificação comum de estudante entre arquivos temáticos;",
        "- associações entre indicadores de arquivos diferentes são ecológicas;",
        "- cursos pequenos podem apresentar estimativas instáveis;",
        "- os benchmarks são descritivos e não constituem desenho causal;",
        "- itens de processo formativo não foram condensados em índice único.",
    ]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    garantir_pastas()
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "sprint_07.log")
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
    logger.info("Preparando catálogo nacional de Letras–Inglês")
    cursos = preparar_catalogo_ingles(extraida, conceito_path)
    codigos = cursos["CO_CURSO"].astype(int).tolist()

    logger.info("Agregando desempenho, perfil, trajetória, processo formativo e recomendação")
    temas = agregar_temas_ingles(pasta_dados, codigos)
    base = juntar_um_para_um(cursos, [
        ("desempenho", temas["desempenho"]),
        ("demografia", temas["demografia"]),
        ("trajetoria", temas["trajetoria"]),
        ("socioeconomico", temas["socioeconomico"]),
        ("processo_formativo", temas["processo_formativo"]),
        ("recomendacao", temas["recomendacao"]),
    ])
    base = adicionar_posicoes(base)
    validar_base_ingles(base)

    comparaveis, resumo_comparaveis = construir_benchmark_comparavel(base)
    comparacoes = construir_comparacoes_regionais(base)
    indicadores = [
        "nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "taxa_presenca_microdados",
        "renda_ate_3sm_pct", "trabalha_pct", "acao_afirmativa_pct",
        "auxilio_permanencia_pct", "qe_i68_media", "qe_i69_media",
    ]
    benchmarks_amplos = resumo_por_grupo(base, indicadores)

    out = ROOT / "dados_processados" / "ingles"
    produtos = {
        "cursos_ingles.csv": cursos,
        "agregado_desempenho.csv": temas["desempenho"],
        "agregado_demografia.csv": temas["demografia"],
        "agregado_trajetoria.csv": temas["trajetoria"],
        "agregado_socioeconomico.csv": temas["socioeconomico"],
        "agregado_processo_formativo.csv": temas["processo_formativo"],
        "agregado_recomendacao.csv": temas["recomendacao"],
        "base_analitica_cursos.csv": base,
        "benchmarks_amplos.csv": benchmarks_amplos,
        "benchmark_comparavel_cursos.csv": comparaveis,
        "benchmarks_comparaveis.csv": resumo_comparaveis,
        "comparacoes_regionais_nacionais.csv": comparacoes,
        "distribuicao_sexo.csv": temas["distribuicao_sexo"],
        "distribuicao_turno.csv": temas["distribuicao_turno"],
        "distribuicao_socioeconomica.csv": temas["distribuicao_socioeconomica"],
        "regras_indicadores_socioeconomicos.csv": temas["regras_socioeconomicos"],
        "itens_processo_formativo.csv": temas["itens_processo_formativo"],
        "diagnostico_consistencia_processo.csv": temas["diagnostico_processo"],
        "distribuicao_recomendacao.csv": temas["distribuicao_recomendacao"],
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, out / nome)

    figdir = ROOT / "figuras" / "ingles"
    painel_ufpa(base, figdir / "01_painel_ofertas_ufpa.png")
    posicao_relativa(base, figdir / "02_posicao_relativa_nt_ger.png")
    distribuicao_notas(
        temas["desempenho_individual"],
        cursos,
        "NT_GER",
        figdir / "03_distribuicao_nt_ger.png",
    )
    distribuicao_notas(
        temas["desempenho_individual"],
        cursos,
        "NT_OBJ",
        figdir / "04_distribuicao_nt_obj.png",
    )
    distribuicao_notas(
        temas["desempenho_individual"],
        cursos,
        "NT_DIS",
        figdir / "05_distribuicao_nt_dis.png",
    )
    perfil_socioeconomico(base, figdir / "06_perfil_socioeconomico.png")
    processo_formativo(
        temas["itens_processo_formativo"],
        cursos,
        figdir / "07_processo_formativo.png",
    )
    comparacao_regional(comparacoes, figdir / "08_comparacao_regional_nacional.png")

    gerar_relatorio_piloto(
        base, comparacoes, resumo_comparaveis,
        ROOT / "relatorios" / "sprint_07_piloto_letras_ingles.md",
    )
    logger.info(
        "Sprint 7 concluída: %s cursos de Letras–Inglês, %s ofertas da UFPA e 8 figuras",
        len(base), int(base["CO_IES"].eq(INGLES.co_ies_focal).sum()),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
