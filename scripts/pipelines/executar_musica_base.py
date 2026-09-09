from __future__ import annotations

# ruff: noqa: E402

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analise.estatisticas_descritivas import (
    adicionar_posicoes,
    resumo_por_grupo,
)
from src.configuracao.caminhos import (
    ROOT,
    caminho_relativo,
    carregar_config,
    garantir_pastas,
)
from src.musica import MUSICA
from src.musica.agregar_musica import agregar_temas_musica
from src.musica.analise_musica import (
    construir_benchmark_comparavel,
    construir_comparacao_conceitos,
    construir_comparacao_recortes,
    juntar_temas,
)
from src.musica.preparar_catalogo import (
    preparar_catalogo_musica,
    tabela_mestra_ufpa,
)
from src.musica.validar_musica import validar_base_musica
from src.utilitarios.leitura import encontrar_arquivo
from src.utilitarios.logs import configurar_logger


def salvar_csv(
    tabela: pd.DataFrame,
    caminho: Path,
    encoding: str,
) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(caminho, index=False, encoding=encoding)


def main() -> int:
    garantir_pastas()
    cfg = carregar_config()
    logger = configurar_logger(ROOT / "logs" / "musica_base.log")

    extraida = caminho_relativo(cfg["arquivos"]["pasta_extraida"])
    conceito_path = caminho_relativo(cfg["arquivos"]["conceito_enade"])
    encoding_saida = cfg["saida"]["csv_encoding"]

    if not conceito_path.exists():
        logger.error("Planilha de conceito ausente: %s", conceito_path)
        return 2

    try:
        arq1 = encontrar_arquivo(extraida, "microdados2025_arq1.txt")
    except FileNotFoundError:
        logger.error(
            "Microdados extraídos não encontrados. "
            "Execute primeiro: python executar.py fontes"
        )
        return 2

    pasta_dados = arq1.parent

    logger.info("Preparando catálogo nacional de %s", MUSICA.nome)
    cursos, auditoria = preparar_catalogo_musica(extraida, conceito_path)

    ids_cursos = (
        pd.to_numeric(cursos["CO_CURSO"], errors="coerce")
        .dropna()
        .astype(int)
        .tolist()
    )

    logger.info("Agregando desempenho, perfil, trajetória e questionários")
    temas = agregar_temas_musica(pasta_dados, ids_cursos)

    base = juntar_temas(cursos, temas)
    base = adicionar_posicoes(base)
    validar_base_musica(base)

    comparacao_recortes = construir_comparacao_recortes(base)
    comparacao_conceitos = construir_comparacao_conceitos(base)
    benchmark_cursos, benchmark_resumo = construir_benchmark_comparavel(base)

    indicadores_benchmark = [
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
    benchmarks_amplos = resumo_por_grupo(base, indicadores_benchmark)

    out_dir = ROOT / "dados_processados" / "musica"
    produtos = {
        "cursos_musica.csv": cursos,
        "tabela_mestra_ufpa.csv": tabela_mestra_ufpa(cursos),
        "auditoria_fontes_ufpa.csv": auditoria,
        "agregado_desempenho.csv": temas["desempenho"],
        "desempenho_individual_mesmo_arquivo.csv": temas[
            "desempenho_individual"
        ],
        "agregado_demografia.csv": temas["demografia"],
        "agregado_trajetoria.csv": temas["trajetoria"],
        "agregado_socioeconomico.csv": temas["socioeconomico"],
        "agregado_processo_formativo.csv": temas["processo_formativo"],
        "agregado_recomendacao.csv": temas["recomendacao"],
        "base_analitica_cursos.csv": base,
        "benchmarks_amplos.csv": benchmarks_amplos,
        "benchmark_comparavel_cursos.csv": benchmark_cursos,
        "benchmark_comparavel_resumo.csv": benchmark_resumo,
        "comparacao_recortes.csv": comparacao_recortes,
        "comparacao_conceitos_nacionais.csv": comparacao_conceitos,
        "distribuicao_sexo.csv": temas["distribuicao_sexo"],
        "distribuicao_turno.csv": temas["distribuicao_turno"],
        "distribuicao_socioeconomica.csv": temas[
            "distribuicao_socioeconomica"
        ],
        "regras_indicadores_socioeconomicos.csv": temas[
            "regras_socioeconomicos"
        ],
        "itens_processo_formativo.csv": temas["itens_processo_formativo"],
        "diagnostico_consistencia_processo.csv": temas[
            "diagnostico_processo"
        ],
        "distribuicao_recomendacao.csv": temas[
            "distribuicao_recomendacao"
        ],
    }

    for nome, tabela in produtos.items():
        salvar_csv(tabela, out_dir / nome, encoding_saida)

    ufpa = base[base["CO_IES"].eq(MUSICA.co_ies_focal)][
        [
            "CO_CURSO",
            "ROTULO_OFERTA",
            "CONCEITO_ENADE_NUM",
            "INSCRITOS_NUM",
            "PARTICIPANTES_NUM",
            "PCT_PADRAO_PROFICIENCIA_NUM",
            "nt_ger_mean",
            "nt_obj_mean",
            "nt_dis_mean",
            "nt_ger_percentil_brasil",
            "nt_ger_percentil_norte",
            "nt_ger_percentil_para",
        ]
    ].copy()

    print("\nMúsica — UFPA")
    print(ufpa.to_string(index=False))
    print(
        "\nBase concluída: "
        f"{len(base)} cursos nacionais; {len(ufpa)} oferta UFPA."
    )

    logger.info(
        "Base concluída: %s cursos nacionais; %s oferta UFPA",
        len(base),
        len(ufpa),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
