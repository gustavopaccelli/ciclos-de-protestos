"""Gera produtos/mapa-fases/index.html a partir do cycle_phases.csv e do codebook.

Rode a partir da raiz: python produtos/mapa-fases/gera.py
Edite modelo.html, não index.html (que é sobrescrito).
"""
import csv
import json
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import paths  # noqa: E402

AQUI = Path(__file__).resolve().parent
CSV = paths.PROCESSED / "cycle_phases" / "cycle_phases.csv"
CODEBOOK = paths.DOCS / "codebook" / "cycle_phases_codebook.yaml"

ESCALA = {0: "ausente/nulo", 1: "baixo/incipiente", 2: "moderado/presente", 3: "alto/determinante"}
ROTULOS = {
    "op_abertura_institucional": "Abertura institucional",
    "op_divisao_elites": "Divisão das elites",
    "op_aliados_influentes": "Aliados influentes",
    "op_crise_legitimidade": "Crise de legitimidade",
    "op_repressao": "Repressão",
    "od_visibilidade_midia": "Visibilidade midiática",
    "od_ressonancia_discursiva": "Ressonância discursiva",
    "od_legitimidade_narrativa": "Legitimidade narrativa",
    "traducao_institucional": "Tradução institucional",
}

cb = yaml.safe_load(CODEBOOK.read_text(encoding="utf-8"))
blocos = cb["blocos"]
trad = blocos["traducao_institucional"]

variaveis = []
for bloco, chave in (("EOP", "oportunidades_politicas"), ("DOS", "oportunidades_discursivas")):
    for nome, d in blocos[chave].items():
        variaveis.append({"id": nome, "bloco": bloco, "rotulo": ROTULOS[nome],
                          "descricao": d["descricao"], "fundamento": d["fundamento"],
                          "escala": {str(k): v for k, v in ESCALA.items()}})
ti = trad["traducao_institucional"]
variaveis.append({"id": "traducao_institucional", "bloco": "Tradução", "rotulo": ROTULOS["traducao_institucional"],
                  "descricao": ti["descricao"], "fundamento": ti["fundamento"],
                  "escala": {str(k): v for k, v in ti["escala"].items()}})

categorias = {k: {str(c): str(v).strip() for c, v in trad[k]["valores"].items()}
              for k in ("traducao_direcao", "traducao_valencia", "traducao_controle_gatilho")}

with CSV.open(encoding="utf-8") as f:
    fases = list(csv.DictReader(f))
assert len(fases) == 24, f"esperava 24 fases, li {len(fases)}"
for v in variaveis:
    for fase in fases:
        assert fase[v["id"]] in {"0", "1", "2", "3", "NA"}, (fase["phase_id"], v["id"], fase[v["id"]])

dados = {
    "ciclos": {c["id"]: {"nome": c["nome"], "periodo": c["periodo"]} for c in cb["ciclos"]},
    "variaveis": variaveis,
    "categorias": categorias,
    "fases": fases,
    "gerado_em": date.today().isoformat(),
}
html = (AQUI / "modelo.html").read_text(encoding="utf-8")
assert "/*DADOS*/null" in html
html = html.replace("/*DADOS*/null", json.dumps(dados, ensure_ascii=False))
(AQUI / "index.html").write_text(html, encoding="utf-8")
print(f"index.html gerado: {len(fases)} fases, {len(variaveis)} variáveis ordinais")
