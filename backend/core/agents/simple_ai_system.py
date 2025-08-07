#!/usr/bin/env python3
"""
🦖 Simple AI System for Restaceratops
Works without external API keys - provides intelligent responses
"""

import logging
from typing import Dict, Any

log = logging.getLogger("agent.simple_ai_system")

class SimpleAISystem:
    """Simple AI system that provides intelligent responses without external APIs."""
    
    def __init__(self):
        """Initialize the simple AI system."""
        log.info("Simple AI system initialized - no external API required")
    
    async def handle_conversation(self, user_input: str) -> str:
        """Handle user conversation with intelligent responses."""
        try:
            user_input_lower = user_input.lower().strip()
            
            # Handle debugging requests (when user pastes test results)
            if any(keyword in user_input_lower for keyword in ['solve', 'fix', 'error', 'failed', 'debug', 'help with', 'debbug']):
                return self._get_debugging_guidance(user_input)
            
            # Handle greetings
            if any(greeting in user_input_lower for greeting in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']):
                if not any(test_keyword in user_input_lower for test_keyword in ['status', 'response', 'failed', 'error', 'ms', 'code']):
                    return self._get_greeting_response()
            
            # Handle API testing questions
            if any(keyword in user_input_lower for keyword in ['test api', 'api testing', 'how to test', 'testing api']):
                return self._get_api_testing_guidance(user_input)
            
            # Handle general API questions
            if any(keyword in user_input_lower for keyword in ['api', 'rest', 'http', 'endpoint']):
                return self._get_general_api_guidance(user_input)
            
            # Default response
            return self._get_intelligent_fallback_response(user_input)
            
        except Exception as e:
            log.error(f"Error in conversation: {e}")
            return self._get_intelligent_fallback_response(user_input)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "provider": "Simple AI",
            "model": "Local Intelligence",
            "api_key_configured": False,
            "conversation_history_length": 0,
            "status": "active"
        }
    
    def _get_greeting_response(self) -> str:
        """Provide friendly greeting responses."""
        return """🦖 Hello! I'm Restaceratops, your AI-powered API testing assistant.

I can help you with:
✅ API testing strategies and best practices
✅ Test case generation and automation
✅ Debugging API issues and errors
✅ Performance testing and optimization
✅ Security testing guidance
✅ Code generation for test scripts

How can I assist you with API testing today?"""
    
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
        """Provide debugging guidance for test failures and errors."""
        
        # Check if user pasted test results
        user_input_lower = user_input.lower()
        test_result_indicators = [
            'failed', 'error', 'status', 'response', 'ms', 'code', 
            'expected status', 'got', 'test name', 'response time', 'response code'
        ]
        
        if any(indicator in user_input_lower for indicator in test_result_indicators):
            return self._analyze_test_results(user_input)
        
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

**💡 Pro Tip**: If you have specific test results that failed, paste them here and I'll help you analyze the exact issue!

Need help debugging a specific issue?"""
    
    def _analyze_test_results(self, user_input: str) -> str:
        """Analyze test results and provide specific solutions."""
        
        # Extract common patterns from test results
        lines = user_input.split('\n')
        status_codes = []
        errors = []
        
        for line in lines:
            line_lower = line.lower()
            # Extract status codes
            if any(char.isdigit() for char in line):
                words = line.split()
                for i, word in enumerate(words):
                    if word.isdigit() and len(word) == 3:  # Likely HTTP status code
                        status_codes.append(word)
                    elif word.lower() == 'got' and i + 1 < len(words) and words[i + 1].isdigit():
                        status_codes.append(words[i + 1])
                    elif word.lower() == 'status' and i + 1 < len(words) and words[i + 1].isdigit():
                        status_codes.append(words[i + 1])
            
            # Extract errors and failed tests
            if 'error' in line_lower or 'failed' in line_lower:
                errors.append(line.strip())
        
        # Provide specific guidance based on patterns
        if status_codes:
            status_analysis = self._analyze_status_codes(status_codes)
        else:
            status_analysis = ""
            
        if errors:
            error_analysis = self._analyze_errors(errors)
        else:
            error_analysis = ""
            
        return f"""🔍 **Test Results Analysis**

