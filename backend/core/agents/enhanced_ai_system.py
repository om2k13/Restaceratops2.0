#!/usr/bin/env python3
"""
🦖 Enhanced AI System for Restaceratops
Advanced AI system with multi-model support, RAG integration, and context-aware responses
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

# Import free AI model support
try:
    from langchain_community.llms import Ollama
    from langchain_community.chat_models import ChatOllama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from langchain_community.llms import HuggingFaceEndpoint
    from langchain_community.chat_models import ChatHuggingFace
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False

from backend.core.models.vector_store import get_vector_store, setup_vector_store
from backend.core.agents.rag_system import get_rag_system

log = logging.getLogger("agent.enhanced_ai_system")

class MultiProviderAI:
    """Manages multiple AI providers with automatic fallback."""
    
    def __init__(self):
        self.providers = []
        self.current_provider_index = 0
        self.failed_providers = set()
        
        # Initialize all available providers
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available AI providers in order of preference."""
        
        # 1. DeepSeek (Primary - Best quality)
        deepseek_keys = [
            os.getenv("DEEPSEEK_API_KEY"),
            os.getenv("DEEPSEEK_API_KEY_2"),
            os.getenv("DEEPSEEK_API_KEY_3"),
            os.getenv("DEEPSEEK_API_KEY_4"),
            os.getenv("DEEPSEEK_API_KEY_5")
        ]
        
        for i, key in enumerate(deepseek_keys):
            if key and key != "your-deepseek-api-key-here":
                self.providers.append({
                    "name": f"DeepSeek-{i+1}",
                    "type": "deepseek",
                    "api_key": key,
                    "base_url": "https://api.deepseek.com/v1",
                    "model": "deepseek-chat",
                    "priority": 1
                })
        
        # 2. Hugging Face (Secondary - Good quality)
        huggingface_tokens = [
            os.getenv("HUGGINGFACE_API_TOKEN"),
            os.getenv("HUGGINGFACE_API_TOKEN_2"),
            os.getenv("HUGGINGFACE_API_TOKEN_3"),
            os.getenv("HUGGINGFACE_API_TOKEN_4"),
            os.getenv("HUGGINGFACE_API_TOKEN_5")
        ]
        
        for i, token in enumerate(huggingface_tokens):
            if token and token != "your-huggingface-token-here":
                self.providers.append({
                    "name": f"HuggingFace-{i+1}",
                    "type": "huggingface",
                    "api_key": token,
                    "model_id": "microsoft/DialoGPT-medium",
                    "priority": 2
                })
        
        # 3. Ollama (Local - Always available)
        if OLLAMA_AVAILABLE:
            self.providers.append({
                "name": "Ollama-Local",
                "type": "ollama",
                "model": "llama3.2:3b",
                "priority": 3
            })
        
        # 4. OpenAI (Fallback - if user has key)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your-openai-api-key-here":
            self.providers.append({
                "name": "OpenAI",
                "type": "openai",
                "api_key": openai_key,
                "model": "gpt-4o-mini",
                "priority": 4
            })
        
        # Sort by priority
        self.providers.sort(key=lambda x: x["priority"])
        
        log.info(f"Initialized {len(self.providers)} AI providers")
        for provider in self.providers:
            log.info(f"  - {provider['name']} ({provider['type']})")
    
    def get_next_working_provider(self):
        """Get the next working provider, skipping failed ones."""
        attempts = 0
        while attempts < len(self.providers):
            provider = self.providers[self.current_provider_index]
            
            if provider["name"] not in self.failed_providers:
                return provider
            
            # Move to next provider
            self.current_provider_index = (self.current_provider_index + 1) % len(self.providers)
            attempts += 1
        
        # If all providers failed, reset and try again
        self.failed_providers.clear()
        self.current_provider_index = 0
        return self.providers[0] if self.providers else None
    
    def mark_provider_failed(self, provider_name: str):
        """Mark a provider as failed."""
        self.failed_providers.add(provider_name)
        log.warning(f"Marked provider {provider_name} as failed")
    
    def create_llm(self, provider: Dict) -> Optional[Any]:
        """Create an LLM instance for the given provider."""
        try:
            if provider["type"] == "deepseek":
                return ChatOpenAI(
                    model=provider["model"],
                    temperature=0.7,
                    max_tokens=1500,
                    api_key=provider["api_key"],
                    base_url=provider["base_url"]
                )
            
            elif provider["type"] == "huggingface":
                if HUGGINGFACE_AVAILABLE:
                    return ChatHuggingFace(
                        model_id=provider["model_id"],
                        token=provider["api_key"],
                        temperature=0.7,
                        max_tokens=1500
                    )
            
            elif provider["type"] == "ollama":
                if OLLAMA_AVAILABLE:
                    return ChatOllama(
                        model=provider["model"],
                        temperature=0.7,
                        max_tokens=1500
                    )
            
            elif provider["type"] == "openai":
                return ChatOpenAI(
                    model=provider["model"],
                    temperature=0.7,
                    max_tokens=1500,
                    api_key=provider["api_key"]
                )
            
        except Exception as e:
            log.error(f"Failed to create LLM for {provider['name']}: {e}")
            return None
        
        return None

