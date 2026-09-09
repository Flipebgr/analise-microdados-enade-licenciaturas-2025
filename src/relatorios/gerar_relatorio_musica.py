from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'relatorios' / 'musica'
OUT.mkdir(parents=True, exist_ok=True)
DOCX = OUT / 'relatorio_musica_enade_2025_ufpa.docx'
FIG = ROOT / 'figuras' / 'musica'
D = Document()
sec = D.sections[0]
sec.top_margin = Cm(3)
sec.left_margin = Cm(3)
sec.right_margin = Cm(2)
sec.bottom_margin = Cm(2)
sec.header_distance = Cm(1.5)
sec.footer_distance = Cm(1.25)
styles = D.styles
styles['Normal'].font.name = 'Arial'
styles['Normal'].font.size = Pt(12)
styles['Normal'].paragraph_format.line_spacing = 1.5
styles['Normal'].paragraph_format.first_line_indent = Cm(1.25)
styles['Normal'].paragraph_format.space_after = Pt(0)
for s in ['Title', 'Heading 1', 'Heading 2', 'Heading 3']:
    styles[s].font.name = 'Arial'
styles['Heading 1'].font.size = Pt(12)
styles['Heading 1'].font.bold = True
styles['Heading 1'].paragraph_format.space_before = Pt(18)
styles['Heading 1'].paragraph_format.space_after = Pt(8)
styles['Heading 2'].font.size = Pt(12)
styles['Heading 2'].font.bold = True
styles['Heading 2'].paragraph_format.space_before = Pt(12)
styles['Heading 2'].paragraph_format.space_after = Pt(6)
styles['Heading 3'].font.size = Pt(11)
styles['Heading 3'].font.bold = True
styles['Heading 3'].paragraph_format.space_before = Pt(10)
styles['Heading 3'].paragraph_format.space_after = Pt(4)
if 'Legenda' not in styles:
    st = styles.add_style('Legenda', WD_STYLE_TYPE.PARAGRAPH)
else:
    st = styles['Legenda']
st.font.name = 'Arial'
st.font.size = Pt(10)
st.paragraph_format.line_spacing = 1.0
st.paragraph_format.first_line_indent = Cm(0)
st.paragraph_format.space_after = Pt(4)
for section in D.sections:
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    p._p.append(fld)

def add_para(text='', bold_prefix=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first=True, size=None):
    p = D.add_paragraph()
    p.alignment = align
    if not first:
        p.paragraph_format.first_line_indent = Cm(0)
    if bold_prefix and text.startswith(bold_prefix):
        r = p.add_run(bold_prefix)
        r.bold = True
        p.add_run(text[len(bold_prefix):])
    else:
        p.add_run(text)
    if size:
        for r in p.runs:
            r.font.size = Pt(size)
    return p

def heading(text, level=1):
    p = D.add_paragraph(style=f'Heading {level}')
    p.paragraph_format.first_line_indent = Cm(0)
    p.add_run(text)
    return p

def shade(cell, fill='D9EAF7'):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), fill)
    tcPr.append(shd)

def set_cell_width(cell, cm):
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn('w:tcW'))
    if tcW is None:
        tcW = OxmlElement('w:tcW')
        tcPr.append(tcW)
    tcW.set(qn('w:w'), str(int(Cm(cm).emu / 635)))
    tcW.set(qn('w:type'), 'dxa')

def table(rows, widths=None, font=9, header=True):
    t = D.add_table(rows=len(rows), cols=len(rows[0]))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = 'Table Grid'
    t.autofit = False
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = str(val)
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if widths:
                set_cell_width(c, widths[j])
            for p in c.paragraphs:
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(0)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.name = 'Arial'
                    r.font.size = Pt(font)
                    if i == 0 and header:
                        r.bold = True
            if i == 0 and header:
                shade(c)
    D.add_paragraph().paragraph_format.space_after = Pt(0)
    return t

def fig(title, filename, note, discussion):
    p = D.add_paragraph(style='Legenda')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title)
    r.bold = True
    pic = D.add_paragraph()
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.paragraph_format.first_line_indent = Cm(0)
    pic.add_run().add_picture(str(FIG / filename), width=Cm(15.5))
    n = D.add_paragraph(style='Legenda')
    n.alignment = WD_ALIGN_PARAGRAPH.LEFT
    n.add_run('Nota: ').bold = True
    n.add_run(note)
    add_para(discussion)
