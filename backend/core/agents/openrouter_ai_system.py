#!/usr/bin/env python3
"""
🦖 OpenRouter AI System for Restaceratops
Multi-model AI system using OpenRouter with automatic fallback
"""

import os
import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

log = logging.getLogger("agent.openrouter_ai")

class OpenRouterAISystem:
    """Advanced AI system using OpenRouter with multiple free models and automatic fallback."""
    
    def __init__(self):
        """Initialize the OpenRouter AI system."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.current_model_index = 0
        self.failed_models = set()
        
        # List of free models to try (in order of preference)
        self.free_models = [
            "openai/gpt-3.5-turbo",           # Reliable, fast
            "anthropic/claude-3-haiku",       # Good reasoning
            "google/gemini-2.5-flash-lite",   # Fast responses
            "qwen/qwen3-235b-a22b-2507:free", # High quality
            "z-ai/glm-4.5-air",              # Good for tasks
            "meta-llama/llama-3.1-8b-instruct", # Reliable
            "microsoft/phi-3.5-mini-128k",   # Fast
            "deepseek-ai/deepseek-coder-6.7b-instruct", # Good for code
            "mistralai/mistral-7b-instruct", # Reliable
            "nousresearch/nous-hermes-2-mixtral-8x7b-dpo" # High quality
        ]
        
        # Track usage for rate limiting
        self.model_usage = {}
        
        log.info(f"Initialized OpenRouter AI system with {len(self.free_models)} free models")
    
    def get_next_working_model(self) -> Optional[str]:
        """Get the next working model, skipping failed ones."""
        attempts = 0
        while attempts < len(self.free_models):
            model = self.free_models[self.current_model_index]
            
            if model not in self.failed_models:
                return model
            
            # Move to next model
            self.current_model_index = (self.current_model_index + 1) % len(self.free_models)
            attempts += 1
        
        # If all models failed, reset and try again
        self.failed_models.clear()
        self.current_model_index = 0
        return self.free_models[0] if self.free_models else None
    
    def mark_model_failed(self, model: str, reason: str = "unknown"):
        """Mark a model as failed."""
        self.failed_models.add(model)
        log.warning(f"Marked model {model} as failed: {reason}")
    
    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> Optional[str]:
        """Send a chat completion request with automatic fallback."""
        if not self.api_key:
            log.error("No OpenRouter API key configured")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Try each model until one works
        for attempt in range(len(self.free_models)):
            model = self.get_next_working_model()
            if not model:
                log.error("All models have failed")
                return None
            
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        content = result['choices'][0]['message']['content']
                        
                        # Success! Move to next model for next request
                        self.current_model_index = (self.current_model_index + 1) % len(self.free_models)
                        
                        log.info(f"Successfully used model: {model}")
                        return content
                    
                    elif response.status_code == 429:
                        # Rate limited - mark as failed temporarily
                        self.mark_model_failed(model, "rate_limited")
                        log.warning(f"Rate limited on model: {model}")
                    
                    elif response.status_code == 402:
                        # Payment required - mark as failed
                        self.mark_model_failed(model, "payment_required")
                        log.warning(f"Payment required for model: {model}")
                    
                    else:
                        # Other error - mark as failed
                        self.mark_model_failed(model, f"status_{response.status_code}")
                        log.warning(f"Model {model} failed with status {response.status_code}")
                
            except Exception as e:
                self.mark_model_failed(model, str(e))
                log.error(f"Error with model {model}: {e}")
        
        log.error("All models failed")
        return None
    
    async def generate_api_tests(self, api_spec: str, requirements: str) -> str:
        """Generate API tests using OpenRouter AI."""
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
        """Handle general conversation using OpenRouter AI."""
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
            "total_models": len(self.free_models),
            "working_models": len(self.free_models) - len(self.failed_models),
            "failed_models": len(self.failed_models),
            "current_model": self.free_models[self.current_model_index] if self.free_models else None,
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
    print("🦖 Testing OpenRouter AI System...")
    
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