#!/bin/bash

# Shell script to set up and run the HackRx API

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in PATH. Please install Python 3.8 or higher."
    exit 1
fi

# Check if .env file exists, if not create from example
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Created .env file from .env.example. Please update it with your API keys."
    else
        echo "No .env.example file found. Please create a .env file with your API keys."
    fi
fi

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the API
echo "Starting the HackRx API..."
python main.py