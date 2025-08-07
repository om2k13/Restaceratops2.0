#!/usr/bin/env python3
"""
🦖 Enhanced AI System for Restaceratops
Intelligent AI system that provides expert API testing guidance
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import asyncio
import random
from openai import OpenAI

log = logging.getLogger("agent.enhanced_ai_system")

class OpenRouterAI:
    """OpenRouter AI provider using free Llama 3.2 3B model."""
    
    def __init__(self):
        """Initialize OpenRouter AI with free Llama 3.2 3B model."""
        # Get API key from environment - REQUIRED for real AI
        self.api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPEN_ROUTER_API_KEY")
        # Use a completely free model from OpenRouter (costs $0)
        self.model = "meta-llama/llama-3.2-3b-instruct:free"  # Completely free model
        self.base_url = "https://openrouter.ai/api/v1"
        
        if not self.api_key:
            log.error("❌ No OpenRouter API key found. Please set OPENROUTER_API_KEY environment variable.")
            raise ValueError("OpenRouter API key is required")
        
        # Initialize OpenAI client for OpenRouter
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        log.info(f"✅ OpenRouter AI configured with {self.model}")
        log.info(f"🔧 API key configured: {self.api_key[:10]}...")
    
    async def generate_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Generate response using OpenRouter's free Llama 3.2 3B model."""
        try:
            # Convert messages to OpenAI format
            openai_messages = []
            for msg in messages:
                openai_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Call OpenRouter API
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://restaceratops.com",
                    "X-Title": "Restaceratops",
                },
                model=self.model,  # "meta-llama/llama-3.2-3b-instruct:free"
                messages=openai_messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            response = completion.choices[0].message.content
            log.info(f"✅ OpenRouter response generated successfully")
            return response
                        
        except Exception as e:
            log.error(f"❌ Failed to call OpenRouter API with {self.model}: {e}")
            return None

class IntelligentAI:
    """Intelligent AI system that provides expert API testing guidance."""
    
    def __init__(self):
        """Initialize the intelligent AI system."""
        self.model = "Restaceratops AI v4.0"
        self.provider = "Local Intelligence"
        
        log.info(f"✅ Intelligent AI configured with {self.model}")
        log.info(f"🔧 Provider: {self.provider}")
    
    async def generate_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Generate intelligent response for API testing guidance."""
        try:
            # Get the user's message
            user_message = ""
            for msg in messages:
                if msg["role"] == "user":
                    user_message = msg["content"]
                    break
            
            if not user_message:
                return "I'm here to help with API testing. What would you like to know?"
            
            # Generate intelligent response based on user input
            response = self._generate_intelligent_response(user_message)
            log.info(f"✅ Intelligent response generated successfully")
            return response
                        
        except Exception as e:
            log.error(f"❌ Failed to generate intelligent response: {e}")
            return None
    
    def _generate_intelligent_response(self, user_input: str) -> str:
        """Generate intelligent response based on user input."""
        user_input_lower = user_input.lower()
        
        # API Testing Strategy
        if any(keyword in user_input_lower for keyword in ['strategy', 'approach', 'how to test', 'testing strategy']):
            return """🧪 **API Testing Strategy**

Here's a comprehensive approach to API testing:

## 1. **Functional Testing**
- Test all endpoints and HTTP methods
- Verify correct responses and status codes
- Test with valid and invalid data

## 2. **Data Validation Testing**
- Test required fields
- Test data types and formats
- Test boundary values and edge cases

## 3. **Error Handling Testing**
- Test 4xx error responses (400, 401, 403, 404, 422)
- Test 5xx error responses (500, 502, 503)
- Verify meaningful error messages

## 4. **Performance Testing**
- Test response times
- Test under load
- Monitor resource usage

## 5. **Security Testing**
- Test authentication and authorization
- Test input validation and sanitization
- Test for common vulnerabilities

Would you like me to help you create specific test cases for any of these areas?"""

        # Test Case Generation
        elif any(keyword in user_input_lower for keyword in ['generate', 'create', 'test case', 'yaml', 'test file']):
            return """📝 **Test Case Generation**

