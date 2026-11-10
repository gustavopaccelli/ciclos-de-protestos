"""Gera produtos/e1-triangulacao/index.html a partir dos resultados da E1.

Rode a partir da raiz, depois de src/analysis/e1_cruzamento_series.py:
    python produtos/e1-triangulacao/gera.py
Edite modelo.html, não index.html (que é sobrescrito).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import paths  # noqa: E402

AQUI = Path(__file__).resolve().parent
DADOS = paths.TRIANGULACAO / "e1_cruzamento_mm_nepac" / "dados" / "painel_dados.json"

dados = json.loads(DADOS.read_text(encoding="utf-8"))
assert len(dados["fases"]) == 48, "esperava 24 fases × 2 fontes"
assert dados["meta"]["fontes"]["NEPAC"]["n_eventos"] == 1284 and dados["meta"]["fontes"]["MM"]["n_eventos"] == 224
html = (AQUI / "modelo.html").read_text(encoding="utf-8")
assert "/*DADOS*/null" in html
html = html.replace("/*DADOS*/null", json.dumps(dados, ensure_ascii=False))
(AQUI / "index.html").write_text(html, encoding="utf-8")
print(f"index.html gerado (dados de {dados['meta']['gerado_em']})")
