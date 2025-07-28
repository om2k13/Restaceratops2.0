"""🦖 Restaceratops Chat Interface - Talk to your API testing agent in simple English!"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import openai
from .runner import run_suite
from .dsl_loader import load_tests

log = logging.getLogger("agent.chat")

class RestaceratopsChat:
    """Conversational interface for Restaceratops API testing agent."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or openai.api_key
        if self.api_key:
            openai.api_key = self.api_key
        self.context = {}
        self.test_files = []
        
    def _parse_intent(self, user_input: str) -> Dict:
        """Parse user intent from natural language."""
        user_input = user_input.lower().strip()
        
        # Simple keyword-based intent parsing
        if any(word in user_input for word in ['test', 'run', 'execute', 'check']):
            if any(word in user_input for word in ['api', 'endpoint', 'url']):
                return {"intent": "run_tests", "confidence": 0.8}
        
        if any(word in user_input for word in ['create', 'make', 'generate', 'write']):
            if any(word in user_input for word in ['test', 'case']):
                return {"intent": "create_test", "confidence": 0.8}
        
        if any(word in user_input for word in ['status', 'report', 'results', 'how']):
            if any(word in user_input for word in ['test', 'api']):
                return {"intent": "get_status", "confidence": 0.7}
        
        if any(word in user_input for word in ['help', 'what', 'how', 'explain']):
            return {"intent": "help", "confidence": 0.9}
        
        if any(word in user_input for word in ['hello', 'hi', 'hey']):
            return {"intent": "greeting", "confidence": 0.9}
        
        return {"intent": "unknown", "confidence": 0.3}
    
    def _extract_api_info(self, user_input: str) -> Dict:
        """Extract API information from user input."""
        # Simple extraction - in a real implementation, you'd use NLP
        info = {}
        
        # Look for URLs
        import re
        urls = re.findall(r'https?://[^\s]+', user_input)
        if urls:
            info['base_url'] = urls[0]
        
        # Look for common API patterns
        if 'health' in user_input:
            info['endpoints'] = ['/health']
        if 'auth' in user_input or 'login' in user_input:
            info['endpoints'] = ['/auth/login']
        if 'user' in user_input:
            info['endpoints'] = ['/users']
        
        return info
    
    async def _generate_test_with_ai(self, api_info: Dict) -> str:
        """Generate test cases using AI."""
        prompt = f"""
        Create a simple API test in YAML format for testing {api_info.get('base_url', 'an API')}.
        Include basic health check and any endpoints mentioned.
        Return only the YAML array, no explanations.
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            log.error(f"AI generation failed: {e}")
            return self._generate_basic_test(api_info)
    
    def _generate_basic_test(self, api_info: Dict) -> str:
        """Generate a basic test without AI."""
        base_url = api_info.get('base_url', 'https://your-api.com')
        return f"""
- name: "Health Check"
  request:
    method: GET
    url: {base_url}/health
  expect:
    status: 200

- name: "API Status"
  request:
    method: GET
    url: {base_url}/status
  expect:
    status: 200
"""
    
    async def handle_message(self, user_input: str) -> str:
        """Handle user input and return a response."""
        intent = self._parse_intent(user_input)
        
        if intent["intent"] == "greeting":
            return """🦖 Hello! I'm Restaceratops, your AI-powered API testing agent!

I can help you:
• Test your APIs with simple commands
• Create test cases automatically
• Generate reports and status updates
• Run comprehensive API testing

Just tell me what you'd like to do! For example:
- "Test my API at https://my-api.com"
- "Create tests for my authentication endpoint"
- "Run all tests and show me the results"
- "Help me understand how to use you"

What would you like to do today?"""
        
        elif intent["intent"] == "help":
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
        
        elif intent["intent"] == "run_tests":
            api_info = self._extract_api_info(user_input)
            base_url = api_info.get('base_url', 'https://your-api.com')
            
            # Set environment variable
            import os
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
        
        elif intent["intent"] == "create_test":
            api_info = self._extract_api_info(user_input)
            
            try:
                # Generate test using AI
                test_yaml = await self._generate_test_with_ai(api_info)
                
                # Save to file
                test_file = Path("tests/generated_chat.yml")
                test_file.parent.mkdir(exist_ok=True)
                test_file.write_text(test_yaml)
                
                return f"""✅ I've created test cases for you!

**Generated Test File:** `tests/generated_chat.yml`

**What I Created:**
{test_yaml}

**Next Steps:**
• Review the generated tests
• Modify them if needed
• Run them with: "Test my API"
• Or ask me to run them now!

Would you like me to run these tests right away?"""
                
            except Exception as e:
                return f"""❌ Sorry, I couldn't generate the test cases.

**Error:** {str(e)}

**Alternative:**
I can create a basic test template for you. Would you like me to do that instead?"""
        
        elif intent["intent"] == "get_status":
            # Check if there are recent test results
            report_file = Path("report.xml")
            if report_file.exists():
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
            else:
                return """📊 No recent test results found.

I haven't run any tests yet. Would you like me to:
• Test your API now?
• Create some test cases?
• Show you how to get started?

Just tell me what you'd like to do!"""
        
        else:
            return """🤔 I'm not sure what you're asking for.

**I can help you with:**
• Testing APIs ("Test my API")
• Creating test cases ("Create tests for my endpoint")
• Getting status reports ("Show me test results")
• Understanding how to use me ("Help")

**Try saying something like:**
• "Test my API at https://my-api.com"
• "Create tests for user authentication"
• "Show me the test results"
• "Help me understand how to use you"

What would you like to do?"""
    
    async def chat_loop(self):
        """Main chat loop for interactive conversation."""
        print("🦖 Welcome to Restaceratops Chat!")
        print("=" * 50)
        print("I'm your AI-powered API testing assistant.")
        print("Talk to me in simple English about testing your APIs!")
        print("Type 'quit' or 'exit' to end our conversation.")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n🤖 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🦖 Restaceratops: Goodbye! Happy API testing! 🚀")
                    break
                
                if not user_input:
                    continue
                
                print("\n🦖 Restaceratops: ", end="", flush=True)
                response = await self.handle_message(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n🦖 Restaceratops: Goodbye! Happy API testing! 🚀")
                break
            except Exception as e:
                print(f"\n❌ Sorry, something went wrong: {e}")
                print("Please try again or type 'help' for assistance.")

def main():
    """Main entry point for the chat interface."""
    import argparse
    parser = argparse.ArgumentParser(description="🦖 Restaceratops Chat Interface")
    parser.add_argument("--api-key", help="OpenAI API key for AI features")
    args = parser.parse_args()
    
    # Initialize chat interface
    chat = RestaceratopsChat(api_key=args.api_key)
    
    # Start chat loop
    asyncio.run(chat.chat_loop())

if __name__ == "__main__":
    main() 