for txt, sz, bold in [('UNIVERSIDADE FEDERAL DO PARÁ', 12, True), ('ENADE DAS LICENCIATURAS 2025', 12, True)]:
    p = add_para(txt, align=WD_ALIGN_PARAGRAPH.CENTER, first=False, size=sz)
    p.runs[0].bold = bold
for _ in range(5):
    D.add_paragraph()
p = add_para('MÚSICA', align=WD_ALIGN_PARAGRAPH.CENTER, first=False, size=14)
p.runs[0].bold = True
p = add_para('Desempenho, perfil discente, processo formativo e benchmarks da oferta da UFPA', align=WD_ALIGN_PARAGRAPH.CENTER, first=False, size=12)
p.runs[0].bold = True
for _ in range(8):
    D.add_paragraph()
add_para('Belém', align=WD_ALIGN_PARAGRAPH.CENTER, first=False)
add_para('2026', align=WD_ALIGN_PARAGRAPH.CENTER, first=False)
D.add_page_break()
p = add_para('MÚSICA NO ENADE DAS LICENCIATURAS 2025: DESEMPENHO, PERFIL, PROCESSO FORMATIVO E BENCHMARKS DA OFERTA DA UFPA', align=WD_ALIGN_PARAGRAPH.CENTER, first=False, size=12)
p.runs[0].bold = True
heading('RESUMO', 2)
add_para('Este relatório técnico-científico analisa a Licenciatura em Música da Universidade Federal do Pará (UFPA) no Enade das Licenciaturas 2025. O universo reúne 107 cursos identificados por CO_CURSO. A UFPA possui uma única oferta localizada nas fontes analisadas, em Belém, presencial (CO_CURSO=114950), com 44 inscritos, 37 participantes, participação oficial de 84,1% e Conceito Enade 1. Não há outra oferta de Música da UFPA nem outra oferta da área no Pará nas fontes oficiais, de modo que os grupos B e C são estruturalmente vazios. A oferta apresenta NT_GER médio de 41,64, situando-se no percentil 19,4 da distribuição nacional das médias de curso. O contraste com cursos estruturalmente comparáveis indica diferença de cerca de 8 pontos abaixo da mediana do benchmark. Em contrapartida, as avaliações do processo formativo e os itens de recomendação são, em geral, favoráveis. Os resultados evidenciam uma configuração multidimensional e não sustentam causalidade individual.')
p = add_para('Palavras-chave: Enade; Música; UFPA; formação de professores; microdados; Conceito Enade; benchmark.', first=False)
p.runs[0].bold = True
heading('ABSTRACT', 2)
add_para("This technical-scientific report examines the UFPA Music teacher-education program in the 2025 Enade. The analytical universe comprises 107 courses. UFPA has one on-campus offer in Belém (CO_CURSO=114950), with 44 enrolled students, 37 participants and Enade Concept 1. There are no other UFPA Music offers and no other Music offers in Pará in the official sources. UFPA's mean NT_GER is 41.64, around the 19.4th national percentile of course means, and roughly eight points below the median of structurally comparable courses. Formative-process perceptions and recommendation indicators, however, are generally favorable. Results are descriptive and non-causal.")
p = add_para('Keywords: Enade; Music; UFPA; teacher education; microdata; benchmark.', first=False)
p.runs[0].bold = True
D.add_page_break()
heading('SUMÁRIO', 1)
for line in ['1 INTRODUÇÃO', '2 REFERENCIAL INSTITUCIONAL E METODOLÓGICO', '3 METODOLOGIA', '4 PANORAMA DA LICENCIATURA EM MÚSICA', '5 RESULTADOS', '5.1 Desempenho', '5.2 Perfil demográfico e socioeconômico', '5.3 Trajetória e condições acadêmicas', '5.4 Processo formativo', '5.5 Recomendação', '5.6 Benchmark comparável', '5.7 Associações ecológicas', '5.8 Narrativa gráfica', '6 DISCUSSÃO', '7 CONCLUSÃO', 'REFERÊNCIAS', 'APÊNDICES']:
    add_para(line, align=WD_ALIGN_PARAGRAPH.LEFT, first=False)
