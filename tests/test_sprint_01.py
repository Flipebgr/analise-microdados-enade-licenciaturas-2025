from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _base():
    path = ROOT / "dados_processados" / "matematica" / "base_analitica_cursos.csv"
    return pd.read_csv(path, encoding="utf-8-sig")


def test_base_unica_e_area_matematica():
    df = _base()
    assert df["CO_CURSO"].is_unique
    assert set(df["CO_GRUPO"]) == {702}


def test_grupos_exclusivos_e_ufpa():
    df = _base()
    assert set(df["GRUPO_CODIGO"]).issubset(set("ABCDE") | {"SEM_GRUPO"})
    foco = df[df["GRUPO_CODIGO"] == "A"]
    assert len(foco) == 7
    assert foco["CO_IES"].eq(569).all()
    assert foco["CONCEITO_ENADE_NUM"].eq(1).all()


def test_percentuais_no_dominio():
    df = _base()
    cols = [c for c in df.columns if c.endswith("_pct") or c.startswith("taxa_")]
    for c in cols:
        s = pd.to_numeric(df[c], errors="coerce").dropna()
        assert s.between(0, 1).all(), c


def test_figuras_geradas():
    figs = list((ROOT / "figuras" / "matematica").glob("*.png"))
    assert len(figs) >= 7
