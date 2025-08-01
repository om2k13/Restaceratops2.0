#!/usr/bin/env python3
"""
🦖 Clean Restaceratops Backend API
Focused on core API testing functionality with AI capabilities
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
import logging
from contextlib import asynccontextmanager
import uvicorn
import os

# Import core services
from core.agents.enhanced_ai_system import EnhancedAISystem
from core.services.runner import run_suite
from core.services.dsl_loader import load_tests
from core.services.openapi_generator import OpenAPITestGenerator
from core.models.database import get_db_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("restaceratops.clean_backend")

# Initialize AI system
ai_system = EnhancedAISystem()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    try:
        # Initialize database
        db_manager = await get_db_manager()
        await db_manager.connect()
        
        log.info("🦖 Clean Restaceratops backend started successfully!")
        log.info("AI system initialized")
        log.info("Database connection established")
        log.info("Core API testing functionality ready")
    except Exception as e:
        log.error(f"Failed to initialize services: {e}")
    
    yield
    
    # Shutdown
    try:
        db_manager = await get_db_manager()
        await db_manager.close()
    except:
        pass
    log.info("Shutting down Clean Restaceratops backend...")

# Create FastAPI app
app = FastAPI(
    title="🦖 Clean Restaceratops API",
    description="Focused AI-Powered API Testing Platform - Core Functionality Only",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            except:
                pass

manager = ConnectionManager()

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class TestRunRequest(BaseModel):
    test_file: str
    options: Optional[Dict[str, Any]] = None

class OpenAPIRequest(BaseModel):
    spec_path: str
    output_path: Optional[str] = "tests/generated_from_openapi.yml"
    include_security: Optional[bool] = True

class TestReport(BaseModel):
    test_name: str
    status: str
    response_time: float
    response_code: int
    response_body: str
    error: Optional[str] = None
    timestamp: str

# --- Core Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic information"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🦖 Restaceratops - API Testing Platform</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { background: #f0f0f0; padding: 20px; border-radius: 8px; }
            .endpoints { margin-top: 20px; }
            .endpoint { background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🦖 Restaceratops</h1>
                <p><strong>AI-Powered API Testing Platform</strong></p>
                <p>Core functionality focused on efficient API testing with AI assistance.</p>
            </div>
            
            <div class="endpoints">
                <h2>Available Endpoints:</h2>
                
                <div class="endpoint">
                    <span class="method">GET</span> <code>/health</code> - System health check
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <code>/api/chat</code> - AI chat interface
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <code>/api/tests/run</code> - Execute API tests
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <code>/api/generate-tests/openapi</code> - Generate tests from OpenAPI spec
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <code>/api/dashboard</code> - System statistics
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <code>/docs</code> - API documentation
                </div>
            </div>
            
            <div style="margin-top: 30px; padding: 15px; background: #e8f5e8; border-radius: 5px;">
                <h3>🎯 Core Features:</h3>
                <ul>
                    <li>✅ AI-powered test generation</li>
                    <li>✅ Real-time test execution</li>
                    <li>✅ Comprehensive test reporting</li>
                    <li>✅ OpenAPI specification parsing</li>
                    <li>✅ Intelligent chat assistance</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        ai_status = "operational" if ai_system.openrouter_ai.api_key else "no_api_key"
        
        return {
            "status": "healthy",
            "timestamp": asyncio.get_event_loop().time(),
            "ai_system": ai_status,
            "websocket_connections": len(manager.active_connections),
            "active_executions": 0,
            "version": "4.0.0",
            "features": {
                "ai_chat": "enabled",
                "test_execution": "enabled",
                "test_generation": "enabled",
                "reporting": "enabled"
            }
        }
    except Exception as e:
        log.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.get("/api/dashboard")
async def get_dashboard_stats():
    """Get system statistics and dashboard data"""
    try:
        # Get AI system stats
        ai_stats = ai_system.get_system_stats()
        
        # Get database stats
        db_manager = await get_db_manager()
        db_stats = await db_manager.get_dashboard_stats()
        
        return {
            "total_tests": db_stats["total_tests"],
            "success_rate": db_stats["success_rate"],
            "avg_response_time": db_stats["avg_response_time"],
            "running_tests": db_stats["running_tests"],
            "recent_results": db_stats["recent_results"],
            "ai_system": ai_stats,
            "websocket_connections": len(manager.active_connections),
            "system_status": "operational"
        }
    except Exception as e:
        log.error(f"Failed to get dashboard stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dashboard stats")

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """AI chat interface for API testing assistance"""
    try:
        response = await ai_system.handle_conversation(request.message)
        
        # Save chat message to database
        try:
            db_manager = await get_db_manager()
            await db_manager.save_chat_message(request.message, response)
        except Exception as db_error:
            log.warning(f"Failed to save chat message: {db_error}")
        
        return {
            "response": response,
            "timestamp": asyncio.get_event_loop().time(),
            "ai_model": "qwen/qwen3-coder:free"
        }
    except Exception as e:
        log.error(f"Chat request failed: {e}")
        raise HTTPException(status_code=500, detail="Chat request failed")

@app.get("/api/chat/system-stats")
async def get_system_stats():
    """Get AI system statistics"""
    try:
        return ai_system.get_system_stats()
    except Exception as e:
        log.error(f"Failed to get system stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system stats")

@app.post("/api/tests/run")
async def run_tests(request: TestRunRequest):
    """Execute API tests and return results"""
    try:
        # Run tests using the new run_suite function
        from core.services.runner import run_suite
        
        # Run tests
        results = await run_suite(request.test_file, options=request.options or {})
        
        # Check if results contain error
        if "error" in results:
            raise Exception(results["error"])
        
        # Save results to database
        try:
            db_manager = await get_db_manager()
            await db_manager.save_test_execution(results)
        except Exception as db_error:
            log.warning(f"Failed to save to database: {db_error}")
        
        # Return the results directly (they're already formatted correctly)
        return results
        
    except Exception as e:
        log.error(f"Test execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")

@app.post("/api/generate-tests/openapi")
async def generate_tests_openapi(request: OpenAPIRequest):
    """Generate test cases from OpenAPI specification"""
    try:
        # Generate tests using OpenAPI generator
        generator = OpenAPITestGenerator(request.spec_path)
        tests = generator.generate_tests()
        
        # Save generated tests
        output_path = request.output_path or "tests/generated_from_openapi.yml"
        generator.save_tests(output_path)
        
        return {
            "status": "success",
            "message": "Tests generated successfully",
            "output_path": output_path,
            "tests_generated": True,
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        log.error(f"Test generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")

@app.get("/api/tests/status")
async def get_tests_status():
    """Get current test execution status"""
    return {
        "active_executions": 0,
        "total_executions": 0,
        "last_execution": None,
        "status": "idle"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "chat":
                response = await ai_system.handle_conversation(message.get("message", ""))
                await manager.send_personal_message(
                    json.dumps({
                        "type": "chat_response",
                        "response": response,
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
            elif message.get("type") == "ping":
                await manager.send_personal_message(
                    json.dumps({"type": "pong", "timestamp": asyncio.get_event_loop().time()}),
                    websocket
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        log.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": [
                "/health",
                "/api/chat",
                "/api/tests/run",
                "/api/generate-tests/openapi",
                "/api/dashboard",
                "/docs"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": asyncio.get_event_loop().time()
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 