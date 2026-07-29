from __future__ import annotations


import pandas as pd


def _fmt(v: float, casas: int = 1) -> str:
    if pd.isna(v):
        return "não disponível"
    return f"{v:.{casas}f}".replace(".", ",")


def resumo_executivo(base: pd.DataFrame) -> str:
    ufpa = base[base["CO_IES"].eq(569)].copy()
    c1 = ufpa[ufpa["CONCEITO_ENADE_NUM"].eq(1)]
    superior = ufpa[ufpa["CONCEITO_ENADE_NUM"].gt(1)]
    m1 = c1["nt_ger_mean"].mean()
    ms = superior["nt_ger_mean"].mean()
    return (
        f"Este relatório analisa {len(ufpa)} ofertas validadas de licenciatura em Física da UFPA no "
        f"Enade das Licenciaturas 2025, das quais {len(c1)} receberam Conceito Enade 1. A unidade "
        "principal é o curso (CO_CURSO). Os arquivos temáticos foram tratados separadamente e "
        "agregados por curso, sem reconstrução de registros individuais. Entre as ofertas da UFPA, "
        f"a média das médias de NT_GER foi {_fmt(m1)} nas ofertas conceito 1 e {_fmt(ms)} na oferta "
        "com conceito superior. O contraste deve ser interpretado junto ao porte, à modalidade, à "
        "participação e à composição discente. As associações entre desempenho, perfil e processo "
        "formativo são ecológicas e não sustentam inferência causal ou individual."
    )


def panorama_texto(cursos: pd.DataFrame) -> str:
    ufpa = cursos[cursos["CO_IES"].eq(569)]
    grupos = cursos["GRUPO_CODIGO"].value_counts().to_dict()
    return (
        f"Foram identificados {len(cursos)} cursos de Física com registros no cadastro analítico. "
        f"A UFPA possui {len(ufpa)} ofertas validadas: quatro classificadas no grupo A "
        "(Conceito Enade 1) e uma no grupo B (conceito superior). Os demais cursos distribuem-se "
        f"entre outras IES do Pará (grupo C: {grupos.get('C', 0)}), restante da Região Norte "
        f"(grupo D: {grupos.get('D', 0)}) e restante do Brasil (grupo E: {grupos.get('E', 0)}). "
        "A oferta inicialmente informada para Tucuruí permanece registrada como ausência de "
        "localização analítica e não foi reclassificada como conceito 1."
    )



def tucurui_texto() -> str:
    return (
        "A oferta de Física da UFPA em Tucuruí, identificada pelo código de curso 1627581, "
        "constava na relação institucional inicial, mas não foi localizada na planilha de "
        "resultados do Conceito Enade 2025 nem nos arquivos dos microdados utilizados nesta "
        "análise. Por isso, não foi possível informar inscritos, participantes, presença, "
        "proficiência ou Conceito Enade para essa oferta com base nas fontes disponíveis. A "
        "ausência de registros não foi interpretada como valor zero nem como Conceito Enade 1. "
        "As fontes analisadas também não permitem determinar a causa administrativa exata da "
        "ausência. Hipóteses gerais incluem inexistência de concluintes habilitados, alteração "
        "do código do curso, não enquadramento na população avaliada ou ausência de condições "
        "para cálculo e divulgação do conceito; nenhuma dessas hipóteses foi confirmada para "
        "Tucuruí. Diferentemente dessa oferta, Belém Presencial, Belém EaD, Abaetetuba, "
        "Ananindeua e Salinópolis foram localizadas tanto na planilha de Conceito Enade quanto "
        "no cadastro dos microdados, com correspondência pelo CO_CURSO."
    )

