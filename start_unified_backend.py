#!/usr/bin/env python3
"""
🦖 Unified Restaceratops Backend Startup Script
Start the comprehensive unified backend that provides access to all functionality
"""

import uvicorn
from backend.api.unified_backend import app

if __name__ == "__main__":
    print("🦖 Starting Unified Restaceratops Backend...")
    print("📊 This unified interface provides access to ALL backend functionality!")
    print("🌐 Main Dashboard: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Alternative Docs: http://localhost:8000/redoc")
    print("💚 Health Check: http://localhost:8000/health")
    print("📡 WebSocket: ws://localhost:8000/ws")
    print("\n🚀 Starting server...")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    ) 