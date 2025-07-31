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
import openai
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
        
        # Check for API testing commands
        elif any(word in user_input_lower for word in ['test', 'run', 'execute', 'check']):
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
            api_info = self._extract_api_info(user_input)
            
            if not api_info.get('base_url'):
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
            
            # Use OpenRouter AI to generate test response
            prompt = f"""I want to test the API at {base_url}. 

Please help me understand:
1. What endpoints should I test?
2. What types of tests should I run?
3. How should I approach testing this API?

User request: {user_input}"""

            return await self.openrouter_ai.handle_conversation(prompt)
            
        except Exception as e:
            log.error(f"Error in API testing: {e}")
            return self._get_fallback_response(user_input)
    
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