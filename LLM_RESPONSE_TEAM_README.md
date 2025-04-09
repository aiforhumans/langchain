# LLM Response Team

This script creates a team of specialized AI agents that work together to handle different types of user queries, all powered by a local LM Studio model.

## Features

- **Multi-agent architecture** with specialized roles:
  - **Router Agent**: Analyzes queries and directs them to the appropriate specialist
  - **Research Agent**: Handles factual questions and information retrieval
  - **Math Agent**: Solves mathematical problems and calculations
  - **Weather Agent**: Provides weather information
  - **Conversation Agent**: Manages general conversation and personal interactions

- **LangGraph orchestration** for agent coordination and memory management
- **Tool integration** for enhanced capabilities
- **Conversation memory** that persists throughout the session
- **Interactive chat interface** in the terminal

## How It Works

1. When a user sends a message, the Router Agent analyzes it and determines which specialist agent should handle it
2. The appropriate specialist agent processes the query using its specialized tools and knowledge
3. The response is returned to the user along with information about which agent handled the query
4. The conversation history is maintained throughout the session

## Prerequisites

1. LM Studio installed and running with a local server
2. Python 3.8+ with required packages

## Setup

1. Make sure LM Studio is running with a server on port 1234
2. Install the required packages:
   ```bash
   pip install langchain langchain-openai langgraph python-dotenv
   ```

3. Run the script:
   ```bash
   python llm_response_team.py
   ```

## Usage

1. Start the script and wait for the "You:" prompt
2. Type your questions or requests
3. The system will automatically route your query to the most appropriate agent
4. Type 'exit', 'quit', or 'bye' to end the conversation

## Example Conversation

```
=== LM Studio Agent Team Chat ===
Type 'exit' or 'quit' to end the conversation.

You: Hello, my name is Sarah

AI: Hello Sarah! It's nice to meet you. How can I assist you today?
[Handled by Conversation Agent]

You: What's the capital of France?

AI: The capital of France is Paris.
[Handled by Research Agent]

You: Calculate 25 * 16

AI: The result of 25 * 16 is 400.
[Handled by Math Agent]

You: What's the weather like in Tokyo?

AI: The weather in Tokyo is currently sunny and 72 degrees. (This is a mock response - implement real weather API as needed.)
[Handled by Weather Agent]

You: exit

AI: Goodbye! Have a great day!

Thank you for chatting!
```

## Customization

You can customize the agent team by:

1. Adding more specialist agents for different domains
2. Modifying the system prompts for each agent
3. Adding new tools to enhance agent capabilities
4. Adjusting the routing logic in the Router Agent

## Technical Details

This implementation uses:

1. **LangGraph** for orchestration and state management
2. **LangChain** for agent creation and tool integration
3. **Local LM Studio model** for all language processing
4. **Conditional routing** based on query content

## Troubleshooting

If you encounter issues:

1. Ensure LM Studio is running with a server on port 1234
2. Check that you have the required packages installed
3. Verify that your model in LM Studio supports the OpenAI chat format
4. Try reducing the complexity of your queries if the model struggles

## Note

The tool implementations (web search, weather) are mocks. In a production environment, you would replace these with real API calls.