class EnhancedAISystem:
    """Advanced AI system for Restaceratops with multi-model support and RAG integration."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", 
                 use_free_models: bool = True, free_model_provider: str = "auto"):
        """Initialize the enhanced AI system."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.use_free_models = use_free_models
        self.free_model_provider = free_model_provider
        
        # Initialize multi-provider AI system
        self.multi_provider = MultiProviderAI()
        
        # Initialize AI models
        self.models = {
            'conversation': 'gpt-4o-mini',
            'test_generation': 'gpt-4o',
            'code_analysis': 'gpt-4o',
            'troubleshooting': 'gpt-4o-mini'
        }
        
        # Initialize LLM instances
        self.llms = {}
        
        # Initialize vector store
        self.vector_store = get_vector_store()
        
        # Initialize RAG system
        self.rag_system = get_rag_system(api_key, self.models['conversation'])
        
        # Initialize conversation memory
        self.conversation_memory = ConversationBufferWindowMemory(
            k=10,  # Remember last 10 exchanges
            return_messages=True
        )
        
        # System prompts for different tasks
        self.system_prompts = {
            'conversation': """You are Restaceratops, an AI-powered API testing agent with advanced capabilities.

Your personality:
- Friendly and helpful dinosaur-themed assistant
- Expert in API testing and automation
- Patient and thorough in explanations
- Always provide actionable advice

Your capabilities:
- Test APIs and endpoints automatically
- Generate comprehensive test cases
- Analyze API specifications
- Provide troubleshooting guidance
- Create detailed reports
- Explain complex concepts simply

Always maintain your dinosaur theme with 🦖 emojis and be helpful!""",

            'test_generation': """You are an expert API testing specialist. Generate comprehensive, production-ready test cases.

Requirements:
- Use YAML format for test definitions
- Include positive and negative test scenarios
- Test authentication, error handling, and edge cases
- Use realistic test data
- Follow API testing best practices
- Include proper assertions and validations

Generate tests that are:
- Comprehensive and thorough
- Easy to understand and maintain
- Production-ready and reliable
- Well-documented with clear descriptions""",

            'troubleshooting': """You are an expert API testing troubleshooter. Provide detailed, actionable solutions.

Your approach:
- Identify the root cause of issues
- Provide step-by-step solutions
- Suggest preventive measures
- Use clear, technical language
- Include code examples when helpful
- Consider security implications

Always be thorough and helpful in your troubleshooting guidance.""",

            'code_analysis': """You are an expert API code analyst. Analyze code and provide insights.

Your analysis should include:
- Code quality assessment
- Security considerations
- Performance implications
- Best practices recommendations
- Potential improvements
- Testing strategy suggestions

Provide clear, actionable feedback with examples."""
        }
        
        log.info(f"Enhanced AI system initialized with {len(self.multi_provider.providers)} providers")
    
    async def _get_working_llm(self, task_type: str = 'conversation') -> Optional[Any]:
        """Get a working LLM instance with automatic fallback."""
        max_attempts = len(self.multi_provider.providers)
        attempts = 0
        
        while attempts < max_attempts:
            provider = self.multi_provider.get_next_working_provider()
            if not provider:
                break
            
            try:
                log.info(f"Trying provider: {provider['name']}")
                llm = self.multi_provider.create_llm(provider)
                
                if llm:
                    # Test the LLM with a simple request
                    test_message = "Hello"
                    response = await llm.agenerate([[HumanMessage(content=test_message)]])
                    
                    if response and response.generations:
                        log.info(f"Successfully connected to {provider['name']}")
                        return llm
                
            except Exception as e:
                log.warning(f"Provider {provider['name']} failed: {e}")
                self.multi_provider.mark_provider_failed(provider['name'])
            
            attempts += 1
        
        log.error("All AI providers failed")
        return None
    
    async def handle_conversation(self, user_input: str) -> str:
        """Handle user conversation with automatic provider fallback."""
        try:
            llm = await self._get_working_llm('conversation')
            
            if llm:
                # Get conversation history
                messages = self.conversation_memory.load_memory_variables({})
                history = messages.get("history", [])
                
                # Add system prompt
                all_messages = [SystemMessage(content=self.system_prompts['conversation'])]
                all_messages.extend(history)
                all_messages.append(HumanMessage(content=user_input))
                
                # Generate response
                response = await llm.agenerate([all_messages])
                
                if response and response.generations:
                    ai_response = response.generations[0][0].text
                    
                    # Update memory
                    self.conversation_memory.save_context(
                        {"input": user_input},
                        {"output": ai_response}
                    )
                    
                    return ai_response
            
            # Fallback to enhanced responses
            return self._get_fallback_response(user_input)
            
        except Exception as e:
            log.error(f"Error in conversation: {e}")
            return self._get_fallback_response(user_input)
    
    async def generate_intelligent_tests(self, api_spec: str, requirements: str) -> str:
        """Generate intelligent test cases with automatic provider fallback."""
        try:
            llm = await self._get_working_llm('test_generation')
            
            if llm:
                prompt = f"""Generate comprehensive API test cases for: {api_spec}

Requirements: {requirements}

Generate YAML test cases that include:
- Health checks
- Authentication tests
- Error handling
- Edge cases
- Realistic test data

Return only valid YAML, no markdown formatting."""

                response = await llm.agenerate([[HumanMessage(content=prompt)]])
                
                if response and response.generations:
                    return response.generations[0][0].text
            
            # Fallback to RAG system
            return self.rag_system._get_fallback_test_generation(api_spec, requirements)
            
        except Exception as e:
            log.error(f"Error generating tests: {e}")
            return self.rag_system._get_fallback_test_generation(api_spec, requirements)
    
    async def generate_troubleshooting_guide(self, error_description: str) -> str:
        """Generate troubleshooting guide with automatic provider fallback."""
        try:
            llm = await self._get_working_llm('troubleshooting')
            
            if llm:
                prompt = f"""Provide a detailed troubleshooting guide for this API testing issue:

{error_description}

Include:
- Root cause analysis
- Step-by-step solutions
- Prevention strategies
- Code examples if relevant

Be thorough and actionable."""

                response = await llm.agenerate([[HumanMessage(content=prompt)]])
                
                if response and response.generations:
                    return response.generations[0][0].text
            
            # Fallback to RAG system
            return self.rag_system._get_fallback_troubleshooting(error_description)
            
        except Exception as e:
            log.error(f"Error generating troubleshooting: {e}")
            return self.rag_system._get_fallback_troubleshooting(error_description)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics including provider status."""
        stats = {
            "total_providers": len(self.multi_provider.providers),
            "working_providers": len(self.multi_provider.providers) - len(self.multi_provider.failed_providers),
            "failed_providers": list(self.multi_provider.failed_providers),
            "current_provider": self.multi_provider.providers[self.multi_provider.current_provider_index]["name"] if self.multi_provider.providers else "None",
            "providers": [
                {
                    "name": p["name"],
                    "type": p["type"],
                    "status": "working" if p["name"] not in self.multi_provider.failed_providers else "failed"
                }
                for p in self.multi_provider.providers
            ]
        }
        return stats
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Enhanced fallback response when AI models are not available."""
        user_input_lower = user_input.lower().strip()
        
        # Enhanced keyword-based responses
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return """🦖 Hello! I'm Restaceratops, your AI-powered API testing agent!

I can help you with:
• 🧪 **API Testing**: Run comprehensive tests on your APIs
• 📝 **Test Generation**: Create test cases from OpenAPI specs
• 🔍 **Troubleshooting**: Debug API issues and errors
• 📊 **Reporting**: Generate detailed test reports
• 🛠️ **Automation**: Set up CI/CD testing pipelines

**Quick Start:**
• "Test my API at https://httpbin.org"
• "Create tests for authentication"
• "Show me test results"
• "Help me debug a 500 error"

What would you like to work on today?"""

        elif any(word in user_input_lower for word in ['test', 'run', 'execute', 'check']):
            if any(word in user_input_lower for word in ['api', 'endpoint', 'url']):
                return """🧪 **API Testing Ready!**

I can help you test your APIs! Here's what I can do:

**Basic Testing:**
• Health checks and status endpoints
• Authentication flows
• CRUD operations (GET, POST, PUT, DELETE)
• Error handling and edge cases
• Performance and response time validation

**Advanced Features:**
• Schema validation
• Variable capture and reuse
• Concurrent test execution
• Custom assertions
• Detailed reporting

**To get started:**
1. Tell me your API URL: "Test my API at https://your-api.com"
2. I'll create and run comprehensive tests
3. You'll get detailed results and recommendations

**Example commands:**
• "Test my API at https://httpbin.org"
• "Create tests for user authentication"
• "Run performance tests on my API"

Would you like me to test a specific API?"""

        elif any(word in user_input_lower for word in ['create', 'generate', 'make', 'write']):
            if any(word in user_input_lower for word in ['test', 'case']):
                return """📝 **Test Generation Ready!**

I can create comprehensive test cases for your APIs! Here's what I generate:

**Test Types:**
• ✅ **Functional Tests**: Verify endpoints work correctly
• 🔐 **Authentication Tests**: Test login, tokens, permissions
• 🛡️ **Security Tests**: Validate input, check vulnerabilities
• ⚡ **Performance Tests**: Measure response times
• 🔄 **Integration Tests**: Test data flow between endpoints

**Generation Methods:**
• **From OpenAPI/Swagger specs** (recommended)
• **From API URLs** (basic tests)
• **From your descriptions** (custom scenarios)

**To generate tests:**
1. "Create tests from https://api.example.com/swagger.json"
2. "Generate tests for user management endpoints"
3. "Make authentication test cases"

**Example:**
• "Create tests from my OpenAPI spec"
• "Generate tests for user CRUD operations"
• "Make tests for OAuth2 authentication"

What type of tests would you like me to create?"""

        elif any(word in user_input_lower for word in ['help', 'what', 'how', 'explain']):
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
• "Help me debug a 500 error"

