#!/usr/bin/env python
"""
Team agent implementation with multiple specialized agents working together with LM Studio model.
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
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent

# Import LangGraph components for orchestration and memory
from langgraph.graph import END, StateGraph
from typing import Dict, Any, TypedDict, Optional, List

# Import tools
from src.tools.search_tools import search_web
from src.tools.weather_tools import get_current_weather
from src.tools.math_tools import calculate

# Define the state type for our LangGraph
class TeamState(TypedDict):
    """State for the multi-agent conversation."""
    messages: List[Dict[str, Any]]  # The conversation history
    user_input: Optional[str]       # The current user input
    current_agent: Optional[str]    # The agent currently processing
    final_response: Optional[str]   # The final response to the user

def create_team():
    """Create a team of agents with the local LM Studio model using LangGraph for orchestration."""
    
    # Initialize the model with LM Studio
    llm = ChatOpenAI(
        model_name="local-model",
        openai_api_base="http://localhost:1234/v1",
        openai_api_key="not-needed",
        temperature=0.7
    )
    
    # Each agent will use its own specific tools
    
    # Create the system messages for each agent
    router_system_message = SystemMessage(content=(
        "You are the Router Agent, responsible for analyzing the user's query and deciding which specialist "
        "agent should handle it. Your job is to route the query to the most appropriate agent based on the "
        "content of the query.\n\n"
        "You have access to the following specialist agents:\n"
        "1. Research Agent - For factual questions, information retrieval, and knowledge-based queries\n"
        "2. Math Agent - For calculations, mathematical problems, and numerical analysis\n"
        "3. Weather Agent - For weather-related questions and forecasts\n"
        "4. Conversation Agent - For general conversation, greetings, opinions, and personal interactions\n\n"
        "Respond ONLY with the name of the agent that should handle the query. Do not add any explanation."
    ))
    
    research_system_message = SystemMessage(content=(
        "You are the Research Agent, specialized in answering factual questions and providing accurate information. "
        "Use the search_web tool to find information when needed. Be concise but thorough in your responses, "
        "focusing on providing accurate and relevant information."
    ))
    
    math_system_message = SystemMessage(content=(
        "You are the Math Agent, specialized in solving mathematical problems and performing calculations. "
        "Use the calculate tool to solve mathematical expressions. Provide step-by-step explanations when appropriate."
    ))
    
    weather_system_message = SystemMessage(content=(
        "You are the Weather Agent, specialized in providing weather information. "
        "Use the get_current_weather tool to retrieve weather data. Be specific about locations and conditions."
    ))
    
    conversation_system_message = SystemMessage(content=(
        "You are the Conversation Agent, specialized in friendly and engaging conversation. "
        "Handle greetings, personal questions, opinions, and general chit-chat. Be personable and conversational. "
        "When users introduce themselves, acknowledge them by name in your response."
    ))
    
    # Define the router agent function
    def router_agent(state: TeamState) -> Dict[str, Any]:
        # Get the user's input
        user_input = state["user_input"]
        
        # Create messages for the router
        router_messages = [
            router_system_message,
            HumanMessage(content=f"Route this query to the appropriate agent: '{user_input}'")
        ]
        
        # Get the routing decision
        response = llm.invoke(router_messages)
        agent_name = response.content.strip()
        
        # Normalize the agent name
        if "research" in agent_name.lower():
            return {"current_agent": "research"}
        elif "math" in agent_name.lower():
            return {"current_agent": "math"}
        elif "weather" in agent_name.lower():
            return {"current_agent": "weather"}
        else:
            return {"current_agent": "conversation"}
    
    # Define the research agent function
    def research_agent(state: TeamState) -> Dict[str, Any]:
        # Get the user's input and conversation history
        user_input = state["user_input"]
        messages = state["messages"]
        
        # Convert messages to the correct format
        formatted_messages = [
            HumanMessage(content=msg["content"]) if msg["role"] == "user" else
            SystemMessage(content=msg["content"]) if msg["role"] == "system" else
            HumanMessage(content=msg["content"])
            for msg in messages
        ]
        
        # Create the prompt for the research agent
        prompt = ChatPromptTemplate.from_messages([
            research_system_message,
            *formatted_messages,
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_tools_agent(llm, [search_web], prompt)
        
        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=[search_web],
            verbose=False,
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )
        
        # Run the agent
        response = agent_executor.invoke({"input": user_input})
        
        # Return the final response
        return {"final_response": response["output"]}
    
    # Define the math agent function
    def math_agent(state: TeamState) -> Dict[str, Any]:
        # Get the user's input and conversation history
        user_input = state["user_input"]
        messages = state["messages"]
        
        # Convert messages to the correct format
        formatted_messages = [
            HumanMessage(content=msg["content"]) if msg["role"] == "user" else
            SystemMessage(content=msg["content"]) if msg["role"] == "system" else
            HumanMessage(content=msg["content"])
            for msg in messages
        ]
        
        # Create the prompt for the math agent
        prompt = ChatPromptTemplate.from_messages([
            math_system_message,
            *formatted_messages,
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_tools_agent(llm, [calculate], prompt)
        
        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=[calculate],
            verbose=False,
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )
        
        # Run the agent
        response = agent_executor.invoke({"input": user_input})
        
        # Return the final response
        return {"final_response": response["output"]}
    
    # Define the weather agent function
    def weather_agent(state: TeamState) -> Dict[str, Any]:
        # Get the user's input and conversation history
        user_input = state["user_input"]
        messages = state["messages"]
        
        # Convert messages to the correct format
        formatted_messages = [
            HumanMessage(content=msg["content"]) if msg["role"] == "user" else
            SystemMessage(content=msg["content"]) if msg["role"] == "system" else
            HumanMessage(content=msg["content"])
            for msg in messages
        ]
        
        # Create the prompt for the weather agent
        prompt = ChatPromptTemplate.from_messages([
            weather_system_message,
            *formatted_messages,
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_tools_agent(llm, [get_current_weather], prompt)
        
        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=[get_current_weather],
            verbose=False,
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )
        
        # Run the agent
        response = agent_executor.invoke({"input": user_input})
        
        # Return the final response
        return {"final_response": response["output"]}
    
    # Define the conversation agent function
    def conversation_agent(state: TeamState) -> Dict[str, Any]:
        # Get the user's input and conversation history
        user_input = state["user_input"]
        messages = state["messages"]
        
        # Create a list of messages for the conversation agent
        conversation_messages = [
            conversation_system_message,
            *[HumanMessage(content=msg["content"]) if msg["role"] == "user" else
              SystemMessage(content=msg["content"]) if msg["role"] == "system" else
              HumanMessage(content=msg["content"])
              for msg in messages],
            HumanMessage(content=user_input)
        ]
        
        # Get the response directly (no tools needed)
        response = llm.invoke(conversation_messages)
        
        # Return the final response
        return {"final_response": response.content}
    
    # Define the conditional edge function to route to the appropriate agent
    def route_to_agent(state: TeamState) -> str:
        return state["current_agent"]
    
    # Create the graph
    workflow = StateGraph(TeamState)
    
    # Add the nodes
    workflow.add_node("router", router_agent)
    workflow.add_node("research", research_agent)
    workflow.add_node("math", math_agent)
    workflow.add_node("weather", weather_agent)
    workflow.add_node("conversation", conversation_agent)
    
    # Set the entry point
    workflow.set_entry_point("router")
    
    # Add the edges
    workflow.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "research": "research",
            "math": "math",
            "weather": "weather",
            "conversation": "conversation"
        }
    )
    
    # All specialist agents go to END
    workflow.add_edge("research", END)
    workflow.add_edge("math", END)
    workflow.add_edge("weather", END)
    workflow.add_edge("conversation", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

def chat_loop():
    """Run an interactive chat loop with the agent team using LangGraph for orchestration."""
    
    print("\n=== LM Studio Agent Team Chat ===")
    print("Type 'exit' or 'quit' to end the conversation.")
    
    try:
        # Create the agent team
        team = create_team()
        
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
            
            # Add the user message to the state
            state["messages"].append({"role": "user", "content": user_input})
            
            # Update the state with the user input
            state["user_input"] = user_input
            
            # Get response from agent team
            try:
                # Invoke the team with the current state
                new_state = team.invoke(state)
                
                # Get the final response
                agent_response = new_state["final_response"]
                
                # Add the agent's response to the messages
                state["messages"].append({"role": "assistant", "content": agent_response})
                
                # Display the response
                print(f"\nAI: {agent_response}")
                
                # Display which agent handled the query (for demonstration purposes)
                agent_name = new_state["current_agent"].capitalize()
                print(f"[Handled by {agent_name} Agent]")
                
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
