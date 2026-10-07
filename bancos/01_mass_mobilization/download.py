#!/usr/bin/env python3
"""Baixa o Mass Mobilization do Harvard Dataverse e extrai o recorte Brasil.

Ainda não foi executado: a rede do ambiente de nuvem bloqueia dataverse.harvard.edu.
Rode localmente ou depois de liberar o domínio.

    python bancos/01_mass_mobilization/download.py            # baixa e filtra
    python bancos/01_mass_mobilization/download.py --listar   # só lista os arquivos

Os arquivos globais vão para fonte-original/global/ (ignorado pelo git) e o recorte
Brasil (ccode == 140) é gravado em dados/. Compare com o CSV já versionado antes de
substituí-lo.
"""
import argparse
import csv
import json
import sys
import urllib.request
from pathlib import Path

DOI = "doi:10.7910/DVN/HTTWYL"
API = "https://dataverse.harvard.edu/api"
AQUI = Path(__file__).resolve().parent
GLOBAL = AQUI / "fonte-original" / "global"
CCODE_BRASIL = "140"


def arquivos():
    url = f"{API}/datasets/:persistentId/?persistentId={DOI}"
    with urllib.request.urlopen(url, timeout=60) as r:
        meta = json.load(r)["data"]["latestVersion"]
    return meta["versionNumber"], meta.get("versionMinorNumber"), meta["files"]


def baixa(file_id, destino):
    url = f"{API}/access/datafile/{file_id}?format=original"
    destino.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as r, open(destino, "wb") as f:
        f.write(r.read())


def filtra_brasil(origem, destino):
    with open(origem, encoding="utf-8", errors="replace", newline="") as f:
        leitor = csv.DictReader(f)
        linhas = [l for l in leitor if l.get("ccode") == CCODE_BRASIL and l.get("protest") == "1"]
        campos = leitor.fieldnames
    with open(destino, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)
    return len(linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--listar", action="store_true")
    args = ap.parse_args()

    v, vmin, files = arquivos()
    print(f"Dataset {DOI}, versão {v}.{vmin}")
    for f in files:
        df = f["dataFile"]
        print(f"  {df['id']:>10}  {df.get('originalFileName', df['filename'])}  {df.get('filesize', '?')} B")
    if args.listar:
        return

    for f in files:
        df = f["dataFile"]
        nome = df.get("originalFileName", df["filename"])
        baixa(df["id"], GLOBAL / nome)
        print(f"baixado: {nome}")
        if nome.lower().endswith(".csv"):
            saida = AQUI / "dados" / f"protestos_brasil_{Path(nome).stem}.csv"
            n = filtra_brasil(GLOBAL / nome, saida)
            print(f"  recorte Brasil: {n} protestos -> {saida.relative_to(AQUI)}")


if __name__ == "__main__":
    sys.exit(main())
