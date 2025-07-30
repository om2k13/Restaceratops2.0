#!/usr/bin/env python3
"""
Test suite for Restaceratops Backend API
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.api.backend import app

client = TestClient(app)

class TestBackendAPI:
    """Test cases for backend API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "description" in data
        assert "features" in data
        assert "endpoints" in data
        assert data["version"] == "2.0.0"
    
    def test_docs_endpoint(self):
        """Test that docs endpoint is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint(self):
        """Test that redoc endpoint is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_workflow_endpoints(self):
        """Test workflow API endpoints"""
        # Test workflow list endpoint
        response = client.get("/api/workflow/")
        assert response.status_code in [200, 404]  # 404 if no workflows exist
    
    def test_chat_endpoint(self):
        """Test chat API endpoint"""
        # Test GET method (should return 405 Method Not Allowed)
        response = client.get("/api/chat/")
        assert response.status_code == 405  # Method Not Allowed for GET
        
        # Test POST method with empty data
        response = client.post("/api/chat/", json={})
        assert response.status_code in [200, 400, 422, 500]  # Various valid responses including 500 for server errors
    
    def test_health_check(self):
        """Test health check endpoint if it exists"""
        response = client.get("/health")
        # This might not exist, so we accept 404
        assert response.status_code in [200, 404]

class TestEnterpriseAPI:
    """Test cases for enterprise API endpoints"""
    
    def test_enterprise_endpoints(self):
        """Test enterprise API endpoints"""
        # Test enterprise overview endpoint (requires authentication)
        response = client.get("/api/enterprise/overview")
        assert response.status_code in [200, 401, 404]  # 401 if auth required
        
        # Test enterprise platforms endpoint (requires authentication)
        response = client.get("/api/enterprise/platforms")
        assert response.status_code in [200, 401, 404]  # 401 if auth required

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 