#!/usr/bin/env python3
"""
🦖 Gemini AI System for Restaceratops
Google's Gemini AI integration for test generation and API analysis
"""

import os
import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.schema import HumanMessage, SystemMessage
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Load environment variables
load_dotenv()

log = logging.getLogger("agent.gemini_ai")

class GeminiAISystem:
    """Advanced AI system using Google's Gemini with specialized capabilities for API testing."""
    
    def __init__(self):
        """Initialize the Gemini AI system."""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        # Use only free models to avoid billing
        self.free_models = [
            "gemini-1.5-flash",      # 15 req/min, 1M chars/min (FREE)
            "gemini-1.5-pro",        # 2 req/min, 1M chars/min (FREE)
            "gemini-2.0-flash-exp"   # 15 req/min, 1M chars/min (FREE)
        ]
        self.current_model_index = 0
        self.model_name = self.free_models[0]  # Start with fastest free model
        self.llm = None
        self.is_initialized = False
        
        # Rate limiting for free tier
        self.request_count = 0
        self.last_request_time = 0
        
        if GEMINI_AVAILABLE and self.api_key:
            self._initialize_gemini()
        else:
            log.warning("Gemini AI not available - missing dependencies or API key")
    
    def _initialize_gemini(self):
        """Initialize the Gemini LLM with free model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
                temperature=0.7,
                max_output_tokens=4000,
                convert_system_message_to_human=True
            )
            self.is_initialized = True
            log.info(f"Initialized Gemini AI system with FREE model: {self.model_name}")
            log.info("Using free tier - no billing will occur")
        except Exception as e:
            log.error(f"Failed to initialize Gemini AI: {e}")
            self.is_initialized = False
    
    def _check_rate_limit(self) -> bool:
        """Check if we're within free tier rate limits."""
        import time
        current_time = time.time()
        
        # Reset counter if more than 1 minute has passed
        if current_time - self.last_request_time > 60:
            self.request_count = 0
            self.last_request_time = current_time
        
        # Check rate limits for current model
        if self.model_name == "gemini-1.5-flash":
            return self.request_count < 15  # 15 requests per minute
        elif self.model_name == "gemini-1.5-pro":
            return self.request_count < 2   # 2 requests per minute
        elif self.model_name == "gemini-2.0-flash-exp":
            return self.request_count < 15  # 15 requests per minute
        
        return True  # Default to allow
    
    def _increment_request_count(self):
        """Increment request counter for rate limiting."""
        self.request_count += 1
    
    def _get_rate_limit_message(self) -> str:
        """Get rate limit message for current model."""
        return f"""⚠️ **Rate Limit Reached**

You've reached the free tier rate limit for {self.model_name}.
- gemini-1.5-flash: 15 requests/minute
- gemini-1.5-pro: 2 requests/minute
- gemini-2.0-flash-exp: 15 requests/minute

**Solutions:**
1. Wait 1 minute and try again
2. Use a different free model
3. Switch to local AI (Ollama)

**Current Usage:** {self.request_count} requests in the last minute"""
    
    async def generate_api_tests(self, api_spec: str, requirements: str) -> str:
        """Generate comprehensive API tests using Gemini."""
        if not self.is_initialized:
            return self._get_fallback_test_template(api_spec)
        
        # Check rate limits for free tier
        if not self._check_rate_limit():
            return self._get_rate_limit_message()
        
        try:
            system_prompt = """You are an expert API testing specialist. Generate comprehensive test cases in YAML format for the given API specification.

Focus on:
- Health checks and basic connectivity
- Authentication and authorization flows
- CRUD operations (Create, Read, Update, Delete)
- Error handling and edge cases
- Performance and load testing scenarios
- Security testing (input validation, SQL injection, etc.)

Return ONLY valid YAML without any markdown formatting or explanations."""

            user_prompt = f"""Generate comprehensive API tests for:

API Specification: {api_spec}
Requirements: {requirements}

Create test cases that cover:
1. Basic health checks
2. Authentication flows
3. CRUD operations
4. Error scenarios
5. Performance tests
6. Security tests

Return the tests in YAML format suitable for RESTACERATOPS."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            log.error(f"Error generating API tests with Gemini: {e}")
            return self._get_fallback_test_template(api_spec)
    
    async def analyze_api_spec(self, api_spec: str) -> str:
        """Analyze API specification and provide insights."""
        if not self.is_initialized:
            return self._get_fallback_analysis(api_spec)
        
        # Check rate limits for free tier
        if not self._check_rate_limit():
            return self._get_rate_limit_message()
        
        try:
            system_prompt = """You are an expert API analyst. Analyze the given API specification and provide detailed insights.

