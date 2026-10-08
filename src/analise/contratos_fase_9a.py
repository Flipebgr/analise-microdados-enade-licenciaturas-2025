"""Contratos compartilhados da Fase 9A.

Este módulo declara políticas e estados sem depender de uma edição específica.
Os cálculos que consomem esses contratos ficam em módulos analíticos próprios.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Final


class EstadoElegibilidade(StrEnum):
    INSUFICIENTE_COBERTURA = "insuficiente_cobertura"
    BAIXO_N = "baixo_n"
    ELEGIVEL = "elegivel"


class StatusAnalise(StrEnum):
    DISPONIVEL = "disponivel"
    DESCRITIVO_APENAS = "descritivo_apenas"
    INSUFICIENTE = "insuficiente"
    NAO_APLICAVEL = "nao_aplicavel"


class TipoEstimando(StrEnum):
    CURSO_TIPICO = "curso_tipico"
    PARTICIPANTE_TIPICO = "participante_respondente_tipico"


class Territorio(StrEnum):
    PARA = "para"
    NORTE = "norte"
    BRASIL = "brasil"


class CriterioBenchmark(StrEnum):
    MODALIDADE_CATEGORIA_ORGANIZACAO_PORTE_75_125 = "modalidade_categoria_organizacao_porte_75_125"
    MODALIDADE_CATEGORIA_ORGANIZACAO_PORTE_50_200 = "modalidade_categoria_organizacao_porte_50_200"
    MODALIDADE_CATEGORIA_PORTE_50_200 = "modalidade_categoria_porte_50_200"
    MODALIDADE_PORTE_50_200 = "modalidade_porte_50_200"


POLITICA_N_V1: Final = "fase_9a_n_v1"
SEED_BASE_BOOTSTRAP: Final = 20250901
NUMERO_REAMOSTRAGENS: Final = 5_000
N_MINIMO_INFERENCIA: Final = 10
N_MINIMO_DESCRITIVO: Final = 5
N_MINIMO_CORRELACAO: Final = 20


@dataclass(frozen=True, slots=True)
class PoliticaElegibilidade:
    """Limiares operacionais versionados para elegibilidade por indicador."""

    versao: str = POLITICA_N_V1
    cobertura_minima: float = 0.5
    n_minimo: int = N_MINIMO_INFERENCIA

    def __post_init__(self) -> None:
        if not self.versao.strip():
            raise ValueError("A versão da política de elegibilidade deve ser informada")
        if not 0 < self.cobertura_minima <= 1:
            raise ValueError("cobertura_minima deve estar no intervalo (0, 1]")
        if self.n_minimo < 1:
            raise ValueError("n_minimo deve ser positivo")


@dataclass(frozen=True, slots=True)
class PoliticaTamanhoBenchmark:
    """Interpretação operacional do número de cursos em um benchmark."""

    versao: str = POLITICA_N_V1
    n_minimo_completo: int = N_MINIMO_INFERENCIA
    n_minimo_sintese: int = N_MINIMO_DESCRITIVO

    def __post_init__(self) -> None:
        if not self.versao.strip():
            raise ValueError("A versão da política de tamanho deve ser informada")
        if self.n_minimo_sintese < 1:
            raise ValueError("n_minimo_sintese deve ser positivo")
        if self.n_minimo_completo < self.n_minimo_sintese:
            raise ValueError("n_minimo_completo não pode ser inferior a n_minimo_sintese")


@dataclass(frozen=True, slots=True)
class NivelRelaxamentoBenchmark:
    """Um degrau da cascata determinística de comparabilidade."""

    ordem: int
    criterio: CriterioBenchmark
    limite_inferior_porte: float
    limite_superior_porte: float
    exige_categoria: bool
    exige_organizacao: bool

    def __post_init__(self) -> None:
        if self.ordem < 1:
            raise ValueError("ordem deve ser positiva")
        if self.limite_inferior_porte <= 0:
            raise ValueError("limite inferior de porte deve ser positivo")
        if self.limite_superior_porte < self.limite_inferior_porte:
            raise ValueError("limite superior de porte deve ser >= ao limite inferior")


NIVEIS_RELAXAMENTO_BENCHMARK: Final[tuple[NivelRelaxamentoBenchmark, ...]] = (
    NivelRelaxamentoBenchmark(
        ordem=1,
        criterio=CriterioBenchmark.MODALIDADE_CATEGORIA_ORGANIZACAO_PORTE_75_125,
        limite_inferior_porte=0.75,
        limite_superior_porte=1.25,
        exige_categoria=True,
        exige_organizacao=True,
    ),
    NivelRelaxamentoBenchmark(
        ordem=2,
        criterio=CriterioBenchmark.MODALIDADE_CATEGORIA_ORGANIZACAO_PORTE_50_200,
        limite_inferior_porte=0.5,
        limite_superior_porte=2.0,
        exige_categoria=True,
        exige_organizacao=True,
    ),
    NivelRelaxamentoBenchmark(
        ordem=3,
        criterio=CriterioBenchmark.MODALIDADE_CATEGORIA_PORTE_50_200,
        limite_inferior_porte=0.5,
        limite_superior_porte=2.0,
        exige_categoria=True,
        exige_organizacao=False,
    ),
    NivelRelaxamentoBenchmark(
        ordem=4,
        criterio=CriterioBenchmark.MODALIDADE_PORTE_50_200,
        limite_inferior_porte=0.5,
        limite_superior_porte=2.0,
        exige_categoria=False,
        exige_organizacao=False,
    ),
)


@dataclass(frozen=True, slots=True)
class ElegibilidadeIndicador:
    """Denominadores e estado de inclusão de um curso em um indicador."""

    n_total: int
    n_valido: int
    cobertura_valida: float | None
    estado: EstadoElegibilidade
    motivo: str | None = None

    def __post_init__(self) -> None:
        if self.n_total < 0 or self.n_valido < 0:
            raise ValueError("n_total e n_valido devem ser não negativos")
        if self.n_valido > self.n_total:
            raise ValueError("n_valido não pode exceder n_total")
        if self.cobertura_valida is not None and not 0 <= self.cobertura_valida <= 1:
            raise ValueError("cobertura_valida deve estar no intervalo [0, 1]")
        if self.estado == EstadoElegibilidade.INSUFICIENTE_COBERTURA and not self.motivo:
            raise ValueError("insuficiente_cobertura exige motivo explícito")
        if self.estado == EstadoElegibilidade.BAIXO_N and self.motivo != "n_valido_abaixo_do_minimo":
            raise ValueError("baixo_n exige o motivo n_valido_abaixo_do_minimo")
        if self.estado == EstadoElegibilidade.ELEGIVEL and self.motivo:
            raise ValueError("elegivel não deve declarar motivo de exclusão")


def classificar_elegibilidade(
    n_total: int,
    n_valido: int,
    politica: PoliticaElegibilidade = PoliticaElegibilidade(),
) -> ElegibilidadeIndicador:
    """Classifica cobertura antes do N conforme a política operacional aprovada."""

    if n_total < 0 or n_valido < 0 or n_valido > n_total:
        raise ValueError("Denominadores inválidos para elegibilidade")
    cobertura = n_valido / n_total if n_total else None
    if cobertura is None or cobertura < politica.cobertura_minima:
        return ElegibilidadeIndicador(
            n_total,
            n_valido,
            cobertura,
            EstadoElegibilidade.INSUFICIENTE_COBERTURA,
            "denominador_zero" if cobertura is None else "cobertura_abaixo_do_minimo",
        )
    if n_valido < politica.n_minimo:
        return ElegibilidadeIndicador(
            n_total,
            n_valido,
            cobertura,
            EstadoElegibilidade.BAIXO_N,
            "n_valido_abaixo_do_minimo",
        )
    return ElegibilidadeIndicador(n_total, n_valido, cobertura, EstadoElegibilidade.ELEGIVEL)


@dataclass(frozen=True, slots=True)
class ConfiguracaoBootstrap:
    """Configuração reproduzível da incerteza ecológica."""

    nivel_confianca: float = 0.95
    numero_reamostragens: int = NUMERO_REAMOSTRAGENS
    seed_base: int = SEED_BASE_BOOTSTRAP
    unidade_reamostragem: str = "CO_CURSO"
    tipo_incerteza: str = "ecologica"

    def __post_init__(self) -> None:
        if not 0 < self.nivel_confianca < 1:
            raise ValueError("nivel_confianca deve estar no intervalo (0, 1)")
        if self.numero_reamostragens < 1:
            raise ValueError("numero_reamostragens deve ser positivo")
        if self.seed_base < 0:
            raise ValueError("seed_base deve ser não negativa")
        if self.unidade_reamostragem != "CO_CURSO":
            raise ValueError("A unidade de reamostragem da Fase 9A é CO_CURSO")


def seed_para_contraste(identificador: str, configuracao: ConfiguracaoBootstrap = ConfiguracaoBootstrap()) -> int:
    """Deriva seed estável sem depender do hash aleatório do processo Python."""

    if not identificador.strip():
        raise ValueError("identificador do contraste deve ser informado")
    digest = sha256(identificador.encode("utf-8")).digest()
    deslocamento = int.from_bytes(digest[:4], byteorder="big", signed=False)
    return (configuracao.seed_base + deslocamento) % (2**32)
