from pathlib import Path

from src.relatorios.gerar_relatorio_regional_fisica import (
    carregar_base,
    construir_contrastes,
    construir_ofertas_ufpa,
    construir_resumos,
    construir_sensibilidade,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "dados_processados" / "fisica" / "base_analitica_cursos.csv"


def test_base_regional_uma_linha_por_curso():
    df = carregar_base(BASE)
    assert not df["CO_CURSO"].duplicated().any()
    assert set(df["REGIAO"].dropna().unique()) == {"Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"}


def test_resumos_incluem_referencias_exclusivas():
    df = carregar_base(BASE)
    resumos = construir_resumos(df)
    assert {"UFPA", "Norte sem UFPA", "Brasil geral", "Brasil sem UFPA", "Brasil sem Norte"}.issubset(set(resumos["grupo"]))
    assert (resumos["n_cursos"] >= 0).all()
    assert (resumos["n_participantes"] >= 0).all()


def test_ofertas_ufpa_e_tucurui_ausente():
    df = carregar_base(BASE)
    resumos = construir_resumos(df)
    ofertas = construir_ofertas_ufpa(df, resumos)
    assert len(ofertas) == 5
    assert 1627581 not in set(ofertas["CO_CURSO"])
    assert ofertas["nt_ger_count"].gt(0).all()


def test_contrastes_exclusivos():
    df = carregar_base(BASE)
    contrastes = construir_contrastes(construir_resumos(df))
    par = set(zip(contrastes["referencia"], contrastes["comparador"], strict=False))
    assert ("UFPA", "Norte sem UFPA") in par
    assert ("UFPA", "Brasil sem UFPA") in par
    assert ("Norte", "Brasil sem Norte") in par


def test_sensibilidade_tem_recortes():
    df = carregar_base(BASE)
    sens = construir_sensibilidade(df)
    assert {"Todos", "Presencial", "N válido >= 10", "N válido >= 20"}.issubset(set(sens["recorte"]))
    assert {"UFPA", "Norte sem UFPA", "Brasil sem UFPA"}.issubset(set(sens["grupo"]))
