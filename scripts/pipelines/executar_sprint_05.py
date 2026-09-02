from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.configuracao.caminhos import ROOT
from src.fisica.analise_sensibilidade import sensibilidade_benchmarks
from src.fisica.associacoes_ecologicas import calcular_associacoes
from src.fisica.gerar_figuras_validadas import (
    desempenho_validado,
    dificuldade_validada,
    presenca_validada,
    socioeconomico_validado,
)
from src.fisica.validar_desempenho import auditar_desempenho, comparacao_territorial
from src.fisica.validar_dificuldade import diagnosticar_dificuldade
from src.fisica.validar_presenca import auditar_presenca
from src.fisica.validar_processo_formativo import diagnosticar_dimensoes
from src.fisica.validar_resultados_fisica import validar_resultados
from src.fisica.validar_socioeconomico import auditar_socioeconomico
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def gerar_relatorio(
    base: pd.DataFrame,
    presenca: pd.DataFrame,
    territorial: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    dificuldade_ufpa: pd.DataFrame,
    associacoes: pd.DataFrame,
    dimensoes: pd.DataFrame,
    socio_sintese: pd.DataFrame,
    path: Path,
) -> None:
    ufpa = base[base["CO_IES"].eq(569)]
    linhas = [
        "# Sprint 5 — Validação analítica de Física",
        "",
        "## Resumo executivo",
        "",
        f"Foram auditados **{len(base)} cursos de Física**, incluindo **{len(ufpa)} ofertas da UFPA**. A validação preserva `CO_CURSO` como unidade principal e mantém separadas as análises individuais disponíveis no mesmo arquivo e as associações ecológicas entre cursos.",
        "",
        "## Auditoria da presença",
        "",
        presenca.to_markdown(index=False, floatfmt=".2f"),
        "",
        "As taxas ficaram no domínio esperado. Participantes oficiais, presentes e cobertura de NT_GER foram mantidos em colunas distintas.",
        "",
        "## Comparação territorial de NT_GER",
        "",
        territorial.to_markdown(index=False, floatfmt=".2f"),
        "",
        "Os agregados Norte e Brasil são referências descritivas sobrepostas; não são tratados como grupos independentes em testes.",
        "",
        "## Sensibilidade dos benchmarks",
        "",
        sensibilidade.to_markdown(index=False, floatfmt=".2f"),
        "",
        "A estabilidade deve ser julgada pela direção e magnitude das diferenças em critérios alternativos, não pela seleção do resultado mais favorável.",
        "",
        "## Percepção de dificuldade",
        "",
        dificuldade_ufpa.to_markdown(index=False, floatfmt=".2f"),
        "",
        "A relação entre conceito, dificuldade e desempenho é ecológica no nível do curso.",
        "",
        "## Processo formativo",
        "",
        dimensoes.to_markdown(index=False, floatfmt=".3f"),
        "",
        "As dimensões são candidatas exploratórias. A redação oficial dos itens e a coerência teórica deverão ser confirmadas antes de qualquer uso como índice no relatório final.",
        "",
        "## Síntese socioeconômica por oferta",
        "",
        socio_sintese.to_markdown(index=False, floatfmt=".3f"),
        "",
        "A leitura conjunta com desempenho é contextual e não permite inferência individual.",
        "",
        "## Associações ecológicas",
        "",
        associacoes.to_markdown(index=False, floatfmt=".4f"),
        "",
        "Os valores de p são apenas exploratórios. A interpretação prioriza magnitude, direção, N de cursos, dispersão e possibilidade de outliers.",
        "",
        "## Decisões para o relatório final",
        "",
        "- manter taxa de presença, NT_GER, NT_OBJ e NT_DIS por oferta;",
        "- manter comparação territorial com distinção entre ofertas da UFPA e referências agregadas;",
        "- apresentar dificuldade no nível do curso e sem causalidade;",
        "- manter itens ou dimensões de processo formativo somente após validação teórica;",
        "- apresentar perfil socioeconômico por oferta com N e ausências;",
        "- documentar sensibilidade dos benchmarks e instabilidade associada a N pequeno.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    logger = configurar_logger(ROOT / "logs" / "sprint_05.log")
    pasta = ROOT / "dados_processados" / "fisica"
    base_path = pasta / "base_analitica_cursos.csv"
    if not base_path.exists():
        logger.error("Produtos da Sprint 4 ausentes. Execute python executar_sprint_04.py")
        return 2
    logger.info("Carregando produtos da Sprint 4")
    base = pd.read_csv(base_path)

    logger.info("Auditando presença e desempenho")
    presenca = auditar_presenca(base)
    desempenho = auditar_desempenho(base)
    territorial = comparacao_territorial(base)

    logger.info("Executando sensibilidade dos benchmarks")
    sensibilidade, membros = sensibilidade_benchmarks(base)

    logger.info("Validando dificuldade, processo formativo e perfil socioeconômico")
    dificuldade_ufpa, dificuldade_associacoes = diagnosticar_dificuldade(base)
    dimensoes, scores_dimensoes = diagnosticar_dimensoes(base)
    socio_auditoria, socio_sintese = auditar_socioeconomico(base)
    associacoes = calcular_associacoes(base)
    associacoes = pd.concat([associacoes, dificuldade_associacoes], ignore_index=True, sort=False)

    salvar_csv(presenca, pasta / "auditoria_presenca_validada.csv")
    salvar_csv(desempenho, pasta / "auditoria_desempenho.csv")
    salvar_csv(territorial, pasta / "comparacao_territorial_validada.csv")
    salvar_csv(sensibilidade, pasta / "sensibilidade_benchmarks.csv")
    salvar_csv(membros, pasta / "sensibilidade_benchmark_membros.csv")
    salvar_csv(dificuldade_ufpa, pasta / "diagnostico_dificuldade.csv")
    salvar_csv(dimensoes, pasta / "diagnostico_dimensoes_processo.csv")
    salvar_csv(scores_dimensoes, pasta / "scores_dimensoes_exploratorios.csv")
    salvar_csv(socio_auditoria, pasta / "auditoria_indicadores_socioeconomicos.csv")
    salvar_csv(socio_sintese, pasta / "tabela_socioeconomica_ufpa.csv")
    salvar_csv(associacoes, pasta / "associacoes_ecologicas.csv")

    figdir = ROOT / "figuras" / "fisica"
    figuras = [
        figdir / "validada_02_taxa_presenca.png",
        figdir / "validada_03_nt_ger_ofertas.png",
        figdir / "validada_07_conceito_dificuldade.png",
        figdir / "validada_13_sintese_socioeconomica.png",
    ]
    presenca_validada(presenca, figuras[0])
    desempenho_validado(base, figuras[1])
    dificuldade_validada(base, figuras[2])
    socioeconomico_validado(base, figuras[3])

    gerar_relatorio(
        base, presenca, territorial, sensibilidade, dificuldade_ufpa,
        associacoes, dimensoes, socio_sintese,
        ROOT / "relatorios" / "sprint_05_validacao_fisica.md",
    )
    validar_resultados(base, presenca, desempenho, sensibilidade, figuras)
    logger.info(
        "Sprint 5 concluída: %d cursos auditados, %d benchmarks e %d figuras validadas",
        len(base), len(sensibilidade), len(figuras),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
