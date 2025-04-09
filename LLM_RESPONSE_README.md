# LLM Response Agent

This script creates an interactive chat agent that connects to a local LM Studio model and provides tool-augmented responses.

## Features

- Interactive chat interface in the terminal
- Connection to local LM Studio model
- Tool-augmented responses (web search, weather, calculations)
- Conversation memory to maintain context
- Error handling for robustness

## Prerequisites

1. LM Studio installed and running with a local server
2. Python 3.8+ with required packages

## Setup

1. Make sure LM Studio is running with a server on port 1234
2. Install the required packages:
   ```bash
   pip install langchain langchain-openai python-dotenv
   ```

3. Run the script:
   ```bash
   python llm_response.py
   ```

## Usage

1. Start the script and wait for the "You:" prompt
2. Type your questions or requests
3. The agent will respond, using tools when appropriate
4. Type 'exit', 'quit', or 'bye' to end the conversation

## Example Conversation

```
=== LM Studio Agent Chat ===
Type 'exit' or 'quit' to end the conversation.

You: What's the weather in New York?

AI: The weather in New York is currently sunny and 72 degrees. (This is a mock response - implement real weather API as needed.)

You: Calculate 15 * 24

AI: The result of 15 * 24 is 360

You: exit

AI: Goodbye! Have a great day!

Thank you for chatting!
```

## Customization

You can customize the agent by:

1. Adding more tools in the script
2. Changing the system prompt
3. Adjusting the model parameters
4. Implementing real APIs for the mock tools

## Troubleshooting

If you encounter issues:

1. Ensure LM Studio is running with a server on port 1234
2. Check that you have the required packages installed
3. Verify that your model in LM Studio supports the OpenAI chat format
4. Try reducing the complexity of your queries if the model struggles

## Note

The tool implementations (web search, weather) are mocks. In a production environment, you would replace these with real API calls.