**📚 Common Use Cases:**
1. **New API Testing**: "Test my new API endpoints"
2. **Authentication**: "Create tests for login/logout"
3. **Performance**: "Run performance tests on my API"
4. **Debugging**: "Help me fix this API error"
5. **Documentation**: "Generate test documentation"

**🛠️ Advanced Features:**
• Schema validation
• Variable capture and reuse
• Concurrent test execution
• Custom assertions
• Multiple report formats (HTML, JUnit, Prometheus)

**Need specific help?**
• "How do I test authentication?"
• "Explain JSON schema validation"
• "What are API testing best practices?"

What would you like to learn more about?"""

        elif any(word in user_input_lower for word in ['error', 'debug', 'fix', 'troubleshoot']):
            return """🔍 **API Troubleshooting Assistant**

I can help you debug API issues! Here's what I can do:

**Common Problems I Can Help With:**
• 🚫 **4xx Errors**: Bad requests, authentication issues
• ⚠️ **5xx Errors**: Server errors, timeouts
• 🔐 **Authentication**: Token issues, permission problems
• 📊 **Performance**: Slow responses, timeouts
• 🔄 **Data Issues**: Invalid responses, schema mismatches

**Debugging Process:**
1. **Identify the Problem**: What error are you seeing?
2. **Analyze the Context**: When does it happen?
3. **Test Hypotheses**: Run targeted tests
4. **Provide Solutions**: Fix recommendations

