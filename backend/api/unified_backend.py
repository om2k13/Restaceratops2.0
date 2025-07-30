#!/usr/bin/env python3
"""
🦖 Unified Restaceratops Web Backend (FastAPI)
Exposes all agent features as web endpoints for the frontend
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.core.agents.unified_agent import UnifiedRestaceratopsAgent

app = FastAPI(title="Unified Restaceratops API")

# Allow all origins for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = UnifiedRestaceratopsAgent()

# --- Models ---
class CredentialIn(BaseModel):
    name: str
    type: str
    value: str
    header_name: Optional[str] = None
    description: Optional[str] = None

class OpenAPIGenIn(BaseModel):
    spec_path: str
    output_path: Optional[str] = "tests/generated_from_openapi.yml"
    include_security: Optional[bool] = True

class DataSourceIn(BaseModel):
    name: str
    type: str
    path: str
    options: Optional[Dict[str, Any]] = None

class TemplateIn(BaseModel):
    name: str
    template: Dict[str, Any]

class TestDataGenIn(BaseModel):
    template_name: str
    count: Optional[int] = 1
    context: Optional[Dict[str, Any]] = None

class TestSuiteIn(BaseModel):
    suite_path: str

# --- Endpoints ---
@app.get("/")
def root():
    return {"message": "Unified Restaceratops API is running!"}

@app.post("/credentials/add")
def add_credential(cred: CredentialIn):
    ok = agent.add_credential(cred.name, cred.type, cred.value, cred.header_name, cred.description)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to add credential")
    return {"success": True}

@app.get("/credentials/list")
def list_credentials():
    return agent.list_credentials()

@app.delete("/credentials/remove/{name}")
def remove_credential(name: str):
    ok = agent.remove_credential(name)
    if not ok:
        raise HTTPException(status_code=404, detail="Credential not found")
    return {"success": True}

@app.get("/credentials/validate/{name}")
def validate_credential(name: str):
    ok = agent.validate_credential(name)
    return {"valid": ok}

@app.post("/generate-tests/openapi")
def generate_tests_openapi(req: OpenAPIGenIn):
    out = agent.generate_tests_from_openapi(req.spec_path, req.output_path, req.include_security)
    return {"output_file": str(out)}

@app.post("/data-source/add")
def add_data_source(ds: DataSourceIn):
    ok = agent.add_data_source(ds.name, ds.type, ds.path, ds.options)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to add data source")
    return {"success": True}

@app.post("/template/add")
def add_template(tmpl: TemplateIn):
    ok = agent.add_template(tmpl.name, tmpl.template)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to add template")
    return {"success": True}

@app.post("/test-data/generate")
def generate_test_data(req: TestDataGenIn):
    data = agent.generate_test_data(req.template_name, req.count, req.context)
    return {"data": data}

@app.post("/test-suite/load")
def load_test_suite(req: TestSuiteIn):
    suite = agent.load_test_suite(req.suite_path)
    return suite

@app.post("/run-tests")
def run_tests(test_file: str = Query("tests/generated_from_openapi.yml")):
    result = agent.run_tests(test_file)
    return {"result": result} 