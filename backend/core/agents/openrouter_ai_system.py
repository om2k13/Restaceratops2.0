#!/usr/bin/env python3
"""
🦖 OpenRouter AI System for Restaceratops
Single-model AI system using Qwen3 Coder from OpenRouter
Upgraded to use OpenAI Python SDK for better integration
"""

import os
import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

log = logging.getLogger("agent.openrouter_ai")

class OpenRouterAISystem:
    """AI system using OpenRouter with Qwen3 Coder model only."""
    
    def __init__(self):
        """Initialize the OpenRouter AI system with Qwen3 Coder only."""
        from dotenv import load_dotenv
        load_dotenv()
        
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        # Initialize OpenAI client for OpenRouter
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
        # Use ONLY Qwen3 Coder model
        self.model = "qwen/qwen3-coder:free"
        
        log.info(f"Initialized OpenRouter AI system with Qwen3 Coder model: {self.model}")
    
    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> Optional[str]:
        """Send a chat completion request using Qwen3 Coder only."""
        if not self.api_key:
            log.error("No OpenRouter API key configured")
            return None
        
        try:
            # Use OpenAI SDK with OpenRouter
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://restaceratops.com",
                    "X-Title": "Restaceratops API Testing Agent"
                },
                extra_body={},
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            content = completion.choices[0].message.content
            
            # Log detailed conversation for debugging
            user_message = next((msg['content'] for msg in messages if msg['role'] == 'user'), 'Unknown')
            log.info(f"=== AI Conversation Log ===")
            log.info(f"Model: {self.model}")
            log.info(f"User Input: {user_message}")
            log.info(f"AI Response: {content}")
            log.info(f"==========================")
            
            log.info(f"Successfully used Qwen3 Coder model")
            return content
            
        except Exception as e:
            log.error(f"Error with Qwen3 Coder model: {e}")
            return None
    
    async def generate_api_tests(self, api_spec: str, requirements: str) -> str:
        """Generate API tests using Qwen3 Coder."""
        messages = [
            {
                "role": "system",
                "content": """You are an expert API testing specialist. Generate comprehensive YAML test cases for REST APIs.

IMPORTANT: Make your responses user-friendly and easy to understand. Use simple language and clear explanations.

Your response should include:
1. A friendly summary of what tests were created
2. Clear explanations of what each test does
3. Valid YAML test cases that include:
   - HTTP method, URL, headers, body
   - Expected status codes and response validation
   - Variable capture and reuse
   - Error handling scenarios
   - Performance testing

Format your response with:
- Friendly introduction explaining what you're creating
- Clear section headers
- Simple explanations for each test
- Clean YAML formatting
- Summary of what the user can do next

Make it easy for non-technical users to understand what each test does and how to use them."""
            },
            {
                "role": "user",
                "content": f"Generate API test cases for:\n\nAPI Specification:\n{api_spec}\n\nRequirements:\n{requirements}"
            }
        ]
        
        response = await self.chat_completion(messages, max_tokens=2000)
        if response:
            return response
        else:
            return self._get_fallback_test_template(api_spec)
    
    async def handle_conversation(self, user_input: str) -> str:
        """Handle general conversation using Qwen3 Coder."""
        messages = [
            {
                "role": "system",
                "content": """You are Restaceratops, an AI-powered API testing agent. You help users test APIs, create test cases, and debug issues.

IMPORTANT: Make your responses user-friendly and easy to understand for non-technical users. Use simple language, avoid jargon, and explain things clearly.

When generating test cases:
- Use simple, clear language
- Explain what each test does in plain English
- Provide step-by-step instructions
- Use emojis and formatting to make it easy to read
- Focus on practical, actionable advice

Be helpful, friendly, and provide practical advice for API testing. You can:
- Run API tests
- Generate test cases
- Help debug issues
- Explain testing concepts
- Provide best practices

Keep responses concise but informative and always user-friendly."""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
        
        response = await self.chat_completion(messages, max_tokens=500)
        if response:
            return response
        else:
            return self._get_fallback_response(user_input)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "provider": "OpenRouter",
            "total_models": 1,
            "working_models": 1,
            "failed_models": 0,
            "current_model": self.model,
            "api_key_configured": bool(self.api_key)
        }
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Fallback response when AI is unavailable."""
        return f"""🦖 Hello! I'm Restaceratops, your API testing agent.

I can help you with:
• 🧪 API Testing: Run comprehensive tests on your APIs
• 📝 Test Generation: Create test cases from OpenAPI specs
• 🔍 Troubleshooting: Debug API issues and errors
• 📊 Reporting: Generate detailed test reports

**Quick Start:**
• "Test my API at https://your-api.com"
• "Create tests for authentication"
• "Show me test results"

What would you like to work on today?"""
    
    def _get_fallback_test_template(self, api_spec: str) -> str:
        """Fallback test template when AI is unavailable."""
        return f"""# Generated API Tests for {api_spec}

- name: "Health Check"
  request:
    method: GET
    url: https://your-api.com/health
  expect:
    status: 200

- name: "Authentication Test"
  request:
    method: POST
    url: https://your-api.com/auth/login
    json:
      username: "testuser"
      password: "testpass"
  expect:
    status: 200
    save:
      token: $.access_token

- name: "Protected Endpoint Test"
  request:
    method: GET
    url: https://your-api.com/protected
    headers:
      Authorization: "Bearer {token}"
  expect:
    status: 200"""

# Global instance
_openrouter_ai = None

def get_openrouter_ai_system() -> OpenRouterAISystem:
    """Get the global OpenRouter AI system instance."""
    global _openrouter_ai
    if _openrouter_ai is None:
        _openrouter_ai = OpenRouterAISystem()
    return _openrouter_ai

async def test_openrouter_system():
    """Test the OpenRouter AI system."""
    print("🦖 Testing OpenRouter AI System with Qwen3 Coder...")
    
    ai = get_openrouter_ai_system()
    
    # Test conversation
    print("\n🧪 Testing conversation...")
    response = await ai.handle_conversation("Hello! Can you help me test my API?")
    print(f"Response: {response[:200]}...")
    
    # Test API test generation
    print("\n🧪 Testing API test generation...")
    tests = await ai.generate_api_tests(
        "https://httpbin.org",
        "Create basic health check and authentication tests"
    )
    print(f"Generated tests: {tests[:200]}...")
    
    # Show stats
    print("\n📊 System Stats:")
    stats = ai.get_system_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ OpenRouter AI system test completed!")

if __name__ == "__main__":
    asyncio.run(test_openrouter_system()) 