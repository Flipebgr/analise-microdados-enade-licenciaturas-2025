from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analise.estatisticas_descritivas import adicionar_posicoes, resumo_por_grupo
from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo, garantir_pastas
from src.extracao.extrair_zip import extrair_e_manifestar
from src.pedagogia import PEDAGOGIA
from src.pedagogia.agregar_pedagogia import agregar_temas_pedagogia, juntar_um_para_um
from src.pedagogia.analise_pedagogia import (
    construir_benchmarks_por_oferta,
    construir_comparacao_interna_ufpa,
    construir_comparacao_recortes,
)
from src.pedagogia.comparacoes_regionais import construir_comparacoes_regionais
from src.pedagogia.gerar_figuras import (
    benchmarks_ufpa,
    comparacao_regional,
    contraste_interno_ufpa,
    desempenho_ufpa,
    distribuicao_notas,
    painel_ufpa,
    percentis_ufpa,
    perfil_socioeconomico,
    posicao_relativa,
    processo_formativo,
    recomendacao,
)
from src.pedagogia.preparar_catalogo import preparar_catalogo_pedagogia
from src.pedagogia.validar_pedagogia import validar_base_pedagogia
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")


def gerar_relatorio_piloto(
    base: pd.DataFrame,
    comparacoes: pd.DataFrame,
    benchmarks_resumo: pd.DataFrame,
    comparacao_recortes: pd.DataFrame,
    comparacao_interna: pd.DataFrame,
    caminho: Path,
) -> None:
    ufpa = base[base["CO_IES"].eq(PEDAGOGIA.co_ies_focal)].copy()
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
        "nt_ger_percentil_norte",
        "nt_ger_percentil_para",
    ]
    linhas = [
        "# Sprint 13 — Pedagogia: base analítica e panorama inicial",
        "",
        "## Síntese",
        "",
        f"A base analítica reúne **{len(base)} cursos** de Pedagogia. "
        f"Foram localizadas **{len(ufpa)} ofertas da UFPA**. Não há oferta da UFPA "
        "com Conceito Enade 1; portanto, o Grupo A permanece vazio.",
        "",
        "O contraste interno da UFPA compara a oferta de Castanhal, Conceito Enade 5, "
        "com as seis ofertas Conceito Enade 4. Esse contraste é descritivo e não "
        "transforma Conceito 4 em categoria de insuficiência.",
        "",
        "A unidade principal de análise é `CO_CURSO`. Cada arquivo temático é tratado "
        "e agregado separadamente antes das junções one-to-one. Não há join individual "
        "entre arquivos temáticos distintos.",
        "",
        "## Ofertas da UFPA",
        "",
        ufpa[colunas].sort_values("ROTULO_OFERTA").to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Comparação regional e nacional",
        "",
        comparacoes[comparacoes["INDICADOR"].eq("nt_ger_mean")].to_markdown(
            index=False, floatfmt=".3f"
        ),
        "",
        "## Benchmarks comparáveis por oferta UFPA",
        "",
        benchmarks_resumo.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Recortes exclusivos",
        "",
        comparacao_recortes.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Contraste interno UFPA",
        "",
        comparacao_interna.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Limitações",
        "",
        "- não há identificação comum de estudante entre arquivos temáticos;",
        "- relações entre indicadores de arquivos distintos são ecológicas;",
        "- o contraste Conceito 4 versus Conceito 5 é descritivo, não causal;",
        "- os benchmarks controlam apenas características observáveis selecionadas;",
        "- cursos com menor N podem apresentar estimativas mais instáveis;",
        "- itens de processo formativo não são condensados em índice único sem validação.",
    ]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    garantir_pastas()
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "sprint_13_pedagogia.log")
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
    logger.info("Preparando catálogo nacional de Pedagogia")
    cursos = preparar_catalogo_pedagogia(extraida, conceito_path)
    codigos = cursos["CO_CURSO"].astype(int).tolist()

    logger.info("Agregando desempenho, perfil, trajetória, processo formativo e recomendação")
    temas = agregar_temas_pedagogia(pasta_dados, codigos)
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
    validar_base_pedagogia(base)

    comparacoes = construir_comparacoes_regionais(base)
    benchmarks_cursos, benchmarks_resumo = construir_benchmarks_por_oferta(base)
    comparacao_recortes = construir_comparacao_recortes(base)
    comparacao_interna = construir_comparacao_interna_ufpa(base)

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

    out = ROOT / "dados_processados" / "pedagogia"
    produtos = {
        "cursos_pedagogia.csv": cursos,
        "agregado_desempenho.csv": temas["desempenho"],
        "agregado_demografia.csv": temas["demografia"],
        "agregado_trajetoria.csv": temas["trajetoria"],
        "agregado_socioeconomico.csv": temas["socioeconomico"],
        "agregado_processo_formativo.csv": temas["processo_formativo"],
        "agregado_recomendacao.csv": temas["recomendacao"],
        "base_analitica_cursos.csv": base,
        "benchmarks_amplos.csv": benchmarks_amplos,
        "benchmark_comparavel_cursos.csv": benchmarks_cursos,
        "benchmark_comparavel_resumo.csv": benchmarks_resumo,
        "comparacoes_regionais_nacionais.csv": comparacoes,
        "comparacao_recortes.csv": comparacao_recortes,
        "comparacao_interna_ufpa.csv": comparacao_interna,
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

    figdir = ROOT / "figuras" / "pedagogia"
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
    desempenho_ufpa(base, figdir / "09_desempenho_ofertas_ufpa.png")
    percentis_ufpa(base, figdir / "10_percentis_ofertas_ufpa.png")
    benchmarks_ufpa(benchmarks_resumo, figdir / "11_benchmarks_ofertas_ufpa.png")
    recomendacao(base, figdir / "12_recomendacao.png")
    contraste_interno_ufpa(comparacao_interna, figdir / "13_contraste_interno_ufpa.png")

    gerar_relatorio_piloto(
        base,
        comparacoes,
        benchmarks_resumo,
        comparacao_recortes,
        comparacao_interna,
        ROOT / "relatorios" / "sprint_13_piloto_pedagogia.md",
    )
    logger.info(
        "Sprint 13 concluída: %s cursos de Pedagogia, %s ofertas da UFPA e 13 figuras",
        len(base),
        int(base["CO_IES"].eq(PEDAGOGIA.co_ies_focal).sum()),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
