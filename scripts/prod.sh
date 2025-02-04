#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Activate virtual environment
source venv/bin/activate

# Add the current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the application with hypercorn for production
echo "Starting production server..."
hypercorn wsgi:app \
    --bind ${HOST:-0.0.0.0}:${PORT:-5555} \
    --workers ${WORKERS:-4} \
    --access-logfile - \
    --error-logfile - \
    --log-level ${LOG_LEVEL:-info} 