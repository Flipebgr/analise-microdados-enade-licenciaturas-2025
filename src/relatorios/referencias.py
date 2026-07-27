from __future__ import annotations

REFERENCIAS = [
    "BRASIL. Lei nº 10.861, de 14 de abril de 2004. Institui o Sistema Nacional de Avaliação da Educação Superior - SINAES. Brasília, DF: Presidência da República, 2004.",
    "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Enade das Licenciaturas: microdados 2025. Brasília, DF: Inep, 2026.",
    "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Manual do usuário: Enade das Licenciaturas 2025. Brasília, DF: Inep, 2026.",
    "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Nota Técnica nº 8/2026/CEI/CGGI/DAES-INEP: metodologia do Conceito Enade para os cursos de licenciatura a partir da edição de 2025. Brasília, DF: Inep, 2026.",
    "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Questionário do Estudante - Enade das Licenciaturas 2025. Brasília, DF: Inep, 2025.",
    "INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Normas de apresentação tabular. 3. ed. Rio de Janeiro: IBGE, 1993.",
    "COHEN, J. Statistical power analysis for the behavioral sciences. 2. ed. Hillsdale: Lawrence Erlbaum Associates, 1988.",
    "CLIFF, N. Ordinal methods for behavioral data analysis. Mahwah: Lawrence Erlbaum Associates, 1996.",
]


def adicionar_referencias(doc) -> None:
    for ref in sorted(REFERENCIAS):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = 0
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = 12
        p.add_run(ref)
