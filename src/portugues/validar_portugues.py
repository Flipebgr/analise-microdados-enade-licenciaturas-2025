from __future__ import annotations

import pandas as pd

from src.core.validacao import validar_base_area
from src.portugues import CO_CURSO_BELEM_EAD, PORTUGUES
from src.validacao.validar_grupos import validar_grupos

CURSOS_UFPA_ESPERADOS = {
    27645: ("Belém", "Presencial", 4),
    114846: ("Cametá", "Presencial", 3),
    114850: ("Abaetetuba", "Presencial", 3),
    114857: ("Castanhal", "Presencial", 3),
    114874: ("Bragança", "Presencial", 3),
    114876: ("Altamira", "Presencial", 2),
    115013: ("Breves", "Presencial", 3),
    115161: ("Belém", "EaD", 1),
}


def validar_base_portugues(base: pd.DataFrame) -> None:
    validar_base_area(base, PORTUGUES).exigir_valido()
    validar_grupos(base)
    ufpa = base[base["CO_IES"].eq(PORTUGUES.co_ies_focal)].copy()

    if len(ufpa) != len(CURSOS_UFPA_ESPERADOS):
        raise ValueError(
            f"Esperadas {len(CURSOS_UFPA_ESPERADOS)} ofertas localizadas da UFPA; "
            f"encontradas {len(ufpa)}."
        )

    encontrados: dict[int, tuple[str, str, int]] = {}
    for _, linha in ufpa.iterrows():
        codigo = int(pd.to_numeric(linha["CO_CURSO"], errors="raise"))
        conceito = int(pd.to_numeric(linha["CONCEITO_ENADE_NUM"], errors="raise"))
        encontrados[codigo] = (
            str(linha["MUNICIPIO"]),
            str(linha["MODALIDADE"]),
            conceito,
        )
    if encontrados != CURSOS_UFPA_ESPERADOS:
        raise ValueError(
            f"Relação UFPA divergente: esperado={CURSOS_UFPA_ESPERADOS}, "
            f"encontrado={encontrados}"
        )

    conceito1 = ufpa[ufpa["CONCEITO_ENADE_NUM"].eq(1)]
    if len(conceito1) != 1:
        raise ValueError("Esperada exatamente uma oferta UFPA com Conceito Enade 1.")
    if int(conceito1.iloc[0]["CO_CURSO"]) != CO_CURSO_BELEM_EAD:
        raise ValueError("A oferta UFPA Conceito 1 deve ser Belém EaD, CO_CURSO 115161.")
    if conceito1.iloc[0]["GRUPO_CODIGO"] != "A":
        raise ValueError("Belém EaD Conceito 1 deve pertencer ao Grupo A.")

    superiores = ufpa[ufpa["CONCEITO_ENADE_NUM"].gt(1)]
    if len(superiores) != 7 or not superiores["GRUPO_CODIGO"].eq("B").all():
        raise ValueError("As sete demais ofertas UFPA devem pertencer ao Grupo B.")

    municipio = ufpa["MUNICIPIO"].astype("string").str.strip().str.casefold()
    if municipio.eq("soure").any():
        raise ValueError(
            "Soure não deve ser fabricada na base: não foi localizada nas fontes oficiais de 2025."
        )


def validar_auditoria_relacao(auditoria: pd.DataFrame) -> None:
    if len(auditoria) != 9:
        raise ValueError("A auditoria deve preservar as nove ofertas inicialmente informadas.")
    soure = auditoria[
        auditoria["MUNICIPIO_INFORMADO"].astype("string").str.casefold().eq("soure")
    ]
    if len(soure) != 1:
        raise ValueError("A oferta informada de Soure deve aparecer uma vez na auditoria.")
    linha = soure.iloc[0]
    if linha["STATUS_VALIDACAO"] != "Não localizado nas fontes":
        raise ValueError("Soure deve ser marcada como não localizada nas fontes.")
    if pd.notna(linha["CO_CURSO"]):
        raise ValueError("Não deve ser inventado CO_CURSO para a oferta de Soure.")
