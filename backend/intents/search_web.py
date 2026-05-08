"""
search_web intent handler for Friday AI
Uses DuckDuckGo Instant Answers API — no API key required.
Returns top-3 results as formatted context for Friday to summarise.
"""

from typing import Optional

try:
    from duckduckgo_search import DDGS
    _HAS_DDGS = True
except ImportError:
    _HAS_DDGS = False


def search_and_summarize(query: str, max_results: int = 3) -> str:
    """
    Search DuckDuckGo for the given query and return top results
    formatted as a human-readable context string.

    Args:
        query       : search query string
        max_results : number of results to return (default 3)

    Returns:
        Formatted string with numbered results, or an error message.
    """
    if not _HAS_DDGS:
        return (
            "Web search is not available. "
            "Install it with: pip install duckduckgo-search"
        )

    if not query or not query.strip():
        return "Please provide a search query."

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        return f"Search failed: {e}"

    if not results:
        return f"No results found for '{query}'."

    lines = [f"Search results for: **{query}**\n"]
    for i, r in enumerate(results, 1):
        title = r.get("title", "No title")
        body = r.get("body", "")
        href = r.get("href", "")
        # Trim body to ~200 chars for conciseness
        snippet = (body[:200] + "…") if len(body) > 200 else body
        lines.append(f"{i}. **{title}**\n   {snippet}\n   🔗 {href}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Standalone test — run:  python -m backend.intents.search_web
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    query = "Python programming best practices"
    print(f"=== search_web Test: '{query}' ===\n")
    result = search_and_summarize(query)
    print(result)