I can help you create comprehensive test cases! Here's a sample YAML structure:

```yaml
- name: "Test User Authentication"
  request:
    method: POST
    url: "https://api.example.com/auth/login"
    json:
      email: "test@example.com"
      password: "password123"
  expect:
    status: 200
    json:
      token: "string"
      user_id: "number"

- name: "Test Invalid Credentials"
  request:
    method: POST
    url: "https://api.example.com/auth/login"
    json:
      email: "invalid@example.com"
      password: "wrongpassword"
  expect:
    status: 401
    json:
      error: "Invalid credentials"
```

**What type of API are you testing?** I can help you create specific test cases for:
- Authentication APIs
- CRUD operations
- File upload/download
- Webhook testing
- GraphQL APIs

Just tell me your API endpoints and I'll generate the test cases!"""

        # Debugging Help
        elif any(keyword in user_input_lower for keyword in ['debug', 'error', 'failed', 'fix', 'help', 'issue']):
            return """🔧 **API Debugging Guide**

Let me help you debug your API issues! Here's a systematic approach:

## 1. **Check Response Status Codes**
- 2xx: Success (200, 201, 204)
- 4xx: Client errors (400, 401, 403, 404, 422)
- 5xx: Server errors (500, 502, 503)

## 2. **Common Issues & Solutions**

**401 Unauthorized:**
- Check authentication headers
- Verify API keys/tokens
- Ensure proper authorization

**400 Bad Request:**
- Validate request body format
- Check required fields
- Verify data types

**404 Not Found:**
- Check URL path
- Verify endpoint exists
- Check HTTP method

**500 Internal Server Error:**
- Check server logs
- Verify database connections
- Check external service dependencies

**3. Share Your Test Results**
Copy your test results and paste them here. I'll help you identify the specific issues and provide solutions!

What specific error are you encountering?"""

        # Performance Testing
        elif any(keyword in user_input_lower for keyword in ['performance', 'load', 'stress', 'speed', 'response time']):
            return """⚡ **Performance Testing Guide**

Here's how to test your API performance:

## 1. **Response Time Testing**
```yaml
- name: "Test Response Time"
  request:
    method: GET
    url: "https://api.example.com/users"
  expect:
    status: 200
    response_time: "< 1000ms"  # Should respond within 1 second
```

## 2. **Load Testing**
- Test with multiple concurrent requests
- Monitor response times under load
- Check for rate limiting

## 3. **Stress Testing**
- Test beyond normal capacity
- Monitor system behavior
- Check for graceful degradation

## 4. **Performance Metrics**
- Average response time
- 95th percentile response time
- Requests per second (RPS)
- Error rate under load

## 5. **Tools for Performance Testing**
- **Restaceratops**: Built-in performance testing
- **Apache Bench (ab)**: Command-line load testing
- **JMeter**: Advanced load testing
- **Artillery**: Node.js-based testing

Would you like me to help you set up specific performance tests for your API?"""

        # Security Testing
        elif any(keyword in user_input_lower for keyword in ['security', 'auth', 'authentication', 'authorization', 'vulnerability']):
            return """🔒 **Security Testing Guide**

Here's a comprehensive security testing approach:

## 1. **Authentication Testing**
```yaml
- name: "Test Missing Authentication"
  request:
    method: GET
    url: "https://api.example.com/protected"
  expect:
    status: 401

- name: "Test Invalid Token"
  request:
    method: GET
    url: "https://api.example.com/protected"
    headers:
      Authorization: "Bearer invalid-token"
  expect:
    status: 401
```

## 2. **Input Validation Testing**
- Test SQL injection attempts
- Test XSS payloads
- Test path traversal
- Test buffer overflow attempts

## 3. **Authorization Testing**
- Test role-based access control
- Test privilege escalation
- Test horizontal access control

## 4. **Data Protection**
- Test sensitive data exposure
- Check for proper encryption
- Verify secure headers

## 5. **Common Security Headers**
- `X-Frame-Options`
- `X-Content-Type-Options`
- `X-XSS-Protection`
- `Strict-Transport-Security`

Would you like me to help you create specific security test cases?"""

        # General API Help
        elif any(keyword in user_input_lower for keyword in ['api', 'rest', 'http', 'endpoint']):
            return """🌐 **API Testing Fundamentals**

Here are the essential concepts for API testing:

## 1. **HTTP Methods**
- **GET**: Retrieve data
- **POST**: Create new data
- **PUT**: Update entire resource
- **PATCH**: Partial update
- **DELETE**: Remove data

## 2. **Status Codes**
- **2xx Success**: 200 OK, 201 Created, 204 No Content
- **3xx Redirection**: 301 Moved, 304 Not Modified
- **4xx Client Error**: 400 Bad Request, 401 Unauthorized, 404 Not Found
- **5xx Server Error**: 500 Internal Server Error, 502 Bad Gateway

## 3. **Request Components**
- **Headers**: Authentication, Content-Type, Accept
- **Body**: JSON, XML, Form data
- **Query Parameters**: URL parameters
- **Path Parameters**: URL path variables

## 4. **Response Validation**
- Status code verification
- Response body validation
- Header validation
- Response time checking

## 5. **Test Types**
- **Positive Testing**: Valid inputs
- **Negative Testing**: Invalid inputs
- **Boundary Testing**: Edge cases
- **Integration Testing**: End-to-end flows

What specific aspect of API testing would you like to learn more about?"""

        # Greeting
        elif any(keyword in user_input_lower for keyword in ['hello', 'hi', 'hey', 'greetings']):
            return """🦖 **Hello! I'm Restaceratops AI**

I'm your expert API testing assistant, ready to help you build robust and reliable APIs!

## What I can help you with:
✅ **API Testing Strategy** - Design comprehensive testing approaches
✅ **Test Case Generation** - Create YAML test specifications
✅ **Debugging & Analysis** - Troubleshoot API issues
✅ **Performance Testing** - Optimize API performance
✅ **Security Testing** - Ensure API security
✅ **Best Practices** - Follow industry standards

## Quick Start:
1. **Test Strategy**: Ask me about testing approaches
2. **Generate Tests**: Share your API endpoints for test case generation
3. **Debug Issues**: Paste test results for debugging help
4. **Performance**: Get guidance on load and stress testing

**What would you like to work on today?** 🚀"""

        # Default response
        else:
            return """🤖 **I'm here to help with API testing!**

Based on your message: *"{user_input}"*

I can assist you with:

## 🧪 **API Testing**
- Test case generation
- YAML test specifications
- Debugging failed tests
- Performance optimization

## 🔧 **Common Tasks**
- Create test strategies
- Generate test data
- Analyze test results
- Security testing guidance

## 💡 **Quick Actions**
- **"Generate tests for my API"** - I'll help create test cases
- **"Help debug this error"** - Share test results for analysis
- **"Performance testing guide"** - Get optimization tips
- **"Security testing"** - Learn about API security

**What specific API testing challenge are you facing?** I'm ready to help! 🚀"""

