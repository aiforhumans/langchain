#!/usr/bin/env python
"""
Single agent implementation for chatting with local LM Studio model.
"""

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

# Import LangGraph components for memory
from langgraph.graph import END, StateGraph
from typing import Dict, Any, TypedDict, Optional, List

# Import tools
from src.tools.search_tools import search_web
from src.tools.weather_tools import get_current_weather
from src.tools.math_tools import calculate

# Define the state type for our LangGraph
class AgentState(TypedDict):
    """State for the agent conversation."""
    messages: List[Dict[str, Any]]  # The conversation history
    user_input: Optional[str]       # The current user input
    agent_output: Optional[str]     # The agent's response

def create_agent():
    """Create a LangChain agent with the local LM Studio model using LangGraph for memory."""
    
    # Initialize the model with LM Studio
    llm = ChatOpenAI(
        model_name="local-model",
        openai_api_base="http://localhost:1234/v1",
        openai_api_key="not-needed",
        temperature=0.7
    )
    
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
        
        # Convert messages to the correct format
        formatted_messages = [
            SystemMessage(content=msg["content"]) if msg["role"] == "system" else
            HumanMessage(content=msg["content"]) if msg["role"] == "user" else
            AIMessage(content=msg["content"])
            for msg in messages
        ]
        
        # Create the prompt with the current messages
        prompt = ChatPromptTemplate.from_messages([
            system_message,
            *formatted_messages,
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_tools_agent(llm, [search_web, get_current_weather, calculate], prompt)
        
        # Create the agent executor (without memory since we're handling it in the graph)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=[search_web, get_current_weather, calculate],
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
    
    # Start the chat loop
    chat_loop()
