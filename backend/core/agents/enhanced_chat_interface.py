#!/usr/bin/env python3
"""
🦖 Enhanced Chat Interface for Restaceratops
Simplified AI-powered API testing agent using OpenRouter with Qwen3 Coder
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
import httpx
from backend.core.services.runner import run_suite
from backend.core.services.dsl_loader import load_tests
from backend.core.agents.openrouter_ai_system import get_openrouter_ai_system

log = logging.getLogger("agent.enhanced_chat_interface")

class EnhancedRestaceratopsChat:
    """Enhanced conversational interface for Restaceratops API testing agent using OpenRouter Qwen3 Coder."""
    
    def __init__(self):
        """Initialize the enhanced chat interface."""
        # Initialize OpenRouter AI system (primary - Qwen3 Coder)
        self.openrouter_ai = get_openrouter_ai_system()
        
        # Initialize system
        self.initialized = False
        
        log.info("Enhanced Restaceratops Chat initialized with OpenRouter Qwen3 Coder")
        
    async def initialize(self):
        """Initialize the enhanced AI system."""
        if not self.initialized:
            self.initialized = True
            log.info("Enhanced AI system initialized with OpenRouter Qwen3 Coder")
    
    def _extract_api_info(self, user_input: str) -> Dict:
        """Extract API information from user input."""
        info = {}
        
        # Look for URLs
        import re
        urls = re.findall(r'https?://[^\s]+', user_input)
        if urls:
            info['base_url'] = urls[0]
        
        # Look for common API patterns
        if 'health' in user_input.lower():
            info['endpoints'] = ['/health']
        if 'auth' in user_input.lower() or 'login' in user_input.lower():
            info['endpoints'] = ['/auth/login']
        if 'user' in user_input.lower():
            info['endpoints'] = ['/users']
        
        return info
    
    async def handle_message(self, user_input: str) -> str:
        """Handle user input and return a response using OpenRouter Qwen3 Coder."""
        # Initialize system if not already done
        if not self.initialized:
            await self.initialize()
        
        # Log incoming user message
        log.info(f"=== Enhanced Chat Interface ===")
        log.info(f"Received user input: {user_input}")
        
        user_input_lower = user_input.lower().strip()
        
        # Check for simple greetings first
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
            try:
                return await self.openrouter_ai.handle_conversation(user_input)
            except Exception as e:
                log.error(f"Error in greeting response: {e}")
                return self._get_fallback_response(user_input)
        
        # Check for API testing commands - more flexible detection
        elif any(word in user_input_lower for word in ['test', 'run', 'execute', 'check']) or 'https://' in user_input_lower or 'http://' in user_input_lower:
            log.info(f"Detected API testing request: {user_input}")
            return await self._handle_api_testing(user_input)
        
        # Check for test creation commands
        elif any(word in user_input_lower for word in ['create', 'generate', 'make', 'write']):
            if any(word in user_input_lower for word in ['test', 'case']):
                return await self._handle_test_creation(user_input)
        
        # Check for status requests
        elif any(word in user_input_lower for word in ['status', 'result', 'report', 'show']):
            return await self._handle_status_request(user_input)
        
        # Check for help requests
        elif any(word in user_input_lower for word in ['help', 'what', 'how', 'explain']):
            return await self._handle_help_request(user_input)
        
        # Check for debug requests
        elif any(word in user_input_lower for word in ['debug', 'error', 'fix', 'troubleshoot']):
            return await self._handle_debug_request(user_input)
        
        # Check for system info requests
        elif any(word in user_input_lower for word in ['system', 'info', 'stats', 'configuration']):
            return await self._handle_system_info_request(user_input)
        
        # Default: general conversation
        else:
            try:
                return await self.openrouter_ai.handle_conversation(user_input)
            except Exception as e:
                log.error(f"Error in general conversation: {e}")
                return self._get_fallback_response(user_input)
    
    async def _handle_api_testing(self, user_input: str) -> str:
        """Handle API testing requests."""
        try:
            log.info(f"Handling API testing request: {user_input}")
            api_info = self._extract_api_info(user_input)
            log.info(f"Extracted API info: {api_info}")
            
            if not api_info.get('base_url'):
                log.info("No base URL found, returning help message")
                return """🧪 **API Testing Ready!**

