# Chat model examples demonstrating different invocation and streaming methods with LangSmith integration

import asyncio
import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # This loads the variables from .env
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not installed. Run: pip install python-dotenv")

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessageChunk

# Import LangSmith tracing utilities if available
try:
    # Try importing from langchain.callbacks first (newer versions)
    from langchain.callbacks.tracers import LangSmithTracer
    from langchain.callbacks.tracers.context import tracing_v2_enabled
    LANGSMITH_AVAILABLE = True
except ImportError:
    try:
        # Try importing from langchain_core.tracers (older versions)
        from langchain_core.tracers.langsmith import LangSmithTracer
        from langchain_core.tracers.context import tracing_v2_enabled
        LANGSMITH_AVAILABLE = True
    except ImportError:
        # Fallback if LangSmith is not installed
        LANGSMITH_AVAILABLE = False

        # Define dummy function if tracing is not available
        def tracing_v2_enabled():
            return None

# Helper function for async examples
async def run_async_examples(llm):
    print("\n=== ASYNC STREAMING EXAMPLE ===")
    print("Async streaming tokens for 'Write a short poem about coding':")
    print("Tokens: ", end="")
    async for chunk in llm.astream("Write a short poem about coding"):
        print(chunk.content, end="|", flush=True)
    print("\nAsync streaming complete!")

    print("\n=== ASTREAM EVENTS EXAMPLE ===")
    print("Streaming events for 'Tell me a short joke':")
    idx = 0
    async for event in llm.astream_events("Tell me a short joke"):
        idx += 1
        if idx >= 5:  # Truncate the output to keep it manageable
            print("\n...Truncated")
            break
        print(f"\nEvent {idx}: {event['event']}")
        if 'data' in event and 'chunk' in event['data']:
            if hasattr(event['data']['chunk'], 'content') and event['data']['chunk'].content:
                print(f"Content: {event['data']['chunk'].content}")

# Function to setup LangSmith environment variables
def setup_langsmith():
    # First check if LangSmith is available
    if not LANGSMITH_AVAILABLE:
        print("\n=== LANGSMITH SETUP INFORMATION ===")
        print("LangSmith tracing is not available. To enable it:")
        print("1. Install the required packages: pip install langchain langsmith")
        print("2. Sign up at https://smith.langchain.com/")
        print("3. Set these environment variables:")
        print("   export LANGSMITH_TRACING=\"true\"")
        print("   export LANGSMITH_API_KEY=\"your-api-key\"")
        print("   export LANGSMITH_PROJECT=\"default\" # or any project name")
        print("\nRunning without LangSmith tracing...\n")
        return False

    # Then check if environment variables are set
    if not os.environ.get("LANGSMITH_API_KEY"):
        print("\n=== LANGSMITH SETUP INFORMATION ===")
        print("LangSmith environment variables not set. To enable tracing:")
        print("1. Sign up at https://smith.langchain.com/")
        print("2. Set these environment variables:")
        print("   export LANGSMITH_TRACING=\"true\"")
        print("   export LANGSMITH_API_KEY=\"your-api-key\"")
        print("   export LANGSMITH_PROJECT=\"default\" # or any project name")
        print("\nRunning without LangSmith tracing...\n")
        return False

    return True

