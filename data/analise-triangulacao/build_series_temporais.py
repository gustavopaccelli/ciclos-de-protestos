#!/usr/bin/env python3
"""Gera series_temporais_eventos.csv — contagem mensal de eventos por fonte.

Fontes (mantidas independentes, uma linha por fonte × mês; nunca somadas):
  - NEPAC/UNICAMP (2011-2016): data de início do protesto
  - Mass Mobilization v16 (1990-2020): startyear/startmonth
  - Seeds Diretas Já (1983-1984) e Fora Collor (1992): coluna date

Saída deliberadamente SEM as fases do cycle_phases — a comparação com a
periodização é etapa analítica posterior (decisão do usuário, 2026-07-17).
"""
import csv
import os
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # data/
OUT = os.path.join(BASE, "analise-triangulacao", "series_temporais_eventos.csv")

series = []  # (fonte, ano_mes) -> contagem


def add(counter, fonte):
    for ym, n in sorted(counter.items()):
        series.append({"fonte": fonte, "ano_mes": ym, "n_eventos": n})


# --- NEPAC (deduplicado por Codigo_evento: 2.548 registros -> ~1.284 eventos) ---
c = Counter()
descartados_nepac = 0
vistos = set()
with open(os.path.join(BASE, "bancos-externos/nepac-tatagiba-galvao-2019/dados/protestos_2011-2016.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cod = (row.get("Codigo_evento") or "").strip()
        d = (row.get("Data_de_Inicio_do_protesto") or "").strip()
        if cod:
            if cod in vistos:
                continue
            vistos.add(cod)
        if len(d) >= 7 and d[:4].isdigit():
            c[d[:7]] += 1
        else:
            descartados_nepac += 1
add(c, "NEPAC")

# --- Mass Mobilization ---
c = Counter()
descartados_mm = 0
with open(os.path.join(BASE, "bancos-externos/mass-mobilization-clark-regan-2020/dados/protestos_brasil_1990-2020.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("protest") != "1":
            continue  # linhas país-ano sem protesto
        y, m = (row.get("startyear") or "").strip(), (row.get("startmonth") or "").strip()
        if y.isdigit() and m.isdigit():
            c[f"{int(y):04d}-{int(m):02d}"] += 1
        else:
            descartados_mm += 1
add(c, "MassMobilization")

# --- Seeds ---
for path, fonte in [
    ("protest_events_seeds/protest_events_diretas_ja_seed.csv", "Seed_DiretasJa"),
    ("protest_events_seeds/protest_events_fora_collor_seed.csv", "Seed_ForaCollor"),
]:
    c = Counter()
    with open(os.path.join(BASE, path), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = (row.get("date") or "").strip()
            if len(d) >= 7 and d[:4].isdigit():
                c[d[:7]] += 1
    add(c, fonte)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["fonte", "ano_mes", "n_eventos"])
    w.writeheader()
    w.writerows(series)

print(f"OK: {OUT}")
for fonte in ("NEPAC", "MassMobilization", "Seed_DiretasJa", "Seed_ForaCollor"):
    rows = [r for r in series if r["fonte"] == fonte]
    total = sum(r["n_eventos"] for r in rows)
    print(f"  {fonte}: {total} eventos em {len(rows)} meses ({rows[0]['ano_mes']} a {rows[-1]['ano_mes']})" if rows else f"  {fonte}: vazio")
print(f"  descartados sem data valida: NEPAC={descartados_nepac}, MM={descartados_mm}")
