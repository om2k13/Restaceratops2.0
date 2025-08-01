#!/usr/bin/env python3
"""
🦖 Enhanced AI System for Restaceratops
Simplified AI system using OpenRouter with Qwen3 Coder model
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import asyncio

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory

from core.models.vector_store import get_vector_store, setup_vector_store

log = logging.getLogger("agent.enhanced_ai_system")

class OpenRouterAI:
    """OpenRouter AI provider using Qwen3 Coder model."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "qwen/qwen3-coder:free"
        self.base_url = "https://openrouter.ai/api/v1"
        
        if not self.api_key:
            log.warning("⚠️ No OpenRouter API key configured")
        else:
            log.info(f"✅ OpenRouter AI configured with {self.model}")
    
    def create_llm(self) -> Optional[Any]:
        """Create OpenRouter LLM instance."""
        if not self.api_key:
            log.warning("⚠️ No OpenRouter API key provided")
            return None
        
        try:
            log.info(f"🤖 Creating OpenRouter LLM with model: {self.model}")
            llm = ChatOpenAI(
                model=self.model,
                openai_api_key=self.api_key,
                openai_api_base=self.base_url,
                temperature=0.7,
                max_tokens=2000,
                timeout=30
            )
            log.info("✅ OpenRouter LLM created successfully")
            return llm
        except Exception as e:
            log.error(f"❌ Failed to create OpenRouter LLM: {e}")
            return None