# Main function
def main():
    try:
        # Setup LangSmith
        langsmith_enabled = setup_langsmith()

        # Initialize the model
        llm = ChatOpenAI(
            model_name="local-model",
            openai_api_base="http://localhost:1234/v1",
            openai_api_key="not-needed"
        )

        # Enable tracing context if LangSmith is configured and available
        trace_context = None
        if langsmith_enabled and LANGSMITH_AVAILABLE:
            try:
                trace_context = tracing_v2_enabled()
                if trace_context:
                    print("\n=== LANGSMITH TRACING ENABLED ===")
                    print(f"Project: {os.environ.get('LANGSMITH_PROJECT', 'default')}")
                    print("View traces at: https://smith.langchain.com/")
            except Exception as e:
                print(f"\nError enabling LangSmith tracing: {e}")
                print("Running without tracing...")

        print("\n=== DIFFERENT WAYS TO INVOKE CHAT MODELS ===")

        # Method 1: Using a simple string
        print("\n1. Using a simple string:")
        response1 = llm.invoke("Say hello in English")
        print(f"Response: {response1}")

        # Method 2: Using OpenAI format
        print("\n2. Using OpenAI message format:")
        response2 = llm.invoke([{"role": "user", "content": "Say hello in Spanish"}])
        print(f"Response: {response2}")

        # Method 3: Using LangChain message objects
        print("\n3. Using LangChain message objects:")
        response3 = llm.invoke([HumanMessage(content="Say hello in French")])
        print(f"Response: {response3}")

        # Method 4: Using multiple messages for a translation example
        print("\n4. Using system and user messages for translation:")
        messages = [
            SystemMessage(content="Translate the following from English into Italian"),
            HumanMessage(content="hi!"),
        ]
        translation = llm.invoke(messages)
        print(f"Response: {translation}")

        print("\n=== SYNC STREAMING EXAMPLE ===")
        print("Streaming tokens for 'Say hello in Italian':")
        print("Tokens: ", end="")
        for token in llm.stream("Say hello in Italian"):
            print(token.content, end="|", flush=True)
        print("\nSync streaming complete!")

        # Run async examples if supported
        if sys.platform != "win32" or sys.version_info >= (3, 8):
            asyncio.run(run_async_examples(llm))
        else:
            print("\nAsync examples not supported on this platform/Python version")

    except Exception as e:
        print("\nError occurred:", str(e))
        print("Make sure:")
        print("1. LM Studio is running")
        print("2. Server is started in LM Studio")
        print("3. Port 1234 is correct")

# Run the main function
if __name__ == "__main__":
    main()
# Chat model examples demonstrating different invocation and streaming methods with LangSmith integration

import asyncio
import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # This loads the variables from .env
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not installed. Run: pip install python-dotenv")

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessageChunk

# Import LangSmith tracing utilities if available
try:
    # Try importing from langchain.callbacks first (newer versions)
    from langchain.callbacks.tracers import LangSmithTracer
    from langchain.callbacks.tracers.context import tracing_v2_enabled
    LANGSMITH_AVAILABLE = True
except ImportError:
    try:
        # Try importing from langchain_core.tracers (older versions)
        from langchain_core.tracers.langsmith import LangSmithTracer
        from langchain_core.tracers.context import tracing_v2_enabled
        LANGSMITH_AVAILABLE = True
    except ImportError:
        # Fallback if LangSmith is not installed
        LANGSMITH_AVAILABLE = False

        # Define dummy function if tracing is not available
        def tracing_v2_enabled():
            return None

# Helper function for async examples
async def run_async_examples(llm):
    print("\n=== ASYNC STREAMING EXAMPLE ===")
    print("Async streaming tokens for 'Write a short poem about coding':")
    print("Tokens: ", end="")
    async for chunk in llm.astream("Write a short poem about coding"):
        print(chunk.content, end="|", flush=True)
    print("\nAsync streaming complete!")

    print("\n=== ASTREAM EVENTS EXAMPLE ===")
    print("Streaming events for 'Tell me a short joke':")
    idx = 0
    async for event in llm.astream_events("Tell me a short joke"):
        idx += 1
        if idx >= 5:  # Truncate the output to keep it manageable
            print("\n...Truncated")
            break
        print(f"\nEvent {idx}: {event['event']}")
        if 'data' in event and 'chunk' in event['data']:
            if hasattr(event['data']['chunk'], 'content') and event['data']['chunk'].content:
                print(f"Content: {event['data']['chunk'].content}")

