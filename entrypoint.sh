#!/bin/bash
set -e

# Check if environment variables are set
if [ -z "$LANGSMITH_API_KEY" ]; then
  echo "Warning: LANGSMITH_API_KEY is not set. LangSmith tracing will not work."
fi

# Run the specified command or default to main.py
if [ $# -eq 0 ]; then
  echo "Running default application (main.py)"
  exec python main.py
else
  echo "Running command: $@"
  exec "$@"
fi
