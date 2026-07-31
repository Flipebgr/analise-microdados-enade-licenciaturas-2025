from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConfiguracaoArea:
    """Parâmetros estáveis que identificam uma área do Enade."""

    slug: str
    nome: str
    co_grupo: int
    co_ies_focal: int = 569

    def __post_init__(self) -> None:
        slug = self.slug.strip()
        nome = self.nome.strip()
        if not slug:
            raise ValueError("slug deve ser informado")
        if not nome:
            raise ValueError("nome deve ser informado")
        if not isinstance(self.co_grupo, int) or isinstance(self.co_grupo, bool) or self.co_grupo <= 0:
            raise ValueError("co_grupo deve ser um inteiro positivo")
        if (
            not isinstance(self.co_ies_focal, int)
            or isinstance(self.co_ies_focal, bool)
            or self.co_ies_focal <= 0
        ):
            raise ValueError("co_ies_focal deve ser um inteiro positivo")
        object.__setattr__(self, "slug", slug)
        object.__setattr__(self, "nome", nome)


MATEMATICA = ConfiguracaoArea("matematica", "Matemática", 702)
PORTUGUES = ConfiguracaoArea("portugues", "Letras–Português", 904)
FISICA = ConfiguracaoArea("fisica", "Física", 1402)
QUIMICA = ConfiguracaoArea("quimica", "Química", 1502)
INGLES = ConfiguracaoArea("ingles", "Letras–Inglês", 6407)

AREAS: dict[str, ConfiguracaoArea] = {
    area.slug: area
    for area in (MATEMATICA, PORTUGUES, FISICA, QUIMICA, INGLES)
}


def obter_area(slug: str) -> ConfiguracaoArea:
    """Retorna uma configuração conhecida pelo slug normalizado."""

    chave = slug.strip().lower()
    try:
        return AREAS[chave]
    except KeyError as exc:
        disponiveis = ", ".join(sorted(AREAS))
        raise KeyError(f"Área desconhecida: {slug!r}. Disponíveis: {disponiveis}") from exc