D.add_page_break()
heading('1 INTRODUÇÃO')
p = add_para('A pergunta central é: quais características de desempenho, composição discente, trajetória acadêmica e avaliação do processo formativo diferenciam a oferta de Música da UFPA, com Conceito Enade 1, das demais ofertas da mesma área na Região Norte e no Brasil?')
p.runs[0].bold = True
add_para('A planilha oficial identifica 107 ofertas nacionais, mas apenas uma oferta da UFPA e nenhuma outra oferta de Música no Pará. Assim, os contrastes principais são com o restante da Região Norte, o restante do Brasil, os cursos nacionais de Conceito 1, os cursos de conceito superior e benchmarks estruturalmente comparáveis.')
heading('2 REFERENCIAL INSTITUCIONAL E METODOLÓGICO')
add_para('O Enade integra o Sistema Nacional de Avaliação da Educação Superior (Sinaes) e fornece evidências de desempenho e informações declaradas pelos estudantes sobre trajetória, perfil e experiência formativa. O Conceito Enade é tratado como classificação externa do curso, não como variável causal nem explicação suficiente do desempenho.')
add_para('Resultados de prova, composição discente, condições acadêmicas, processo formativo e recomendação são dimensões distintas. A coexistência de resultados favoráveis e desfavoráveis entre dimensões é interpretada como heterogeneidade institucional.')
heading('3 METODOLOGIA')
add_para('A unidade principal é CO_CURSO. Os 28 arquivos temáticos não permitem reconhecer o mesmo estudante entre temas. Não se utiliza posição de linha como chave, não se cria identificador artificial e não se realizam joins individuais entre desempenho, perfil e percepção. O fluxo é: arquivo temático → tratamento de ausências → agregação por CO_CURSO → uma linha por curso → junções one-to-one → comparação entre cursos.')
add_para('NT_GER, NT_OBJ e NT_DIS são examinadas conjuntamente porque pertencem ao mesmo arquivo. Relações entre desempenho e indicadores de questionário ou perfil são apenas ecológicas.')
add_para('Grupos exclusivos: A) UFPA Conceito 1, N=1; B) demais ofertas UFPA com conceito superior, N=0; C) outras IES do Pará, N=0; D) restante da Região Norte, N=8; E) restante do Brasil, N=98. B e C permanecem vazios.')
add_para('O benchmark mantém modalidade, categoria administrativa e organização acadêmica e varia a janela de porte em 0,75–1,25x, 0,50–1,50x e 0,50–2,00x o número de participantes da oferta UFPA.')
add_para('No processo formativo, QE_I20–QE_I66 usam respostas 1–6; 7 e 8 são ausências analíticas. QE_I31, QE_I32 e QE_I43 são específicos de EaD e não entram nas dimensões comuns da oferta presencial. Não há itens invertidos. As oito dimensões são exploratórias e não formam índice global.')
add_para('No desempenho, reportam-se média, mediana, dispersão, IC95%, diferença padronizada de Hedges e comparação com os recortes externos usando somente o arquivo de desempenho.')
heading('4 PANORAMA DA LICENCIATURA EM MÚSICA')
add_para('O universo contém 107 cursos de Música. A distribuição dos conceitos é: Conceito 1 = 44; Conceito 2 = 36; Conceito 3 = 14; Conceito 4 = 8; Conceito 5 = 1; sem conceito numérico = 4. A concentração nacional em Conceito 1 torna indispensável observar também a nota contínua.')
add_para('Tabela 1 – Oferta de Música da UFPA', align=WD_ALIGN_PARAGRAPH.LEFT, first=False, size=10).runs[0].bold = True
table([['Indicador', 'Valor'], ['CO_CURSO', '114950'], ['Oferta', 'Belém — Presencial'], ['Inscritos', '44'], ['Participantes', '37'], ['Participação', '84,1%'], ['Padrão de proficiência', '24,3%'], ['Conceito', '1'], ['NT_GER', '41,64'], ['NT_OBJ', '39,27'], ['NT_DIS', '5,11'], ['Percentil Brasil', '19,4']], [7, 9], font=9)
add_para('Fonte: elaboração própria com base nos microdados e na planilha de Conceito Enade 2025.', align=WD_ALIGN_PARAGRAPH.LEFT, first=False, size=9)
add_para('A taxa de presença no arquivo de desempenho coincide com a participação oficial: 84,1%. Não houve reaplicações.')
heading('5 RESULTADOS')
heading('5.1 Desempenho', 2)
add_para('A UFPA apresenta NT_GER médio de 41,64, mediana de 40,68, DP de 10,92 e IC95% de 38,12 a 45,16. O NT_OBJ médio é 39,27 e o NT_DIS médio é 5,11.')
add_para('Entre os 103 cursos nacionais com NT_GER calculável, a UFPA está no percentil 19,4.')
add_para('Tabela 2 – Referências territoriais de desempenho', align=WD_ALIGN_PARAGRAPH.LEFT, first=False, size=10).runs[0].bold = True
table([['Recorte', 'Cursos', 'Com NT_GER', 'Média NT_GER', 'Mediana NT_GER', 'Média NT_OBJ', 'Média NT_DIS'], ['UFPA — Belém', '1', '1', '41,64', '41,64', '39,27', '5,11'], ['Norte sem Pará', '8', '7', '41,67', '43,68', '41,11', '4,39'], ['Brasil sem Norte', '98', '95', '47,98', '47,98', '45,69', '5,71']], [3.4, 1.4, 1.8, 2.2, 2.4, 2.2, 2.2], font=7.5)
add_para('Fonte: elaboração própria a partir do arquivo de desempenho do Enade 2025.', align=WD_ALIGN_PARAGRAPH.LEFT, first=False, size=9)
add_para('No arquivo de desempenho, a diferença de NT_GER entre UFPA e Norte sem Pará é -2,06 pontos (IC95% -6,97 a 2,86; Hedges g=-0,158). Frente ao Brasil sem Norte, a diferença é -4,54 pontos (IC95% -8,22 a -0,85; g=-0,331). O contraste é mais forte em NT_OBJ; em NT_DIS o efeito é pequeno.')
add_para('O percentual no padrão de proficiência é 24,3% (9 de 37 participantes).')
heading('5.2 Perfil demográfico e socioeconômico', 2)
add_para('Entre 44 registros válidos de sexo, 36,4% são do sexo feminino. A idade média é 31,77 anos e a mediana, 28,50.')
add_para('Em raça/cor (QE_I03, N=40), a distribuição válida é: Parda 70,0% (n=28), Preta 17,5% (n=7), Branca 7,5% (n=3), Não quer declarar 5,0% (n=2). Quatro registros não tiveram resposta analítica válida.')
add_para('Tabela 3 – Perfil selecionado da oferta UFPA', align=WD_ALIGN_PARAGRAPH.LEFT, first=False, size=10).runs[0].bold = True
table([['Indicador', 'Valor', 'N válido'], ['Sexo feminino', '36,4%', '44'], ['Idade média (anos)', '31,77', '44'], ['Primeira geração no ensino superior', '38,9%', '36'], ['Mãe com ensino superior', '25,6%', '39'], ['Pai com ensino superior', '20,6%', '34'], ['Renda até 3 SM', '75,0%', '40'], ['Trabalha', '52,5%', '40'], ['Trabalha 40h', '7,5%', '40'], ['Ação afirmativa', '42,5%', '40'], ['Auxílio permanência', '12,5%', '40'], ['Bolsa acadêmica', '74,4%', '39'], ['Estudo ≥4h/semana', '55,0%', '40'], ['Pretende magistério', '80,0%', '40']], [9, 3.5, 3.5], font=9)
add_para('A renda até três salários mínimos alcança 75,0%, acima das medianas do Norte sem Pará (64,9%) e do Brasil sem Norte (59,5%). A bolsa acadêmica aparece em 74,4% e o auxílio permanência em 12,5% das respostas válidas. Essas diferenças são descritivas; não podem explicar individualmente o desempenho porque os indicadores vêm de arquivos distintos.')
heading('5.3 Trajetória e condições acadêmicas', 2)
add_para('O tempo médio desde o ingresso é 5,07 anos. O turno noturno não aparece entre os 44 registros válidos. A proporção que estuda quatro horas ou mais por semana é 55,0%. A intenção de exercer o magistério é 80,0%. No QE_I70, 37 dos 40 respondentes válidos escolheram “Quero ser professor da rede pública”, indicando forte interesse declarado pela docência pública.')
heading('5.4 Processo formativo', 2)
add_para('As médias UFPA nas oito dimensões variam entre 5,09 e 5,46, em escala de 1 a 6.')
add_para('Tabela 4 – Dimensões do processo formativo', align=WD_ALIGN_PARAGRAPH.LEFT, first=False, size=10).runs[0].bold = True
table([['Dimensão', 'UFPA', 'N UFPA', 'Mediana Norte sem Pará', 'Mediana Brasil sem Norte'], ['Oportunidades', '5,12', '39', '5,34', '4,93'], ['Atuação docente', '5,44', '40', '5,16', '5,18'], ['Organização / teoria-prática', '5,43', '40', '5,16', '5,12'], ['Infraestrutura', '5,09', '38', '4,80', '4,79'], ['Planejamento / ensino', '5,40', '40', '5,36', '5,21'], ['Inclusão / diversidade', '5,12', '38', '4,92', '4,84'], ['Gestão / avaliação', '5,28', '40', '5,17', '5,04'], ['Colaboração / famílias', '5,46', '39', '5,26', '5,23']], [5.4, 2, 2, 3.5, 3.5], font=8)
add_para('Na UFPA, os alfas calculáveis variam de 0,748 a 0,956. Em infraestrutura e recursos há apenas 9 casos completos, abaixo do mínimo de 10 adotado, e por isso o alfa UFPA não é reportado. Alfa elevado não comprova unidimensionalidade. A oferta apresenta avaliações formativas favoráveis apesar do baixo posicionamento relativo em desempenho, o que impede uma leitura monocausal do Conceito 1.')
heading('5.5 Recomendação', 2)
add_para('No QE_I68, recomendação do curso, a média é 8,88 (N=40). No QE_I69, recomendação da IES, a média é 9,55 (N=40). As medianas Norte sem Pará são 8,48 e 9,27; no Brasil sem Norte, 8,56 e 8,88. Os itens são tratados como recomendação, conforme o instrumento oficial, e não como satisfação.')
heading('5.6 Benchmark comparável', 2)
add_para('A análise produz entre 5 e 11 cursos comparáveis, dependendo da janela de porte.')
add_para('Tabela 5 – Sensibilidade do benchmark comparável em NT_GER', align=WD_ALIGN_PARAGRAPH.LEFT, first=False, size=10).runs[0].bold = True
table([['Critério de porte', 'N comparáveis', 'NT_GER UFPA', 'Média benchmark', 'Mediana benchmark', 'Diferença para mediana'], ['±25%', '5', '41,64', '48,30', '49,30', '-7,66'], ['0,5–1,5x', '10', '41,64', '49,22', '49,95', '-8,30'], ['0,5–2x', '11', '41,64', '49,13', '49,68', '-8,03']], [3.1, 2.4, 2.3, 2.7, 2.7, 3], font=8)
add_para('A diferença para a mediana permanece entre aproximadamente -7,7 e -8,3 pontos. A estabilidade torna o contraste mais informativo que a comparação territorial ampla, embora o pareamento observacional não controle todas as diferenças institucionais.')
heading('5.7 Associações ecológicas', 2)
add_para('Tabela 6 – Associações ecológicas com NT_GER médio', align=WD_ALIGN_PARAGRAPH.LEFT, first=False, size=10).runs[0].bold = True
table([['Indicador agregado', 'N cursos', 'Spearman ρ', 'p'], ['Renda até 3 SM', '103', '-0,293', '0,0027'], ['Trabalha', '103', '-0,021', '0,8345'], ['Auxílio permanência', '103', '0,455', '<0,0001'], ['Recomendação do curso (QE_I68)', '103', '-0,261', '0,0078'], ['Recomendação da IES (QE_I69)', '103', '0,009', '0,9299'], ['Atuação docente', '103', '-0,169', '0,0885'], ['Infraestrutura e recursos', '103', '-0,333', '0,0006'], ['Organização e integração', '103', '-0,263', '0,0073']], [9, 2.4, 2.8, 2.8], font=9)
add_para('As maiores magnitudes aparecem em auxílio permanência, infraestrutura e recursos e renda até três salários mínimos. Essas associações são ecológicas e podem refletir composição, políticas institucionais, padrões de resposta e variáveis não modeladas; não autorizam interpretação individual ou causal.')
heading('5.8 Narrativa gráfica', 2)
fig('Figura 1 – Oferta UFPA: participação e proficiência', '01_painel_oferta_ufpa.png', 'N=44 inscritos; N=37 participantes; oferta presencial UFPA; ausências não são recodificadas.', 'Participação oficial de 84,1% e 24,3% no padrão de proficiência. A presença elevada indica que o baixo resultado não pode ser atribuído simplesmente à baixa adesão. Limitação: participação não explica desempenho.')
fig('Figura 2 – Posição relativa de NT_GER', '02_posicao_relativa_nt_ger.png', 'N=103 cursos com NT_GER calculável; mesma área de Música; a UFPA é destacada.', 'A UFPA está no percentil 19,4 nacional das médias de curso. Hipótese: a faixa 1 corresponde também a posição baixa na nota contínua. Limitação: média do curso não descreve toda a dispersão individual.')
fig('Figura 3 – Distribuição individual de NT_GER', '03a_distribuicao_nt_ger.png', 'N válido indicado no gráfico; variáveis do mesmo arquivo de desempenho.', 'O boxplot usa apenas o arquivo de desempenho. O distanciamento é observado no centro da distribuição, sem vínculo individual com variáveis de outros arquivos.')
fig('Figura 4 – Distribuição individual de NT_OBJ', '03b_distribuicao_nt_obj.png', 'N válido indicado no gráfico; mesma fonte temática de desempenho.', 'O distanciamento é mais visível no componente objetivo. Limitação: NT_OBJ possui relação mecânica com NT_GER.')
fig('Figura 5 – Distribuição individual de NT_DIS', '03c_distribuicao_nt_dis.png', 'N válido indicado no gráfico; mesma fonte temática de desempenho.', 'No componente discursivo o contraste é menor. Limitação: NT_DIS possui relação mecânica com NT_GER.')
fig('Figura 6 – Perfil socioeconômico', '04_perfil_socioeconomico.png', 'percentuais entre respostas válidas; benchmarks são medianas de cursos dos recortes.', 'A UFPA apresenta maior renda baixa e menor trabalho que as medianas externas, além de ação afirmativa e bolsa acadêmica elevadas. Limitação: esses indicadores não podem ser ligados individualmente às notas.')
fig('Figura 7 – Processo formativo', '05_processo_formativo_dimensoes.png', 'escala 1–6; respostas 7 e 8 tratadas como ausências; QE_I31, QE_I32 e QE_I43 excluídos das dimensões comuns.', 'As médias UFPA são altas e em geral superiores às medianas externas. Isso evidencia que percepção formativa favorável e baixo resultado na prova podem coexistir. Limitação: dimensões exploratórias e autorrelato.')
fig('Figura 8 – Benchmark comparável', '06_benchmark_sensibilidade.png', 'mesma modalidade, categoria administrativa e organização acadêmica; janelas de porte explicitadas no eixo.', 'A mediana dos pares permanece acima da UFPA nas três janelas. A estabilidade reforça o diagnóstico de diferença de desempenho, sem causalidade.')
fig('Figura 9 – Recomendação', '07_recomendacao.png', 'QE_I68 e QE_I69 em escala 0–10; não interpretados automaticamente como satisfação.', 'Curso e IES têm médias altas, sobretudo a recomendação da instituição. Recomendação e desempenho são construtos distintos.')
fig('Figura 10 – Associação ecológica', '08_associacao_ecologica.png', 'unidade = curso; associação de Spearman; interpretação ecológica, não individual.', 'A dispersão entre cursos e a posição da UFPA mostram que o coeficiente não deve ser lido isoladamente. Limitação: falácia ecológica e outliers.')
fig('Figura 11 – Síntese', '09_sintese_ufpa.png', 'indicadores em escalas percentuais/percentis; não constituem índice único.', 'Reúne percentil de desempenho, participação, proficiência e indicadores socioeconômicos sem criar índice global.')
heading('6 DISCUSSÃO')
add_para('A oferta de Música da UFPA combina participação elevada, desempenho contínuo baixo e percepções formativas favoráveis. Dos 44 inscritos, 37 participaram. O NT_GER médio de 41,64 situa a oferta aproximadamente no percentil 19,4 nacional e cerca de oito pontos abaixo da mediana de cursos comparáveis.')
add_para('O processo formativo apresenta médias acima de 5 nas oito dimensões exploratórias, e as recomendações do curso e da IES são altas. Portanto, a evidência não sustenta uma narrativa simples em que Conceito 1 corresponda a percepção generalizadamente negativa de docentes, infraestrutura ou organização.')
add_para('O perfil discente é marcado por 75,0% de renda até três salários mínimos, 42,5% de ação afirmativa e 74,4% de bolsa acadêmica entre respostas válidas. Ao mesmo tempo, 52,5% declaram trabalhar. Esses padrões podem orientar investigação institucional, mas não podem ser ligados individualmente à nota.')
add_para('Música apresenta forte concentração nacional em Conceito 1: 44 de 107 cursos. A média de NT_GER dos cursos Conceito 1 é 42,12, próxima da UFPA, enquanto cursos com conceito superior têm média 51,49. Isso mostra que a faixa sintetiza uma diferença relevante, mas não elimina a heterogeneidade dentro de cada faixa.')
add_para('O benchmark comparável é o achado de desempenho mais consistente e sugere prioridade para investigação dos componentes da prova, conteúdos específicos, estrutura curricular e preparação dos concluintes. A análise atual não identifica o mecanismo responsável.')
heading('7 CONCLUSÃO')
add_para('A Licenciatura em Música da UFPA em Belém obteve Conceito Enade 1, com 44 inscritos e 37 participantes. A participação de 84,1% é elevada, enquanto 24,3% dos participantes atingiram o padrão de proficiência.')
add_para('O NT_GER médio de 41,64 coloca a oferta aproximadamente no percentil 19,4 nacional. Frente a pares comparáveis, a oferta permanece cerca de oito pontos abaixo da mediana. O distanciamento é mais forte no componente objetivo que no discursivo.')
add_para('O perfil discente apresenta renda baixa elevada, presença de ação afirmativa e bolsa acadêmica e forte intenção de atuar no magistério. As avaliações do processo formativo e de recomendação são favoráveis.')
p = add_para('O principal resultado é uma configuração multidimensional: baixo desempenho relativo na prova não coincide com avaliação formativa ou recomendação generalizadamente baixas. O aprofundamento institucional deve buscar explicar esse descompasso sem atribuir causalidade a características individuais ou a um único componente.')
p.runs[0].bold = True
heading('REFERÊNCIAS')
for ref in ['BRASIL. Lei nº 10.861, de 14 de abril de 2004. Institui o Sistema Nacional de Avaliação da Educação Superior - SINAES. Brasília, DF: Presidência da República, 2004.', 'INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Dicionário de arquivos e variáveis: microdados do Enade das Licenciaturas 2025. Brasília, DF: Inep, 2026.', 'INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Enade das Licenciaturas: microdados 2025. Brasília, DF: Inep, 2026.', 'INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Manual do usuário: Enade das Licenciaturas 2025. Brasília, DF: Inep, 2026.', 'INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Questionário do Estudante - Enade das Licenciaturas 2025. Brasília, DF: Inep, 2025.']:
    add_para(ref, first=False)
