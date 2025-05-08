from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools import Tool

from helpers.config import get_settings

settings = get_settings()

def tool_search():
    from stores.llm.providers.CoHereProvider import CoHereProvider
    cohere_llm = CoHereProvider(api_key = settings.COHERE_API_KEY,
                            default_max_input_tokens=1000,
                            default_max_output_tokens=1000,
                            default_temperature=0.1)
    # You can create the tool to pass to an agent 
    search = DuckDuckGoSearchResults()
    search_tool = Tool(name="duckduck",description="A web search engine. Use this to as a search engine for general queries."
                    ,func=search.run)

    # Prepare tools 
    # tools = load_tools(["llm-math"], llm=cohere_llm) 
    # tools.append(search_tool)
    return [search_tool]
