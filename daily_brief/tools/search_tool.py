from duckduckgo_search import DDGS


def web_search(query: str) -> dict:
    """
    Searches the web using DuckDuckGo. No API key required.
    Returns up to 5 results with title, URL and a short snippet.
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
        return {"status": "error", "message": f"Search failed: {e}"}
