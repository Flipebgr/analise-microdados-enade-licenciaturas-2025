"""Fontes sintéticas completas: não dependem de dados locais oficiais."""
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from src.core.configuracao_area import BIOLOGIA_BACHARELADO_2017
from src.edicoes import ENADE_2017
from src.orquestracao.area import analisar_area


def fontes_sinteticas(pasta: Path, edicao=ENADE_2017, area=BIOLOGIA_BACHARELADO_2017):
    pasta.mkdir(parents=True, exist_ok=True)
    zip_path = pasta / "micro.zip"
    extraidos = pasta / "extraidos"
    extraidos.mkdir()
    with ZipFile(zip_path, "w") as zip_file:
        for schema in edicao.arquivos:
            linhas = []
            for curso, ies in (("00001", str(area.co_ies_focal)), ("00002", "9")):
                for resposta in ("1", "2", "4", "5", "6", "6", "4", "7", "8", ""):
                    r = {c: "" for c in schema.colunas_obrigatorias}
                    for c in schema.colunas_obrigatorias:
                        if c in edicao.desempenho.variaveis_numericas:
                            r[c] = "50"
                        if c in edicao.questionario.itens_processo_formativo:
                            r[c] = resposta
                        if c in edicao.questionario.itens_gerais:
                            r[c] = "B"
                    r.update(NU_ANO=str(edicao.ano), CO_CURSO=curso, CO_IES=ies,
                             CO_GRUPO=str(area.co_grupo), CO_MUNIC_CURSO="1501402",
                             CO_UF_CURSO="15", CO_REGIAO_CURSO="1", CO_MODALIDADE="1",
                             CO_CATEGAD="1", CO_ORGACAD="1", TP_PRES="555")
                    linhas.append(";".join(r[c] for c in schema.colunas_obrigatorias))
            conteudo = ";".join(schema.colunas_obrigatorias) + "\n" + "\n".join(linhas) + "\n"
            nome = edicao.nome_arquivo(schema.numero)
            zip_file.writestr(nome, conteudo)
            (extraidos / nome).write_text(conteudo, encoding="utf-8", newline="")
    conceitos = []
    for curso, ies, conceito in (("00001", str(area.co_ies_focal), "3"), ("00002", "9", "SC")):
        valores = dict(NU_ANO=str(edicao.ano), CO_CURSO=curso, CO_IES=ies,
                       CO_GRUPO=str(area.co_grupo), CO_MUNIC_CURSO="1501402",
                       INSCRITOS="23", PARTICIPANTES="13", CONCEITO_ENADE_ORIGINAL=conceito)
        conceitos.append({origem: valores.get(destino, "") for origem, destino in edicao.conceito.mapa_colunas})
    xlsx = pasta / "conceito.xlsx"
    pd.DataFrame(conceitos).to_excel(xlsx, sheet_name=edicao.conceito.aba, index=False)
    return zip_path, extraidos, xlsx


def resultado_sintetico(pasta, edicao=ENADE_2017, area=BIOLOGIA_BACHARELADO_2017):
    fonte, diretorio, conceito = fontes_sinteticas(pasta, edicao, area)
    return analisar_area(fonte, conceito, edicao, area), fonte, diretorio, conceito
