# tools/tavily_search.py

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import tool
from dotenv import load_dotenv

load_dotenv(override=True)

# Tavily Search Tool instance
tavily_tool = TavilySearchResults(k=5)

@tool
def tavily_search(query: str) -> str:
    """
    Perform a web search using Tavily and return the top search results.
    """
    return tavily_tool.run(query)

# A wrapper for use without agent tool context
def search_web(query: str) -> str:
    return tavily_search.run(query)
