#!/usr/bin/env python3
"""
🦖 Restaceratops Backend API
Main FastAPI application with comprehensive endpoints
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import logging
from typing import Dict, List, Any
from contextlib import asynccontextmanager
import uvicorn

# Import our services and agents
from backend.core.agents.enhanced_chat_interface import EnhancedRestaceratopsChat
from backend.core.services.runner import run_suite
from backend.core.services.dsl_loader import load_tests
from backend.api.workflow_api import router as workflow_router
from backend.api.enterprise_api import router as enterprise_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('conversation_logs.txt', mode='a')  # File output
    ]
)
log = logging.getLogger("restaceratops.backend")

# Initialize enhanced chat interface
chat_interface = EnhancedRestaceratopsChat()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    try:
        await chat_interface.initialize()
        
        # Initialize enterprise manager
        from backend.api.enterprise_api import initialize_enterprise_manager
        await initialize_enterprise_manager()
        
        log.info("🦖 Restaceratops backend started successfully!")
        log.info("Enhanced chat interface initialized")
        log.info("Enterprise manager initialized")
        log.info("Workflow management system ready")
    except Exception as e:
        log.error(f"Failed to initialize services: {e}")
    
    yield
    
    # Shutdown
    log.info("Shutting down Restaceratops backend...")

# Create FastAPI app
app = FastAPI(
    title="🦖 Restaceratops API",
    description="AI-Powered API Testing Platform with Advanced Workflow Management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include workflow API routes
app.include_router(workflow_router)

# Include enterprise API routes
app.include_router(enterprise_router)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        log.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        log.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                log.error(f"Failed to send message to WebSocket: {e}")
                # Remove failed connection
                try:
                    self.active_connections.remove(connection)
                except ValueError:
                    pass

manager = ConnectionManager()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🦖 Welcome to Restaceratops API",
        "version": "2.0.0",
        "description": "AI-Powered API Testing Platform",
        "features": [
            "Advanced Workflow Management",
            "Jira Integration",
            "AI-Powered Test Generation",
            "Real-time Test Execution",
            "Comprehensive Reporting",
            "Enhanced Chat Interface"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "workflow": "/api/workflow",
            "chat": "/api/chat",
            "tests": "/api/tests",
            "websocket": "/ws"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Restaceratops API",
        "version": "2.0.0",
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/api/dashboard")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        "total_tests": 150,
        "success_rate": 0.95,
        "avg_response_time": 245,
        "running_tests": 3,
        "recent_results": [
            {
                "test_name": "User Authentication Test",
                "status": "success",
                "response_time": 180,
                "response_code": 200,
                "response_body": "User authenticated successfully"
            },
            {
                "test_name": "API Endpoint Test",
                "status": "success",
                "response_time": 320,
                "response_code": 200,
                "response_body": "API endpoint working correctly"
            },
            {
                "test_name": "Database Connection Test",
                "status": "error",
                "response_time": 1500,
                "response_code": 500,
                "response_body": "Database connection timeout"
            }
        ]
    }

# Chat API endpoints
@app.post("/api/chat")
async def chat_endpoint(request: Dict[str, Any]):
    """Enhanced chat endpoint with AI-powered responses"""
    try:
        user_message = request.get("message", "")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get response from enhanced chat interface
        response = await chat_interface.handle_message(user_message)
        
        return {
            "success": True,
            "response": response,
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        log.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/system-stats")
async def get_system_stats():
    """Get system statistics and status"""
    try:
        stats = chat_interface.get_system_stats()
        return {
            "success": True,
            "stats": stats,
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        log.error(f"System stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Test execution endpoints
@app.post("/api/tests/run")
async def run_tests(request: Dict[str, Any]):
    """Run test suite"""
    try:
        test_file = request.get("test_file", "tests/sample.yml")
        results = await run_suite(test_file)
        
        return {
            "success": True,
            "results": results,
            "test_file": test_file,
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        log.error(f"Test execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tests/load")
async def load_test_suite(request: Dict[str, Any]):
    """Load test suite from file"""
    try:
        test_file = request.get("test_file", "tests/sample.yml")
        tests = load_tests(test_file)
        
        return {
            "success": True,
            "tests": tests,
            "test_file": test_file,
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        log.error(f"Test loading error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            message_type = message.get("type", "chat")
            
            if message_type == "chat":
                # Handle chat messages
                user_message = message.get("message", "")
                response = await chat_interface.handle_message(user_message)
                
                await manager.send_personal_message(
                    json.dumps({
                        "type": "chat_response",
                        "response": response,
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
            
            elif message_type == "workflow_update":
                # Handle workflow updates
                await manager.broadcast(
                    json.dumps({
                        "type": "workflow_update",
                        "data": message.get("data", {}),
                        "timestamp": asyncio.get_event_loop().time()
                    })
                )
            
            elif message_type == "test_execution":
                # Handle test execution updates
                await manager.broadcast(
                    json.dumps({
                        "type": "test_execution_update",
                        "data": message.get("data", {}),
                        "timestamp": asyncio.get_event_loop().time()
                    })
                )
            
            else:
                # Unknown message type
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {message_type}",
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        log.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Jira integration endpoints
@app.post("/api/jira/connect")
async def connect_to_jira(request: Dict[str, Any]):
    """Connect to Jira and test connection"""
    try:
        from backend.core.services.jira_integration import JiraConfig, create_jira_integration
        
        jira_config = JiraConfig(**request)
        integration = await create_jira_integration(jira_config)
        
        return {
            "success": True,
            "message": "Successfully connected to Jira",
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        log.error(f"Jira connection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jira/stories")
async def get_jira_stories(request: Dict[str, Any]):
    """Get user stories from Jira"""
    try:
        from backend.core.services.jira_integration import JiraConfig, JiraIntegration
        
        jira_config = JiraConfig(**request.get("config", {}))
        filters = request.get("filters", {})
        
        async with JiraIntegration(jira_config) as jira:
            stories = await jira.fetch_user_stories(
                status_filter=filters.get("status"),
                epic_filter=filters.get("epic"),
                assignee_filter=filters.get("assignee")
            )
            
            return {
                "success": True,
                "stories": [vars(story) for story in stories],
                "count": len(stories),
                "timestamp": asyncio.get_event_loop().time()
            }
    except Exception as e:
        log.error(f"Jira stories error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Missing endpoints that frontend is trying to call
# Note: All required endpoints already exist in workflow_api.py and enterprise_api.py

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": str(request.url.path)
        }
    )

# Development endpoints (only in development mode)
if __name__ == "__main__":
    uvicorn.run(
        "backend.api.backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 