from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.agregacao.agregar_demografia import agregar_demografia
from src.agregacao.agregar_desempenho import agregar_desempenho
from src.agregacao.agregar_processo_formativo import agregar_processo_formativo
from src.agregacao.agregar_recomendacao import agregar_recomendacao
from src.agregacao.agregar_socioeconomico import agregar_socioeconomico
from src.agregacao.agregar_trajetoria import agregar_trajetoria
from src.core.juncoes import juntar_por_curso
from src.validacao.validar_agregacoes import validar_tabela_agregada


def juntar_um_para_um(
    base: pd.DataFrame,
    partes: list[tuple[str, pd.DataFrame]],
) -> pd.DataFrame:
    resultado = base.copy(deep=True)
    for nome, parte in partes:
        validar_tabela_agregada(parte, nome)
        resultado = juntar_por_curso(resultado, parte)
    return resultado


def agregar_temas_biologia(pasta_dados: Path, cursos: list[int]) -> dict[str, pd.DataFrame]:
    desempenho, desempenho_individual = agregar_desempenho(
        pasta_dados / "microdados2025_arq3.txt", cursos
    )
    demografia, distribuicao_sexo = agregar_demografia(
        pasta_dados / "microdados2025_arq5.txt",
        pasta_dados / "microdados2025_arq6.txt",
        cursos,
    )
    trajetoria, distribuicao_turno = agregar_trajetoria(
        pasta_dados / "microdados2025_arq2.txt", cursos
    )
    socio, distribuicao_socio, regras_socio = agregar_socioeconomico(
        pasta_dados, cursos
    )
    processo, itens_processo, diagnostico_processo = agregar_processo_formativo(
        pasta_dados / "microdados2025_arq4.txt", cursos
    )
    recomendacao, distribuicao_recomendacao = agregar_recomendacao(
        pasta_dados / "microdados2025_arq26.txt",
        pasta_dados / "microdados2025_arq27.txt",
        pasta_dados / "microdados2025_arq28.txt",
        cursos,
    )
    return {
        "desempenho": desempenho,
        "desempenho_individual": desempenho_individual,
        "demografia": demografia,
        "distribuicao_sexo": distribuicao_sexo,
        "trajetoria": trajetoria,
        "distribuicao_turno": distribuicao_turno,
        "socioeconomico": socio,
        "distribuicao_socioeconomica": distribuicao_socio,
        "regras_socioeconomicos": regras_socio,
        "processo_formativo": processo,
        "itens_processo_formativo": itens_processo,
        "diagnostico_processo": diagnostico_processo,
        "recomendacao": recomendacao,
        "distribuicao_recomendacao": distribuicao_recomendacao,
    }