class EnhancedAISystem:
    """Enhanced AI system using OpenRouter with Qwen3 Coder."""
    
    def __init__(self):
        """Initialize the enhanced AI system."""
        self.openrouter_ai = OpenRouterAI()
        self.conversation_history = []
        
        log.info("Enhanced AI system initialized with OpenRouter Llama 3.2 3B Instruct (free)")
    
    async def handle_conversation(self, user_input: str) -> str:
        """Handle user conversation using OpenRouter Meta Llama with real AI only."""
        try:
            # Always use real AI for all requests
            user_input_lower = user_input.lower().strip()
            
            # Create comprehensive system prompt for Llama 3.2 3B
            system_prompt = """You are Restaceratops, an advanced AI-powered API testing assistant built with the Meta Llama 3.2 3B Instruct model. Your core purpose is to provide expert-level guidance for API testing and development.

## Your Capabilities:
1. **API Testing Strategy**: Design comprehensive testing strategies for REST APIs, GraphQL, and microservices
2. **Test Case Generation**: Create detailed test cases including positive, negative, edge cases, and performance tests
3. **Code Generation**: Generate YAML test specifications, Python test scripts, and automation code
4. **Debugging & Analysis**: Analyze API responses, error codes, and provide troubleshooting guidance
5. **Performance Testing**: Guide users on load testing, stress testing, and performance optimization
6. **Security Testing**: Provide guidance on authentication, authorization, and security testing
7. **Best Practices**: Share industry best practices for API testing and quality assurance

## Your Response Style:
- Be professional yet approachable
- Provide actionable, practical advice
- Include code examples when relevant
- Use markdown formatting for clarity
- Focus specifically on API testing context
- Ask clarifying questions when needed

## Current Context:
You're integrated into the Restaceratops platform, which provides:
- Real-time test execution
- MongoDB data persistence
- Dashboard analytics
- File upload capabilities
- Report generation

Remember: You're helping users build robust, reliable APIs through comprehensive testing."""
            
            # Build messages array for Qwen3
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history (last 4 messages for context)
            for msg in self.conversation_history[-4:]:
                messages.append(msg)
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Get response from Qwen3
            ai_response = await self.openrouter_ai.generate_response(messages)
            
            if ai_response:
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                
                # Keep only last 10 messages to prevent memory issues
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]
                
                return ai_response
            else:
                # If AI fails, return a simple error message
                return "I'm sorry, I'm having trouble connecting to the AI service right now. Please try again in a moment."
            
        except Exception as e:
            log.error(f"Error in conversation: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try again."
    
    async def generate_intelligent_tests(self, api_spec: str, requirements: str) -> str:
        """Generate intelligent test cases using OpenRouter Qwen3 Coder."""
        try:
            # Create comprehensive test generation prompt
            system_prompt = """You are an expert API testing engineer using the Meta Llama 3.2 3B Instruct model. Your task is to generate comprehensive, production-ready test cases for REST APIs.

## Test Generation Guidelines:
1. **Coverage**: Include positive, negative, edge cases, and error scenarios
2. **Format**: Generate valid YAML test specifications
3. **Realism**: Use realistic test data and scenarios
4. **Best Practices**: Follow API testing best practices
5. **Documentation**: Include clear descriptions for each test

## Output Format:
- Valid YAML structure
- Clear test names and descriptions
- Proper request/response expectations
- Error handling scenarios
- Performance considerations where relevant"""

            user_prompt = f"""Generate comprehensive API test cases for the following specification:

**API Specification:**
{api_spec}

**Requirements:**
{requirements}

**Expected Output:**
- Valid YAML test specification
- Multiple test scenarios (positive, negative, edge cases)
- Clear assertions and expectations
- Error handling tests
- Performance considerations

Please provide a complete, ready-to-use test suite."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            log.info("🤖 Generating test cases with Qwen3-30b-a3b...")
            ai_response = await self.openrouter_ai.generate_response(messages)
            
            if ai_response:
                log.info("✅ Test cases generated successfully")
                return ai_response
            else:
                return "I'm sorry, I couldn't generate test cases right now. Please try again in a moment."
            
        except Exception as e:
            log.error(f"Error generating tests: {e}")
            return "I'm sorry, I encountered an error while generating test cases. Please try again."
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "provider": "OpenRouter",
            "model": self.openrouter_ai.model,
            "api_key_configured": bool(self.openrouter_ai.api_key),
            "conversation_history_length": len(self.conversation_history)
        }
    
    # All predefined functions removed - using only real AI
    
    # All predefined functions removed - using only real AI
    
    async def reset_system(self) -> str:
        """Reset the AI system."""
        try:
            self.conversation_history = []
            return "✅ AI system reset successfully"
        except Exception as e:
            log.error(f"Error resetting system: {e}")
            return "❌ Failed to reset AI system"

def get_enhanced_ai_system() -> EnhancedAISystem:
    """Get enhanced AI system instance."""
    return EnhancedAISystem()

async def test_enhanced_ai_system():
    """Test the enhanced AI system."""
    system = get_enhanced_ai_system()
    
    # Test conversation
    response = await system.handle_conversation("Hello! Can you help me with API testing?")
    print(f"Conversation Response: {response}")
    
    # Test stats
    stats = system.get_system_stats()
    print(f"System Stats: {stats}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_ai_system()) 