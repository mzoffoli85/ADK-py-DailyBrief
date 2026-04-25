from ddgs import DDGS


def web_search(query: str) -> dict:
    """
    Busca en la web usando DuckDuckGo. No requiere API key.
    Retorna hasta 5 resultados con título, URL y un extracto breve.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(
                    {
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                    }
                )
        return {"status": "success", "query": query, "results": results}
    except Exception as e:
        return {"status": "error", "message": f"La búsqueda falló: {e}"}
