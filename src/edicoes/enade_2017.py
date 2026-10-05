from __future__ import annotations

from src.edicoes.base import (
    CapacidadesEdicao,
    ConfiguracaoLeitura,
    ContratoEdicao,
    RegraIndicadorQuestionario,
    SchemaArquivo,
    SchemaConceito,
    SchemaDesempenho,
    SchemaPresenca,
    SchemaQuestionario,
)


def _qe(numero: int) -> str:
    return f"QE_I{numero:02d}"


COLUNAS_ARQ1 = (
    "NU_ANO",
    "CO_CURSO",
    "CO_IES",
    "CO_CATEGAD",
    "CO_ORGACAD",
    "CO_GRUPO",
    "CO_MODALIDADE",
    "CO_MUNIC_CURSO",
    "CO_UF_CURSO",
    "CO_REGIAO_CURSO",
)
COLUNAS_ARQ2 = ("NU_ANO", "CO_CURSO", "ANO_FIM_EM", "ANO_IN_GRAD", "CO_TURNO_GRADUACAO")
COLUNAS_ARQ3 = (
    "NU_ANO",
    "CO_CURSO",
    "TP_PRES",
    "TP_PR_GER",
    "TP_PR_OB_FG",
    "TP_PR_DI_FG",
    "TP_PR_OB_CE",
    "TP_PR_DI_CE",
    "NT_GER",
    "NT_FG",
    "NT_OBJ_FG",
    "NT_DIS_FG",
    "NT_CE",
    "NT_OBJ_CE",
    "NT_DIS_CE",
    "DS_VT_GAB_OFG_FIN",
    "DS_VT_GAB_OCE_FIN",
    "DS_VT_ESC_OFG",
    "DS_VT_ACE_OFG",
    "DS_VT_ESC_OCE",
    "DS_VT_ACE_OCE",
)

ITENS_GERAIS = tuple(_qe(numero) for numero in range(1, 27))
ITENS_PROCESSO = tuple(_qe(numero) for numero in range(27, 69))
ITENS_LICENCIATURA = tuple(_qe(numero) for numero in range(69, 82))


def _schemas_arquivos() -> tuple[SchemaArquivo, ...]:
    schemas = [
        SchemaArquivo(1, COLUNAS_ARQ1),
        SchemaArquivo(2, COLUNAS_ARQ2),
        SchemaArquivo(3, COLUNAS_ARQ3),
        SchemaArquivo(4, ("NU_ANO", "CO_CURSO", *ITENS_PROCESSO)),
        SchemaArquivo(5, ("NU_ANO", "CO_CURSO", "TP_SEXO")),
        SchemaArquivo(6, ("NU_ANO", "CO_CURSO", "NU_IDADE")),
    ]
    schemas.extend(
        SchemaArquivo(numero + 6, ("NU_ANO", "CO_CURSO", _qe(numero)))
        for numero in range(1, 27)
    )
    schemas.extend(
        SchemaArquivo(numero - 36, ("NU_ANO", "CO_CURSO", _qe(numero)))
        for numero in range(69, 78)
    )
    schemas.append(SchemaArquivo(42, ("NU_ANO", "CO_CURSO", *tuple(_qe(i) for i in range(78, 82)))))
    return tuple(schemas)


REGRAS_SOCIOECONOMICAS = (
    RegraIndicadorQuestionario(
        "pai_superior_pct", "QE_I04", frozenset("EF"), frozenset("ABCDEF"), "Pai com graduação ou pós-graduação"
    ),
    RegraIndicadorQuestionario(
        "mae_superior_pct", "QE_I05", frozenset("EF"), frozenset("ABCDEF"), "Mãe com graduação ou pós-graduação"
    ),
    RegraIndicadorQuestionario(
        "renda_ate_3sm_pct", "QE_I08", frozenset("AB"), frozenset("ABCDEFG"), "Renda familiar de até três salários mínimos"
    ),
    RegraIndicadorQuestionario(
        "trabalha_pct", "QE_I10", frozenset("BCDE"), frozenset("ABCDE"), "Exerce trabalho, exceto estágio ou bolsa"
    ),
    RegraIndicadorQuestionario(
        "auxilio_permanencia_pct", "QE_I12", frozenset("BCDEF"), frozenset("ABCDEF"), "Recebeu auxílio de permanência"
    ),
    RegraIndicadorQuestionario(
        "bolsa_academica_pct", "QE_I13", frozenset("BCDEF"), frozenset("ABCDEF"), "Recebeu bolsa acadêmica"
    ),
    RegraIndicadorQuestionario(
        "acao_afirmativa_pct", "QE_I15", frozenset("BCDEF"), frozenset("ABCDEF"), "Ingresso por ação afirmativa ou inclusão social"
    ),
    RegraIndicadorQuestionario(
        "primeira_geracao_pct", "QE_I21", frozenset("B"), frozenset("AB"), "Ninguém da família concluiu curso superior"
    ),
    RegraIndicadorQuestionario(
        "estudo_4h_ou_mais_pct", "QE_I23", frozenset("CDE"), frozenset("ABCDE"), "Quatro horas semanais ou mais de estudo"
    ),
)

