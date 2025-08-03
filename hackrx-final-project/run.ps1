# PowerShell script to set up and run the HackRx API

# Check if Python is installed
try {
    python --version
} catch {
    Write-Host "Python is not installed or not in PATH. Please install Python 3.8 or higher."
    exit 1
}

# Check if .env file exists, if not create from example
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "Created .env file from .env.example. Please update it with your API keys."
    } else {
        Write-Host "No .env.example file found. Please create a .env file with your API keys."
    }
}

# Check if virtual environment exists, if not create it
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Run the API
Write-Host "Starting the HackRx API..."
python main.py