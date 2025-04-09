# LangSmith tracing example with a simple chain

import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # This loads the variables from .env
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not installed. Run: pip install python-dotenv")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Import LangSmith tracing utilities if available
try:
    # Try importing from langchain.callbacks first (newer versions)
    from langchain.callbacks.tracers import LangSmithTracer
    LANGSMITH_AVAILABLE = True
except ImportError:
    try:
        # Try importing from langchain_core.tracers (older versions)
        from langchain_core.tracers.langsmith import LangSmithTracer
        LANGSMITH_AVAILABLE = True
    except ImportError:
        # Fallback if LangSmith is not installed
        LANGSMITH_AVAILABLE = False

def setup_langsmith():
    """Check and inform about LangSmith configuration."""
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

def main():
    """Run a simple chain with LangSmith tracing."""
    # Check LangSmith setup
    langsmith_enabled = setup_langsmith()

    if langsmith_enabled:
        print("\n=== LANGSMITH TRACING ENABLED ===")
        print(f"Project: {os.environ.get('LANGSMITH_PROJECT', 'default')}")
        print("View traces at: https://smith.langchain.com/")

    # Initialize the model using the local model
    llm = ChatOpenAI(
        model_name="local-model",
        openai_api_base="http://localhost:1234/v1",
        openai_api_key="not-needed"
    )

    # For OpenAI (if you have an API key):
    # Uncomment these lines and replace with your actual API key
    # api_key = os.environ.get("OPENAI_API_KEY")
    # if api_key:
    #     llm = ChatOpenAI(
    #         model_name="gpt-3.5-turbo",
    #         openai_api_key=api_key,
    #         temperature=0
    #     )

    # Create a simple chain that:
    # 1. Takes a topic
    # 2. Generates a short poem about it
    # 3. Analyzes the sentiment of the poem

    # Step 1: Create a prompt template for poem generation
    poem_prompt = ChatPromptTemplate.from_template(
        "Write a short poem about {topic}. Keep it under 4 lines."
    )

    # Step 2: Create a prompt template for sentiment analysis
    sentiment_prompt = ChatPromptTemplate.from_template(
        "Analyze the sentiment of the following poem. Is it positive, negative, or neutral? Explain why.\n\nPoem: {poem}"
    )

    # Step 3: Create the chain for poem generation
    poem_generator = poem_prompt | llm | StrOutputParser()

    # Step 4: Create the chain for sentiment analysis
    sentiment_analyzer = sentiment_prompt | llm | StrOutputParser()

    # Step 5: Create the full chain
    def generate_poem_and_analyze(topic):
        # Generate the poem
        poem = poem_generator.invoke({"topic": topic})

        # Analyze the sentiment
        sentiment = sentiment_analyzer.invoke({"poem": poem})

        # Return the results
        return {
            "topic": topic,
            "poem": poem,
            "sentiment_analysis": sentiment
        }

    # This is our chain function
    poem_chain = generate_poem_and_analyze

    # Run the chain with tracing
    print("\n=== RUNNING CHAIN WITH LANGSMITH TRACING ===")
    print("This chain will generate a poem and analyze its sentiment.")

    # Get user input for the topic
    topic = input("\nEnter a topic for the poem: ")

    # Run the chain (it's a function now, not a Runnable)
    result = poem_chain(topic)

    # Display the results
    print("\n=== RESULTS ===")
    print(f"Topic: {result['topic']}")
    print(f"\nPoem:\n{result['poem']}")
    print(f"\nSentiment Analysis:\n{result['sentiment_analysis']}")

    if langsmith_enabled:
        print("\n=== LANGSMITH TRACE ===")
        print("Check your LangSmith dashboard to see the full trace of this run.")
        print("URL: https://smith.langchain.com/")
        print("\nThe trace will show:")
        print("- The input to each step")
        print("- The output from each step")
        print("- The time taken for each step")
        print("- Any errors that occurred")
        print("- Token usage and costs (if using OpenAI)")

if __name__ == "__main__":
    main()