SCHEMA_CONCEITO_2017 = SchemaConceito(
    aba="Conceito Enade 2017",
    mapa_colunas=(
        ("Ano", "NU_ANO"),
        ("Código da Área", "CO_GRUPO"),
        ("Área de Avaliação", "AREA"),
        ("Código da IES", "CO_IES"),
        ("Nome da IES", "NO_IES"),
        ("Sigla da IES", "SG_IES"),
        ("Organização Acadêmica", "ORGANIZACAO_ACADEMICA"),
        ("Categoria Administrativa", "CATEGORIA_ADMINISTRATIVA"),
        ("Código do Curso", "CO_CURSO"),
        ("Modalidade de Ensino", "MODALIDADE"),
        ("Código do Município", "CO_MUNIC_CURSO"),
        ("Município do Curso", "MUNICIPIO"),
        ("Sigla da UF", "UF"),
        ("Nº de Concluintes Inscritos", "INSCRITOS"),
        ("Nº  de Concluintes Participantes", "PARTICIPANTES"),
        ("Nota Bruta - FG", "NOTA_BRUTA_FG"),
        ("Nota Padronizada - FG", "NOTA_PADRONIZADA_FG"),
        ("Nota Bruta - CE", "NOTA_BRUTA_CE"),
        ("Nota Padronizada - CE", "NOTA_PADRONIZADA_CE"),
        ("Conceito Enade (Contínuo)", "CONCEITO_ENADE_CONTINUO"),
        ("Conceito Enade (Faixa)", "CONCEITO_ENADE_ORIGINAL"),
        ("Observação", "OBSERVACAO_CONCEITO"),
    ),
    colunas_numericas=(
        "NU_ANO",
        "CO_GRUPO",
        "CO_IES",
        "CO_CURSO",
        "CO_MUNIC_CURSO",
        "INSCRITOS",
        "PARTICIPANTES",
        "NOTA_BRUTA_FG",
        "NOTA_PADRONIZADA_FG",
        "NOTA_BRUTA_CE",
        "NOTA_PADRONIZADA_CE",
        "CONCEITO_ENADE_CONTINUO",
    ),
)

ENADE_2017 = ContratoEdicao(
    ano=2017,
    nome="Enade 2017",
    prefixo_arquivos="microdados2017_arq",
    quantidade_arquivos=42,
    leitura=ConfiguracaoLeitura(
        separador=";",
        decimal=".",
        quotechar='"',
        encodings=("utf-8-sig", "utf-8", "cp1252", "latin1"),
    ),
    arquivos=_schemas_arquivos(),
    desempenho=SchemaDesempenho(
        geral="NT_GER",
        formacao_geral="NT_FG",
        formacao_geral_objetiva="NT_OBJ_FG",
        formacao_geral_discursiva="NT_DIS_FG",
        componente_especifico="NT_CE",
        componente_especifico_objetiva="NT_OBJ_CE",
        componente_especifico_discursiva="NT_DIS_CE",
        vetores_string=(
            "DS_VT_GAB_OFG_FIN",
            "DS_VT_GAB_OCE_FIN",
            "DS_VT_ESC_OFG",
            "DS_VT_ACE_OFG",
            "DS_VT_ESC_OCE",
            "DS_VT_ACE_OCE",
        ),
    ),
    presenca=SchemaPresenca(
        variaveis=(
            "TP_PRES",
            "TP_PR_GER",
            "TP_PR_OB_FG",
            "TP_PR_DI_FG",
            "TP_PR_OB_CE",
            "TP_PR_DI_CE",
        ),
        codigos_tp_pres=(
            (222, "ausente"),
            (333, "inscricao_indevida"),
            (334, "eliminado_participacao_indevida"),
            (444, "ausente_dupla_graduacao"),
            (555, "presente_resultado_valido"),
            (556, "presente_desconsiderado_aplicadora"),
            (888, "presente_desconsiderado_inep"),
        ),
    ),
    questionario=SchemaQuestionario(
        itens_gerais=ITENS_GERAIS,
        itens_processo_formativo=ITENS_PROCESSO,
        itens_licenciatura=ITENS_LICENCIATURA,
        itens_recomendacao=(),
        regras_indicadores=REGRAS_SOCIOECONOMICAS,
        codigos_validos_processo=frozenset(range(1, 7)),
        codigos_especiais_processo=((7, "nao_sabe_responder"), (8, "nao_se_aplica")),
    ),
    capacidades=CapacidadesEdicao(
        proficiencia=False,
        recomendacao=False,
        questionario_licenciatura=True,
    ),
    conceito=SCHEMA_CONCEITO_2017,
    modalidades=((0, "EaD"), (1, "Presencial")),
)
