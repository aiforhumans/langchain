# LangChain Chat Models and LangSmith Examples

This repository contains examples of using LangChain chat models with different invocation methods, streaming capabilities, and LangSmith integration for tracing and debugging.

## Files

- `main.py`: Demonstrates different ways to invoke chat models and streaming capabilities
- `langsmith_example.py`: Shows a more complex chain with LangSmith tracing

## Chat Model Invocation Methods

LangChain chat models can be invoked in multiple ways:

1. Using a simple string:
   ```python
   model.invoke("Hello")
   ```

2. Using OpenAI format:
   ```python
   model.invoke([{"role": "user", "content": "Hello"}])
   ```

3. Using LangChain message objects:
   ```python
   model.invoke([HumanMessage("Hello")])
   ```

## Streaming Capabilities

LangChain supports multiple streaming methods:

1. Synchronous streaming:
   ```python
   for token in model.stream("Hello"):
       print(token.content, end="|")
   ```

2. Asynchronous streaming:
   ```python
   async for token in model.astream("Hello"):
       print(token.content, end="|")
   ```

3. Streaming events:
   ```python
   async for event in model.astream_events("Hello"):
       print(event)
   ```

## LangSmith Integration

LangSmith provides tracing and debugging capabilities for LangChain applications.

### Setup

1. Sign up at [LangSmith](https://smith.langchain.com/)
2. Set environment variables:
   ```bash
   export LANGSMITH_TRACING="true"
   export LANGSMITH_API_KEY="your-api-key"
   export LANGSMITH_PROJECT="default"  # or any project name
   ```

### Running the Examples

1. Basic chat model examples:
   ```bash
   python main.py
   ```

2. LangSmith tracing with a chain:
   ```bash
   python langsmith_example.py
   ```

## Requirements

- Python 3.8+
- LangChain
- OpenAI API key (for `langsmith_example.py` using OpenAI) or a local model server like LM Studio

## Docker Deployment

This project includes Docker configuration for easy deployment.

### Building and Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t langchain-app .
   ```

2. Run the container:
   ```bash
   docker run -it --env-file .env langchain-app
   ```

### Publishing to GitHub Container Registry

1. Log in to GitHub Container Registry:
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u aiforhumans --password-stdin
   ```

2. Tag the image for GitHub Container Registry:
   ```bash
   docker tag langchain-app ghcr.io/aiforhumans/langchain-app:latest
   ```

3. Push the image to GitHub Container Registry:
   ```bash
   docker push ghcr.io/aiforhumans/langchain-app:latest
   ```

4. Pull the image on another machine:
   ```bash
   docker pull ghcr.io/aiforhumans/langchain-app:latest
   ```

### Using Docker Compose

1. Start the application:
   ```bash
   docker-compose up -d
   ```

2. View logs:
   ```bash
   docker-compose logs -f
   ```

3. Stop the application:
   ```bash
   docker-compose down
   ```

### Environment Variables

Make sure to set up your environment variables in a `.env` file:

```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-api-key
LANGSMITH_PROJECT=default
```

**Note:** The `.env` file is included in `.gitignore` to prevent sensitive information from being committed to the repository.