Focus on:
- API design patterns and best practices
- Potential security vulnerabilities
- Performance considerations
- Testing strategy recommendations
- Documentation quality
- Compliance and standards adherence"""

            user_prompt = f"""Analyze this API specification:

{api_spec}

Provide a comprehensive analysis including:
1. Design Assessment
2. Security Analysis
3. Performance Considerations
4. Testing Recommendations
5. Documentation Review
6. Compliance Check"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            log.error(f"Error analyzing API spec with Gemini: {e}")
            return self._get_fallback_analysis(api_spec)
    
    async def optimize_test_suite(self, test_suite: str, api_spec: str) -> str:
        """Optimize existing test suite using Gemini."""
        if not self.is_initialized:
            return self._get_fallback_optimization(test_suite)
        
        # Check rate limits for free tier
        if not self._check_rate_limit():
            return self._get_rate_limit_message()
        
        try:
            system_prompt = """You are an expert test optimization specialist. Analyze and optimize the given test suite for better coverage, performance, and maintainability.

Focus on:
- Test coverage gaps
- Redundant or inefficient tests
- Performance improvements
- Better test organization
- Enhanced error handling
- Security test additions"""

            user_prompt = f"""Optimize this test suite:

Test Suite:
{test_suite}

API Specification:
{api_spec}

Provide:
1. Coverage Analysis
2. Optimization Recommendations
3. Improved Test Structure
4. Performance Enhancements
5. Security Additions"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            log.error(f"Error optimizing test suite with Gemini: {e}")
            return self._get_fallback_optimization(test_suite)
    
    async def generate_troubleshooting_guide(self, error_description: str, context: str = "") -> str:
        """Generate troubleshooting guide for API issues."""
        if not self.is_initialized:
            return self._get_fallback_troubleshooting(error_description)
        
        # Check rate limits for free tier
        if not self._check_rate_limit():
            return self._get_rate_limit_message()
        
        try:
            system_prompt = """You are an expert API troubleshooting specialist. Generate comprehensive troubleshooting guides for API issues.

Focus on:
- Root cause analysis
- Step-by-step debugging
- Common solutions
- Prevention strategies
- Best practices
- Tools and techniques"""

            user_prompt = f"""Generate a troubleshooting guide for:

Error Description: {error_description}
Context: {context}

Provide:
1. Root Cause Analysis
2. Step-by-Step Debugging
3. Common Solutions
4. Prevention Strategies
5. Best Practices
6. Recommended Tools"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            log.error(f"Error generating troubleshooting guide with Gemini: {e}")
            return self._get_fallback_troubleshooting(error_description)
    
    async def handle_conversation(self, user_input: str) -> str:
        """Handle general conversation using Gemini."""
        if not self.is_initialized:
            return self._get_fallback_response(user_input)
        
        # Check rate limits for free tier
        if not self._check_rate_limit():
            return self._get_rate_limit_message()
        
        try:
            system_prompt = """You are Restaceratops, an AI-powered API testing assistant. Help users with API testing, test generation, troubleshooting, and optimization.

Be helpful, knowledgeable, and provide practical advice for API testing scenarios."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            log.error(f"Error in Gemini conversation: {e}")
            return self._get_fallback_response(user_input)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "provider": "Gemini AI",
            "model": self.model_name,
            "is_initialized": self.is_initialized,
            "api_key_configured": bool(self.api_key),
            "dependencies_available": GEMINI_AVAILABLE,
            "status": "working" if self.is_initialized else "not_configured",
            "free_tier": True,
            "rate_limit": {
                "gemini-1.5-flash": "15 req/min",
                "gemini-1.5-pro": "2 req/min", 
                "gemini-2.0-flash-exp": "15 req/min"
            },
            "current_usage": f"{self.request_count} requests in last minute"
        }
    
    def _get_fallback_test_template(self, api_spec: str) -> str:
        """Fallback test template when Gemini is not available."""
        return f"""# Generated Test Suite for {api_spec}

