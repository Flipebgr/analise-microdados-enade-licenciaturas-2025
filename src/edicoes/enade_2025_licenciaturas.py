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
    "IN_REAPLICACAO",
    "DS_VT_GAB_OBJ",
    "DS_VT_ESC_OBJ",
    "DS_VT_ACE_OBJ",
    "TP_PRES",
    "TP_SIT_DISC",
    "PROFICIENCIA",
    "NT_OBJ",
    "NT_DIS",
    "NT_GER",
    "QT_ACERTOS",
)
ITENS_GERAIS = tuple(_qe(numero) for numero in range(1, 20))
ITENS_PROCESSO = tuple(_qe(numero) for numero in range(20, 67))
ITENS_RECOMENDACAO = ("QE_I68", "QE_I69", "QE_I70")


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
        for numero in range(1, 20)
    )
    schemas.extend(
        SchemaArquivo(numero, ("NU_ANO", "CO_CURSO", item))
        for numero, item in zip(range(26, 29), ITENS_RECOMENDACAO, strict=True)
    )
    return tuple(schemas)


REGRAS_SOCIOECONOMICAS = (
    RegraIndicadorQuestionario(
        "primeira_geracao_pct", "QE_I05", frozenset("B"), frozenset("AB"),
        "Primeira geração no ensino superior", respostas_excluidas=frozenset("C")
    ),
    RegraIndicadorQuestionario(
        "mae_superior_pct", "QE_I06", frozenset("EFG"), frozenset("ABCDEFG"),
        "Mãe com ensino superior", respostas_excluidas=frozenset("H")
    ),
    RegraIndicadorQuestionario(
        "pai_superior_pct", "QE_I07", frozenset("EFG"), frozenset("ABCDEFG"),
        "Pai com ensino superior", respostas_excluidas=frozenset("H")
    ),
    RegraIndicadorQuestionario(
        "renda_ate_3sm_pct", "QE_I09", frozenset("AB"), frozenset("ABCDEFG"), "Renda familiar de até três salários mínimos"
    ),
    RegraIndicadorQuestionario(
        "trabalha_pct", "QE_I10", frozenset("BCDE"), frozenset("ABCDE"), "Exerce trabalho"
    ),
    RegraIndicadorQuestionario(
        "trabalha_40h_pct", "QE_I10", frozenset("D"), frozenset("ABCDE"), "Trabalha quarenta horas"
    ),
    RegraIndicadorQuestionario(
        "acao_afirmativa_pct", "QE_I11", frozenset("BCDEF"), frozenset("ABCDEF"), "Ingresso por ação afirmativa"
    ),
    RegraIndicadorQuestionario(
        "auxilio_permanencia_pct", "QE_I15", frozenset("BCDEF"), frozenset("ABCDEF"), "Recebeu auxílio de permanência"
    ),
    RegraIndicadorQuestionario(
        "bolsa_academica_pct", "QE_I16", frozenset("BCDEFGH"), frozenset("ABCDEFGH"),
        "Recebeu bolsa acadêmica", multipla_escolha=True,
        respostas_exclusivas=frozenset("A")
    ),
    RegraIndicadorQuestionario(
        "estudo_4h_ou_mais_pct", "QE_I17", frozenset("CDE"), frozenset("ABCDE"), "Quatro horas semanais ou mais de estudo"
    ),
    RegraIndicadorQuestionario(
        "pretende_magisterio_pct", "QE_I18", frozenset("AB"), frozenset("ABCD"), "Pretende atuar no magistério"
    ),
)

SCHEMA_CONCEITO_2025 = SchemaConceito(
    aba="Conceito Enade Licenciaturas",
    mapa_colunas=(
        ("Ano", "NU_ANO"),
        ("Código da Área", "CO_GRUPO"),
        ("Área de Avaliação", "AREA"),
        ("Código da IES", "CO_IES"),
        ("Nome da IES¹", "NO_IES"),
        ("Sigla da IES ¹", "SG_IES"),
        ("Organização Acadêmica ¹", "ORGANIZACAO_ACADEMICA"),
        ("Categoria Administrativa ²", "CATEGORIA_ADMINISTRATIVA"),
        ("Código do Curso", "CO_CURSO"),
        ("Modalidade de Ensino", "MODALIDADE"),
        ("Código do Município", "CO_MUNIC_CURSO"),
        ("Município do Curso", "MUNICIPIO"),
        ("Sigla da UF", "UF"),
        ("Nº de Concluintes Inscritos", "INSCRITOS"),
        ("Nº  de Concluintes Participantes", "PARTICIPANTES"),
        (
            "Total de Concluinte  Igual ou Acima do Padrão 1 de Proficiência",
            "TOTAL_PADRAO_PROFICIENCIA",
        ),
        (
            "Percentual de Concluintes Igual ou Acima do Padrão 1 de Proficiência",
            "PCT_PADRAO_PROFICIENCIA",
        ),
        ("Conceito Enade (Faixa)", "CONCEITO_ENADE_ORIGINAL"),
    ),
    colunas_numericas=(
        "NU_ANO",
        "CO_GRUPO",
        "CO_IES",
        "CO_CURSO",
        "CO_MUNIC_CURSO",
        "INSCRITOS",
        "PARTICIPANTES",
        "TOTAL_PADRAO_PROFICIENCIA",
        "PCT_PADRAO_PROFICIENCIA",
    ),
)

ENADE_2025_LICENCIATURAS = ContratoEdicao(
    ano=2025,
    nome="Enade das Licenciaturas 2025",
    prefixo_arquivos="microdados2025_arq",
    quantidade_arquivos=28,
    leitura=ConfiguracaoLeitura(
        separador=";",
        decimal=",",
        quotechar='"',
        encodings=("utf-8-sig", "utf-8", "cp1252", "latin1"),
    ),
    arquivos=_schemas_arquivos(),
    desempenho=SchemaDesempenho(
        geral="NT_GER",
        objetiva="NT_OBJ",
        discursiva="NT_DIS",
        proficiencia="PROFICIENCIA",
        acertos="QT_ACERTOS",
        vetores_string=("DS_VT_GAB_OBJ", "DS_VT_ESC_OBJ", "DS_VT_ACE_OBJ"),
    ),
    presenca=SchemaPresenca(
        variaveis=("TP_PRES", "TP_SIT_DISC", "IN_REAPLICACAO"),
        codigos_tp_pres=(
            (222, "ausente"),
            (334, "eliminado"),
            (444, "ausente_dupla_graduacao"),
            (555, "presente_resultado_valido"),
            (888, "resultado_desconsiderado"),
        ),
    ),
    questionario=SchemaQuestionario(
        itens_gerais=ITENS_GERAIS,
        itens_processo_formativo=ITENS_PROCESSO,
        itens_licenciatura=(),
        itens_recomendacao=ITENS_RECOMENDACAO,
        regras_indicadores=REGRAS_SOCIOECONOMICAS,
        codigos_validos_processo=frozenset(range(1, 7)),
        codigos_especiais_processo=((7, "nao_sabe_responder"), (8, "nao_se_aplica")),
        codigos_concordancia_processo=frozenset((4, 5, 6)),
        descricao_escala_processo="1=discordância total; 6=concordância total",
    ),
    capacidades=CapacidadesEdicao(
        proficiencia=True,
        recomendacao=True,
        questionario_licenciatura=False,
    ),
    conceito=SCHEMA_CONCEITO_2025,
    modalidades=((0, "EaD"), (1, "Presencial")),
)
