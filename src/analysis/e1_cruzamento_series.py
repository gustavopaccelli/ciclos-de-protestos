#!/usr/bin/env python3
"""E1 — cruza as séries de eventos do Mass Mobilization e do NEPAC com as fases dos ciclos.

Reconstrução (2026-10-13) do script perdido do PR #12: os arquivos originais ficaram
fora do git por causa do .gitignore. As decisões de método seguem o research-log
(2026-10-07); o que o log não fixava está marcado como "default" no relatório.

As duas fontes nunca são somadas: cada cálculo é feito por fonte.

Uso (a partir da raiz): python src/analysis/e1_cruzamento_series.py
Saída: data/triangulacao/e1_cruzamento_mm_nepac/dados/
"""
import csv
import itertools
import json
import math
import random
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from atribui_ciclo import ciclo_e_fase  # noqa: E402

SAIDA = paths.TRIANGULACAO / "e1_cruzamento_mm_nepac" / "dados"
CYCLE_PHASES = paths.PROCESSED / "cycle_phases" / "cycle_phases.csv"
COBERTURA_MIN = 0.5
N_PERM = 10_000
SEMENTE = 20261007
ALFA = 0.05
# Números registrados no research-log em 2026-10-07, para conferência (não são alvo).
LOG_ORIGINAL = {
    "razao_dentro_fora_MM": 3.2, "razao_dentro_fora_NEPAC": 1.5,
    "rho_mensal": 0.37, "p_mensal": 0.003,
    "rho_repressao_NEPAC": 0.94, "q_repressao_NEPAC": 0.001,
}


# ---------- estatística (só stdlib) ----------
def poisson_cdf(k, lam):
    if k < 0:
        return 0.0
    if lam == 0:
        return 1.0
    return min(1.0, sum(math.exp(i * math.log(lam) - lam - math.lgamma(i + 1)) for i in range(k + 1)))


def _bissecta(f, alvo, lo, hi):
    """f decrescente em lam; acha lam com f(lam) = alvo."""
    for _ in range(200):
        meio = (lo + hi) / 2
        if f(meio) > alvo:
            lo = meio
        else:
            hi = meio
    return (lo + hi) / 2


def ic_poisson(k, alfa=ALFA):
    """IC exato (Garwood 1936) para a média de uma contagem de Poisson k."""
    teto = k + 20 * math.sqrt(k + 1) + 20
    sup = _bissecta(lambda lam: poisson_cdf(k, lam), alfa / 2, 0.0, teto)
    inf = 0.0 if k == 0 else _bissecta(lambda lam: poisson_cdf(k - 1, lam), 1 - alfa / 2, 0.0, teto)
    return inf, sup


