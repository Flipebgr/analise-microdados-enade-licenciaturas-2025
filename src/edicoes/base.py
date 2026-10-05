from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class SituacaoConceito(StrEnum):
    COM_CONCEITO = "com_conceito"
    SEM_CONCEITO = "sem_conceito"
    AUSENTE = "ausente"
    NAO_RECONHECIDA = "nao_reconhecida"


@dataclass(frozen=True, slots=True)
class ConceitoNormalizado:
    conceito_numerico: int | None
    situacao: SituacaoConceito
    valor_original: Any


def normalizar_conceito(valor: Any) -> ConceitoNormalizado:
    """Separa a faixa numérica, a situação e o valor recebido da fonte."""

    if valor is None or (isinstance(valor, str) and not valor.strip()):
        return ConceitoNormalizado(None, SituacaoConceito.AUSENTE, valor)

    texto = str(valor).strip().upper()
    if texto in {"<NA>", "NAN", "NAT"}:
        return ConceitoNormalizado(None, SituacaoConceito.AUSENTE, valor)
    if texto in {"SC", "SEM CONCEITO", "-"}:
        return ConceitoNormalizado(None, SituacaoConceito.SEM_CONCEITO, valor)

    try:
        numero = float(texto.replace(",", "."))
    except ValueError:
        return ConceitoNormalizado(None, SituacaoConceito.NAO_RECONHECIDA, valor)

    if numero.is_integer() and 1 <= numero <= 5:
        return ConceitoNormalizado(int(numero), SituacaoConceito.COM_CONCEITO, valor)
    return ConceitoNormalizado(None, SituacaoConceito.NAO_RECONHECIDA, valor)


@dataclass(frozen=True, slots=True)
class CapacidadesEdicao:
    proficiencia: bool
    recomendacao: bool
    questionario_licenciatura: bool


@dataclass(frozen=True, slots=True)
class ConfiguracaoLeitura:
    separador: str
    decimal: str
    quotechar: str
    encodings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SchemaDesempenho:
    geral: str
    objetiva: str | None = None
    discursiva: str | None = None
    formacao_geral: str | None = None
    formacao_geral_objetiva: str | None = None
    formacao_geral_discursiva: str | None = None
    componente_especifico: str | None = None
    componente_especifico_objetiva: str | None = None
    componente_especifico_discursiva: str | None = None
    proficiencia: str | None = None
    acertos: str | None = None
    vetores_string: tuple[str, ...] = ()

    @property
    def mapa_canonico(self) -> dict[str, str]:
        """Liga cada componente disponível à variável oficial da edição."""

        campos = (
            ("geral", self.geral),
            ("objetiva", self.objetiva),
            ("discursiva", self.discursiva),
            ("formacao_geral_total", self.formacao_geral),
            ("formacao_geral_objetiva", self.formacao_geral_objetiva),
            ("formacao_geral_discursiva", self.formacao_geral_discursiva),
            ("componente_especifico_total", self.componente_especifico),
            ("componente_especifico_objetiva", self.componente_especifico_objetiva),
            ("componente_especifico_discursiva", self.componente_especifico_discursiva),
            ("proficiencia", self.proficiencia),
            ("acertos", self.acertos),
        )
        return {canonico: oficial for canonico, oficial in campos if oficial is not None}

    @property
    def variaveis_numericas(self) -> tuple[str, ...]:
        return tuple(self.mapa_canonico.values())


@dataclass(frozen=True, slots=True)
class SchemaPresenca:
    variaveis: tuple[str, ...]
    codigos_tp_pres: tuple[tuple[int, str], ...]


@dataclass(frozen=True, slots=True)
class RegraIndicadorQuestionario:
    nome: str
    item: str
    respostas_positivas: frozenset[str]
    respostas_validas: frozenset[str]
    descricao: str


@dataclass(frozen=True, slots=True)
class SchemaQuestionario:
    itens_gerais: tuple[str, ...]
    itens_processo_formativo: tuple[str, ...]
    itens_licenciatura: tuple[str, ...]
    itens_recomendacao: tuple[str, ...]
    regras_indicadores: tuple[RegraIndicadorQuestionario, ...]
    codigos_validos_processo: frozenset[int]
    codigos_especiais_processo: tuple[tuple[int, str], ...]


@dataclass(frozen=True, slots=True)
class SchemaConceito:
    aba: str
    mapa_colunas: tuple[tuple[str, str], ...]
    colunas_numericas: tuple[str, ...]
    campo_valor_original: str = "CONCEITO_ENADE_ORIGINAL"
    campo_conceito_numerico: str = "CONCEITO_ENADE_NUM"
    campo_situacao: str = "SITUACAO_CONCEITO"

    def coluna_origem(self, campo_normalizado: str) -> str:
        for origem, destino in self.mapa_colunas:
            if destino == campo_normalizado:
                return origem
        raise KeyError(f"Campo normalizado não declarado: {campo_normalizado}")


@dataclass(frozen=True, slots=True)
class SchemaArquivo:
    numero: int
    colunas_obrigatorias: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ContratoEdicao:
    ano: int
    nome: str
    prefixo_arquivos: str
    quantidade_arquivos: int
    leitura: ConfiguracaoLeitura
    arquivos: tuple[SchemaArquivo, ...]
    desempenho: SchemaDesempenho
    presenca: SchemaPresenca
    questionario: SchemaQuestionario
    capacidades: CapacidadesEdicao
    conceito: SchemaConceito
    modalidades: tuple[tuple[int, str], ...]

    def __post_init__(self) -> None:
        numeros = tuple(arquivo.numero for arquivo in self.arquivos)
        esperados = tuple(range(1, self.quantidade_arquivos + 1))
        if numeros != esperados:
            raise ValueError(
                f"Schemas de {self.ano} devem cobrir os arquivos 1 a {self.quantidade_arquivos}"
            )
        if not self.prefixo_arquivos:
            raise ValueError("prefixo_arquivos deve ser informado")

    def nome_arquivo(self, numero: int) -> str:
        if numero < 1 or numero > self.quantidade_arquivos:
            raise ValueError(f"Arquivo fora do inventário da edição {self.ano}: {numero}")
        return f"{self.prefixo_arquivos}{numero}.txt"

    def schema_arquivo(self, numero: int) -> SchemaArquivo:
        if numero < 1 or numero > self.quantidade_arquivos:
            raise ValueError(f"Arquivo fora do inventário da edição {self.ano}: {numero}")
        return self.arquivos[numero - 1]