I've analyzed your test results and found the following issues:

{status_analysis}
{error_analysis}

**Recommended Solutions:**

1. **Immediate Actions:**
   - Verify the API endpoint is accessible
   - Check if authentication is required
   - Validate request format and headers
   - Test with a simple tool like curl first

2. **Debugging Steps:**
   ```bash
   # Test the endpoint manually
   curl -X GET "YOUR_API_URL" -H "Content-Type: application/json"
   
   # Check response headers
   curl -I "YOUR_API_URL"
   
   # Test with verbose output
   curl -v "YOUR_API_URL"
   ```

3. **Common Fixes:**
   - **401/403**: Add proper authentication headers
   - **404**: Verify the URL is correct
   - **400**: Check request body format
   - **500**: Server issue, check API logs

4. **Test Case Improvements:**
   ```yaml
   - name: "Improved Test Case"
     request:
       method: GET
       url: "YOUR_API_URL"
       headers:
         Authorization: "Bearer YOUR_TOKEN"
         Content-Type: "application/json"
     expect:
       status: 200
       timeout: 10000  # 10 seconds
   ```

**Next Steps:**
1. Try the manual curl commands above
2. Check the API documentation
3. Verify your test environment
4. Run the improved test case

Would you like me to help you create a specific test case for your API?"""
    
    def _analyze_status_codes(self, status_codes: list) -> str:
        """Analyze status codes and provide specific guidance."""
        analysis = "**Status Code Analysis:**\n"
        
        for code in status_codes:
            if code == '401':
                analysis += f"- **401 Unauthorized**: Authentication required. Add proper headers.\n"
            elif code == '403':
                analysis += f"- **403 Forbidden**: Access denied. Check permissions.\n"
            elif code == '404':
                analysis += f"- **404 Not Found**: URL incorrect or endpoint doesn't exist.\n"
            elif code == '400':
                analysis += f"- **400 Bad Request**: Invalid request format or missing parameters.\n"
            elif code == '500':
                analysis += f"- **500 Internal Server Error**: Server issue. Check API logs.\n"
            elif code == '502':
                analysis += f"- **502 Bad Gateway**: Upstream server issue.\n"
            elif code == '503':
                analysis += f"- **503 Service Unavailable**: Server temporarily unavailable.\n"
            else:
                analysis += f"- **{code}**: Unknown status code. Check API documentation.\n"
        
        return analysis
    
    def _analyze_errors(self, errors: list) -> str:
        """Analyze error messages and provide guidance."""
        analysis = "\n**Error Analysis:**\n"
        
        for error in errors[:3]:  # Limit to first 3 errors
            error_lower = error.lower()
            if 'timeout' in error_lower:
                analysis += "- **Timeout**: Increase timeout value or check network.\n"
            elif 'connection' in error_lower:
                analysis += "- **Connection Error**: Check if API is accessible.\n"
            elif 'ssl' in error_lower or 'certificate' in error_lower:
                analysis += "- **SSL Error**: Check certificate or use HTTP for testing.\n"
            elif 'json' in error_lower:
                analysis += "- **JSON Error**: Check response format and parsing.\n"
            else:
                analysis += f"- **Error**: {error[:100]}...\n"
        
        return analysis
    
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
- ✅ AI model: Local Intelligence

I'm here to help you build robust, reliable APIs! What would you like to work on?"""
    
    def _get_intelligent_fallback_response(self, user_input: str) -> str:
        """Get intelligent fallback response using logic-based analysis."""
        user_input_lower = user_input.lower()
        
        # Analyze user input and provide intelligent responses
        if any(greeting in user_input_lower for greeting in ['hi', 'hello', 'hey']):
            return self._get_greeting_response()
        elif "authentication" in user_input_lower or "auth" in user_input_lower:
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