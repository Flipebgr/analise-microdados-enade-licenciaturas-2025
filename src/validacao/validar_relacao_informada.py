from __future__ import annotations
import pandas as pd
from src.utilitarios.normalizacao import normalizar_texto


def comparar_relacao_informada(mestre: pd.DataFrame, ofertas: list[dict], areas: dict[int, str]) -> pd.DataFrame:
    esperado = pd.DataFrame(ofertas).rename(columns={
        "co_grupo": "CO_GRUPO", "municipio": "MUNICIPIO_INFORMADO",
        "modalidade": "MODALIDADE_INFORMADA", "conceito": "CONCEITO_INFORMADO"
    })
    esperado["MUNICIPIO_CHAVE"] = esperado["MUNICIPIO_INFORMADO"].map(normalizar_texto)
    esperado["MODALIDADE_CHAVE"] = esperado["MODALIDADE_INFORMADA"].map(normalizar_texto)

    encontrado = mestre.copy()
    encontrado["MUNICIPIO_CHAVE"] = encontrado["MUNICIPIO"].map(normalizar_texto)
    encontrado["MODALIDADE_CHAVE"] = encontrado["MODALIDADE"].map(normalizar_texto)
    cols = ["CO_GRUPO", "MUNICIPIO_CHAVE", "MODALIDADE_CHAVE", "CO_CURSO", "MUNICIPIO", "MODALIDADE", "CONCEITO_ENADE", "SITUACAO_CONCEITO"]
    resultado = esperado.merge(encontrado[cols], on=["CO_GRUPO", "MUNICIPIO_CHAVE", "MODALIDADE_CHAVE"], how="left", validate="one_to_one")
    resultado["AREA"] = resultado["CO_GRUPO"].map(areas)
    resultado["STATUS_VALIDACAO"] = "Validado"
    ausente = resultado["CO_CURSO"].isna()
    resultado.loc[ausente, "STATUS_VALIDACAO"] = "Não localizado nas fontes"

    def conceito_norm(v):
        t = normalizar_texto(v)
        return "SEM CONCEITO" if t in {"SEM CONCEITO", "SC", ""} else t.replace(".0", "")

    resultado["CONCEITO_ENCONTRADO_NORMALIZADO"] = resultado["CONCEITO_ENADE"].map(conceito_norm)
    resultado["CONCEITO_INFORMADO_NORMALIZADO"] = resultado["CONCEITO_INFORMADO"].map(conceito_norm)
    divergente = (~ausente) & (resultado["CONCEITO_ENCONTRADO_NORMALIZADO"] != resultado["CONCEITO_INFORMADO_NORMALIZADO"])
    resultado.loc[divergente, "STATUS_VALIDACAO"] = "Conceito divergente"
    resultado["CORRECAO_RECOMENDADA"] = "Nenhuma"
    resultado.loc[ausente, "CORRECAO_RECOMENDADA"] = "Manter no cadastro como oferta informada externamente, sem CO_CURSO validado e fora dos grupos comparativos."
    resultado.loc[divergente, "CORRECAO_RECOMENDADA"] = "Adotar o valor encontrado na planilha oficial e registrar a divergência."
    return resultado.sort_values(["CO_GRUPO", "MUNICIPIO_INFORMADO", "MODALIDADE_INFORMADA"])