# Function to setup LangSmith environment variables
def setup_langsmith():
    # First check if LangSmith is available
    if not LANGSMITH_AVAILABLE:
        print("\n=== LANGSMITH SETUP INFORMATION ===")
        print("LangSmith tracing is not available. To enable it:")
        print("1. Install the required packages: pip install langchain langsmith")
        print("2. Sign up at https://smith.langchain.com/")
        print("3. Set these environment variables:")
        print("   export LANGSMITH_TRACING=\"true\"")
        print("   export LANGSMITH_API_KEY=\"your-api-key\"")
        print("   export LANGSMITH_PROJECT=\"default\" # or any project name")
        print("\nRunning without LangSmith tracing...\n")
        return False

    # Then check if environment variables are set
    if not os.environ.get("LANGSMITH_API_KEY"):
        print("\n=== LANGSMITH SETUP INFORMATION ===")
        print("LangSmith environment variables not set. To enable tracing:")
        print("1. Sign up at https://smith.langchain.com/")
        print("2. Set these environment variables:")
        print("   export LANGSMITH_TRACING=\"true\"")
        print("   export LANGSMITH_API_KEY=\"your-api-key\"")
        print("   export LANGSMITH_PROJECT=\"default\" # or any project name")
        print("\nRunning without LangSmith tracing...\n")
        return False

    return True

# Main function
def main():
    try:
        # Setup LangSmith
        langsmith_enabled = setup_langsmith()

        # Initialize the model
        llm = ChatOpenAI(
            model_name="local-model",
            openai_api_base="http://localhost:1234/v1",
            openai_api_key="not-needed"
        )

        # Enable tracing context if LangSmith is configured and available
        trace_context = None
        if langsmith_enabled and LANGSMITH_AVAILABLE:
            try:
                trace_context = tracing_v2_enabled()
                if trace_context:
                    print("\n=== LANGSMITH TRACING ENABLED ===")
                    print(f"Project: {os.environ.get('LANGSMITH_PROJECT', 'default')}")
                    print("View traces at: https://smith.langchain.com/")
            except Exception as e:
                print(f"\nError enabling LangSmith tracing: {e}")
                print("Running without tracing...")

        print("\n=== DIFFERENT WAYS TO INVOKE CHAT MODELS ===")

        # Method 1: Using a simple string
        print("\n1. Using a simple string:")
        response1 = llm.invoke("Say hello in English")
        print(f"Response: {response1}")

        # Method 2: Using OpenAI format
        print("\n2. Using OpenAI message format:")
        response2 = llm.invoke([{"role": "user", "content": "Say hello in Spanish"}])
        print(f"Response: {response2}")

        # Method 3: Using LangChain message objects
        print("\n3. Using LangChain message objects:")
        response3 = llm.invoke([HumanMessage(content="Say hello in French")])
        print(f"Response: {response3}")

        # Method 4: Using multiple messages for a translation example
        print("\n4. Using system and user messages for translation:")
        messages = [
            SystemMessage(content="Translate the following from English into Italian"),
            HumanMessage(content="hi!"),
        ]
        translation = llm.invoke(messages)
        print(f"Response: {translation}")

        print("\n=== SYNC STREAMING EXAMPLE ===")
        print("Streaming tokens for 'Say hello in Italian':")
        print("Tokens: ", end="")
        for token in llm.stream("Say hello in Italian"):
            print(token.content, end="|", flush=True)
        print("\nSync streaming complete!")

        # Run async examples if supported
        if sys.platform != "win32" or sys.version_info >= (3, 8):
            asyncio.run(run_async_examples(llm))
        else:
            print("\nAsync examples not supported on this platform/Python version")

    except Exception as e:
        print("\nError occurred:", str(e))
        print("Make sure:")
        print("1. LM Studio is running")
        print("2. Server is started in LM Studio")
        print("3. Port 1234 is correct")

# Run the main function
if __name__ == "__main__":
    main()
