from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo, garantir_pastas
from src.extracao.extrair_zip import extrair_e_manifestar
from src.core.configuracao_area import MATEMATICA
from src.matematica.agregar_matematica import juntar_um_para_um
from src.matematica.preparar_catalogo import preparar_catalogo_matematica
from src.matematica.validar_matematica import validar_base_matematica
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger
from src.agregacao.agregar_desempenho import agregar_desempenho
from src.agregacao.agregar_demografia import agregar_demografia
from src.agregacao.agregar_trajetoria import agregar_trajetoria
from src.agregacao.agregar_socioeconomico import agregar_socioeconomico
from src.agregacao.agregar_processo_formativo import agregar_processo_formativo
from src.agregacao.agregar_recomendacao import agregar_recomendacao
from src.analise.construir_benchmarks import construir_benchmark_comparavel
from src.analise.estatisticas_descritivas import adicionar_posicoes, resumo_por_grupo
from src.analise.tamanhos_efeito import contrastes_desempenho
from src.visualizacao.graficos_matematica import (
    painel_ufpa, posicao_relativa, boxplot_desempenho, ecdf_desempenho,
    indicadores_socio, heatmap_processo, recomendacao,
)

AREA = MATEMATICA.co_grupo
CO_IES_UFPA = MATEMATICA.co_ies_focal


def salvar_csv(df: pd.DataFrame, path: Path, encoding: str = "utf-8-sig") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding=encoding)



