#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application with uvicorn in development mode
echo "Starting development server..."
python run.py 