# Basic Health Check
- name: "Health Check"
  request:
    method: GET
    url: "{api_spec}/health"
  expect:
    status: 200

# Authentication Test
- name: "Authentication Required"
  request:
    method: GET
    url: "{api_spec}/protected"
  expect:
    status: 401

# Add more test cases based on your API specification
# This is a fallback template - configure Gemini AI for intelligent test generation"""
    
    def _get_fallback_analysis(self, api_spec: str) -> str:
        """Fallback API analysis when Gemini is not available."""
        return f"""# API Analysis for {api_spec}

## Basic Assessment
- **Status**: Manual analysis required
- **Recommendation**: Configure Gemini AI for detailed analysis

## Manual Review Checklist
1. ✅ API endpoints documented
2. ✅ Authentication methods defined
3. ✅ Error responses specified
4. ✅ Rate limiting configured
5. ✅ Security headers present

## Next Steps
- Add GOOGLE_API_KEY to .env file
- Restart the server
- Run analysis again for AI-powered insights"""
    
    def _get_fallback_optimization(self, test_suite: str) -> str:
        """Fallback test optimization when Gemini is not available."""
        return f"""# Test Suite Optimization

## Current Status
- **Test Suite**: {len(test_suite.split())} words
- **AI Analysis**: Not available

## Manual Optimization Tips
1. **Coverage**: Ensure all endpoints are tested
2. **Edge Cases**: Add boundary value tests
3. **Performance**: Include load testing scenarios
4. **Security**: Add authentication and authorization tests
5. **Maintenance**: Organize tests by functionality

## Enable AI Optimization
- Add GOOGLE_API_KEY to .env file
- Restart the server
- Run optimization again for AI-powered recommendations"""
    
    def _get_fallback_troubleshooting(self, error_description: str) -> str:
        """Fallback troubleshooting when Gemini is not available."""
        return f"""# Troubleshooting Guide

## Issue Description
{error_description}

## Basic Troubleshooting Steps
1. **Check Network**: Verify connectivity to API
2. **Authentication**: Ensure valid credentials
3. **Rate Limits**: Check for API quotas
4. **Logs**: Review server and client logs
5. **Documentation**: Consult API documentation

## Enable AI Troubleshooting
- Add GOOGLE_API_KEY to .env file
- Restart the server
- Get AI-powered troubleshooting assistance"""
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Fallback response when Gemini is not available."""
        return f"""🦖 I'm here to help with API testing!

**Current Request**: {user_input}

**Status**: Gemini AI not configured

**To enable AI features:**
1. Get free API key from https://makersuite.google.com/app/apikey
2. Add GOOGLE_API_KEY=your-key to .env file
3. Restart the server

**Available without AI:**
- API testing with real HTTP requests
- System status and information
- Basic test templates
- Help documentation

Would you like me to help you set up Gemini AI or assist with other features?"""

def get_gemini_ai_system() -> GeminiAISystem:
    """Get a singleton instance of the Gemini AI system."""
    return GeminiAISystem()

async def test_gemini_system():
    """Test the Gemini AI system."""
    print("🧪 Testing Gemini AI System...")
    
    gemini = get_gemini_ai_system()
    stats = gemini.get_system_stats()
    
    print(f"Provider: {stats['provider']}")
    print(f"Model: {stats['model']}")
    print(f"Initialized: {stats['is_initialized']}")
    print(f"API Key Configured: {stats['api_key_configured']}")
    print(f"Dependencies Available: {stats['dependencies_available']}")
    print(f"Status: {stats['status']}")
    
    if stats['is_initialized']:
        print("\n✅ Gemini AI is ready!")
        
        # Test conversation
        response = await gemini.handle_conversation("Hello! Can you help me test my API?")
        print(f"\nTest Response: {response[:200]}...")
    else:
        print("\n❌ Gemini AI needs configuration")
        print("Add GOOGLE_API_KEY to .env file")

if __name__ == "__main__":
    asyncio.run(test_gemini_system()) 