**To get help:**
• "Help me debug a 500 error"
• "My API is returning 401 errors"
• "Authentication is failing"
• "Response times are too slow"

**Example debugging session:**
• "I'm getting 500 errors on POST requests"
• "My API returns 401 for valid tokens"
• "Response times are over 5 seconds"

What specific issue are you experiencing?"""

        elif any(word in user_input_lower for word in ['report', 'results', 'status', 'show']):
            return """📊 **Test Results & Reporting**

I can provide comprehensive test reports! Here's what I track:

**📈 Metrics I Monitor:**
• **Success Rate**: Percentage of passing tests
• **Response Times**: Average, min, max latency
• **Error Rates**: Types and frequency of failures
• **Coverage**: Endpoints and scenarios tested
• **Performance**: Throughput and load handling

**📋 Report Types:**
• **Console Reports**: Real-time test progress
• **HTML Reports**: Beautiful, interactive dashboards
• **JUnit XML**: CI/CD integration format
• **Prometheus**: Metrics for monitoring systems

**📊 What You'll See:**
• Test execution progress
• Pass/fail status for each test
• Detailed error messages
• Performance metrics
• Recommendations for improvement

**To view results:**
• "Show me the test results"
• "Generate a test report"
• "What's the status of my tests?"
• "Create an HTML report"

