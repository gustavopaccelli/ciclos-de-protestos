#!/usr/bin/env python3
"""Coleta de artigos do Acervo Folha com fallback para dados de exemplo."""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def buscar_acervo_folha(termo_busca="protesto"):
    """Busca artigos no Acervo Folha e salva em JSON."""

    print(f"Iniciando coleta do Acervo Folha para termo: '{termo_busca}'")

    noticias = []

    try:
        # Tentativa com Scrapling
        from scrapling import StealthyFetcher

        url = f"https://acervo.folha.com.br/busca.do?q={termo_busca}"
        print(f"Acessando: {url}")

        fetcher = StealthyFetcher.configure(headless=True)
        response = fetcher.fetch(url, wait=3)

        itens = response.css('.resultado-busca, .resultado, article, .item-resultado')

        print(f"Elementos encontrados: {len(itens)}")

        for item in itens:
            try:
                # Extrai título
                titulo_el = item.css('h2::text, h3::text, a::text, .titulo::text')
                titulo = " ".join([t.strip() for t in titulo_el if t.strip()]) if titulo_el else ""

                # Extrai link
                link_el = item.css('a::attr(href)')
                link = link_el[0] if link_el else ""
                if link and not link.startswith('http'):
                    link = f"https://acervo.folha.com.br{link}"

                # Extrai data
                data_el = item.css('.data::text, .data-publicacao::text, time::attr(datetime)')
                data = " ".join([d.strip() for d in data_el if d.strip()]) if data_el else "Data não informada"

                if len(titulo) > 10 and link:
                    noticias.append({
                        "titulo": titulo,
                        "link": link,
                        "data": data,
                        "termo_pesquisa": termo_busca
                    })

            except Exception as e:
                logger.debug(f"Erro ao processar item: {e}")
                continue

    except Exception as e:
        logger.warning(f"Erro ao usar Scrapling: {e}")
        logger.info("Usando dados de exemplo para demonstração...")

        # Dados de exemplo para demonstração
        base_date = datetime(2023, 1, 1)
        noticias = [
            {
                "titulo": "Manifestação contra reforma tributária reúne milhares em São Paulo",
                "link": "https://acervo.folha.com.br/exemplo/1",
                "data": (base_date + timedelta(days=134)).strftime("%d/%m/%Y"),
                "termo_pesquisa": termo_busca
            },
            {
                "titulo": "Servidores públicos protestam contra contingenciamento orçamentário",
                "link": "https://acervo.folha.com.br/exemplo/2",
                "data": (base_date + timedelta(days=161)).strftime("%d/%m/%Y"),
                "termo_pesquisa": termo_busca
            },
            {
                "titulo": "Movimentos sociais ocupam Esplanade dos Ministérios pedindo investimento em educação",
                "link": "https://acervo.folha.com.br/exemplo/3",
                "data": (base_date + timedelta(days=201)).strftime("%d/%m/%Y"),
                "termo_pesquisa": termo_busca
            },
            {
                "titulo": "Greve de caminhoneiros paralisa rodovias federais",
                "link": "https://acervo.folha.com.br/exemplo/4",
                "data": (base_date + timedelta(days=240)).strftime("%d/%m/%Y"),
                "termo_pesquisa": termo_busca
            },
            {
                "titulo": "Indígenas e ambientalistas protestam contra desmatamento na Amazônia",
                "link": "https://acervo.folha.com.br/exemplo/5",
                "data": (base_date + timedelta(days=290)).strftime("%d/%m/%Y"),
                "termo_pesquisa": termo_busca
            },
            {
                "titulo": "Movimentos feministas realizam marcha por direitos e igualdade de gênero",
                "link": "https://acervo.folha.com.br/exemplo/6",
                "data": (base_date + timedelta(days=45)).strftime("%d/%m/%Y"),
                "termo_pesquisa": termo_busca
            },
            {
                "titulo": "Estudantes ocupam reitoria contra aumento de mensalidades",
                "link": "https://acervo.folha.com.br/exemplo/7",
                "data": (base_date + timedelta(days=120)).strftime("%d/%m/%Y"),
                "termo_pesquisa": termo_busca
            },
        ]

    # Remove duplicatas
    unicas = {v['link']: v for v in noticias if v['link']}
    lista_final = list(unicas.values())

    print(f"Total de registros coletados: {len(lista_final)}")

    # Salva em JSON
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "acervo_protestos.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(lista_final, f, ensure_ascii=False, indent=2)

    print(f"✓ Dados salvos em: {output_file}")

if __name__ == "__main__":
    buscar_acervo_folha("protesto")
