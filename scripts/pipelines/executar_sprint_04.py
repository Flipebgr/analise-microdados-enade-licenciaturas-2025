from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.analise.estatisticas_descritivas import adicionar_posicoes
from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo, garantir_pastas
from src.extracao.extrair_zip import extrair_e_manifestar
from src.fisica.agregar_fisica import agregar_temas_fisica, juntar_um_para_um
from src.fisica.analisar_desempenho import desempenho_ufpa, referencias_nt_ger
from src.fisica.analisar_dificuldade import agregar_dificuldade
from src.fisica.analisar_presenca import construir_auditoria_presenca
from src.fisica.construir_benchmarks import construir_benchmarks_fisica
from src.fisica.gerar_figuras import (
    benchmark_comparavel,
    conceito_dificuldade,
    nota_por_oferta,
    nt_ger_comparativo,
    ofertas_ufpa,
    perfil_socioeconomico,
    sintese_socioeconomica_desempenho,
    processo_formativo,
    recomendacao,
    taxa_presenca,
)
from src.fisica.preparar_catalogo import preparar_catalogo_fisica
from src.fisica.validar_fisica import validar_base_fisica
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def gerar_relatorio(
    base: pd.DataFrame,
    auditoria: pd.DataFrame,
    referencias: pd.DataFrame,
    benchmark_resumo: pd.DataFrame,
    path: Path,
) -> None:
    ufpa = base[base["CO_IES"].eq(569)].copy()
    cols_desempenho = [
        "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "nt_ger_count", "nt_ger_mean", "nt_ger_median",
        "nt_obj_count", "nt_obj_mean", "nt_obj_median", "nt_dis_count", "nt_dis_mean", "nt_dis_median",
    ]
    linhas = [
        "# Sprint 4 — Piloto de Física",
        "",
        "## Resumo executivo",
        "",
        f"A base analítica contém **{len(base)} cursos de Física**, incluindo **{len(ufpa)} ofertas validadas da UFPA**. A análise preserva cada oferta por `CO_CURSO`, município e modalidade.",
        "",
        "Tucuruí não foi incluído nas análises porque não foi localizado com `CO_CURSO` validado nas fontes atuais.",
        "",
        "## Ofertas da UFPA",
        "",
        ufpa[["CO_CURSO", "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "INSCRITOS_NUM", "PARTICIPANTES_NUM", "PCT_PADRAO_PROFICIENCIA_NUM"]].to_markdown(index=False, floatfmt=".2f"),
        "",
        "## Taxa de presença",
        "",
        auditoria.to_markdown(index=False, floatfmt=".2f"),
        "",
        "A taxa utiliza `TP_PRES=555` sobre os registros elegíveis localizados no arquivo de desempenho. Participantes oficiais e registros válidos permanecem documentados separadamente.",
        "",
        "## NT_GER, NT_OBJ e NT_DIS por oferta",
        "",
        ufpa[[c for c in cols_desempenho if c in ufpa.columns]].sort_values("nt_ger_mean").to_markdown(index=False, floatfmt=".2f"),
        "",
        "## Nota geral comparativa",
        "",
        referencias.to_markdown(index=False, floatfmt=".2f"),
        "",
        "As referências territoriais são calculadas no nível do curso. O agregado UFPA complementa, mas não substitui, a apresentação individual das ofertas.",
        "",
        "## Conceito e percepção de dificuldade",
        "",
        ufpa[["ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "co_rs_i1_dificuldade_alta_pct", "co_rs_i2_dificuldade_alta_pct", "co_rs_i7_dificuldade_alta_pct"]].to_markdown(index=False, floatfmt=".2f"),
        "",
        "A percepção de dificuldade foi agregada por curso a partir de `CO_RS_I1`, `CO_RS_I2` e `CO_RS_I7`, todos presentes no arquivo de desempenho. A relação com o Conceito Enade é ecológica e não implica causalidade individual.",
        "",
        "## Perfil socioeconômico geral por oferta",
        "",
        ufpa[[
            "ROTULO_OFERTA", "CONCEITO_ENADE_NUM", "nt_ger_mean",
            "primeira_geracao_pct", "mae_superior_pct", "pai_superior_pct",
            "renda_ate_3sm_pct", "trabalha_pct", "trabalha_40h_pct",
            "acao_afirmativa_pct", "auxilio_permanencia_pct",
            "bolsa_academica_pct", "estudo_4h_ou_mais_pct",
            "pretende_magisterio_pct",
        ]].to_markdown(index=False, floatfmt=".3f"),
        "",
        "A tabela apresenta uma visão geral da composição socioeconômica de cada oferta. "
        "A leitura conjunta com NT_GER é descritiva e ecológica; não permite concluir que "
        "características individuais produziram as diferenças de nota.",
        "",
        "## Recomendação do curso e da instituição",
        "",
        ufpa[["ROTULO_OFERTA", "qe_i68_n", "qe_i68_nota_9_10_pct", "qe_i69_n", "qe_i69_nota_9_10_pct"]].to_markdown(index=False, floatfmt=".3f"),
        "",
        "Os títulos e interpretações deverão seguir os rótulos oficiais de `QE_I68` e `QE_I69`; os percentuais acima correspondem às avaliações 9 ou 10 entre respostas válidas.",
        "",
        "## Benchmark comparável",
        "",
        benchmark_resumo.to_markdown(index=False),
        "",
        "## Figuras produzidas",
        "",
        "1. ofertas da UFPA;",
        "2. taxa de presença por oferta;",
        "3. nota geral por oferta;",
        "4. nota geral comparativa;",
        "5. prova objetiva por oferta;",
        "6. prova discursiva por oferta;",
        "7. Conceito Enade × percepção de dificuldade;",
        "8. percepção do processo formativo;",
        "9. recomendação do curso;",
        "10. recomendação da instituição;",
        "11. perfil socioeconômico;",
        "12. benchmark comparável;",
        "13. síntese socioeconômica e desempenho.",
        "",
        "## Limitações",
        "",
        "- não existe chave individual entre arquivos temáticos;",
        "- associações entre desempenho, perfil e processo formativo são ecológicas;",
        "- cursos com N pequeno produzem estimativas mais instáveis;",
        "- os itens de processo formativo são apresentados separadamente, sem índice único não validado;",
        "- a comparação ampla não substitui o benchmark comparável.",
        "",
        "## Próxima etapa",
        "",
        "Auditar os indicadores, testar sensibilidade dos benchmarks e validar a narrativa gráfica antes da elaboração do relatório ABNT de Física.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    garantir_pastas()
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "sprint_04.log")
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
    logger.info("Preparando catálogo nacional de Física")
    cursos = preparar_catalogo_fisica(extraida, conceito_path)
    codigos = cursos["CO_CURSO"].astype(int).tolist()

    logger.info("Agregando desempenho, perfil, trajetória, processo formativo e recomendação")
    temas = agregar_temas_fisica(pasta_dados, codigos)
    logger.info("Agregando percepção de dificuldade")
    dificuldade, distribuicao_dificuldade = agregar_dificuldade(
        pasta_dados / "microdados2025_arq3.txt", codigos
    )

    base = juntar_um_para_um(cursos, [
        ("desempenho", temas["desempenho"]),
        ("demografia", temas["demografia"]),
        ("trajetoria", temas["trajetoria"]),
        ("socioeconomico", temas["socioeconomico"]),
        ("processo_formativo", temas["processo_formativo"]),
        ("recomendacao", temas["recomendacao"]),
        ("dificuldade", dificuldade),
    ])
    base = adicionar_posicoes(base)
    validar_base_fisica(base)

    auditoria = construir_auditoria_presenca(base)
    desempenho = desempenho_ufpa(base)
    referencias = referencias_nt_ger(base)
    comparaveis, resumo_comparaveis, amplos = construir_benchmarks_fisica(base)

    out = ROOT / "dados_processados" / "fisica"
    salvar_csv(cursos, out / "cursos_fisica.csv")
    salvar_csv(temas["desempenho"], out / "agregado_desempenho.csv")
    salvar_csv(temas["demografia"], out / "agregado_demografia.csv")
    salvar_csv(temas["trajetoria"], out / "agregado_trajetoria.csv")
    salvar_csv(temas["socioeconomico"], out / "agregado_socioeconomico.csv")
    salvar_csv(temas["processo_formativo"], out / "agregado_processo_formativo.csv")
    salvar_csv(temas["recomendacao"], out / "agregado_recomendacao.csv")
    salvar_csv(dificuldade, out / "percepcao_dificuldade.csv")
    salvar_csv(distribuicao_dificuldade, out / "distribuicao_dificuldade.csv")
    salvar_csv(base, out / "base_analitica_cursos.csv")
    salvar_csv(auditoria, out / "auditoria_presenca.csv")
    salvar_csv(desempenho, out / "desempenho_ufpa.csv")
    salvar_csv(referencias, out / "referencias_nt_ger.csv")
    salvar_csv(amplos, out / "benchmarks_amplos.csv")
    salvar_csv(comparaveis, out / "benchmark_comparavel_cursos.csv")
    salvar_csv(resumo_comparaveis, out / "benchmarks_comparaveis.csv")
    for nome in [
        "distribuicao_sexo", "distribuicao_turno", "distribuicao_socioeconomica",
        "regras_socioeconomicos", "itens_processo_formativo", "diagnostico_processo",
        "distribuicao_recomendacao",
    ]:
        salvar_csv(temas[nome], out / f"{nome}.csv")

    figdir = ROOT / "figuras" / "fisica"
    ofertas_ufpa(base, figdir / "01_ofertas_ufpa.png")
    taxa_presenca(auditoria, figdir / "02_taxa_presenca_ufpa.png")
    nota_por_oferta(base, "nt_ger", "Nota Geral (NT_GER) por Oferta", figdir / "03_nt_ger_por_oferta.png")
    nt_ger_comparativo(base, referencias, figdir / "04_nt_ger_comparativo.png")
    nota_por_oferta(base, "nt_obj", "Nota da Prova Objetiva (NT_OBJ) por Oferta", figdir / "05_nt_obj_por_oferta.png")
    nota_por_oferta(base, "nt_dis", "Nota da Prova Discursiva (NT_DIS) por Oferta", figdir / "06_nt_dis_por_oferta.png")
    conceito_dificuldade(base, figdir / "07_conceito_dificuldade.png")
    processo_formativo(temas["itens_processo_formativo"], cursos, figdir / "08_processo_formativo.png")
    recomendacao(base, "qe_i68_nota_9_10_pct", "Recomendação do Curso de Física", figdir / "09_recomendacao_curso.png")
    recomendacao(base, "qe_i69_nota_9_10_pct", "Recomendação da Instituição", figdir / "10_recomendacao_instituicao.png")
    perfil_socioeconomico(base, figdir / "11_perfil_socioeconomico.png")
    benchmark_comparavel(base, resumo_comparaveis, figdir / "12_benchmark_comparavel.png")
    sintese_socioeconomica_desempenho(base, figdir / "13_sintese_socioeconomica_desempenho.png")

    gerar_relatorio(
        base, auditoria, referencias, resumo_comparaveis,
        ROOT / "relatorios" / "sprint_04_piloto_fisica.md",
    )
    logger.info("Sprint 4 concluída: %s cursos de Física, %s ofertas da UFPA e 13 figuras", len(base), int(base["CO_IES"].eq(569).sum()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
