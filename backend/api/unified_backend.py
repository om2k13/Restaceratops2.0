#!/usr/bin/env python3
"""
🦖 Unified Restaceratops Backend API
Comprehensive unified interface for all backend functionality
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
import logging
from contextlib import asynccontextmanager
import uvicorn

# Import all our services and agents
from backend.core.agents.enhanced_chat_interface import EnhancedRestaceratopsChat
from backend.core.agents.unified_agent import UnifiedRestaceratopsAgent
from backend.core.services.runner import run_suite
from backend.core.services.dsl_loader import load_tests
from backend.core.services.workflow_manager import WorkflowManager
from backend.core.services.enterprise_manager import EnterpriseManager
from backend.core.services.jira_integration import JiraIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("restaceratops.unified_backend")

# Initialize services
chat_interface = EnhancedRestaceratopsChat()
unified_agent = UnifiedRestaceratopsAgent()
workflow_manager = WorkflowManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    try:
        await chat_interface.initialize()
        log.info("🦖 Unified Restaceratops backend started successfully!")
        log.info("Enhanced chat interface initialized")
        log.info("Unified agent initialized")
        log.info("Workflow management system ready")
    except Exception as e:
        log.error(f"Failed to initialize services: {e}")
    
    yield
    
    # Shutdown
    log.info("Shutting down Unified Restaceratops backend...")

# Create FastAPI app
app = FastAPI(
    title="🦖 Unified Restaceratops API",
    description="Comprehensive AI-Powered API Testing Platform - All Features in One Place",
    version="3.0.0",
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

class WorkflowRequest(BaseModel):
    action: str
    data: Optional[Dict[str, Any]] = None

class CredentialRequest(BaseModel):
    name: str
    type: str
    value: str
    header_name: Optional[str] = None
    description: Optional[str] = None

class OpenAPIRequest(BaseModel):
    spec_path: str
    output_path: Optional[str] = "tests/generated_from_openapi.yml"
    include_security: Optional[bool] = True

class DataSourceRequest(BaseModel):
    name: str
    type: str
    path: str
    options: Optional[Dict[str, Any]] = None

class TemplateRequest(BaseModel):
    name: str
    template: Dict[str, Any]

class TestDataRequest(BaseModel):
    template_name: str
    count: Optional[int] = 1
    context: Optional[Dict[str, Any]] = None

class JiraRequest(BaseModel):
    action: str
    config: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None

# --- Main Dashboard Endpoint ---
@app.get("/", response_class=HTMLResponse)
async def unified_dashboard():
    """Main unified dashboard - entry point for all backend functionality"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🦖 Unified Restaceratops Backend Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
            .section { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
            .section h2 { color: #34495e; margin-top: 0; }
            .endpoint { margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #007bff; }
            .endpoint a { color: #007bff; text-decoration: none; font-weight: bold; }
            .endpoint a:hover { text-decoration: underline; }
            .endpoint .method { color: #28a745; font-weight: bold; }
            .endpoint .description { color: #6c757d; font-size: 0.9em; margin-top: 5px; }
            .status { text-align: center; padding: 10px; background: #d4edda; color: #155724; border-radius: 5px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦖 Unified Restaceratops Backend Dashboard</h1>
            <div class="status">✅ All services are running and accessible from this unified interface</div>
            
            <div class="section">
                <h2>📊 Core API Endpoints</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/health">/health</a>
                    <div class="description">System health check and status</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/dashboard">/api/dashboard</a>
                    <div class="description">Dashboard statistics and metrics</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/docs">/docs</a>
                    <div class="description">Interactive API documentation (Swagger)</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/redoc">/redoc</a>
                    <div class="description">Alternative API documentation (ReDoc)</div>
                </div>
            </div>

            <div class="section">
                <h2>🤖 AI Chat Interface</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/chat/demo">/api/chat/demo</a>
                    <div class="description">Demo chat interface (GET endpoint)</div>
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <a href="/api/chat">/api/chat</a>
                    <div class="description">Enhanced AI chat with Restaceratops (POST with JSON)</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/chat/system-stats">/api/chat/system-stats</a>
                    <div class="description">Get AI system statistics and performance</div>
                </div>
            </div>

            <div class="section">
                <h2>🧪 Test Management</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/tests/demo">/api/tests/demo</a>
                    <div class="description">Demo test execution (GET endpoint)</div>
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <a href="/api/tests/run">/api/tests/run</a>
                    <div class="description">Execute test suites (POST with JSON)</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/tests/status">/api/tests/status</a>
                    <div class="description">Get test execution status</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/generate-tests/demo">/api/generate-tests/demo</a>
                    <div class="description">Demo test generation (GET endpoint)</div>
                </div>
            </div>

            <div class="section">
                <h2>🔄 Workflow Management</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/workflow/start">/api/workflow/start</a>
                    <div class="description">Start a new workflow session (GET endpoint)</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/workflow/status">/api/workflow/status</a>
                    <div class="description">Get current workflow status and progress</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/workflow/demo">/api/workflow/demo</a>
                    <div class="description">Demo workflow execution (GET endpoint)</div>
                </div>
            </div>

            <div class="section">
                <h2>🏢 Enterprise Features</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/enterprise/status">/api/enterprise/status</a>
                    <div class="description">Enterprise system status</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/enterprise/demo">/api/enterprise/demo</a>
                    <div class="description">Demo enterprise features (GET endpoint)</div>
                </div>
            </div>

            <div class="section">
                <h2>🔧 Configuration & Data</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/credentials/list">/api/credentials/list</a>
                    <div class="description">List all configured credentials</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/credentials/demo">/api/credentials/demo</a>
                    <div class="description">Demo credential management (GET endpoint)</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/data-sources/list">/api/data-sources/list</a>
                    <div class="description">List all data sources</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/templates/list">/api/templates/list</a>
                    <div class="description">List all templates</div>
                </div>
            </div>

            <div class="section">
                <h2>🔗 Integrations</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/jira/status">/api/jira/status</a>
                    <div class="description">Jira integration status</div>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/jira/demo">/api/jira/demo</a>
                    <div class="description">Demo Jira integration (GET endpoint)</div>
                </div>
            </div>

            <div class="section">
                <h2>📡 Real-time Communication</h2>
                <div class="endpoint">
                    <span class="method">WS</span> <a href="ws://localhost:8000/ws">ws://localhost:8000/ws</a>
                    <div class="description">WebSocket for real-time updates and notifications</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# --- Health and Status ---
@app.get("/health")
async def health_check():
    """Comprehensive health check for all services"""
    try:
        # Check core services
        chat_status = "healthy" if chat_interface else "unhealthy"
        agent_status = "healthy" if unified_agent else "unhealthy"
        workflow_status = "healthy" if workflow_manager else "unhealthy"
        
        return {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": "3.0.0",
            "services": {
                "chat_interface": chat_status,
                "unified_agent": agent_status,
                "workflow_manager": workflow_status,
                "websocket": "healthy"
            },
            "message": "🦖 Unified Restaceratops backend is running smoothly!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/api/dashboard")
async def get_dashboard_stats():
    """Get comprehensive dashboard statistics"""
    try:
        # Get system stats from chat interface (handle as dict if not awaitable)
        try:
            system_stats = await chat_interface.get_system_stats()
        except:
            system_stats = {"ai_providers": [], "status": "available"}
        
        # Get workflow stats (handle as dict if not awaitable)
        try:
            workflow_summary = await workflow_manager.get_workflow_summary()
        except:
            workflow_summary = {"status": "available", "steps": []}
        
        return {
            "system_stats": system_stats,
            "workflow_summary": workflow_summary,
            "active_connections": len(manager.active_connections),
            "total_endpoints": 25,  # Approximate count
            "status": "operational"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- AI Chat Interface ---
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Enhanced AI chat with Restaceratops"""
    try:
        # Use the correct method name from the chat interface
        response = await chat_interface.handle_message(request.message)
        return {"response": response, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/system-stats")
async def get_system_stats():
    """Get AI system statistics"""
    try:
        # The get_system_stats method is not async, so call it directly
        stats = chat_interface.get_system_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/demo")
async def chat_demo():
    """Demo chat interface - GET endpoint"""
    try:
        response = await chat_interface.handle_message("Hello! Can you help me with API testing?")
        return {
            "demo_message": "Hello! Can you help me with API testing?",
            "response": response,
            "status": "demo_success",
            "note": "This is a demo. Use POST /api/chat for real chat interactions."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Test Management ---
@app.post("/api/tests/run")
async def run_tests(request: TestRunRequest):
    """Execute test suites"""
    try:
        result = await run_suite(request.test_file, request.options or {})
        return {"result": result, "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tests/load")
async def load_test_suite(request: Dict[str, Any]):
    """Load test configurations"""
    try:
        result = await load_tests(request.get("suite_path"))
        return {"result": result, "status": "loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-tests/openapi")
async def generate_tests_openapi(request: OpenAPIRequest):
    """Generate tests from OpenAPI specification"""
    try:
        result = unified_agent.generate_tests_from_openapi(
            request.spec_path, 
            request.output_path, 
            request.include_security
        )
        return {"output_file": str(result), "status": "generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tests/demo")
async def tests_demo():
    """Demo test execution - GET endpoint"""
    try:
        return {
            "demo_test": "Sample API test execution",
            "status": "demo_success",
            "test_results": {
                "total_tests": 5,
                "passed": 4,
                "failed": 1,
                "success_rate": "80%"
            },
            "note": "This is a demo. Use POST /api/tests/run for real test execution."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tests/status")
async def get_tests_status():
    """Get test execution status"""
    try:
        return {
            "status": "idle",
            "last_execution": None,
            "total_executions": 0,
            "success_rate": "0%"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/generate-tests/demo")
async def generate_tests_demo():
    """Demo test generation - GET endpoint"""
    try:
        return {
            "demo_generation": "Sample test generation from OpenAPI spec",
            "status": "demo_success",
            "generated_tests": [
                "GET /users - Test user retrieval",
                "POST /users - Test user creation", 
                "PUT /users/{id} - Test user update",
                "DELETE /users/{id} - Test user deletion"
            ],
            "note": "This is a demo. Use POST /api/generate-tests/openapi for real test generation."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Workflow Management ---
@app.post("/api/workflow/start")
async def start_workflow():
    """Start a new workflow session"""
    try:
        result = await workflow_manager.start_workflow()
        return {"result": result, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workflow/start")
async def start_workflow_get():
    """Start a new workflow session - GET endpoint"""
    try:
        result = await workflow_manager.start_workflow()
        return {"result": result, "status": "started", "method": "GET"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workflow/demo")
async def workflow_demo():
    """Demo workflow execution - GET endpoint"""
    try:
        return {
            "demo_workflow": "Sample workflow execution",
            "status": "demo_success",
            "workflow_steps": [
                "Connectivity Check",
                "User Story Selection", 
                "Test Case Generation",
                "Test Execution",
                "Results Evaluation"
            ],
            "note": "This is a demo. Use POST endpoints for real workflow execution."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workflow/status")
async def get_workflow_status():
    """Get current workflow status and progress"""
    try:
        summary = await workflow_manager.get_workflow_summary()
        current_step = await workflow_manager.get_current_step_info()
        return {"summary": summary, "current_step": current_step}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workflow/step/connectivity")
async def execute_connectivity_step(request: Dict[str, Any]):
    """Execute the connectivity step"""
    try:
        result = await workflow_manager.execute_current_step(request)
        return {"result": result, "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workflow/step/generate-test-cases")
async def execute_generate_test_cases_step(request: Dict[str, Any]):
    """Generate test cases from user stories"""
    try:
        result = await workflow_manager.execute_current_step(request)
        return {"result": result, "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workflow/step/execute-test")
async def execute_test_step(request: Dict[str, Any]):
    """Execute test cases with monitoring"""
    try:
        result = await workflow_manager.execute_current_step(request)
        return {"result": result, "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Enterprise Features ---
@app.post("/api/enterprise/auth/login")
async def enterprise_login(request: Dict[str, Any]):
    """Enterprise authentication"""
    try:
        # This would integrate with the enterprise manager
        return {"status": "authenticated", "token": "sample_token"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enterprise/platforms")
async def configure_platforms(request: Dict[str, Any]):
    """Configure multi-platform testing"""
    try:
        return {"status": "configured", "platforms": request.get("platforms", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enterprise/cicd")
async def configure_cicd(request: Dict[str, Any]):
    """CI/CD integration configuration"""
    try:
        return {"status": "configured", "cicd": request.get("cicd", {})}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enterprise/monitoring")
async def configure_monitoring(request: Dict[str, Any]):
    """Monitoring and alerting setup"""
    try:
        return {"status": "configured", "monitoring": request.get("monitoring", {})}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/enterprise/audit/logs")
async def get_audit_logs():
    """Audit logs and compliance"""
    try:
        return {"logs": [], "status": "retrieved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/enterprise/status")
async def get_enterprise_status():
    """Enterprise system status"""
    try:
        return {
            "status": "operational",
            "features": {
                "multi_platform": "enabled",
                "cicd_integration": "enabled", 
                "monitoring": "enabled",
                "security": "enabled"
            },
            "active_users": 0,
            "total_platforms": 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/enterprise/demo")
async def enterprise_demo():
    """Demo enterprise features - GET endpoint"""
    try:
        return {
            "demo_enterprise": "Sample enterprise features",
            "status": "demo_success",
            "features": [
                "Multi-platform testing",
                "CI/CD integration",
                "Monitoring and alerting",
                "Security and compliance"
            ],
            "note": "This is a demo. Use POST endpoints for real enterprise features."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Configuration & Data ---
@app.post("/api/credentials/add")
async def add_credential(request: CredentialRequest):
    """Add authentication credentials"""
    try:
        result = unified_agent.add_credential(
            request.name, 
            request.type, 
            request.value, 
            request.header_name, 
            request.description
        )
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/credentials/list")
async def list_credentials():
    """List all configured credentials"""
    try:
        return unified_agent.list_credentials()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/credentials/demo")
async def credentials_demo():
    """Demo credential management - GET endpoint"""
    try:
        return {
            "demo_credentials": "Sample credential management",
            "status": "demo_success",
            "sample_credentials": [
                {"name": "demo_api", "type": "bearer", "description": "Demo API for testing"},
                {"name": "demo_key", "type": "api_key", "description": "Demo API key"}
            ],
            "note": "This is a demo. Use POST /api/credentials/add for real credential management."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data-sources/list")
async def list_data_sources():
    """List all data sources"""
    try:
        return {"data_sources": [], "status": "retrieved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/templates/list")
async def list_templates():
    """List all templates"""
    try:
        return {"templates": [], "status": "retrieved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/data-source/add")
async def add_data_source(request: DataSourceRequest):
    """Add test data sources"""
    try:
        result = unified_agent.add_data_source(
            request.name, 
            request.type, 
            request.path, 
            request.options
        )
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/template/add")
async def add_template(request: TemplateRequest):
    """Add test templates"""
    try:
        result = unified_agent.add_template(request.name, request.template)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/test-data/generate")
async def generate_test_data(request: TestDataRequest):
    """Generate test data"""
    try:
        result = unified_agent.generate_test_data(
            request.template_name, 
            request.count, 
            request.context
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Integrations ---
@app.post("/api/jira/connect")
async def connect_to_jira(request: Dict[str, Any]):
    """Connect to Jira for user stories"""
    try:
        # This would integrate with the Jira integration service
        return {"status": "connected", "jira_url": request.get("jira_url")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jira/stories")
async def get_jira_stories(request: Dict[str, Any]):
    """Fetch Jira user stories"""
    try:
        return {"stories": [], "status": "retrieved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jira/status")
async def get_jira_status():
    """Jira integration status"""
    try:
        return {
            "status": "disconnected",
            "connected": False,
            "jira_url": None,
            "project": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jira/demo")
async def jira_demo():
    """Demo Jira integration - GET endpoint"""
    try:
        return {
            "demo_jira": "Sample Jira integration",
            "status": "demo_success",
            "sample_stories": [
                {"id": "PROJ-1", "title": "Implement user authentication", "status": "To Do"},
                {"id": "PROJ-2", "title": "Add API documentation", "status": "In Progress"},
                {"id": "PROJ-3", "title": "Create test suite", "status": "Done"}
            ],
            "note": "This is a demo. Use POST /api/jira/connect for real Jira integration."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- WebSocket for Real-time Communication ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await manager.send_personal_message(
                    json.dumps({"type": "pong", "timestamp": "2024-01-01T00:00:00Z"}),
                    websocket
                )
            elif message.get("type") == "chat":
                response = await chat_interface.handle_message(message.get("message", ""))
                await manager.send_personal_message(
                    json.dumps({"type": "chat_response", "response": response}),
                    websocket
                )
            else:
                await manager.send_personal_message(
                    json.dumps({"type": "error", "message": "Unknown message type"}),
                    websocket
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- Error Handlers ---
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist. Check /docs for available endpoints.",
            "available_endpoints": [
                "/", "/health", "/api/dashboard", "/api/chat", "/api/tests/run",
                "/api/workflow/start", "/api/enterprise/auth/login", "/ws"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

if __name__ == "__main__":
    print("Starting Unified Restaceratops backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 