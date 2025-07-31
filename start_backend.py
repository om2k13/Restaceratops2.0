#!/usr/bin/env python3
"""
Simple script to start the Restaceratops backend
"""

import uvicorn
from dotenv import load_dotenv
from backend.api.backend import app

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    print("Starting Restaceratops backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 