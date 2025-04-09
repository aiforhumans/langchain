"""
Weather tools for LangChain agents.
"""

from langchain.tools import tool

@tool
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location."""
    # This is a mock implementation - in a real app, you would use a weather API
    return f"The weather in {location} is currently sunny and 72 degrees. (This is a mock response - implement real weather API as needed.)"
