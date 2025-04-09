"""
Search tools for LangChain agents.
"""

from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information about a query."""
    # This is a mock implementation - in a real app, you would use a search API
    
    # Handle common queries with hardcoded responses for better demo experience
    query_lower = query.lower()
    if "capital" in query_lower and "netherlands" in query_lower:
        return "The capital of the Netherlands is Amsterdam."
    elif "capital" in query_lower and "australia" in query_lower:
        return "The capital of Australia is Canberra."
    elif "capital" in query_lower and "france" in query_lower:
        return "The capital of France is Paris."
    elif "capital" in query_lower and "japan" in query_lower:
        return "The capital of Japan is Tokyo."
    elif "capital" in query_lower and "brazil" in query_lower:
        return "The capital of Brazil is Brasília."
    
    # Generic response for other queries
    return f"Found results for: {query}. (This is a mock response - implement real search functionality as needed.)"
