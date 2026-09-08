from __future__ import annotations

# ruff: noqa: E402

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.configuracao.caminhos import ROOT, carregar_config, caminho_relativo
from src.educacao_fisica import EDUCACAO_FISICA
from src.educacao_fisica.gerar_figuras import gerar_todas
from src.educacao_fisica.validacao_analitica import (
    agregar_dimensoes_por_curso,
    associacoes_ecologicas,
    carregar_processo_individual,
    catalogo_itens_processo,
    diagnosticar_dimensoes,
    resumo_qualidade,
    sensibilidade_benchmarks,
)
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger


def salvar_csv(df: pd.DataFrame, path: Path, encoding: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding=encoding)


def _percentual(valor: object) -> str:
    numero = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]
    return "—" if pd.isna(numero) else f"{100 * numero:.1f}%"


def _numero(valor: object, casas: int = 2) -> str:
    numero = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]
    return "—" if pd.isna(numero) else f"{numero:.{casas}f}"


def gerar_relatorio_markdown(
    base: pd.DataFrame,
    dimensoes: pd.DataFrame,
    benchmark: pd.DataFrame,
    associacoes: pd.DataFrame,
    figuras: list[Path],
    caminho: Path,
) -> None:
    ufpa = base[
        base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal)
    ].sort_values("ROTULO_OFERTA")

    linhas = [
        "# Educação Física — validação analítica e narrativa gráfica",
        "",
        "## Escopo",
        "",
        "A área possui 406 cursos nacionais e duas ofertas UFPA, ambas com Conceito Enade 4. "
        "Não existe Grupo A (UFPA Conceito 1); a análise interna contrasta Belém e Castanhal "
        "sem pressupor desempenho problemático.",
        "",
        "## Ofertas UFPA",
        "",
        "| Oferta | Participantes | Participação oficial | NT_GER média | Percentil Brasil | Conceito |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for _, row in ufpa.iterrows():
        linhas.append(
            f"| {row['ROTULO_OFERTA']} | {int(row['PARTICIPANTES_NUM'])} | "
            f"{_percentual(row['TAXA_PARTICIPACAO_OFICIAL'])} | "
            f"{_numero(row['nt_ger_mean'])} | "
            f"{_numero(row['nt_ger_percentil_brasil'], 1)} | "
            f"{int(row['CONCEITO_ENADE_NUM'])} |"
        )

    linhas.extend(
        [
            "",
            "## Processo formativo",
            "",
            "Os itens QE_I20–QE_I66 utilizam escala 1–6 para discordância/concordância. "
            "As categorias 7 (não sei responder) e 8 (não se aplica) são tratadas como "
            "ausência analítica. Todos os itens incluídos são formulados em direção positiva; "
            "não há itens invertidos. QE_I31, QE_I32 e QE_I43 são específicos de EaD e "
            "foram mantidos fora das dimensões comuns usadas para comparar as duas ofertas "
            "presenciais da UFPA.",
            "",
            "Não há item explicitamente dedicado a estágio entre QE_I20–QE_I66; portanto "
            "nenhum índice de estágio foi criado.",
            "",
            "### Consistência interna das dimensões",
            "",
            "| Recorte | Dimensão | Itens | N casos completos | Alfa de Cronbach |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for _, row in dimensoes.iterrows():
        linhas.append(
            f"| {row['RECORTE']} | {row['ROTULO_DIMENSAO']} | {row['N_ITENS']} | "
            f"{row['N_CASOS_COMPLETOS']} | {_numero(row['ALPHA_CRONBACH'], 3)} |"
        )

    linhas.extend(
        [
            "",
            "Os escores dimensionais permanecem exploratórios: alfa elevado não demonstra, "
            "sozinho, unidimensionalidade. Eles são usados como síntese descritiva, com "
            "composição documentada.",
            "",
            "## Benchmark comparável — sensibilidade",
            "",
            "O benchmark mantém modalidade, categoria administrativa e organização acadêmica "
            "e varia apenas a janela de porte. Isso permite verificar se a posição das ofertas "
            "é sensível ao critério de tamanho.",
            "",
            "| Oferta | Critério | N | NT_GER alvo | Mediana benchmark | Diferença |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    b = benchmark[benchmark["INDICADOR"].eq("nt_ger_mean")].copy()
    for _, row in b.iterrows():
        linhas.append(
            f"| {row['ROTULO_ALVO']} | {row['CRITERIO']} | {row['N_COMPARAVEIS']} | "
            f"{_numero(row['VALOR_ALVO'])} | {_numero(row['MEDIANA_BENCHMARK'])} | "
            f"{_numero(row['DIF_MEDIANA'])} |"
        )

    linhas.extend(
        [
            "",
            "## Associações ecológicas",
            "",
            "As correlações abaixo são calculadas entre indicadores agregados por curso e "
            "não podem ser interpretadas como relações individuais ou causais.",
            "",
            "| X | Y | N cursos | Spearman rho | p |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for _, row in associacoes.iterrows():
        linhas.append(
            f"| {row['X']} | {row['Y']} | {row['N_CURSOS']} | "
            f"{_numero(row['SPEARMAN_RHO'], 3)} | {_numero(row['P_VALOR'], 4)} |"
        )

    linhas.extend(["", "## Narrativa gráfica", ""])
    descricoes = [
        (
            "01 — Painel das ofertas UFPA",
            "Descrição: compara a participação oficial das duas ofertas e informa N e Conceito. "
            "Interpretação: permite verificar diferença de adesão entre Belém e Castanhal. "
            "Hipótese: diferenças de participação podem refletir organização local e composição da turma. "
            "Limitação: participação não mede qualidade do curso. "
            "Relação com a pergunta: contextualiza o universo efetivamente observado.",
        ),
        (
            "02 — Posição relativa em NT_GER",
            "Descrição: posiciona as médias de Belém e Castanhal sobre a distribuição dos cursos nacionais. "
            "Interpretação: mostra posição relativa sem comparar áreas distintas. "
            "Hipótese: diferenças internas podem coexistir com bom posicionamento nacional. "
            "Limitação: média de curso não descreve heterogeneidade individual. "
            "Relação: responde ao componente de desempenho.",
        ),
        (
            "03 — Distribuições NT_GER, NT_OBJ e NT_DIS",
            "Descrição: boxplots individuais construídos somente com variáveis do mesmo arquivo de desempenho. "
            "Interpretação: permite comparar centro e dispersão entre os dois campi. "
            "Hipótese: médias próximas podem esconder distribuições diferentes. "
            "Limitação: não relacionar essas notas individualmente a questionários de outros arquivos. "
            "Relação: detalha o desempenho além da média.",
        ),
        (
            "04 — Perfil socioeconômico",
            "Descrição: percentuais válidos de indicadores selecionados por oferta. "
            "Interpretação: caracteriza composição discente sem atribuir causalidade. "
            "Hipótese: diferenças de condições materiais podem acompanhar diferenças de trajetória. "
            "Limitação: indicadores vêm de arquivos distintos do desempenho e só podem ser relacionados no nível do curso. "
            "Relação: cobre composição discente.",
        ),
        (
            "05 — Processo formativo",
            "Descrição: médias das dimensões exploratórias validadas teoricamente e por consistência interna. "
            "Interpretação: identifica áreas de percepção relativamente mais fortes ou frágeis. "
            "Hipótese: padrões podem diferir entre os campi apesar do mesmo Conceito Enade. "
            "Limitação: alfa não comprova unidimensionalidade. "
            "Relação: cobre avaliação do processo formativo.",
        ),
        (
            "06 — Benchmark comparável",
            "Descrição: mostra sensibilidade da mediana dos cursos comparáveis a três janelas de porte. "
            "Interpretação: diferença persistente entre critérios é mais robusta que diferença dependente de uma única janela. "
            "Hipótese: parte da posição observada pode estar associada à estrutura do conjunto comparável. "
            "Limitação: pareamento observacional não elimina diferenças não medidas. "
            "Relação: qualifica a comparação externa.",
        ),
        (
            "07 — Recomendação",
            "Descrição: médias oficiais de QE_I68 e QE_I69. "
            "Interpretação: distingue recomendação do curso e da IES. "
            "Hipótese: as duas avaliações podem divergir. "
            "Limitação: não denominar automaticamente essas medidas como satisfação. "
            "Relação: cobre a dimensão de recomendação.",
        ),
        (
            "08 — Síntese UFPA",
            "Descrição: reúne indicadores em escala percentual/percentil para contraste descritivo. "
            "Interpretação: evidencia perfis distintos sem criar escore global. "
            "Hipótese: as ofertas podem combinar vantagens em dimensões diferentes. "
            "Limitação: indicadores não formam índice composto. "
            "Relação: integra a pergunta central sem inferência causal.",
        ),
    ]
    for titulo, texto in descricoes:
        linhas.extend([f"### {titulo}", "", texto, ""])

    linhas.extend(["## Arquivos gráficos", ""])
    for fig in figuras:
        linhas.append(f"- `{fig.name}`")

    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    cfg = carregar_config()
    logger = configurar_logger(
        ROOT / "logs" / "educacao_fisica_validacao.log"
    )
    encoding_saida = cfg["saida"]["csv_encoding"]

    dados = ROOT / "dados_processados" / "educacao_fisica"
    base_path = dados / "base_analitica_cursos.csv"
    individual_path = dados / "desempenho_individual_mesmo_arquivo.csv"

    if not base_path.exists() or not individual_path.exists():
        logger.error(
            "Base da Entrega 01 ausente. Execute: "
            "python executar.py educacao-fisica base"
        )
        return 2

    base = pd.read_csv(base_path)
    individual_desempenho = pd.read_csv(individual_path)

    extraida = caminho_relativo(cfg["arquivos"]["pasta_extraida"])
    arq1 = encontrar_arquivo(extraida, "microdados2025_arq1.txt")
    arq4 = arq1.parent / "microdados2025_arq4.txt"

    ids = (
        pd.to_numeric(base["CO_CURSO"], errors="coerce")
        .dropna()
        .astype(int)
        .tolist()
    )
    ufpa_ids = set(
        pd.to_numeric(
            base.loc[
                base["CO_IES"].eq(EDUCACAO_FISICA.co_ies_focal),
                "CO_CURSO",
            ],
            errors="coerce",
        )
        .dropna()
        .astype(int)
        .tolist()
    )

    processo_individual = carregar_processo_individual(arq4, ids)
    catalogo_itens = catalogo_itens_processo()
    diagnostico = diagnosticar_dimensoes(processo_individual, ufpa_ids)
    dimensoes_curso = agregar_dimensoes_por_curso(processo_individual)

    base_validada = base.merge(
        dimensoes_curso,
        on="CO_CURSO",
        how="left",
        validate="one_to_one",
    )

    benchmark_resumo, benchmark_membros = sensibilidade_benchmarks(
        base_validada
    )
    associacoes = associacoes_ecologicas(base_validada)
    qualidade = resumo_qualidade(
        base_validada,
        catalogo_itens,
        diagnostico,
        benchmark_resumo,
    )

    if not qualidade["APROVADO"].all():
        logger.error(
            "Validação analítica reprovada:\n%s",
            qualidade.loc[~qualidade["APROVADO"]].to_string(index=False),
        )
        return 1

    produtos = {
        "base_analitica_validada.csv": base_validada,
        "catalogo_itens_processo_formativo.csv": catalogo_itens,
        "consistencia_dimensoes_processo.csv": diagnostico,
        "dimensoes_processo_por_curso.csv": dimensoes_curso,
        "benchmark_sensibilidade_resumo.csv": benchmark_resumo,
        "benchmark_sensibilidade_membros.csv": benchmark_membros,
        "associacoes_ecologicas.csv": associacoes,
        "validacao_analitica.csv": qualidade,
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, dados / nome, encoding_saida)

    pasta_figuras = ROOT / "figuras" / "educacao_fisica"
    figuras = gerar_todas(
        base_validada,
        individual_desempenho,
        benchmark_resumo,
        pasta_figuras,
    )

    gerar_relatorio_markdown(
        base_validada,
        diagnostico,
        benchmark_resumo,
        associacoes,
        figuras,
        ROOT / "relatorios" / "educacao_fisica" / "validacao_analitica.md",
    )

    print("\nValidação analítica — Educação Física")
    print(qualidade.to_string(index=False))
    print(f"\nFiguras geradas: {len(figuras)}")
    print(
        "Relatório intermediário: "
        "relatorios/educacao_fisica/validacao_analitica.md"
    )
    logger.info("Validação analítica concluída.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
