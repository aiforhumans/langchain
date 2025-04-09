# LangChain Project with LM Studio Integration

This repository contains a structured project for building AI agents with LangChain and LM Studio, featuring different agent architectures, tools, and examples.

## Project Structure

```
langchain/
├── src/                    # Source code
│   ├── agents/             # Agent implementations
│   │   ├── single_agent.py # Single agent implementation
│   │   └── team_agent.py   # Team of specialized agents
│   ├── examples/           # Example scripts
│   │   ├── chat_model_example.py  # Chat model usage examples
│   │   └── langsmith_example.py   # LangSmith tracing example
│   └── tools/              # Tool implementations
│       ├── search_tools.py # Web search tools
│       ├── math_tools.py   # Math calculation tools
│       └── weather_tools.py # Weather information tools
├── docs/                   # Documentation
│   ├── agent_docs.md       # Single agent documentation
│   └── team_agent_docs.md  # Team agent documentation
├── docker/                 # Docker-related files
│   ├── Dockerfile          # Docker image definition
│   ├── docker-compose.yml  # Development compose file
│   ├── docker-compose.prod.yml # Production compose file
│   └── entrypoint.sh       # Container entrypoint script
└── scripts/                # Utility scripts
    ├── deploy.ps1          # Windows deployment script
    └── deploy.sh           # Linux/macOS deployment script
```

## Features

- **Agent Architectures**:
  - Single agent with multiple tools
  - Team of specialized agents with a router

- **Tools**:
  - Web search (mock implementation)
  - Weather information (mock implementation)
  - Math calculations

- **Examples**:
  - Chat model invocation methods
  - Streaming capabilities
  - LangSmith tracing

- **Docker Support**:
  - Development and production configurations
  - GitHub Container Registry integration

## Getting Started

### Prerequisites

- Python 3.8+
- LM Studio installed and running with a local server
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aiforhumans/langchain.git
   cd langchain
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start LM Studio and run a local server on port 1234

### Running the Examples

#### Chat Model Example
```bash
python -m src.examples.chat_model_example
```

#### LangSmith Example
```bash
python -m src.examples.langsmith_example
```

### Running the Agents

#### Single Agent
```bash
python -m src.agents.single_agent
```

#### Team Agent
```bash
python -m src.agents.team_agent
```

## Docker Deployment

### Development Environment

1. Start the application in development mode:
   ```bash
   ./scripts/deploy.sh dev
   # On Windows: .\scripts\deploy.ps1 dev
   ```

### Production Environment

1. Create a production environment file:
   ```bash
   cp .env.prod.example .env.prod
   # Edit .env.prod with your actual production values
   ```

2. Start the application in production mode:
   ```bash
   ./scripts/deploy.sh prod
   # On Windows: .\scripts\deploy.ps1 prod
   ```

## Publishing to GitHub Container Registry

### Manual Publishing

1. Log in to GitHub Container Registry:
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u aiforhumans --password-stdin
   ```

2. Tag the image:
   ```bash
   docker tag langchain-app ghcr.io/aiforhumans/langchain-app:latest
   ```

3. Push the image:
   ```bash
   docker push ghcr.io/aiforhumans/langchain-app:latest
   ```

### Automated Publishing with GitHub Actions

This repository includes a GitHub Actions workflow that automatically builds and pushes the Docker image to GitHub Container Registry whenever you push to the main branch or create a new tag.

## Documentation

- [Single Agent Documentation](docs/agent_docs.md)
- [Team Agent Documentation](docs/team_agent_docs.md)

## License

MIT
