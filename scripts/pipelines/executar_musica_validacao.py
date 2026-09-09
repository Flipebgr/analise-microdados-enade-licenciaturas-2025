from __future__ import annotations

# ruff: noqa: E402

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.configuracao.caminhos import (
    ROOT,
    caminho_relativo,
    carregar_config,
)
from src.musica import MUSICA
from src.musica.gerar_figuras import gerar_todas
from src.musica.validacao_analitica import (
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


def salvar_csv(
    tabela: pd.DataFrame,
    caminho: Path,
    encoding: str,
) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(caminho, index=False, encoding=encoding)


def _numero(valor: object, casas: int = 2) -> str:
    num = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]
    if pd.isna(num):
        return "NA"
    return f"{num:.{casas}f}".replace(".", ",")


def gerar_relatorio_markdown(
    base: pd.DataFrame,
    dimensoes: pd.DataFrame,
    benchmark: pd.DataFrame,
    associacoes: pd.DataFrame,
    diagnostico_assoc: pd.DataFrame,
    figuras: list[Path],
    caminho: Path,
) -> None:
    ufpa = base[base["CO_IES"].eq(MUSICA.co_ies_focal)].iloc[0]

    linhas = [
        "# Validação analítica — Música — Enade 2025",
        "",
        "## Escopo",
        "",
        "A análise cobre 107 cursos de Música. A UFPA possui uma única oferta "
        "localizada nas fontes Enade 2025: Belém, presencial, Conceito Enade 1.",
        "",
        "Os grupos B (outras ofertas UFPA com conceito superior) e C "
        "(outras IES do Pará) são estruturalmente vazios. Os contrastes externos "
        "principais são o restante da Região Norte e o restante do Brasil.",
        "",
        "## Oferta UFPA",
        "",
        "| CO_CURSO | Oferta | Inscritos | Participantes | Participação | "
        "Proficiência | Conceito | NT_GER |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
        (
            f"| {int(ufpa['CO_CURSO'])} | {ufpa['ROTULO_OFERTA']} | "
            f"{int(ufpa['INSCRITOS_NUM'])} | "
            f"{int(ufpa['PARTICIPANTES_NUM'])} | "
            f"{_numero(100 * ufpa['TAXA_PARTICIPACAO_OFICIAL'])}% | "
            f"{_numero(ufpa['PCT_PADRAO_PROFICIENCIA_NUM'])}% | "
            f"{int(ufpa['CONCEITO_ENADE_NUM'])} | "
            f"{_numero(ufpa['nt_ger_mean'])} |"
        ),
        "",
        "## Processo formativo",
        "",
        "QE_I20–QE_I66 usam escala analítica 1–6. Respostas 7 (Não sei) e "
        "8 (Não se aplica) são tratadas como ausentes analíticas. Os itens "
        "QE_I31, QE_I32 e QE_I43 são específicos de EaD e ficam fora das "
        "dimensões comuns para a oferta presencial da UFPA.",
        "",
        "| Recorte | Dimensão | Itens | N completos | Alfa de Cronbach |",
        "|---|---|---:|---:|---:|",
    ]

    for _, row in dimensoes.iterrows():
        linhas.append(
            f"| {row['RECORTE']} | {row['ROTULO_DIMENSAO']} | "
            f"{row['N_ITENS']} | {row['N_CASOS_COMPLETOS']} | "
            f"{_numero(row['ALPHA_CRONBACH'], 3)} |"
        )

    linhas.extend(
        [
            "",
            "Alfa de Cronbach avalia consistência interna, mas não comprova "
            "unidimensionalidade. Os escores são exploratórios e descritivos.",
            "",
            "## Benchmark comparável — sensibilidade",
            "",
            "O benchmark mantém modalidade, categoria administrativa e organização "
            "acadêmica e varia apenas a janela de porte.",
            "",
            "| Critério | N | NT_GER UFPA | Mediana benchmark | Diferença |",
            "|---|---:|---:|---:|---:|",
        ]
    )

    b = benchmark[benchmark["INDICADOR"].eq("nt_ger_mean")].copy()
    for _, row in b.iterrows():
        linhas.append(
            f"| {row['CRITERIO']} | {row['N_COMPARAVEIS']} | "
            f"{_numero(row['VALOR_ALVO'])} | "
            f"{_numero(row['MEDIANA_BENCHMARK'])} | "
            f"{_numero(row['DIF_MEDIANA'])} |"
        )

    linhas.extend(
        [
            "",
            "## Associações ecológicas",
            "",
            "As correlações são calculadas entre indicadores agregados por curso. "
            "Não representam relações individuais e não permitem inferência causal.",
            "",
            "| X | Y | N cursos | Spearman rho | p |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for _, row in associacoes.iterrows():
        linhas.append(
            f"| {row['X']} | {row['Y']} | {row['N_CURSOS']} | "
            f"{_numero(row['SPEARMAN_RHO'], 3)} | "
            f"{_numero(row['P_VALOR'], 4)} |"
        )

    linhas.extend(
        [
            "",
            "O arquivo `associacoes_ecologicas_diagnostico.csv` registra "
            "dispersão e quantidade de outliers pelo critério de Tukey para "
            "cada par analisado.",
            "",
            "## Narrativa gráfica",
            "",
        ]
    )

    descricoes = [
        (
            "01 — Painel da oferta UFPA",
            "Descrição: apresenta participação oficial e percentual no padrão de "
            "proficiência da oferta de Belém. Interpretação: contextualiza adesão "
            "e proficiência sem inferir qualidade causal. Hipótese: a combinação "
            "entre participação e desempenho pode ajudar a interpretar a posição "
            "da oferta. Limitação: ambos são indicadores agregados. Relação: "
            "define o universo observado da UFPA.",
        ),
        (
            "02 — Posição relativa em NT_GER",
            "Descrição: posiciona a média da UFPA na distribuição nacional dos "
            "cursos de Música. Interpretação: mostra posição relativa dentro da "
            "mesma área. Hipótese: o Conceito 1 pode corresponder a uma posição "
            "inferior também na nota contínua. Limitação: média do curso não "
            "descreve toda a distribuição individual. Relação: desempenho.",
        ),
        (
            "03 — Distribuições NT_GER, NT_OBJ e NT_DIS",
            "Descrição: compara os estudantes da UFPA, do Norte sem Pará e do "
            "Brasil sem Norte usando apenas variáveis do mesmo arquivo de "
            "desempenho. Interpretação: permite observar centro e dispersão. "
            "Hipótese: o contraste pode ser mais forte em algum componente da "
            "nota. Limitação: não relacionar individualmente essas notas a "
            "questionários de outros arquivos. Relação: desempenho.",
        ),
        (
            "04 — Perfil socioeconômico",
            "Descrição: compara a oferta UFPA com medianas de cursos nos recortes "
            "externos. Interpretação: caracteriza composição discente. Hipótese: "
            "diferenças de condições materiais podem acompanhar diferenças "
            "acadêmicas. Limitação: associação com nota apenas no nível ecológico. "
            "Relação: composição discente.",
        ),
        (
            "05 — Processo formativo",
            "Descrição: contrasta dimensões exploratórias da UFPA com medianas "
            "regionais/nacionais. Interpretação: identifica dimensões relativamente "
            "mais ou menos favoráveis. Hipótese: fragilidades percebidas podem "
            "coexistir com o baixo desempenho. Limitação: alfa não comprova "
            "unidimensionalidade. Relação: avaliação do processo formativo.",
        ),
        (
            "06 — Benchmark comparável",
            "Descrição: mostra a sensibilidade da mediana de NT_GER a três janelas "
            "de porte. Interpretação: diferenças persistentes são mais robustas ao "
            "critério. Hipótese: parte do contraste amplo pode refletir composição "
            "institucional. Limitação: pareamento observacional não elimina "
            "diferenças não medidas. Relação: benchmark comparável.",
        ),
        (
            "07 — Recomendação",
            "Descrição: compara QE_I68 e QE_I69 com seus rótulos oficiais. "
            "Interpretação: recomendação do curso e da IES podem divergir. "
            "Hipótese: avaliação institucional e avaliação do curso não são "
            "intercambiáveis. Limitação: não chamar automaticamente de satisfação. "
            "Relação: recomendação.",
        ),
        (
            "08 — Associação ecológica",
            "Descrição: mostra o par com maior |rho| entre os pares pré-definidos. "
            "Interpretação: auxilia a inspeção de dispersão e outliers. Hipótese: "
            "associações de curso podem refletir composição institucional. "
            "Limitação: não é associação individual nem causal. Relação: "
            "associações ecológicas.",
        ),
        (
            "09 — Síntese UFPA",
            "Descrição: reúne indicadores em escala percentual/percentil sem "
            "compor índice único. Interpretação: evidencia dimensões distintas da "
            "oferta. Hipótese: fragilidades e fortalezas podem coexistir. "
            "Limitação: os indicadores não são aditivos. Relação: síntese da "
            "pergunta central.",
        ),
    ]

    for titulo, texto in descricoes:
        linhas.extend([f"### {titulo}", "", texto, ""])

    linhas.extend(["## Arquivos gráficos", ""])
    for fig in figuras:
        linhas.append(f"- `{fig.name}`")

    linhas.extend(
        [
            "",
            "## Diagnóstico de associações",
            "",
            f"Pares avaliados: {len(diagnostico_assoc)}.",
        ]
    )

    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main() -> int:
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "musica_validacao.log")
    encoding_saida = cfg["saida"]["csv_encoding"]

    dados = ROOT / "dados_processados" / "musica"
    base_path = dados / "base_analitica_cursos.csv"
    individual_path = dados / "desempenho_individual_mesmo_arquivo.csv"

    if not base_path.exists() or not individual_path.exists():
        logger.error(
            "Base da Entrega 01 ausente. Execute: "
            "python executar.py musica base"
        )
        return 2

    base = pd.read_csv(base_path, low_memory=False)
    individual_desempenho = pd.read_csv(
        individual_path,
        low_memory=False,
    )

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
                base["CO_IES"].eq(MUSICA.co_ies_focal),
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
    associacoes, diagnostico_assoc = associacoes_ecologicas(base_validada)
    qualidade = resumo_qualidade(
        base_validada,
        catalogo_itens,
        diagnostico,
        benchmark_resumo,
    )

    if not qualidade["APROVADO"].all():
        logger.error(
            "Validação analítica reprovada:\n%s",
            qualidade.loc[
                ~qualidade["APROVADO"]
            ].to_string(index=False),
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
        "associacoes_ecologicas_diagnostico.csv": diagnostico_assoc,
        "validacao_analitica.csv": qualidade,
    }
    for nome, tabela in produtos.items():
        salvar_csv(tabela, dados / nome, encoding_saida)

    pasta_figuras = ROOT / "figuras" / "musica"
    figuras = gerar_todas(
        base_validada,
        individual_desempenho,
        benchmark_resumo,
        associacoes,
        pasta_figuras,
    )

    relatorio = (
        ROOT
        / "relatorios"
        / "musica"
        / "validacao_analitica.md"
    )
    gerar_relatorio_markdown(
        base_validada,
        diagnostico,
        benchmark_resumo,
        associacoes,
        diagnostico_assoc,
        figuras,
        relatorio,
    )

    print("\nValidação analítica — Música")
    print(qualidade.to_string(index=False))
    print(f"\nFiguras geradas: {len(figuras)}")
    print(
        "Relatório intermediário: "
        "relatorios/musica/validacao_analitica.md"
    )
    logger.info("Validação analítica concluída.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
