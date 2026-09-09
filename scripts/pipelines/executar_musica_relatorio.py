from __future__ import annotations

# ruff: noqa: E402

from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    figuras = PROJECT_ROOT / "figuras" / "musica"
    obrigatorias = [
        "01_painel_oferta_ufpa.png",
        "02_posicao_relativa_nt_ger.png",
        "03a_distribuicao_nt_ger.png",
        "03b_distribuicao_nt_obj.png",
        "03c_distribuicao_nt_dis.png",
        "04_perfil_socioeconomico.png",
        "05_processo_formativo_dimensoes.png",
        "06_benchmark_sensibilidade.png",
        "07_recomendacao.png",
        "08_associacao_ecologica.png",
        "09_sintese_ufpa.png",
    ]
    ausentes = [nome for nome in obrigatorias if not (figuras / nome).exists()]
    if ausentes:
        print(
            "ERRO: figuras da validação ausentes. Execute primeiro: "
            "python executar.py musica validacao",
            file=sys.stderr,
        )
        return 2

    resultado = subprocess.run(
        [sys.executable, "-m", "src.relatorios.gerar_relatorio_musica"],
        cwd=PROJECT_ROOT,
        check=False,
    )
    if resultado.returncode != 0:
        return resultado.returncode

    docx = PROJECT_ROOT / "relatorios" / "musica" / "relatorio_musica_enade_2025_ufpa.docx"
    if not docx.exists() or docx.stat().st_size == 0:
        print("ERRO: DOCX final não foi gerado.", file=sys.stderr)
        return 1

    print("Relatório de Música concluído.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
