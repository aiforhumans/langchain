# PowerShell deployment script for Windows users

# Function to print colored messages
function Write-ColoredMessage {
    param (
        [string]$Message,
        [string]$Type = "INFO"
    )
    
    switch ($Type) {
        "INFO" { 
            Write-Host "[DEPLOY] " -ForegroundColor Green -NoNewline
            Write-Host $Message 
        }
        "WARNING" { 
            Write-Host "[WARNING] " -ForegroundColor Yellow -NoNewline
            Write-Host $Message 
        }
        "ERROR" { 
            Write-Host "[ERROR] " -ForegroundColor Red -NoNewline
            Write-Host $Message 
        }
    }
}

# Check if .env.prod exists for production deployment
if ($args[0] -eq "prod" -and -not (Test-Path .env.prod)) {
    Write-ColoredMessage "Production environment file (.env.prod) not found." "WARNING"
    Write-ColoredMessage "Creating from example file..."
    Copy-Item .env.prod.example .env.prod
    Write-ColoredMessage "Please edit .env.prod with your actual production values before deploying."
    exit 1
}

# Check command line arguments
if ($args.Count -eq 0 -or $args[0] -eq "dev") {
    $env = "dev"
    $composeFile = "docker-compose.yml"
    Write-ColoredMessage "Deploying in DEVELOPMENT mode..."
}
elseif ($args[0] -eq "prod") {
    $env = "prod"
    $composeFile = "docker-compose.prod.yml"
    Write-ColoredMessage "Deploying in PRODUCTION mode..."
}
else {
    Write-ColoredMessage "Unknown environment: $($args[0])" "ERROR"
    Write-ColoredMessage "Usage: .\deploy.ps1 [dev|prod]"
    exit 1
}

# Pull latest changes if in production mode
if ($env -eq "prod") {
    Write-ColoredMessage "Pulling latest image from GitHub Container Registry..."
    docker pull ghcr.io/aiforhumans/langchain-app:latest
}

# Start the application
Write-ColoredMessage "Starting the application..."
docker-compose -f $composeFile down
docker-compose -f $composeFile up -d

Write-ColoredMessage "Deployment completed successfully!"
Write-ColoredMessage "To view logs: docker-compose -f $composeFile logs -f"
