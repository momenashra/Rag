from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools import Tool
from duckduckgo_search import DDGS
from functools import partial


from helpers.config import get_settings

settings = get_settings()

def tool_search():
    # Define DuckDuckGo Search Tool
    def duckduckgo_search(query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if not results:
                    return "No results found"
                return "\n".join([f"{r['title']}: {r['body']}" for r in results])
        except Exception as e:
            return f"Search error: {str(e)}"

    # Create tool with exact name matching
    tools = [
        Tool(
            name="DuckDuckGo_Search",
            func=duckduckgo_search,
            description="Useful for searching the web for current information. Input should be a search query."
        )
    ]
    return tools
