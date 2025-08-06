#!/usr/bin/env python3
"""
🦖 Clean Restaceratops Backend API
Focused on core API testing functionality with AI capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
import logging
from contextlib import asynccontextmanager
import uvicorn
import tempfile
import shutil
import uuid
from pathlib import Path

# Import core services
from core.agents.enhanced_ai_system import EnhancedAISystem
from core.services.runner import run_suite
from core.services.dsl_loader import load_tests
from core.services.openapi_generator import OpenAPITestGenerator
from core.services.postman_parser import postman_parser
from core.models.database import get_db_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("restaceratops.clean_backend")

# Initialize AI system with OpenRouter
ai_system = EnhancedAISystem()

# Create uploads directory
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

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

# Pydantic models
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

class SingleUrlTestRequest(BaseModel):
    method: str
    url: str

class TestReport(BaseModel):
    test_name: str
    status: str
    response_time: float
    response_code: int
    response_body: str
    error: Optional[str] = None
    timestamp: str

# File upload endpoint
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a test file"""
    try:
        # Validate file type
        if not file.filename.endswith(('.yml', '.yaml')):
            raise HTTPException(status_code=400, detail="Only YAML files are supported")
        
        # Create unique filename with timestamp and UUID to prevent overwrites
        file_extension = Path(file.filename).suffix
        file_name_without_ext = Path(file.filename).stem
        unique_filename = f"{file_name_without_ext}_{uuid.uuid4().hex[:8]}{file_extension}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save uploaded file with proper error handling
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Verify file was written correctly by reading it back
            with open(file_path, "rb") as verify_buffer:
                verify_content = verify_buffer.read()
                if len(verify_content) == 0:
                    raise Exception("Uploaded file is empty")
                    
        except Exception as upload_error:
            # Clean up the file if it was partially written
            if file_path.exists():
                file_path.unlink()
            raise upload_error
        
        log.info(f"File uploaded successfully: {file_path} (size: {file_path.stat().st_size} bytes)")
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "filename": unique_filename,
            "file_path": str(file_path)
        }
    except Exception as e:
        log.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

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

@app.post("/api/tests/single-url")
async def test_single_url(request: SingleUrlTestRequest):
    """Test a single URL and return results."""
    try:
        import httpx
        import time
        from datetime import datetime
        
        log.info(f"Testing single URL: {request.method} {request.url}")
        
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=request.url,
                headers={"User-Agent": "Restaceratops/1.0"}
            )
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Determine if test passed (2xx status codes)
        status = "passed" if 200 <= response.status_code < 300 else "failed"
        
        result = {
            "execution_id": f"single-url-{int(time.time())}",
            "status": status,
            "response_time": round(response_time, 2),
            "response_code": response.status_code,
            "response_body": response.text[:1000],  # Limit response body
            "error": None if status == "passed" else f"HTTP {response.status_code}",
            "timestamp": datetime.now().isoformat()
        }
        
        log.info(f"Single URL test completed. Status: {status}, Response time: {response_time:.2f}ms")
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        log.error(f"Single URL test failed: {e}")
        return JSONResponse(content={
            "execution_id": f"single-url-error-{int(time.time())}",
            "status": "failed",
            "response_time": 0,
            "response_code": 0,
            "response_body": "",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, status_code=200)  # Return 200 to show the error in the UI

@app.post("/api/import/postman")
async def import_postman_collection(file: UploadFile = File(...)):
    """Import Postman collection JSON and convert to test cases"""
    try:
        log.info(f"Importing Postman collection: {file.filename}")
        
        # Read the uploaded file
        content = await file.read()
        json_content = content.decode('utf-8')
        
        # Parse the Postman collection
        collection_data = postman_parser.parse_collection(json_content)
        
        # Generate YAML test file
        yaml_content = postman_parser.generate_yaml(collection_data)
        
        # Save the generated YAML file with unique filename
        base_filename = f"postman_import_{collection_data['name'].replace(' ', '_').lower()}"
        unique_filename = f"{base_filename}_{uuid.uuid4().hex[:8]}.yml"
        file_path = UPLOADS_DIR / unique_filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            
            # Verify file was written correctly
            with open(file_path, 'r', encoding='utf-8') as verify_f:
                verify_content = verify_f.read()
                if len(verify_content.strip()) == 0:
                    raise Exception("Generated YAML file is empty")
                    
        except Exception as write_error:
            # Clean up the file if it was partially written
            if file_path.exists():
                file_path.unlink()
            raise write_error
        
        log.info(f"Successfully imported Postman collection: {collection_data['name']}")
        log.info(f"Generated {len(collection_data['test_cases'])} test cases")
        log.info(f"Postman import file saved: {file_path} (size: {file_path.stat().st_size} bytes)")
        
        return {
            "status": "success",
            "message": f"Successfully imported Postman collection: {collection_data['name']}",
            "filename": unique_filename,
            "file_path": str(file_path),
            "collection_info": {
                "name": collection_data['name'],
                "description": collection_data['description'],
                "total_test_cases": len(collection_data['test_cases']),
                "variables": len(collection_data.get('variables', [])),
                "test_cases": collection_data['test_cases']
            }
        }
        
    except Exception as e:
        log.error(f"Postman import failed: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to import Postman collection: {str(e)}")

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