def desempenho_texto(base: pd.DataFrame) -> str:
    ufpa = base[base["CO_IES"].eq(569)].sort_values("nt_ger_mean", ascending=False)
    topo = ufpa.iloc[0]
    baixo = ufpa.iloc[-1]
    return (
        f"A maior média de NT_GER entre as ofertas da UFPA foi observada em {topo['ROTULO_OFERTA']} "
        f"({_fmt(topo['nt_ger_mean'])}; N={int(topo['nt_ger_count'])}), enquanto a menor ocorreu em "
        f"{baixo['ROTULO_OFERTA']} ({_fmt(baixo['nt_ger_mean'])}; N={int(baixo['nt_ger_count'])}). "
        "Média, mediana, dispersão e intervalos devem ser examinados conjuntamente, sobretudo nos "
        "cursos de menor porte. A direção do contraste interno é consistente com o Conceito Enade, "
        "mas não identifica mecanismo causal."
    )


def socio_texto(tabela: pd.DataFrame) -> str:
    renda = tabela.loc[tabela["renda_ate_3sm_pct"].idxmax()]
    trabalho = tabela.loc[tabela["trabalha_pct"].idxmax()]
    return (
        f"A maior proporção agregada de estudantes com renda familiar de até três salários mínimos "
        f"foi observada em {renda['ROTULO_OFERTA']} ({_fmt(renda['renda_ate_3sm_pct'] * 100)}%). "
        f"A maior proporção de estudantes que trabalham ocorreu em {trabalho['ROTULO_OFERTA']} "
        f"({_fmt(trabalho['trabalha_pct'] * 100)}%). Esses indicadores descrevem a composição das "
        "ofertas e podem orientar hipóteses institucionais, mas não permitem afirmar que uma "
        "característica individual produziu determinada nota."
    )


def associacoes_texto(associacoes: pd.DataFrame) -> str:
    validas = associacoes.dropna(subset=["spearman_rho"])
    if validas.empty:
        return "Não foram obtidas associações ecológicas válidas para síntese."
    linha = validas.loc[validas["spearman_rho"].abs().idxmax()]
    intensidade = abs(float(linha["spearman_rho"]))
    classe = "fraca" if intensidade < 0.3 else "moderada" if intensidade < 0.6 else "forte"
    direcao = "positiva" if linha["spearman_rho"] > 0 else "negativa"
    return (
        f"A associação ecológica de maior magnitude entre as combinações examinadas relacionou "
        f"{linha['desfecho']} e {linha['preditor']} (ρ={_fmt(linha['spearman_rho'], 2)}; "
        f"N={int(linha['n_cursos'])}), classificada descritivamente como {classe} e {direcao}. "
        "O coeficiente descreve cursos, não estudantes, pode ser sensível a outliers e não deve ser "
        "interpretado como efeito causal."
    )


def aprofundamentos() -> list[tuple[str, str]]:
    return [
        ("Série histórica", "Pergunta: os contrastes persistem em edições anteriores? Variáveis: conceito, participação e notas padronizadas por edição. Método: painel descritivo por CO_CURSO quando a correspondência institucional for validada. Limitação: mudanças de instrumento e cadastro."),
        ("Pareamento ampliado", "Pergunta: quais diferenças permanecem entre cursos estruturalmente semelhantes? Variáveis: modalidade, categoria, organização acadêmica, porte e território. Método: escore de propensão ou distância de Mahalanobis no nível do curso. Limitação: confundimento não observado."),
        ("Diagnóstico qualitativo", "Pergunta: quais processos institucionais podem explicar os padrões agregados? Fontes: PPC, relatórios de autoavaliação, entrevistas e grupos focais. Método: estudo de casos múltiplos. Limitação: generalização analítica, não estatística."),
        ("Itens do processo formativo", "Pergunta: quais itens específicos concentram as maiores diferenças? Variáveis: QE_I20–QE_I66. Método: análise por item, consistência interna e invariância quando o N permitir. Limitação: respostas autorreferidas e cobertura variável."),
        ("Comparação entre licenciaturas", "Pergunta: há padrões comuns às ofertas conceito 1 da UFPA? Variáveis: indicadores padronizados dentro de CO_GRUPO. Método: percentis e escores z por área. Limitação: não comparar notas brutas entre áreas."),
    ]