def gerar_relatorio(base: pd.DataFrame, grupos: pd.DataFrame, efeitos: pd.DataFrame, benchmark_resumo: pd.DataFrame, diagnostico: pd.DataFrame, path: Path) -> None:
    ufpa = base[base["CO_IES"].eq(CO_IES_UFPA)].copy()
    foco = ufpa[ufpa["GRUPO_CODIGO"].eq("A")]
    contraste = ufpa[ufpa["GRUPO_CODIGO"].eq("B")]
    linhas = [
        "# Sprint 1 — Piloto de Matemática",
        "",
        "## Resumo executivo",
        "",
        f"A base analítica contém **{len(base)} cursos de Matemática**, dos quais **{len(ufpa)}** pertencem à UFPA. Foram classificados **{len(foco)}** cursos da UFPA no grupo A (Conceito Enade 1) e **{len(contraste)}** no grupo B (conceito superior).",
        "",
        "A unidade analítica final é `CO_CURSO`. Todos os arquivos temáticos foram tratados separadamente e agregados antes da junção um-para-um.",
        "",
        "## Grupos comparativos",
        "",
        grupos.to_markdown(index=False),
        "",
        "## Desempenho — cursos da UFPA",
        "",
        ufpa[["CO_CURSO", "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "PARTICIPANTES_NUM", "nt_ger_count", "nt_ger_mean", "nt_ger_median", "nt_ger_std", "nt_ger_percentil_brasil"]].sort_values("nt_ger_mean").to_markdown(index=False, floatfmt=".2f"),
        "",
        "## Contrastes exploratórios de NT_GER",
        "",
        efeitos.to_markdown(index=False, floatfmt=".3f"),
        "",
        "Os tamanhos de efeito descrevem diferenças de distribuição entre participantes nos arquivos de desempenho. Não estabelecem causalidade e não vinculam nota a respostas de outros arquivos.",
        "",
        "## Benchmark comparável",
        "",
        benchmark_resumo.to_markdown(index=False),
        "",
        "## Processo formativo",
        "",
        diagnostico.to_markdown(index=False, floatfmt=".3f"),
        "",
        "O alfa total é apenas diagnóstico. Não foi criado índice único para QE_I20–QE_I66 porque o bloco reúne dimensões teoricamente distintas.",
        "",
        "## Produtos gráficos",
        "",
        "1. painel das ofertas da UFPA;",
        "2. posição relativa nacional;",
        "3. boxplot e ECDF de NT_GER;",
        "4. indicadores socioeconômicos agregados;",
        "5. heatmap do processo formativo;",
        "6. recomendação do curso e da instituição.",
        "",
        "## Limitações",
        "",
        "- não há chave individual entre arquivos;",
        "- associações entre desempenho, perfil e percepção são ecológicas;",
        "- percentuais de cursos pequenos podem ser instáveis;",
        "- o benchmark comparável desta sprint usa filtros determinísticos, não pareamento causal;",
        "- os itens de processo formativo ainda exigem validação dimensional antes de índices.",
        "",
        "## Decisão para a próxima sprint",
        "",
        "Validar os gráficos, os indicadores derivados e os critérios do benchmark antes de iniciar a redação ABNT definitiva ou replicar o protocolo para outras áreas.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    garantir_pastas()
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "sprint_01.log")
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
    logger.info("Preparando catálogo nacional de Matemática")
    cursos = preparar_catalogo_matematica(extraida, conceito_path)
    codigos = cursos["CO_CURSO"].astype(int).tolist()

    logger.info("Agregando desempenho")
    desempenho, individual_desempenho = agregar_desempenho(pasta_dados / "microdados2025_arq3.txt", codigos)
    logger.info("Agregando demografia")
    demografia, dist_sexo = agregar_demografia(pasta_dados / "microdados2025_arq5.txt", pasta_dados / "microdados2025_arq6.txt", codigos)
    logger.info("Agregando trajetória")
    trajetoria, dist_turno = agregar_trajetoria(pasta_dados / "microdados2025_arq2.txt", codigos)
    logger.info("Agregando perfil socioeconômico")
    socio, dist_socio, regras_socio = agregar_socioeconomico(pasta_dados, codigos)
    logger.info("Agregando processo formativo")
    processo, itens_processo, diagnostico = agregar_processo_formativo(pasta_dados / "microdados2025_arq4.txt", codigos)
    logger.info("Agregando recomendação")
    recomend, dist_recomend = agregar_recomendacao(pasta_dados / "microdados2025_arq26.txt", pasta_dados / "microdados2025_arq27.txt", pasta_dados / "microdados2025_arq28.txt", codigos)

    base = juntar_um_para_um(cursos, [
        ("desempenho", desempenho), ("demografia", demografia), ("trajetoria", trajetoria),
        ("socioeconomico", socio), ("processo_formativo", processo), ("recomendacao", recomend),
    ])
    base = adicionar_posicoes(base)
    validar_base_matematica(base)

    comparaveis, resumo_comparaveis = construir_benchmark_comparavel(base)
    indicadores_resumo = ["nt_ger_mean", "nt_obj_mean", "nt_dis_mean", "taxa_presenca_microdados", "renda_ate_3sm_pct", "trabalha_pct", "acao_afirmativa_pct", "auxilio_permanencia_pct", "qe_i68_media", "qe_i69_media"]
    resumo_grupos = resumo_por_grupo(base, indicadores_resumo)
    efeitos = contrastes_desempenho(individual_desempenho, cursos, "NT_GER")

    out = ROOT / "dados_processados" / "matematica"
    salvar_csv(cursos, out / "cursos_matematica.csv")
    salvar_csv(desempenho, out / "agregado_desempenho.csv")
    salvar_csv(demografia, out / "agregado_demografia.csv")
    salvar_csv(trajetoria, out / "agregado_trajetoria.csv")
    salvar_csv(socio, out / "agregado_socioeconomico.csv")
    salvar_csv(processo, out / "agregado_processo_formativo.csv")
    salvar_csv(recomend, out / "agregado_recomendacao.csv")
    salvar_csv(base, out / "base_analitica_cursos.csv")
    salvar_csv(resumo_grupos, out / "benchmarks_amplos.csv")
    salvar_csv(comparaveis, out / "benchmark_comparavel_cursos.csv")
    salvar_csv(resumo_comparaveis, out / "benchmarks_comparaveis.csv")
    salvar_csv(efeitos, out / "contrastes_tamanho_efeito.csv")
    salvar_csv(dist_sexo, out / "distribuicao_sexo.csv")
    salvar_csv(dist_turno, out / "distribuicao_turno.csv")
    salvar_csv(dist_socio, out / "distribuicao_socioeconomica.csv")
    salvar_csv(regras_socio, out / "regras_indicadores_socioeconomicos.csv")
    salvar_csv(itens_processo, out / "itens_processo_formativo.csv")
    salvar_csv(diagnostico, out / "diagnostico_consistencia_processo.csv")
    salvar_csv(dist_recomend, out / "distribuicao_recomendacao.csv")

    figdir = ROOT / "figuras" / "matematica"
    painel_ufpa(base, figdir / "01_painel_ofertas_ufpa.png")
    posicao_relativa(base, figdir / "02_posicao_relativa_nt_ger.png")
    boxplot_desempenho(individual_desempenho, cursos, figdir / "03_boxplot_nt_ger_grupos.png")
    ecdf_desempenho(individual_desempenho, cursos, figdir / "04_ecdf_nt_ger_grupos.png")
    indicadores_socio(base, figdir / "05_indicadores_socioeconomicos.png")
    heatmap_processo(itens_processo, cursos, figdir / "06_heatmap_processo_formativo.png")
    recomendacao(base, figdir / "07_recomendacao.png")

    grupos = cursos.groupby(["GRUPO_CODIGO", "GRUPO"], observed=True).agg(N_CURSOS=("CO_CURSO", "nunique"), N_PARTICIPANTES_OFICIAIS=("PARTICIPANTES_NUM", "sum")).reset_index()
    gerar_relatorio(base, grupos, efeitos, resumo_comparaveis, diagnostico, ROOT / "relatorios" / "sprint_01_piloto_matematica.md")
    logger.info("Sprint 1 concluída: %s cursos de Matemática e %s figuras", len(base), 7)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
