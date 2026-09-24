import json
import time
from pathlib import Path
from scrapling import StealthyFetcher

def buscar_acervo_folha(termo_busca="protesto"):
    # URL de busca avançada / listagem do Acervo Folha
    url = f"https://acervo.folha.com.br/busca.do?q={termo_busca}"
    print(f"Acessando o Acervo Folha em: {url}")

    # O StealthyFetcher simula um navegador real e bypassa barreiras anti-bot
    fetcher = StealthyFetcher()

    try:
        # Carrega a página aguardando o tempo necessário para o JS do acervo injetar os resultados
        response = fetcher.get(url, wait=5)
    except Exception as e:
        print(f"Erro ao carregar a página do acervo: {e}")
        return

    noticias = []

    # Seletores focados na estrutura típica de resultados do Acervo Histórico da Folha
    # (Buscando blocos de artigos/resultados na página de busca do acervo)
    itens = response.css('.resultado-busca, article, .item-busca, li')

    print(f"Elementos encontrados na página: {len(itens)}")

    for item in itens:
        try:
            # Ajuste fino para extrair título, data e link dos jornais históricos
            titulo_el = item.css('h2::text, h3::text, a::text, .titulo::text')
            titulo = "".join(titulo_el).strip() if titulo_el else ""

            link_el = item.css('a::attr(href)')
            link = link_el.get() if link_el else ""
            if link and not link.startswith('http'):
                link = f"https://acervo.folha.com.br/{link}"

            data_el = item.css('.data::text, time::text, span::text')
            data = "".join(data_el).strip() if data_el else "Data não informada"

            if len(titulo) > 5: # Filtra ruídos vazios
                noticias.append({
                    "titulo": titulo,
                    "link": link,
                    "data": data,
                    "termo_pesquisa": termo_busca
                })
        except Exception as e:
            continue

    # Remove duplicadas caso o seletor traga redundâncias
    noticias_unicas = {v['link']: v for v in noticias if v['link']}
    lista_final = list(noticias_unicas.values())

    print(f"Total de registros históricos coletados: {len(lista_final)}")

    # Salvando os dados estruturados na pasta data/
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "acervo_protestos.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(lista_final, f, ensure_ascii=False, indent=4)

    print(f"Dados salvos com sucesso em {output_file}")

if __name__ == "__main__":
    # Termo ajustado para o contexto de ciclos de protestos nos registros históricos
    buscar_acervo_folha("protesto")