def postos(x):
    ordem = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[ordem[j + 1]] == x[ordem[i]]:
            j += 1
        for t in range(i, j + 1):
            r[ordem[t]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = postos(x), postos(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    if sxx == 0 or syy == 0:
        return None  # variável constante: correlação indefinida
    return sxy / math.sqrt(sxx * syy)


def p_permutacao(x, y, rng, n=N_PERM):
    rho = spearman(x, y)
    if rho is None:
        return None, None
    y2, extremos = list(y), 0
    for _ in range(n):
        rng.shuffle(y2)
        r = spearman(x, y2)
        if r is not None and abs(r) >= abs(rho) - 1e-12:
            extremos += 1
    return rho, (extremos + 1) / (n + 1)


def p_exato(x, y):
    rho = spearman(x, y)
    if rho is None:
        return None, None
    perms = list(itertools.permutations(y))
    extremos = sum(1 for p in perms if (r := spearman(x, list(p))) is not None and abs(r) >= abs(rho) - 1e-12)
    return rho, extremos / len(perms)


def benjamini_hochberg(ps):
    """q-valores de BH (1995); None passa direto."""
    validos = sorted((p, i) for i, p in enumerate(ps) if p is not None)
    m, q, minimo = len(validos), [None] * len(ps), 1.0
    for pos in range(m - 1, -1, -1):
        p, i = validos[pos]
        minimo = min(minimo, p * m / (pos + 1))
        q[i] = minimo
    return q


def _autoteste():
    assert spearman([1, 2, 3, 4], [10, 20, 30, 40]) == 1.0
    assert abs(spearman([1, 2, 3, 4], [4, 3, 2, 1]) + 1) < 1e-12
    assert spearman([1, 1, 1], [1, 2, 3]) is None
    assert abs(ic_poisson(0)[1] - 3.6889) < 1e-3          # Garwood, k = 0
    lo, hi = ic_poisson(10)
    assert abs(lo - 4.7954) < 1e-3 and abs(hi - 18.3904) < 1e-3
    q = benjamini_hochberg([0.01, 0.04, 0.03, 0.005])
    assert [round(v, 4) for v in q] == [0.02, 0.04, 0.04, 0.02]


# ---------- dados ----------
def carrega_mm():
    ev = []
    with open(paths.MM / "dados" / "protestos_brasil_1990-2020.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["protest"] != "1":
                continue  # linha país-ano sem protesto
            ev.append((r["id"], date(int(r["startyear"]), int(r["startmonth"]), int(r["startday"]))))
    return ev


def carrega_nepac():
    """Um evento por Codigo_evento, datado pelo início mais antigo entre suas linhas-cidade."""
    datas = {}
    with open(paths.NEPAC / "dados" / "protestos_2011-2016.csv", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f)):
            cod = r["Codigo_evento"].strip() or f"sem_codigo_{i}"
            d = r["Data_de_Inicio_do_protesto"].strip()
            if d:
                d = date.fromisoformat(d[:10])
                datas[cod] = min(d, datas.get(cod, d))
    return sorted(datas.items(), key=lambda t: t[1])


def main():
    _autoteste()
    rng = random.Random(SEMENTE)
    SAIDA.mkdir(parents=True, exist_ok=True)

    with open(CYCLE_PHASES, encoding="utf-8") as f:
        fases = list(csv.DictReader(f))
    variaveis = [c for c in fases[0] if c.startswith(("op_", "od_")) or c == "traducao_institucional"]

    nepac = carrega_nepac()
    fontes = {
        # default: MM cobre 1990–2020 (nominal); NEPAC de 01/2011 até a última data observada
        "MM": {"eventos": carrega_mm(), "ini": date(1990, 1, 1), "fim": date(2020, 12, 31)},
        "NEPAC": {"eventos": nepac, "ini": date(2011, 1, 1), "fim": nepac[-1][1]},
    }

    # eventos atribuídos
    atrib = []
    for fonte, F in fontes.items():
        for eid, d in F["eventos"]:
            ciclo, fase = ciclo_e_fase(d.isoformat())
            atrib.append({"fonte": fonte, "id_evento": eid, "data": d.isoformat(), "ciclo": ciclo, "fase": fase or ""})
    por_fase = Counter((a["fonte"], a["fase"]) for a in atrib if a["fase"])

    # taxa por fase
    linhas_fase = []
    for fs in fases:
        ini, fim = date.fromisoformat(fs["date_start"]), date.fromisoformat(fs["date_end"])
        dias = (fim - ini).days + 1
        for fonte, F in fontes.items():
            a, b = max(ini, F["ini"]), min(fim, F["fim"])
            cob_dias = max(0, (b - a).days + 1)
            linha = {"phase_id": fs["phase_id"], "cycle": fs["cycle"], "phase": fs["phase"],
                     "date_start": fs["date_start"], "date_end": fs["date_end"], "fonte": fonte,
                     "dias": dias, "dias_cobertos": cob_dias, "cobertura": round(cob_dias / dias, 3),
                     "n_eventos": None, "taxa_30d": None, "ic_inf": None, "ic_sup": None,
                     "elegivel": cob_dias / dias >= COBERTURA_MIN}
            if cob_dias:  # fora da cobertura fica NA, não zero
                n = por_fase[(fonte, fs["phase_id"])]
                lo, hi = ic_poisson(n)
                k = 30 / cob_dias
                linha.update(n_eventos=n, taxa_30d=round(n * k, 3), ic_inf=round(lo * k, 3), ic_sup=round(hi * k, 3))
            linha.update({v: fs[v] for v in variaveis})
            linhas_fase.append(linha)

    # linha de base: dentro × fora das fases, dentro da cobertura
    dias_fase = set()
    for fs in fases:
        d, fim = date.fromisoformat(fs["date_start"]), date.fromisoformat(fs["date_end"])
        while d <= fim:
            dias_fase.add(d)
            d += timedelta(days=1)
    base = []
    for fonte, F in fontes.items():
        tot = (F["fim"] - F["ini"]).days + 1
        dentro_d = sum(1 for d in dias_fase if F["ini"] <= d <= F["fim"])
        dentro_n = sum(1 for _, d in F["eventos"] if d in dias_fase)
        fora_n = sum(1 for _, d in F["eventos"] if F["ini"] <= d <= F["fim"]) - dentro_n
        t_in, t_out = dentro_n / dentro_d * 30, fora_n / (tot - dentro_d) * 30
        base.append({"fonte": fonte, "dias_dentro": dentro_d, "eventos_dentro": dentro_n, "taxa_dentro_30d": round(t_in, 3),
                     "dias_fora": tot - dentro_d, "eventos_fora": fora_n, "taxa_fora_30d": round(t_out, 3),
                     "razao": round(t_in / t_out, 2)})

    # teste de picos
    picos = []
    for fonte in fontes:
        for ciclo in dict.fromkeys(f["cycle"] for f in fases):
            el = [l for l in linhas_fase if l["fonte"] == fonte and l["cycle"] == ciclo and l["elegivel"]]
            if not any(l["phase"] == "pico" for l in el):
                continue
            maior = max(el, key=lambda l: l["taxa_30d"])
            pico = next(l for l in el if l["phase"] == "pico")
            picos.append({"fonte": fonte, "ciclo": ciclo, "fase_maior_taxa": maior["phase_id"],
                          "taxa_maior": maior["taxa_30d"], "taxa_pico": pico["taxa_30d"],
                          "pico_e_maximo": pico["taxa_30d"] >= maior["taxa_30d"]})

    # associação EOP/DOS × taxa, por fonte (BH dentro da fonte)
    assoc = []
    for fonte in fontes:
        el = [l for l in linhas_fase if l["fonte"] == fonte and l["elegivel"]]
        res = []
        for v in variaveis:
            par = [(float(l[v]), l["taxa_30d"]) for l in el if l[v] != "NA"]
            rho, p = p_permutacao([a for a, _ in par], [b for _, b in par], rng)
            res.append({"fonte": fonte, "variavel": v, "n_fases": len(par),
                        "rho": None if rho is None else round(rho, 3), "p_perm": None if p is None else round(p, 4)})
        for r, q in zip(res, benjamini_hochberg([r["p_perm"] for r in res])):
            r["q_bh"] = None if q is None else round(q, 4)
        assoc += res

    intra = []
    for fonte in fontes:
        for ciclo in dict.fromkeys(f["cycle"] for f in fases):
            el = [l for l in linhas_fase if l["fonte"] == fonte and l["cycle"] == ciclo and l["elegivel"]]
            if len(el) < 4:
                continue
            for v in variaveis:
                par = [(float(l[v]), l["taxa_30d"]) for l in el if l[v] != "NA"]
                rho, p = p_exato([a for a, _ in par], [b for _, b in par])
                intra.append({"fonte": fonte, "ciclo": ciclo, "variavel": v, "n_fases": len(par),
                              "rho": None if rho is None else round(rho, 3), "p_exato": None if p is None else round(p, 4)})

    # séries mensais na sobreposição das duas fontes
    ini = max(F["ini"] for F in fontes.values())
    fim = min(F["fim"] for F in fontes.values())
    meses = []
    y, m = ini.year, ini.month
    while (y, m) <= (fim.year, fim.month):
        meses.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    cont = {fonte: Counter(d.isoformat()[:7] for _, d in F["eventos"]) for fonte, F in fontes.items()}
    mensal = [{"ano_mes": mes, "MM": cont["MM"][mes], "NEPAC": cont["NEPAC"][mes]} for mes in meses]

    def limiar_p90(xs):
        s = sorted(xs)
        return s[math.ceil(0.9 * len(s)) - 1]

    conv = []
    for rotulo, linhas in (("todos os meses", mensal), ("sem 2013-06", [r for r in mensal if r["ano_mes"] != "2013-06"])):
        rho, p = p_permutacao([r["MM"] for r in linhas], [r["NEPAC"] for r in linhas], rng)
        l_mm, l_ne = limiar_p90([r["MM"] for r in linhas]), limiar_p90([r["NEPAC"] for r in linhas])
        comuns = [r["ano_mes"] for r in linhas if r["MM"] >= l_mm and r["NEPAC"] >= l_ne]
        conv.append({"recorte": rotulo, "n_meses": len(linhas), "rho": round(rho, 3), "p_perm": round(p, 4),
                     "limiar_p90_MM": l_mm, "limiar_p90_NEPAC": l_ne, "meses_pico_comuns": ";".join(comuns)})
    picos_comuns = conv[0]["meses_pico_comuns"].split(";")

    # gravação
    def grava(nome, linhas):
        with open(SAIDA / nome, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0]))
            w.writeheader()
            w.writerows([{k: ("NA" if v is None else v) for k, v in r.items()} for r in linhas])

    grava("eventos_atribuidos.csv", atrib)
    grava("eventos_por_fase.csv", linhas_fase)
    grava("linha_de_base.csv", base)
    grava("teste_picos.csv", picos)
    grava("associacao_eop_dos.csv", assoc)
    grava("associacao_intraciclo.csv", intra)
    grava("serie_mensal_sobreposicao.csv", mensal)
    grava("convergencia_fontes.csv", conv)

    rb = {b["fonte"]: b["razao"] for b in base}
    rep = next(a for a in assoc if a["fonte"] == "NEPAC" and a["variavel"] == "op_repressao")
    reconstruido = {
        "razao_dentro_fora_MM": rb["MM"], "razao_dentro_fora_NEPAC": rb["NEPAC"],
        "rho_mensal": conv[0]["rho"], "p_mensal": conv[0]["p_perm"],
        "rho_repressao_NEPAC": rep["rho"], "q_repressao_NEPAC": rep["q_bh"],
    }
    meta = {
        "gerado_em": date.today().isoformat(), "n_permutacoes": N_PERM, "semente": SEMENTE,
        "cobertura_min": COBERTURA_MIN,
        "fontes": {f: {"n_eventos": len(F["eventos"]), "ini": F["ini"].isoformat(), "fim": F["fim"].isoformat()}
                   for f, F in fontes.items()},
        "comparacao_log": [{"medida": k, "log_2026_10_07": LOG_ORIGINAL[k], "reconstrucao": reconstruido[k]}
                           for k in LOG_ORIGINAL],
    }
    with open(SAIDA / "painel_dados.json", "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "variaveis": variaveis, "fases": linhas_fase, "linha_de_base": base,
                   "picos": picos, "associacao": assoc, "intraciclo": intra, "mensal": mensal,
                   "convergencia": conv, "meses_pico_comuns": picos_comuns}, f, ensure_ascii=False, indent=1)

    print(f"OK: {SAIDA}")
    for f, F in meta["fontes"].items():
        print(f"  {f}: {F['n_eventos']} eventos, cobertura {F['ini']} a {F['fim']}")
    print("  medida | log 2026-10-07 | reconstrução")
    for c in meta["comparacao_log"]:
        print(f"  {c['medida']} | {c['log_2026_10_07']} | {c['reconstrucao']}")


if __name__ == "__main__":
    main()
