#!/usr/bin/env python
# LLM Response - Agent for chatting with local LM Studio model

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # This loads the variables from .env
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not installed. Run: pip install python-dotenv")

# Import LangChain components
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool

# Import LangGraph components for memory
from langgraph.graph import END, StateGraph
from typing import Dict, Any, TypedDict, Optional, List

# Define the state type for our LangGraph
class AgentState(TypedDict):
    """State for the agent conversation."""
    messages: List[Dict[str, Any]]  # The conversation history
    user_input: Optional[str]       # The current user input
    agent_output: Optional[str]     # The agent's response

# Define some tools for the agent to use
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

@tool
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location."""
    # This is a mock implementation - in a real app, you would use a weather API
    return f"The weather in {location} is currently sunny and 72 degrees. (This is a mock response - implement real weather API as needed.)"

@tool
def calculate(expression: str) -> str:
    """Calculate the result of a mathematical expression."""
    try:
        # Be careful with eval - in production you'd want to use a safer alternative
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

def create_agent():
    """Create a LangChain agent with the local LM Studio model using LangGraph for memory."""

    # Initialize the model with LM Studio
    llm = ChatOpenAI(
        model_name="local-model",
        openai_api_base="http://localhost:1234/v1",
        openai_api_key="not-needed",
        temperature=0.7
    )

    # Define the tools the agent can use
    tools = [search_web, get_current_weather, calculate]

    # Create the system message
    system_message = SystemMessage(content=(
        "You are a helpful AI assistant named LM Studio Agent. When asked to introduce yourself, "
        "explain that you are an AI assistant powered by a local LM Studio model and can help with "
        "various tasks including answering questions, providing information, and using tools.\n\n"
        "You have access to the following tools:\n"
        "- search_web: Search the web for information (only use for factual queries)\n"
        "- get_current_weather: Get the current weather in a location\n"
        "- calculate: Calculate the result of a mathematical expression\n\n"
        "Only use these tools when necessary to answer specific questions that require external information. "
        "For general conversation, introductions, or opinions, respond directly without using tools.\n\n"
        "When the user introduces themselves (e.g., 'I am Mark'), respond appropriately by acknowledging "
        "their name and asking how you can help them. Do not use tools for personal introductions."
    ))

    # Define the agent node function
    def agent_node(state: AgentState) -> dict:
        # Extract messages from state
        messages = state["messages"]

        # Create the prompt with the current messages
        prompt = ChatPromptTemplate.from_messages([
            system_message,
            *messages,
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create the agent
        agent = create_openai_tools_agent(llm, tools, prompt)

        # Create the agent executor (without memory since we're handling it in the graph)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=False,  # Set to False to avoid duplicate output
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )

        # Get the user's last message
        user_message = state["user_input"]

        # Run the agent
        response = agent_executor.invoke({"input": user_message})

        # Update the state with the agent's response
        return {"agent_output": response["output"]}

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add the agent node
    workflow.add_node("agent", agent_node)

    # Set the entry point
    workflow.set_entry_point("agent")

    # Set the exit point
    workflow.add_edge("agent", END)

    # Compile the graph
    app = workflow.compile()

    return app

def chat_loop():
    """Run an interactive chat loop with the agent using LangGraph for memory."""

    print("\n=== LM Studio Agent Chat ===")
    print("Type 'exit' or 'quit' to end the conversation.")

    try:
        # Create the agent
        agent = create_agent()

        # Initialize the conversation state
        state = {"messages": []}

        # Chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check if user wants to exit
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nAI: Goodbye! Have a great day!")
                break

            # Add the user message to the state (using the correct format for LangChain)
            state["messages"].append({"role": "user", "content": user_input})

            # Update the state with the user input
            state["user_input"] = user_input

            # Get response from agent
            try:
                # Invoke the agent with the current state
                new_state = agent.invoke(state)

                # Get the agent's response
                agent_response = new_state["agent_output"]

                # Add the agent's response to the messages (using the correct format for LangChain)
                state["messages"].append({"role": "assistant", "content": agent_response})

                # Display the response
                print(f"\nAI: {agent_response}")
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("AI: I'm sorry, I encountered an error. Please try again.")

    except KeyboardInterrupt:
        print("\n\nConversation ended by user.")
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")

    print("\nThank you for chatting!")

if __name__ == "__main__":
    # Check if LM Studio is running
    print("Connecting to LM Studio at http://localhost:1234/v1...")

    # You could add a check here to verify the connection before starting

    # Start the chat loop
    chat_loop()
