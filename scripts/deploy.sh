#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
  echo -e "${GREEN}[DEPLOY]${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
  print_warning "Production environment file (.env.prod) not found."
  print_message "Creating from example file..."
  cp .env.prod.example .env.prod
  print_message "Please edit .env.prod with your actual production values before deploying."
  exit 1
fi

# Check command line arguments
if [ "$1" == "dev" ] || [ "$1" == "" ]; then
  ENV="dev"
  COMPOSE_FILE="docker/docker-compose.yml"
  print_message "Deploying in DEVELOPMENT mode..."
elif [ "$1" == "prod" ]; then
  ENV="prod"
  COMPOSE_FILE="docker/docker-compose.prod.yml"
  print_message "Deploying in PRODUCTION mode..."
else
  print_error "Unknown environment: $1"
  print_message "Usage: ./scripts/deploy.sh [dev|prod]"
  exit 1
fi

# Pull latest changes if in production mode
if [ "$ENV" == "prod" ]; then
  print_message "Pulling latest image from GitHub Container Registry..."
  docker pull ghcr.io/aiforhumans/langchain-app:latest
fi

# Start the application
print_message "Starting the application..."
docker-compose -f $COMPOSE_FILE down
docker-compose -f $COMPOSE_FILE up -d

print_message "Deployment completed successfully!"
print_message "To view logs: docker-compose -f $COMPOSE_FILE logs -f"
