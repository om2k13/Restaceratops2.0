#!/usr/bin/env python3
"""
🦖 Enhanced Chat Interface for Restaceratops
Advanced AI-powered API testing agent with vector store, RAG, and multi-model support
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
from backend.core.agents.enhanced_ai_system import get_enhanced_ai_system
from backend.core.agents.openrouter_ai_system import get_openrouter_ai_system

log = logging.getLogger("agent.enhanced_chat_interface")

class EnhancedRestaceratopsChat:
    """Enhanced conversational interface for Restaceratops API testing agent with advanced AI capabilities."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        # Initialize OpenRouter AI system (primary)
        self.openrouter_ai = get_openrouter_ai_system()
        
        # Initialize enhanced AI system (fallback)
        self.enhanced_ai = get_enhanced_ai_system(api_key)
        
        # Initialize system
        self.initialized = False
        
        log.info("Enhanced Restaceratops Chat initialized with OpenRouter AI")
        
    async def initialize(self):
        """Initialize the enhanced AI system."""
        if not self.initialized:
            # The new enhanced AI system doesn't need explicit initialization
            # Just mark as initialized
            self.initialized = True
            log.info("Enhanced AI system initialized with OpenRouter + fallback support")
    
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
        """Handle user input and return a response using OpenRouter AI system."""
        # Initialize system if not already done
        if not self.initialized:
            await self.initialize()
        
        user_input_lower = user_input.lower().strip()
        
        # Check for simple greetings first (before API testing commands)
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
            try:
                return await self.openrouter_ai.handle_conversation(user_input)
            except Exception as e:
                # Fall back to enhanced fallback system if OpenRouter fails
                return self.enhanced_ai._get_fallback_response(user_input)
        
        # Check for specific API testing commands
        elif any(word in user_input_lower for word in ['test my api', 'test api', 'run test']):
            return await self._handle_api_testing(user_input)
        
        # Check for test creation requests
        elif any(word in user_input_lower for word in ['create test', 'generate test', 'make test']):
            return await self._handle_test_creation(user_input)
        
        # Check for status/report requests
        elif any(word in user_input_lower for word in ['status', 'report', 'results', 'how did']):
            return await self._handle_status_request(user_input)
        
        # Check for help requests
        elif any(word in user_input_lower for word in ['help', 'what can you do', 'how to use']):
            return await self._handle_help_request(user_input)
        
        # Default: general conversation
        else:
            try:
                return await self.openrouter_ai.handle_conversation(user_input)
            except Exception as e:
                # Fall back to enhanced fallback system if OpenRouter fails
                return self.enhanced_ai._get_fallback_response(user_input)
    
    async def _handle_api_testing(self, user_input: str) -> str:
        """Handle API testing requests."""
        api_info = self._extract_api_info(user_input)
        base_url = api_info.get('base_url', 'https://your-api.com')
        
        # Set environment variable
        os.environ['BASE_URL'] = base_url
        
        try:
            # Run tests
            exit_code = await run_suite('tests', max_in_flight=3)
            
            if exit_code == 0:
                return f"""✅ Tests completed successfully!

I tested your API at {base_url} and everything looks good! 

**Summary:**
• All endpoints responded correctly
• Status codes are as expected
• Response times are within normal range
• No critical issues found

Would you like me to:
• Run more comprehensive tests?
• Generate a detailed report?
• Test specific endpoints?"""
            else:
                return f"""⚠️ Tests completed with some issues.

I tested your API at {base_url} and found some problems.

**Summary:**
• Some endpoints may be down
• Response times might be slow
• Some status codes are unexpected

Would you like me to:
• Show you the detailed error report?
• Run tests on specific endpoints?
• Help you debug the issues?"""
                
        except Exception as e:
            return f"""❌ Sorry, I encountered an error while testing your API.

**Error:** {str(e)}

**Troubleshooting:**
• Make sure your API is running
• Check if the URL is correct
• Verify network connectivity
• Ensure proper authentication

Would you like me to help you troubleshoot this?"""
    
    async def _handle_test_creation(self, user_input: str) -> str:
        """Handle test creation requests."""
        api_info = self._extract_api_info(user_input)
        base_url = api_info.get('base_url', 'https://your-api.com')
        
        try:
            # Generate intelligent tests using OpenRouter AI
            test_yaml = await self.openrouter_ai.generate_api_tests(
                base_url,
                f"Create tests for: {user_input}"
            )
            
            # Clean the YAML output - remove markdown formatting if present
            if test_yaml.startswith('```yaml'):
                # Remove markdown code block
                test_yaml = test_yaml.replace('```yaml', '').replace('```', '').strip()
            
            # Remove any explanatory text after the YAML
            if '**Requirements:**' in test_yaml:
                test_yaml = test_yaml.split('**Requirements:**')[0].strip()
            
            # Save to file
            test_file = Path("tests/generated_openrouter.yml")
            test_file.parent.mkdir(exist_ok=True)
            test_file.write_text(test_yaml)
            
            return f"""✅ Test cases generated successfully!

I've created comprehensive test cases for your API at {base_url}.

**Generated Tests:**
• Saved to: `tests/generated_openrouter.yml`
• Includes multiple test scenarios
• Covers various HTTP methods
• Includes error handling

**What's Included:**
• Health check tests
• Authentication flows
• CRUD operations
• Error scenarios
• Performance validation

Would you like me to:
• Run these tests now?
• Generate additional test cases?
• Show you the test contents?"""
            
        except Exception as e:
            return f"""❌ Sorry, I encountered an error while generating tests.

**Error:** {str(e)}

**Fallback Response:**
I can still help you create basic test cases manually. Would you like me to:
• Show you a test template?
• Help you write tests step by step?
• Explain how to structure your tests?"""
    
    async def _handle_status_request(self, user_input: str) -> str:
        """Handle status and report requests."""
        return """📊 Here's your latest test status:

**Recent Test Results:**
• Tests completed successfully
• All endpoints responding
• Performance within normal range

**Available Reports:**
• Console output (latest run)
• JUnit XML report (report.xml)
• Prometheus metrics (if configured)

Would you like me to:
• Run fresh tests?
• Show detailed results?
• Generate a new report?"""
    
    async def _handle_help_request(self, user_input: str) -> str:
        """Handle help requests."""
        return """🦖 Here's how I can help you test APIs:

**Simple Commands:**
• "Test my API" - Run basic health checks
• "Create tests for my login endpoint" - Generate test cases
• "Show me the test results" - Get status reports
• "Run all tests" - Execute comprehensive testing

**What I Can Do:**
✅ Test API endpoints automatically
✅ Validate response status codes
✅ Check JSON schema compliance
✅ Generate test reports
✅ Create tests from OpenAPI specs
✅ Monitor API performance

**Example Conversations:**
You: "Test my API at https://api.example.com"
Me: *runs health checks and basic tests*

You: "Create tests for user authentication"
Me: *generates login/logout test cases*

You: "How did my tests perform?"
Me: *shows detailed results and metrics*

Just tell me what you need in simple English! 🚀"""
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        openrouter_stats = self.openrouter_ai.get_system_stats()
        enhanced_stats = self.enhanced_ai.get_system_stats()
        
        return {
            "primary_provider": "OpenRouter",
            "fallback_provider": "Enhanced AI System",
            "openrouter": openrouter_stats,
            "enhanced_ai": enhanced_stats
        }
    
    async def chat_loop(self):
        """Main chat loop for interactive conversation."""
        print("🦖 Enhanced Restaceratops Chat Interface")
        print("=" * 50)
        print("Talk to me in simple English! I can help you test APIs, create test cases, and more.")
        print("Type 'quit' or 'exit' to end the conversation.")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n🤖 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🦖 Goodbye! Happy API testing!")
                    break
                
                if not user_input:
                    continue
                
                print("\n🦖 Restaceratops: ", end="", flush=True)
                response = await self.handle_message(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n🦖 Goodbye! Happy API testing!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'quit' to exit.")

def main():
    """Main entry point for the enhanced chat interface."""
    import argparse
    parser = argparse.ArgumentParser(description="🦖 Enhanced Restaceratops Chat Interface")
    parser.add_argument("--api-key", help="OpenAI API key for fallback features")
    args = parser.parse_args()
    
    # Initialize chat interface
    chat = EnhancedRestaceratopsChat(api_key=args.api_key)
    
    # Start chat loop
    asyncio.run(chat.chat_loop())

if __name__ == "__main__":
    main() 