"""
Math tools for LangChain agents.
"""

from langchain.tools import tool

@tool
def calculate(expression: str) -> str:
    """Calculate the result of a mathematical expression."""
    try:
        # Be careful with eval - in production you'd want to use a safer alternative
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"
