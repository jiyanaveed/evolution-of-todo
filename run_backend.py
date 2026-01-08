#!/usr/bin/env python3
"""
Run script for the Evolution of Todo backend
"""
import os
import sys
from pathlib import Path
import uvicorn

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Change to the backend directory
os.chdir(backend_dir)

# Now import and run the application
from main import app

if __name__ == "__main__":
    # Handle command line arguments for port
    import argparse
    parser = argparse.ArgumentParser(description='Run the Evolution of Todo backend')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    parser.add_argument('--host', type=str, default="127.0.0.1", help='Host to run the server on (default: 127.0.0.1)')
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)