**Example reports:**
• "Tests completed: 15/15 passed"
• "Average response time: 245ms"
• "2 authentication tests failed"

Would you like me to run tests and show you the results?"""

        else:
            return """🦖 **Restaceratops AI Assistant**

I'm here to help with API testing and automation! Here are some things I can do:

**🧪 Testing:**
• Run comprehensive API tests
• Generate test cases from OpenAPI specs
• Validate responses and schemas
• Test authentication and security

**🔧 Development:**
• Debug API issues
• Optimize performance
• Set up CI/CD pipelines
• Create test documentation

**📊 Analysis:**
• Generate detailed reports
• Analyze API performance
• Identify potential issues
• Provide improvement recommendations

**Quick Commands:**
• "Test my API at https://your-api.com"
• "Create tests for authentication"
• "Help me debug this error"
• "Show me test results"

What would you like to work on? I'm here to help make your API testing easier and more effective! 🚀"""

        return self.rag_system._get_fallback_response(user_input)
    
    def _get_fallback_api_analysis(self, api_spec: str) -> str:
        """Fallback API analysis when AI models are not available."""
        return f"""🦖 API Specification Analysis

**API Specification:**
{api_spec[:200]}...

**Basic Analysis:**
• Review the API endpoints and methods
• Check authentication requirements
• Validate request/response formats
• Test error handling scenarios
• Verify documentation completeness

**Recommended Testing:**
• Create tests for each endpoint
• Test authentication flows
• Validate response schemas
• Test error conditions
• Performance testing

**Next Steps:**
• Generate comprehensive test cases
• Set up automated testing
• Monitor API performance
• Document test results"""
    

    
    async def reset_system(self) -> str:
        """Reset the enhanced AI system."""
        try:
            # Reset conversation memory
            self.conversation_memory.clear()
            
            # Reset vector store collections
            await self.vector_store.reset_collections()
            
            # Reinitialize with default knowledge
            await self.initialize_system()
            
            return "enhanced_ai_system_reset"
            
        except Exception as e:
            log.error(f"Error resetting system: {e}")
            return f"error: {str(e)}"

# Global enhanced AI system instance
_enhanced_ai_system = None

def get_enhanced_ai_system(api_key: Optional[str] = None) -> EnhancedAISystem:
    """Get the global enhanced AI system instance."""
    global _enhanced_ai_system
    if _enhanced_ai_system is None:
        _enhanced_ai_system = EnhancedAISystem(api_key)
    return _enhanced_ai_system

async def test_enhanced_ai_system():
    """Test the enhanced AI system functionality."""
    print("🦖 Testing Enhanced AI System...")
    
    # Initialize enhanced AI system
    ai_system = get_enhanced_ai_system()
    
    # Initialize system
    print("🔧 Initializing system...")
    result = await ai_system.initialize_system()
    print(f"Initialization result: {result}")
    
    # Test conversation handling
    print("💬 Testing conversation handling...")
    response = await ai_system.handle_conversation(
        "How do I test API authentication?"
    )
    print(f"Response: {response[:100]}...")
    
    # Test intelligent test generation
    print("🧪 Testing intelligent test generation...")
    tests = await ai_system.generate_intelligent_tests(
        "https://api.example.com",
        "Test user authentication endpoints"
    )
    print(f"Generated tests: {tests[:100]}...")
    
    # Test API specification analysis
    print("📊 Testing API specification analysis...")
    analysis = await ai_system.analyze_api_specification(
        "GET /users - Retrieve user list\nPOST /users - Create new user"
    )
    print(f"Analysis: {analysis[:100]}...")
    
    # Test troubleshooting
    print("🔧 Testing troubleshooting...")
    troubleshooting = await ai_system.generate_troubleshooting_guide(
        "API returning 500 Internal Server Error"
    )
    print(f"Troubleshooting: {troubleshooting[:100]}...")
    
    # Get system stats
    print("📊 Getting system stats...")
    stats = await ai_system.get_system_stats()
    print(f"System Stats: {stats}")
    
    print("✅ Enhanced AI system test completed!")

def main():
    """Main function for testing the enhanced AI system."""
    asyncio.run(test_enhanced_ai_system())

if __name__ == "__main__":
    main() 