class EnhancedAISystem:
    """Enhanced AI system using OpenRouter with Qwen3 Coder."""
    
    def __init__(self):
        """Initialize the enhanced AI system."""
        self.openrouter_ai = OpenRouterAI()
        self.conversation_memory = ConversationBufferWindowMemory(
            k=10,
            return_messages=True,
            memory_key="chat_history"
        )
        
        # Initialize vector store
        self.vector_store = None
        try:
            self.vector_store = get_vector_store()
            log.info("✅ Vector store initialized")
        except Exception as e:
            log.warning(f"⚠️ Vector store initialization failed: {e}")
        
        log.info("Enhanced AI system initialized with OpenRouter Qwen3 Coder")
    
    async def handle_conversation(self, user_input: str) -> str:
        """Handle user conversation using OpenRouter Qwen3 Coder with proper AI integration."""
        try:
            llm = self.openrouter_ai.create_llm()
            if not llm:
                log.warning("⚠️ No LLM available, using fallback")
                return self._get_intelligent_fallback_response(user_input)
            
            # Get conversation history
            chat_history = self.conversation_memory.chat_memory.messages
            
            # Create comprehensive system prompt for Qwen3
            system_prompt = """You are Restaceratops, an advanced AI-powered API testing assistant built with the Qwen3 Coder model. Your core purpose is to provide expert-level guidance for API testing and development.

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
            messages = []
            
            # Add system message
            messages.append(SystemMessage(content=system_prompt))
            
            # Add conversation history (last 6 messages for context)
            for msg in chat_history[-6:]:
                if isinstance(msg, HumanMessage):
                    messages.append(HumanMessage(content=msg.content))
                elif isinstance(msg, AIMessage):
                    messages.append(AIMessage(content=msg.content))
            
            # Add current user input
            messages.append(HumanMessage(content=user_input))
            
            # Get response from Qwen3
            log.info("🤖 Calling Qwen3 Coder model...")
            response = await llm.agenerate([messages])
            ai_response = response.generations[0][0].text
            
            # Update conversation memory
            self.conversation_memory.chat_memory.add_user_message(user_input)
            self.conversation_memory.chat_memory.add_ai_message(ai_response)
            
            log.info("✅ Qwen3 response generated successfully")
            return ai_response
            
        except Exception as e:
            log.error(f"Error in conversation: {e}")
            return self._get_intelligent_fallback_response(user_input)
    
    async def generate_intelligent_tests(self, api_spec: str, requirements: str) -> str:
        """Generate intelligent test cases using OpenRouter Qwen3 Coder."""
        try:
            llm = self.openrouter_ai.create_llm()
            if not llm:
                log.warning("⚠️ No LLM available for test generation, using fallback")
                return self._get_fallback_test_template(api_spec)
            
            # Create comprehensive test generation prompt
            system_prompt = """You are an expert API testing engineer using the Qwen3 Coder model. Your task is to generate comprehensive, production-ready test cases for REST APIs.

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
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            log.info("🤖 Generating test cases with Qwen3 Coder...")
            response = await llm.agenerate([messages])
            generated_tests = response.generations[0][0].text
            
            log.info("✅ Test cases generated successfully")
            return generated_tests
            
        except Exception as e:
            log.error(f"Error generating tests: {e}")
            return self._get_fallback_test_template(api_spec)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "provider": "OpenRouter",
            "model": self.openrouter_ai.model,
            "api_key_configured": bool(self.openrouter_ai.api_key),
            "vector_store_available": self.vector_store is not None,
            "memory_messages": len(self.conversation_memory.chat_memory.messages)
        }
    
    def _get_intelligent_fallback_response(self, user_input: str) -> str:
        """Get intelligent fallback response using logic-based analysis."""
        user_input_lower = user_input.lower()
        
        # Analyze user input and provide intelligent responses
        if "authentication" in user_input_lower or "auth" in user_input_lower:
            return self._get_authentication_guidance(user_input)
        elif "test" in user_input_lower and "api" in user_input_lower:
            return self._get_api_testing_guidance(user_input)
        elif "error" in user_input_lower or "debug" in user_input_lower:
            return self._get_debugging_guidance(user_input)
        elif "performance" in user_input_lower or "speed" in user_input_lower:
            return self._get_performance_guidance(user_input)
        elif "security" in user_input_lower:
            return self._get_security_guidance(user_input)
        elif "generate" in user_input_lower and "test" in user_input_lower:
            return self._get_test_generation_guidance(user_input)
        else:
            return self._get_general_api_guidance(user_input)
    
    def _get_authentication_guidance(self, user_input: str) -> str:
        """Provide authentication testing guidance."""
        return f"""🔐 **Authentication Testing Guidance**

Based on your question: "{user_input}"

**Essential Authentication Tests:**
1. **Valid Credentials Test**
   - Test with correct username/password
   - Verify 200 OK response
   - Check for valid JWT/token in response

2. **Invalid Credentials Test**
   - Test with wrong username/password
   - Verify 401 Unauthorized response
   - Check error message clarity

3. **Missing Credentials Test**
   - Test without authentication headers
   - Verify 401 Unauthorized response

4. **Token Expiration Test**
   - Test with expired tokens
   - Verify 401 Unauthorized response

5. **Role-Based Access Test**
   - Test different user roles
   - Verify appropriate access levels

**Sample Test Cases:**
```yaml
- name: "Valid Authentication"
  request:
    method: POST
    url: "/api/auth/login"
    json:
      username: "testuser"
      password: "testpass"
  expect:
    status: 200
    json:
      token: "{{token}}"

- name: "Invalid Authentication"
  request:
    method: POST
    url: "/api/auth/login"
    json:
      username: "wronguser"
      password: "wrongpass"
  expect:
    status: 401
```

Would you like me to help you create specific authentication test cases for your API?"""
    
    def _get_api_testing_guidance(self, user_input: str) -> str:
        """Provide API testing guidance."""
        return f"""🧪 **API Testing Best Practices**

Based on your question: "{user_input}"

**Comprehensive API Testing Strategy:**

1. **Functional Testing**
   - Test all endpoints and methods
   - Verify correct responses
   - Test edge cases and boundaries

2. **Data Validation Testing**
   - Test with valid data
   - Test with invalid data
   - Test with missing required fields

3. **Error Handling Testing**
   - Test 4xx error responses
   - Test 5xx error responses
   - Verify meaningful error messages

4. **Performance Testing**
   - Test response times
   - Test under load
   - Monitor resource usage

**Sample Test Structure:**
```yaml
- name: "GET User Profile"
  request:
    method: GET
    url: "/api/users/123"
    headers:
      Authorization: "Bearer {{token}}"
  expect:
    status: 200
    json:
      id: 123
      name: "{{string}}"

- name: "Create User"
  request:
    method: POST
    url: "/api/users"
    json:
      name: "New User"
      email: "user@example.com"
  expect:
    status: 201
    json:
      id: "{{number}}"
```

**Testing Tools Recommendation:**
- Use Restaceratops for automated testing
- Monitor with real-time dashboards
- Generate comprehensive reports

Need help setting up specific test cases?"""
    
    def _get_debugging_guidance(self, user_input: str) -> str:
        """Provide debugging guidance."""
        return f"""🐛 **API Debugging Guide**

Based on your question: "{user_input}"

**Systematic Debugging Approach:**

1. **Check Request Details**
   - Verify HTTP method
   - Check URL and parameters
   - Validate request headers
   - Review request body

2. **Analyze Response**
   - Check status codes
   - Review response headers
   - Examine response body
   - Look for error messages

3. **Common Issues & Solutions**
   - **401 Unauthorized**: Check authentication
   - **400 Bad Request**: Validate request format
   - **404 Not Found**: Verify endpoint URL
   - **500 Internal Error**: Check server logs

4. **Debugging Tools**
   - Use browser DevTools
   - Check network tab
   - Review server logs
   - Use API testing tools

**Debugging Checklist:**
```yaml
- name: "Debug Request"
  request:
    method: "{{method}}"
    url: "{{url}}"
    headers: "{{headers}}"
    body: "{{body}}"
  expect:
    status: "{{expected_status}}"
  debug:
    log_request: true
    log_response: true
    validate_schema: true
```

**Quick Debug Steps:**
1. Test with simple tools (curl, Postman)
2. Check API documentation
3. Verify authentication
4. Review error logs
5. Test with minimal data

Need help debugging a specific issue?"""
    
    def _get_performance_guidance(self, user_input: str) -> str:
        """Provide performance testing guidance."""
        return f"""⚡ **Performance Testing Guide**

Based on your question: "{user_input}"

**Performance Testing Strategy:**

1. **Response Time Testing**
   - Measure individual request times
   - Set acceptable thresholds
   - Monitor under different loads

2. **Load Testing**
   - Test with multiple concurrent users
   - Identify breaking points
   - Monitor resource usage

3. **Stress Testing**
   - Test beyond normal capacity
   - Identify failure modes
   - Test recovery mechanisms

**Performance Metrics:**
- **Response Time**: < 200ms for simple requests
- **Throughput**: Requests per second
- **Error Rate**: < 1% under normal load
- **Resource Usage**: CPU, memory, network

**Sample Performance Test:**
```yaml
- name: "Performance Test"
  request:
    method: GET
    url: "/api/users"
  expect:
    status: 200
    response_time: "< 500ms"
  performance:
    concurrent_users: 10
    duration: "30s"
    ramp_up: "10s"
```

**Optimization Tips:**
- Use caching where appropriate
- Optimize database queries
- Implement pagination
- Use CDN for static content
- Monitor and alert on performance

Need help setting up performance tests?"""
    
    def _get_security_guidance(self, user_input: str) -> str:
        """Provide security testing guidance."""
        return f"""🔒 **Security Testing Guide**

Based on your question: "{user_input}"

**Security Testing Checklist:**

1. **Authentication Security**
   - Test password strength requirements
   - Verify secure token storage
   - Test session management
   - Check for brute force protection

2. **Authorization Testing**
   - Test role-based access control
   - Verify permission boundaries
   - Test privilege escalation
   - Check resource isolation

3. **Input Validation**
   - Test SQL injection prevention
   - Test XSS protection
   - Test file upload security
   - Validate input sanitization

4. **Data Protection**
   - Verify HTTPS usage
   - Check sensitive data encryption
   - Test data exposure prevention
   - Verify GDPR compliance

**Security Test Examples:**
```yaml
- name: "SQL Injection Test"
  request:
    method: POST
    url: "/api/search"
    json:
      query: "'; DROP TABLE users; --"
  expect:
    status: 400
    not_contains: "error in your SQL syntax"

- name: "XSS Test"
  request:
    method: POST
    url: "/api/comments"
    json:
      content: "<script>alert('xss')</script>"
  expect:
    status: 400
    not_contains: "<script>"
```

**Security Best Practices:**
- Use HTTPS everywhere
- Implement proper authentication
- Validate all inputs
- Use parameterized queries
- Regular security audits

Need help implementing security tests?"""
    
    def _get_test_generation_guidance(self, user_input: str) -> str:
        """Provide test generation guidance."""
        return f"""🎯 **Test Generation Guide**

Based on your question: "{user_input}"

**Automated Test Generation Strategy:**

1. **OpenAPI Specification Analysis**
   - Parse API documentation
   - Generate tests for all endpoints
   - Create positive and negative tests
   - Include edge cases

2. **Test Categories to Generate**
   - **Happy Path Tests**: Valid requests
   - **Error Tests**: Invalid inputs
   - **Boundary Tests**: Edge cases
   - **Performance Tests**: Load scenarios

3. **Test Data Generation**
   - Generate realistic test data
   - Create varied input scenarios
   - Include boundary values
   - Test data validation

**Generated Test Structure:**
```yaml
# Generated from OpenAPI spec
- name: "GET /api/users - Success"
  request:
    method: GET
    url: "/api/users"
    headers:
      Authorization: "Bearer {{token}}"
  expect:
    status: 200
    json_schema:
      type: array
      items:
        type: object
        properties:
          id: {type: integer}
          name: {type: string}

- name: "POST /api/users - Invalid Data"
  request:
    method: POST
    url: "/api/users"
    json:
      email: "invalid-email"
  expect:
    status: 400
    json:
      error: "Invalid email format"
```

**Test Generation Tools:**
- Use Restaceratops AI for intelligent generation
- Parse OpenAPI/Swagger specifications
- Generate comprehensive test suites
- Include assertions and validations

Ready to generate tests for your API?"""
    
    def _get_general_api_guidance(self, user_input: str) -> str:
        """Provide general API guidance."""
        return f"""🦖 **Restaceratops API Testing Assistant**

Based on your question: "{user_input}"

**How I Can Help You:**

🔧 **API Testing Services:**
- Generate comprehensive test cases
- Execute automated API tests
- Monitor test performance
- Generate detailed reports

🤖 **AI-Powered Features:**
- Intelligent test generation
- Smart debugging assistance
- Performance optimization tips
- Security testing guidance

📊 **Real-time Monitoring:**
- Live test execution tracking
- Performance metrics dashboard
- Error analysis and reporting
- Success rate monitoring

**Quick Actions:**
1. **Test Generation**: Upload your API spec or describe endpoints
2. **Test Execution**: Run existing test suites
3. **Debugging**: Get help with API issues
4. **Performance**: Analyze response times and throughput

**Sample Commands:**
- "Generate tests for my user API"
- "Help me debug a 500 error"
- "Create performance tests"
- "Test authentication endpoints"

**Current Status:**
- ✅ Test execution engine: Ready
- ✅ Report generation: Active
- ✅ Dashboard monitoring: Live
- ⚠️ AI model: Using intelligent fallback (API key needed for full AI)

I'm here to help you build robust, reliable APIs! What would you like to work on?"""
    
    def _get_fallback_test_template(self, api_spec: str) -> str:
        """Get fallback test template."""
        return f"""# API Test Template

## Test Cases for: {api_spec}

### 1. Basic Functionality Tests
```yaml
- name: "Test basic GET request"
  method: "GET"
  url: "/api/endpoint"
  expected_status: 200
  validate:
    - "response contains expected data"
    - "response time < 1000ms"
```

### 2. Error Handling Tests
```yaml
- name: "Test invalid input"
  method: "POST"
  url: "/api/endpoint"
  body: "{{invalid_data}}"
  expected_status: 400
  validate:
    - "error message is clear"
```

### 3. Authentication Tests
```yaml
- name: "Test without authentication"
  method: "GET"
  url: "/api/protected-endpoint"
  headers: {{}}
  expected_status: 401
```

Please customize these templates based on your specific API requirements."""
    
    async def reset_system(self) -> str:
        """Reset the AI system."""
        try:
            self.conversation_memory.clear()
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