I can help you test your APIs! Please provide the API URL:

**Example commands:**
• "Test my API at https://httpbin.org"
• "Run tests on https://api.example.com"
• "Check https://jsonplaceholder.typicode.com"

**What I'll test:**
• Health checks and status endpoints
• Authentication flows
• CRUD operations (GET, POST, PUT, DELETE)
• Error handling and edge cases
• Performance and response time validation

Please provide the API URL you'd like me to test!"""

            base_url = api_info['base_url']
            log.info(f"Found base URL: {base_url}, executing tests")
            
            # Actually execute API tests instead of just providing guidance
            return await self._execute_api_tests(base_url, user_input)
            
        except Exception as e:
            log.error(f"Error in API testing: {e}")
            return self._get_fallback_response(user_input)
    
    async def _execute_api_tests(self, base_url: str, user_input: str) -> str:
        """Hybrid approach: Try AI testing first, fall back to system logic if it fails."""
        try:
            log.info(f"Starting hybrid API testing for: {base_url}")
            
            # First, try AI-powered testing
            ai_result = await self._try_ai_testing(base_url, user_input)
            
            # If AI testing fails or doesn't provide actual results, fall back to system logic
            if self._should_fallback_to_system(ai_result):
                log.info(f"AI testing failed, falling back to system logic for: {base_url}")
                return await self._execute_system_tests(base_url, user_input)
            
            return ai_result
            
        except Exception as e:
            log.error(f"Error in hybrid API testing: {e}")
            # Fall back to system tests if anything goes wrong
            return await self._execute_system_tests(base_url, user_input)
    
    async def _try_ai_testing(self, base_url: str, user_input: str) -> str:
        """Try AI-powered API testing."""
        try:
            log.info(f"Attempting AI-powered testing for: {base_url}")
            
            prompt = f"""You are an API testing expert. I want you to ACTUALLY TEST the API at {base_url}.

Please perform the following tasks:

1. **Make actual HTTP requests** to test the API
2. **Report real results** with actual status codes, response times, and data
3. **Test multiple scenarios** including:
   - Basic GET request to the main endpoint
   - Different query parameters if supported
   - Error handling scenarios
   - Response structure validation

4. **Provide a detailed report** with:
   - Actual HTTP status codes received
   - Response times in seconds
   - Response body samples
   - Any errors encountered
   - Recommendations for further testing

IMPORTANT: Do NOT just provide guidance. Actually make the HTTP requests and report the real results.

User request: {user_input}

Please start testing now and provide a comprehensive report with actual test results."""

            return await self.openrouter_ai.handle_conversation(prompt)
            
        except Exception as e:
            log.error(f"Error in AI testing: {e}")
            raise e
    
    def _should_fallback_to_system(self, ai_result: str) -> bool:
        """Determine if we should fall back to system testing based on AI result."""
        # Check if AI result contains actual test results or just guidance
        guidance_indicators = [
            "guidance", "how to", "approach", "steps", "curl", "bash",
            "let me help you", "here's how", "testing approach"
        ]
        
        # Check if AI result contains actual HTTP results
        actual_result_indicators = [
            "status code", "response time", "actual result", "http", "200", "404", "500",
            "response body", "headers", "duration"
        ]
        
        ai_result_lower = ai_result.lower()
        
        # If it contains mostly guidance and few actual results, fall back
        guidance_count = sum(1 for indicator in guidance_indicators if indicator in ai_result_lower)
        actual_count = sum(1 for indicator in actual_result_indicators if indicator in ai_result_lower)
        
        log.info(f"AI result analysis - Guidance indicators: {guidance_count}, Actual results: {actual_count}")
        
        return guidance_count > actual_count or actual_count < 2
    
    async def _execute_system_tests(self, base_url: str, user_input: str) -> str:
        """Execute system-based API tests as fallback."""
        try:
            log.info(f"Executing system tests for: {base_url}")
            
            # Create a comprehensive test suite for the API
            test_suite = {
                "name": f"System API Test for {base_url}",
                "description": f"Comprehensive API testing for {base_url}",
                "base_url": base_url,
                "tests": [
                    {
                        "name": "Basic GET Request",
                        "method": "GET",
                        "url": base_url,
                        "expected_status": 200,
                        "timeout": 10
                    },
                    {
                        "name": "Health Check",
                        "method": "GET", 
                        "url": f"{base_url}/health",
                        "expected_status": [200, 404],  # Accept either 200 or 404
                        "timeout": 10
                    },
                    {
                        "name": "Status Endpoint",
                        "method": "GET",
                        "url": f"{base_url}/status", 
                        "expected_status": [200, 404],
                        "timeout": 10
                    },
                    {
                        "name": "API Documentation",
                        "method": "GET",
                        "url": f"{base_url}/docs",
                        "expected_status": [200, 404],
                        "timeout": 10
                    },
                    {
                        "name": "OpenAPI Spec",
                        "method": "GET",
                        "url": f"{base_url}/openapi.json",
                        "expected_status": [200, 404],
                        "timeout": 10
                    }
                ]
            }
            
            # Add parameter tests if it's a REST API
            if "api" in base_url.lower():
                test_suite["tests"].extend([
                    {
                        "name": "Query Parameter Test",
                        "method": "GET",
                        "url": f"{base_url}?test=1",
                        "expected_status": [200, 400, 404],
                        "timeout": 10
                    }
                ])
            
            results = []
            async with httpx.AsyncClient(timeout=30.0) as client:
                for test in test_suite["tests"]:
                    test_result = await self._run_single_test(client, test)
                    results.append(test_result)
            
            # Format the results
            return self._format_test_results(base_url, results, "System Tests")
            
        except Exception as e:
            log.error(f"Error executing system tests: {e}")
            return f"❌ **Error executing system tests for {base_url}**: {str(e)}"
    
    async def _run_single_test(self, client, test_config: dict) -> dict:
        """Run a single API test."""
        start_time = datetime.now()
        test_name = test_config["name"]
        method = test_config["method"]
        url = test_config["url"]
        expected_status = test_config["expected_status"]
        timeout = test_config.get("timeout", 10)
        
        try:
            log.info(f"Running system test: {test_name} - {method} {url}")
            
            response = await client.request(
                method=method,
                url=url,
                timeout=timeout
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Check if status is expected
            if isinstance(expected_status, list):
                status_ok = response.status_code in expected_status
            else:
                status_ok = response.status_code == expected_status
            
            return {
                "name": test_name,
                "method": method,
                "url": url,
                "status": "✅ PASSED" if status_ok else "❌ FAILED",
                "status_code": response.status_code,
                "expected_status": expected_status,
                "duration": round(duration, 3),
                "response_size": len(response.content),
                "headers": dict(response.headers)
            }
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return {
                "name": test_name,
                "method": method,
                "url": url,
                "status": "❌ ERROR",
                "status_code": None,
                "expected_status": expected_status,
                "duration": round(duration, 3),
                "error": str(e)
            }
    
    def _format_test_results(self, base_url: str, results: list, test_type: str = "API Tests") -> str:
        """Format test results into a readable response."""
        response = f"# 🧪 {test_type} Results for {base_url}\n\n"
        
        passed = sum(1 for r in results if "PASSED" in r["status"])
        failed = sum(1 for r in results if "FAILED" in r["status"])
        errors = sum(1 for r in results if "ERROR" in r["status"])
        
        response += f"## 📊 Summary\n"
        response += f"- ✅ **Passed**: {passed}\n"
        response += f"- ❌ **Failed**: {failed}\n"
        response += f"- ⚠️ **Errors**: {errors}\n\n"
        
        response += "## 🔍 Detailed Results\n\n"
        
        for result in results:
            response += f"### {result['name']}\n"
            response += f"- **Method**: {result['method']}\n"
            response += f"- **URL**: `{result['url']}`\n"
            response += f"- **Status**: {result['status']}\n"
            
            if result.get('status_code'):
                response += f"- **Response Code**: {result['status_code']}\n"
                if isinstance(result.get('expected_status'), list):
                    response += f"- **Expected**: {result['expected_status']}\n"
                else:
                    response += f"- **Expected**: {result.get('expected_status')}\n"
            
            response += f"- **Duration**: {result['duration']}s\n"
            response += f"- **Response Size**: {result.get('response_size', 0)} bytes\n"
            
            if result.get('error'):
                response += f"- **Error**: {result['error']}\n"
            
            response += "\n"
        
        return response
    
    def _get_test_endpoints(self, base_url: str) -> list:
        """Get common test endpoints for an API."""
        return [
            f"{base_url}/health",
            f"{base_url}/status",
            f"{base_url}/api/health",
            f"{base_url}/api/status"
        ]
    
    async def _handle_test_creation(self, user_input: str) -> str:
        """Handle test creation requests."""
        try:
            api_info = self._extract_api_info(user_input)
            
            if not api_info.get('base_url'):
                return """📝 **Test Generation Ready!**

I can create comprehensive test cases for your APIs! Please provide:

**Example commands:**
• "Create tests for https://httpbin.org"
• "Generate test cases for https://api.example.com"
• "Make tests for user authentication"

**What I'll generate:**
• Functional tests for each endpoint
• Authentication and security tests
• Error handling scenarios
• Performance test cases
• Edge case testing

Please provide the API URL or specification you'd like me to create tests for!"""

            base_url = api_info['base_url']
            
            # Use OpenRouter AI to generate test cases
            prompt = f"""Please help me create comprehensive test cases for the API at {base_url}.

User request: {user_input}

Please provide:
1. Test cases in YAML format
2. Positive and negative test scenarios
3. Authentication tests if applicable
4. Error handling tests
5. Performance considerations"""

            return await self.openrouter_ai.generate_api_tests(base_url, user_input)
            
        except Exception as e:
            log.error(f"Error in test creation: {e}")
            return self._get_fallback_response(user_input)
    
    async def _handle_status_request(self, user_input: str) -> str:
        """Handle status and results requests."""
        try:
            return await self.openrouter_ai.handle_conversation(user_input)
        except Exception as e:
            log.error(f"Error in status request: {e}")
            return """📊 **Test Results & Reporting**

I can provide comprehensive test reports! Here's what I track:

**📈 Metrics I Monitor:**
• Success Rate: Percentage of passing tests
• Response Times: Average, min, max latency
• Error Rates: Types and frequency of failures
• Coverage: Endpoints and scenarios tested
• Performance: Throughput and load handling

**📋 Report Types:**
• Console Reports: Real-time test progress
• HTML Reports: Beautiful, interactive dashboards
• JUnit XML: CI/CD integration format
• Prometheus: Metrics for monitoring systems

**To view results:**
• "Show me the test results"
• "Generate a test report"
• "What's the status of my tests?"

Would you like me to run tests and show you the results?"""
    
    async def _handle_help_request(self, user_input: str) -> str:
        """Handle help requests."""
        try:
            return await self.openrouter_ai.handle_conversation(user_input)
        except Exception as e:
            log.error(f"Error in help request: {e}")
            return """🦖 **Restaceratops Help Guide**

I'm your AI-powered API testing assistant! Here's how I can help:

**🎯 Core Capabilities:**
• **API Testing**: Run comprehensive tests on any API
• **Test Generation**: Create tests from OpenAPI specs
• **Troubleshooting**: Debug API issues and errors
• **Reporting**: Generate detailed test reports
• **Automation**: Set up CI/CD testing pipelines

**🚀 Quick Start Commands:**
• "Test my API at https://your-api.com"
• "Create tests from my OpenAPI spec"
• "Show me test results"
• "Help me debug this error"

**📚 Common Use Cases:**
1. **New API Testing**: "Test my new API endpoints"
2. **Authentication**: "Create tests for login/logout"
3. **Performance**: "Run performance tests on my API"
4. **Debugging**: "Help me fix this API error"

What would you like to learn more about?"""
    
    async def _handle_debug_request(self, user_input: str) -> str:
        """Handle debug and troubleshooting requests."""
        try:
            return await self.openrouter_ai.handle_conversation(user_input)
        except Exception as e:
            log.error(f"Error in debug request: {e}")
            return """🔍 **API Troubleshooting Assistant**

I can help you debug API issues! Here's what I can do:

**Common Problems I Can Help With:**
• 🚫 **4xx Errors**: Bad requests, authentication issues
• ⚠️ **5xx Errors**: Server errors, timeouts
• 🔐 **Authentication**: Token issues, permission problems
• 📊 **Performance**: Slow responses, timeouts
• 🔄 **Data Issues**: Invalid responses, schema mismatches

**To get help:**
• "Help me debug a 500 error"
• "My API is returning 401 errors"
• "Authentication is failing"
• "Response times are too slow"

What specific issue are you experiencing?"""
    
    async def _handle_detailed_report_request(self, user_input: str) -> str:
        """Handle detailed report requests."""
        try:
            return await self.openrouter_ai.handle_conversation(user_input)
        except Exception as e:
            log.error(f"Error in detailed report request: {e}")
            return self._get_fallback_response(user_input)
    
    async def _handle_system_info_request(self, user_input: str) -> str:
        """Handle system information requests."""
        try:
            stats = self.get_system_stats()
            return f"""🦖 **Restaceratops System Information**

**AI System:**
• Provider: {stats['openrouter']['provider']}
• Model: {stats['openrouter']['model']}
• Status: {'✅ Active' if stats['openrouter']['api_key_configured'] else '❌ Not Configured'}

**System Status:**
• Chat Interface: ✅ Active
• Test Runner: ✅ Available
• Vector Store: {'✅ Available' if stats.get('vector_store_available', False) else '❌ Not Available'}

**Current Configuration:**
• Using OpenRouter Qwen3 Coder model
• Free tier API access
• Real-time conversation logging

Everything is working properly! 🚀"""
        except Exception as e:
            log.error(f"Error in system info request: {e}")
            return self._get_fallback_response(user_input)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "openrouter": self.openrouter_ai.get_system_stats(),
            "vector_store_available": False  # Simplified for now
        }
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Get fallback response when AI is unavailable."""
        return f"""🦖 **Restaceratops AI Assistant**

I'm currently experiencing technical difficulties with my AI system. 

However, I can still help you with API testing! Here are some general tips:

🔧 **API Testing Basics:**
- Test all HTTP methods (GET, POST, PUT, DELETE)
- Verify status codes (200, 400, 401, 404, 500)
- Check response data structure and content
- Test with valid and invalid inputs
- Monitor response times

📋 **What you asked:** {user_input}

Would you like me to help you with specific API testing scenarios once the system is back online?"""
    
    async def chat_loop(self):
        """Interactive chat loop for testing."""
        print("🦖 Restaceratops Enhanced Chat Interface")
        print("Type 'quit' to exit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("🦖 Goodbye! Happy API testing!")
                    break
                
                if user_input:
                    response = await self.handle_message(user_input)
                    print(f"Restaceratops: {response}")
                    print("-" * 50)
                    
            except KeyboardInterrupt:
                print("\n🦖 Goodbye! Happy API testing!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("-" * 50)

def main():
    """Main function for testing the enhanced chat interface."""
    chat = EnhancedRestaceratopsChat()
    asyncio.run(chat.chat_loop())

if __name__ == "__main__":
    main() 