heading('APÊNDICES')
heading('APÊNDICE A – Regras de integridade metodológica', 2)
for x in ['Unidade principal: CO_CURSO.', 'Nenhum join individual entre arquivos temáticos.', 'Junções somente após agregação por curso e validação one-to-one.', 'Ausência de conceito não é Conceito 1.', 'NT_GER, NT_OBJ e NT_DIS podem ser analisadas conjuntamente porque pertencem ao mesmo arquivo.', 'Relações entre desempenho e perfil/questionário são exclusivamente ecológicas.', 'QE_I20–QE_I66 não são condensados em índice único.', 'QE_I68 e QE_I69 são recomendação, não satisfação.', 'Grupos B e C permanecem vazios por inexistência de ofertas correspondentes.']:
    p = D.add_paragraph(style='Normal')
    p.paragraph_format.first_line_indent = Cm(0)
    p.style = D.styles['Normal']
    p.add_run('• ' + x)
heading('APÊNDICE B – Consistência interna das dimensões', 2)
table([['Dimensão', 'Itens', 'N completos Brasil', 'Alfa Brasil', 'N completos UFPA', 'Alfa UFPA'], ['Oportunidades', '4', '1965', '0,805', '36', '0,748'], ['Atuação docente', '8', '2466', '0,928', '37', '0,939'], ['Organização / teoria-prática', '6', '2420', '0,904', '36', '0,930'], ['Infraestrutura', '5', '1156', '0,877', '9', '—'], ['Planejamento / ensino', '6', '2566', '0,943', '38', '0,946'], ['Inclusão / diversidade', '4', '2448', '0,869', '32', '0,892'], ['Gestão / avaliação', '7', '2489', '0,955', '38', '0,956'], ['Colaboração / famílias', '4', '2577', '0,922', '39', '0,898']], [4.8, 1.4, 2.7, 2.1, 2.6, 2.0], font=7.8)
heading('APÊNDICE C – Aprofundamentos sugeridos', 2)
items = [('Desempenho por item e componente.', 'Justificativa: o distanciamento aparece sobretudo em NT_OBJ. Pergunta: quais itens, objetos de conhecimento ou faixas de acerto concentram a diferença? Variáveis: QT_ACERTOS, respostas objetivas, caderno, proficiência, NT_OBJ, NT_DIS. Método: dificuldade por item, ECDF, quantis e análise por caderno. Limitação: relações mecânicas entre acertos, nota e proficiência.'), ('Currículo e aderência aos objetos avaliados.', 'Justificativa: o benchmark comparável permanece acima da UFPA. Pergunta: há desalinhamento entre conteúdos cursados e objetos avaliados? Variáveis: PPC, matriz curricular, conteúdos e matriz de referência do exame. Método: análise documental e mapeamento de cobertura. Limitação: requer fontes institucionais externas aos microdados.'), ('Processo formativo item a item.', 'Justificativa: as médias das dimensões são altas apesar do Conceito 1. Pergunta: existem itens específicos com fragilidade ocultada pelas médias? Variáveis: QE_I20–QE_I66. Método: distribuição ordinal, N válido, concordância e comparação com cursos federais comparáveis. Limitação: autorrelato e múltiplas comparações.'), ('Perfil de trabalho, renda e permanência.', 'Justificativa: a UFPA apresenta composição socioeconômica específica. Pergunta: como o perfil se compara a licenciaturas de Música em universidades federais de porte semelhante? Variáveis: renda, trabalho, ação afirmativa, auxílios, bolsas, horas de estudo. Método: comparação agregada por curso. Limitação: falácia ecológica.'), ('Trajetória docente e interesse na PND.', 'Justificativa: 80% pretendem o magistério e a maioria dos respondentes do QE_I70 quer ser professor da rede pública. Pergunta: quais padrões de intenção profissional distinguem a UFPA? Variáveis: QE_I18, QE_I19, QE_I70. Método: frequências válidas e contrastes por curso. Limitação: intenção declarada não equivale a inserção profissional futura.')]
for i, (title, body) in enumerate(items, 1):
    p = add_para(f'{i}. {title} {body}', first=False)
    p.runs[0].bold = False
for t in D.tables:
    tr = t.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement('w:cantSplit')
        trPr.append(cant)
D.save(DOCX)
try:
    from src.relatorios.conversao_pdf import converter_docx_para_pdf
    resultado_pdf = converter_docx_para_pdf(DOCX, OUT)
    if resultado_pdf.gerado:
        print(f'DOCX: {DOCX}')
        print(f'PDF: {resultado_pdf.caminho_pdf}')
    else:
        print(f'DOCX: {DOCX}')
        print(f'PDF não gerado automaticamente: {resultado_pdf.mensagem}')
except Exception as exc:
    print(f'DOCX: {DOCX}')
    print(f'PDF não gerado automaticamente: {exc}')
