from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analise.construir_benchmarks import construir_benchmark_comparavel
from src.analise.estatisticas_descritivas import adicionar_posicoes, resumo_por_grupo
from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo, garantir_pastas
from src.extracao.extrair_zip import extrair_e_manifestar
from src.portugues import PORTUGUES
from src.portugues.agregar_portugues import agregar_temas_portugues, juntar_um_para_um
from src.portugues.analise_portugues import (
    construir_comparacao_grupos,
    construir_contraste_ufpa,
)
from src.portugues.comparacoes_regionais import construir_comparacoes_regionais
from src.portugues.gerar_figuras import (
    benchmark_conceito1,
    comparacao_regional,
    contraste_ufpa,
    desempenho_ufpa,
    distribuicao_notas,
    painel_ufpa,
    percentis_ufpa,
    perfil_socioeconomico,
    posicao_relativa,
    processo_formativo,
    recomendacao,
)
from src.portugues.preparar_catalogo import (
    construir_auditoria_relacao_ufpa,
    preparar_catalogo_portugues,
)
from src.portugues.validar_portugues import (
    validar_auditoria_relacao,
    validar_base_portugues,
)
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")


def gerar_relatorio_piloto(
    base: pd.DataFrame,
    auditoria: pd.DataFrame,
    comparacoes: pd.DataFrame,
    benchmark_resumo: pd.DataFrame,
    contraste: pd.DataFrame,
    caminho: Path,
) -> None:
    ufpa = base[base["CO_IES"].eq(PORTUGUES.co_ies_focal)].copy()
    conceito1 = ufpa[ufpa["CONCEITO_ENADE_NUM"].eq(1)]
    colunas = [
        "CO_CURSO",
        "ROTULO_OFERTA",
        "CONCEITO_ENADE_NUM",
        "INSCRITOS_NUM",
        "PARTICIPANTES_NUM",
        "TAXA_PARTICIPACAO_OFICIAL",
        "nt_ger_count",
        "nt_ger_mean",
        "nt_obj_mean",
        "nt_dis_mean",
        "nt_ger_percentil_brasil",
    ]
    linhas = [
        "# Sprint 16 — Base analítica de Letras–Português",
        "",
        "## Síntese",
        "",
        f"A base analítica reúne **{len(base)} cursos** de Letras–Português. "
        f"Foram localizadas **{len(ufpa)} ofertas da UFPA**, das quais "
        f"**{len(conceito1)}** possui Conceito Enade 1.",
        "",
        "A oferta inicialmente informada de **Soure** não foi localizada nem no cadastro "
        "`microdados2025_arq1.txt` da área 904 nem na planilha oficial de Conceito Enade 2025. "
        "Ela é preservada na auditoria da relação informada, mas não recebe CO_CURSO artificial, "
        "não é tratada como Conceito 1 e fica fora dos grupos comparativos.",
        "",
        "A unidade de análise é `CO_CURSO`. Cada arquivo temático é agregado separadamente "
        "antes das junções one-to-one.",
        "",
        "## Ofertas localizadas da UFPA",
        "",
        ufpa[colunas].sort_values("ROTULO_OFERTA").to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Auditoria da relação inicialmente informada",
        "",
        auditoria.to_markdown(index=False),
        "",
        "## Comparações regionais e nacionais",
        "",
        comparacoes[comparacoes["INDICADOR"].eq("nt_ger_mean")].to_markdown(
            index=False,
            floatfmt=".3f",
        ),
        "",
        "As médias ponderadas usam participantes válidos em NT_GER; as médias simples "
        "tratam cada curso com o mesmo peso.",
        "",
        "## Benchmark comparável da oferta UFPA Conceito 1",
        "",
        benchmark_resumo.to_markdown(index=False),
        "",
        "## Contraste UFPA Conceito 1 versus conceitos superiores",
        "",
        contraste.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Limitações",
        "",
        "- não há identificação comum de estudante entre arquivos temáticos;",
        "- associações entre temas diferentes somente podem ser ecológicas;",
        "- Soure não foi localizada nas duas fontes de 2025 e não recebe valores artificiais;",
        "- o Grupo A contém uma única oferta da UFPA, o que restringe inferência entre cursos;",
        "- benchmarks são descritivos e não constituem desenho causal;",
        "- QE_I20–QE_I66 não são condensados em índice único nesta sprint.",
    ]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    garantir_pastas()
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "sprint_16.log")
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
    logger.info("Preparando catálogo nacional de Letras–Português")
    cursos = preparar_catalogo_portugues(extraida, conceito_path)
    auditoria = construir_auditoria_relacao_ufpa(
        cursos,
        cfg["ofertas_informadas"],
        {int(k): v for k, v in cfg["areas"].items()},
    )
    validar_auditoria_relacao(auditoria)

    codigos = cursos["CO_CURSO"].astype(int).tolist()
    logger.info(
        "Agregando desempenho, perfil, trajetória, processo formativo e recomendação"
    )
    temas = agregar_temas_portugues(pasta_dados, codigos)
    base = juntar_um_para_um(
        cursos,
        [
            ("desempenho", temas["desempenho"]),
            ("demografia", temas["demografia"]),
            ("trajetoria", temas["trajetoria"]),
            ("socioeconomico", temas["socioeconomico"]),
            ("processo_formativo", temas["processo_formativo"]),
            ("recomendacao", temas["recomendacao"]),
        ],
    )
    base = adicionar_posicoes(base)
    validar_base_portugues(base)

    comparaveis, resumo_comparaveis = construir_benchmark_comparavel(base)
    comparacoes = construir_comparacoes_regionais(base)
    comparacao_grupos = construir_comparacao_grupos(base)
    contraste = construir_contraste_ufpa(base)

    indicadores = [
        "nt_ger_mean",
        "nt_obj_mean",
        "nt_dis_mean",
        "taxa_presenca_microdados",
        "renda_ate_3sm_pct",
        "trabalha_pct",
        "acao_afirmativa_pct",
        "auxilio_permanencia_pct",
        "qe_i68_media",
        "qe_i69_media",
    ]
    benchmarks_amplos = resumo_por_grupo(base, indicadores)

    out = ROOT / "dados_processados" / "portugues"
    produtos = {
        "cursos_portugues.csv": cursos,
        "auditoria_relacao_ufpa.csv": auditoria,
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
        "comparacao_grupos.csv": comparacao_grupos,
        "contraste_ufpa_conceito1_superiores.csv": contraste,
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

    figdir = ROOT / "figuras" / "portugues"
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
    comparacao_regional(
        comparacoes,
        figdir / "08_comparacao_regional_nacional.png",
    )
    desempenho_ufpa(base, figdir / "09_desempenho_ofertas_ufpa.png")
    percentis_ufpa(base, figdir / "10_percentis_ofertas_ufpa.png")
    benchmark_conceito1(
        base,
        comparaveis,
        figdir / "11_benchmark_conceito1.png",
    )
    recomendacao(base, figdir / "12_recomendacao.png")
    contraste_ufpa(contraste, figdir / "13_contraste_ufpa.png")

    gerar_relatorio_piloto(
        base,
        auditoria,
        comparacoes,
        resumo_comparaveis,
        contraste,
        ROOT / "relatorios" / "sprint_16_piloto_letras_portugues.md",
    )
    logger.info(
        "Sprint 16 concluída: %s cursos de Letras–Português, %s ofertas localizadas "
        "da UFPA, %s oferta UFPA Conceito 1 e 13 figuras",
        len(base),
        int(base["CO_IES"].eq(PORTUGUES.co_ies_focal).sum()),
        int(
            (
                base["CO_IES"].eq(PORTUGUES.co_ies_focal)
                & base["CONCEITO_ENADE_NUM"].eq(1)
            ).sum()
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
