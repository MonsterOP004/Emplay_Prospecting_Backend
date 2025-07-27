from tools.tavily_search import search_web

def run_competitor_research(product: str) -> str:
    query = f"Top competitors of {product} and their features, pricing, and positioning"
    return search_web(query)
