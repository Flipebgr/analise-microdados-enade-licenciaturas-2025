from __future__ import annotations
from pathlib import Path
import pandas as pd


def gerar_relatorio(path: Path, manifesto: pd.DataFrame, inventario: pd.DataFrame, mestre: pd.DataFrame, divergencias: pd.DataFrame, erros: list[str]) -> None:
    total_microdados = int((manifesto["categoria"] == "microdados").sum())
    linhas = [
        "# Sprint 0 - Relatório de qualidade e validação inicial",
        "",
        "## Resumo executivo",
        f"- Arquivos temáticos encontrados: **{total_microdados}**.",
        f"- Ofertas selecionadas da UFPA na tabela-mestra: **{len(mestre)}**.",
        f"- Divergências de cruzamento: **{len(divergencias)}**.",
        f"- Erros estruturais: **{len(erros)}**.",
        "",
        "## Regra de relacionamento",
        "Os arquivos não possuem identificador público individual comum. A posição da linha não é uma chave. O fluxo permitido é: tratamento por arquivo, agregação por CO_CURSO, uma linha por curso e somente então junção das tabelas agregadas.",
        "",
        "## Volumetria",
        inventario[["arquivo", "numero_linhas", "numero_colunas", "tamanho_bytes", "encoding_detectado"]].to_markdown(index=False),
        "",
        "## Tabela-mestra da UFPA",
        mestre[[c for c in ["CO_GRUPO", "AREA", "CO_CURSO", "MUNICIPIO", "MODALIDADE", "PARTICIPANTES", "PCT_PADRAO_PROFICIENCIA", "CONCEITO_ENADE", "SITUACAO_CONCEITO", "SITUACAO_CRUZAMENTO"] if c in mestre]].to_markdown(index=False),
        "",
        "## Divergências",
        divergencias.to_markdown(index=False) if not divergencias.empty else "Nenhuma divergência de existência entre as duas fontes.",
        "",
        "## Erros estruturais",
        "\n".join(f"- {e}" for e in erros) if erros else "Nenhum erro estrutural detectado.",
        "",
        "## Limitações obrigatórias",
        "- Não realizar junções individuais entre os 28 arquivos.",
        "- Não tratar curso sem conceito como Conceito 1.",
        "- Não interpretar associações agregadas como relações individuais.",
        "- Não comparar notas brutas entre áreas distintas sem padronização.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(linhas), encoding="utf-8")
