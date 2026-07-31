from pathlib import Path
import pandas as pd

from src.fisica.associacoes_ecologicas import calcular_associacoes
from src.fisica.validar_desempenho import auditar_desempenho
from src.fisica.validar_presenca import auditar_presenca
from src.fisica.validar_resultados_fisica import validar_resultados

ROOT = Path(__file__).resolve().parents[2]
PASTA = ROOT / "dados_processados" / "fisica"


def carregar_base() -> pd.DataFrame:
    return pd.read_csv(PASTA / "base_analitica_cursos.csv")


def test_presenca_ufpa_valida() -> None:
    presenca = auditar_presenca(carregar_base())
    assert len(presenca) == 5
    assert presenca["taxa_presenca_pct"].between(0, 100).all()
    assert presenca["ROTULO_OFERTA"].nunique() == 5


def test_desempenho_contem_tres_componentes() -> None:
    auditoria = auditar_desempenho(carregar_base())
    assert set(auditoria["indicador"]) == {"NT_GER", "NT_OBJ", "NT_DIS"}
    assert len(auditoria) == 15


def test_associacoes_sao_ecologicas_e_tem_n() -> None:
    associacoes = calcular_associacoes(carregar_base())
    assert not associacoes.empty
    assert (associacoes["n_cursos"] > 0).all()
    assert associacoes["interpretacao"].str.contains("ecológica").all()


def test_produtos_sprint_05_existentes() -> None:
    esperados = [
        PASTA / "auditoria_presenca_validada.csv",
        PASTA / "auditoria_desempenho.csv",
        PASTA / "comparacao_territorial_validada.csv",
        PASTA / "sensibilidade_benchmarks.csv",
        PASTA / "diagnostico_dificuldade.csv",
        PASTA / "diagnostico_dimensoes_processo.csv",
        PASTA / "auditoria_indicadores_socioeconomicos.csv",
        PASTA / "associacoes_ecologicas.csv",
        ROOT / "relatorios" / "sprint_05_validacao_fisica.md",
    ]
    assert all(path.exists() and path.stat().st_size > 0 for path in esperados)


def test_validacao_integrada() -> None:
    base = carregar_base()
    presenca = pd.read_csv(PASTA / "auditoria_presenca_validada.csv")
    desempenho = pd.read_csv(PASTA / "auditoria_desempenho.csv")
    sensibilidade = pd.read_csv(PASTA / "sensibilidade_benchmarks.csv")
    figuras = [
        ROOT / "figuras" / "fisica" / "validada_02_taxa_presenca.png",
        ROOT / "figuras" / "fisica" / "validada_03_nt_ger_ofertas.png",
        ROOT / "figuras" / "fisica" / "validada_07_conceito_dificuldade.png",
        ROOT / "figuras" / "fisica" / "validada_13_sintese_socioeconomica.png",
    ]
    validar_resultados(base, presenca, desempenho, sensibilidade, figuras)
