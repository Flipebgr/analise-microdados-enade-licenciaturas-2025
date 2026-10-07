from __future__ import annotations

from dataclasses import dataclass

from src.edicoes.base import ContratoEdicao


@dataclass(frozen=True, slots=True)
class AplicabilidadeArea:
    """Recursos da edição que fazem sentido para uma área e grau específicos."""

    proficiencia: bool = False
    recomendacao: bool = False
    questionario_licenciatura: bool = False
    processo_formativo: bool = True


@dataclass(frozen=True, slots=True)
class ConfiguracaoArea:
    """Identifica uma área dentro de uma edição específica do Enade."""

    slug: str
    nome: str
    co_grupo: int
    co_ies_focal: int = 569
    edicao: int = 2025
    grau: str = "Licenciatura"
    aplicabilidade: AplicabilidadeArea = AplicabilidadeArea()

    def __post_init__(self) -> None:
        slug = self.slug.strip()
        nome = self.nome.strip()
        if not slug:
            raise ValueError("slug deve ser informado")
        if not nome:
            raise ValueError("nome deve ser informado")
        if (
            not isinstance(self.co_grupo, int)
            or isinstance(self.co_grupo, bool)
            or self.co_grupo <= 0
        ):
            raise ValueError("co_grupo deve ser um inteiro positivo")
        if (
            not isinstance(self.co_ies_focal, int)
            or isinstance(self.co_ies_focal, bool)
            or self.co_ies_focal <= 0
        ):
            raise ValueError("co_ies_focal deve ser um inteiro positivo")
        if not isinstance(self.edicao, int) or isinstance(self.edicao, bool) or self.edicao <= 0:
            raise ValueError("edicao deve ser um inteiro positivo")
        grau = self.grau.strip()
        if not grau:
            raise ValueError("grau deve ser informado")
        object.__setattr__(self, "slug", slug)
        object.__setattr__(self, "nome", nome)
        object.__setattr__(self, "grau", grau)


APLICABILIDADE_LICENCIATURAS_2025 = AplicabilidadeArea(
    proficiencia=True,
    recomendacao=True,
)

MATEMATICA = ConfiguracaoArea(
    "matematica", "Matemática", 702, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
PORTUGUES = ConfiguracaoArea(
    "portugues", "Letras–Português", 904, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
FISICA = ConfiguracaoArea(
    "fisica", "Física", 1402, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
QUIMICA = ConfiguracaoArea(
    "quimica", "Química", 1502, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
BIOLOGIA = ConfiguracaoArea(
    "biologia", "Ciências Biológicas", 1602, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
PEDAGOGIA = ConfiguracaoArea(
    "pedagogia", "Pedagogia", 2001, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
GEOGRAFIA = ConfiguracaoArea(
    "geografia", "Geografia", 3002, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
EDUCACAO_FISICA = ConfiguracaoArea(
    "educacao_fisica",
    "Educação Física",
    3502,
    edicao=2025,
    aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025,
)
MUSICA = ConfiguracaoArea(
    "musica", "Música", 4301, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
INGLES = ConfiguracaoArea(
    "ingles", "Letras–Inglês", 6407, edicao=2025, aplicabilidade=APLICABILIDADE_LICENCIATURAS_2025
)
BIOLOGIA_BACHARELADO_2017 = ConfiguracaoArea(
    "biologia_bacharelado",
    "Ciências Biológicas — Bacharelado",
    1601,
    edicao=2017,
    grau="Bacharelado",
    aplicabilidade=AplicabilidadeArea(
        proficiencia=False,
        recomendacao=False,
        questionario_licenciatura=False,
    ),
)

_AREAS_2025 = (
    MATEMATICA,
    PORTUGUES,
    FISICA,
    QUIMICA,
    BIOLOGIA,
    PEDAGOGIA,
    GEOGRAFIA,
    EDUCACAO_FISICA,
    MUSICA,
    INGLES,
)

# Registro legado preservado para consumidores de 2025.
AREAS: dict[str, ConfiguracaoArea] = {area.slug: area for area in _AREAS_2025}

AREAS_POR_EDICAO: dict[tuple[int, str], ConfiguracaoArea] = {
    (area.edicao, area.slug): area
    for area in (*_AREAS_2025, BIOLOGIA_BACHARELADO_2017)
}


def obter_area(edicao: int, slug: str) -> ConfiguracaoArea:
    """Resolve uma área pela edição e pelo slug, sem equivalência entre anos."""

    chave = slug.strip().lower()
    try:
        return AREAS_POR_EDICAO[(edicao, chave)]
    except KeyError as exc:
        disponiveis = ", ".join(
            slug_area for ano, slug_area in sorted(AREAS_POR_EDICAO) if ano == edicao
        )
        if not disponiveis:
            disponiveis = "nenhuma"
        raise KeyError(
            f"Área desconhecida na edição {edicao}: {slug!r}. Disponíveis: {disponiveis}"
        ) from exc


def validar_compatibilidade_area(edicao: ContratoEdicao, area: ConfiguracaoArea) -> None:
    if edicao.ano != area.edicao:
        raise ValueError(
            f"Área {area.slug!r} pertence a {area.edicao}, não à edição {edicao.ano}"
        )

    solicitadas = area.aplicabilidade
    disponiveis = edicao.capacidades
    incompatibilidades = [
        nome
        for nome in ("proficiencia", "recomendacao", "questionario_licenciatura", "processo_formativo")
        if getattr(solicitadas, nome) and not getattr(disponiveis, nome)
    ]
    if incompatibilidades:
        raise ValueError(
            f"Recursos não suportados por {edicao.ano}: {', '.join(incompatibilidades)}"
        )
