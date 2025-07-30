#!/usr/bin/env python3
"""
🦖 RAG System for Restaceratops
Retrieval Augmented Generation system for context-aware AI responses
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import asyncio

from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from backend.core.models.vector_store import get_vector_store

log = logging.getLogger("agent.rag_system")

class RAGSystem:
    """Advanced RAG system for Restaceratops AI agent."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """Initialize the RAG system."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        # Initialize LLM
        if self.api_key:
            self.llm = ChatOpenAI(
                model=model,
                temperature=0.7,
                max_tokens=1000,
                api_key=self.api_key
            )
        else:
            self.llm = None
            log.warning("No OpenAI API key provided. RAG system will use fallback responses.")
        
        # Initialize vector store
        self.vector_store = get_vector_store()
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Define RAG prompts
        self.rag_prompts = {
            "context_enhancement": PromptTemplate(
                input_variables=["query", "context", "conversation_history"],
                template="""
                You are Restaceratops, an AI-powered API testing agent. Use the provided context to give accurate, helpful responses.

                Query: {query}

                Relevant Context:
                {context}

                Recent Conversation History:
                {conversation_history}

                Instructions:
                1. Use the context to provide accurate, detailed responses
                2. If the context doesn't contain relevant information, acknowledge this
                3. Maintain your helpful, dinosaur-themed personality
                4. Provide actionable advice when possible
                5. Keep responses concise but comprehensive

                Response:
                """
            ),
            "test_generation": PromptTemplate(
                input_variables=["api_spec", "user_requirements", "best_practices"],
                template="""
                Generate comprehensive API test cases based on the provided information.

                API Specification:
                {api_spec}

                User Requirements:
                {user_requirements}

                Testing Best Practices:
                {best_practices}

                Instructions:
                1. Generate realistic test cases in YAML format
                2. Include positive and negative test scenarios
                3. Test authentication, error handling, and edge cases
                4. Use realistic test data
                5. Follow API testing best practices

                Generated Test Cases:
                """
            ),
            "troubleshooting": PromptTemplate(
                input_variables=["error_description", "context", "previous_attempts"],
                template="""
                Help troubleshoot API testing issues based on the provided information.

                Error Description:
                {error_description}

                Relevant Context:
                {context}

                Previous Attempts:
                {previous_attempts}

                Instructions:
                1. Analyze the error and provide specific solutions
                2. Suggest debugging steps
                3. Recommend preventive measures
                4. Provide code examples when helpful
                5. Consider common API testing pitfalls

                Troubleshooting Guide:
                """
            )
        }
        
        log.info("RAG system initialized")
    
    async def get_relevant_context(self, 
                                 query: str, 
                                 max_results: int = 10,
                                 include_conversation: bool = True,
                                 include_knowledge: bool = True,
                                 include_api_docs: bool = True) -> Dict[str, List[Dict]]:
        """Retrieve relevant context for a query."""
        try:
            context = {}
            
            if include_conversation:
                context["conversation_context"] = await self.vector_store.search_conversation_context(
                    query, n_results=max_results // 3
                )
            
            if include_knowledge:
                context["test_knowledge"] = await self.vector_store.search_test_knowledge(
                    query, n_results=max_results // 3
                )
            
            if include_api_docs:
                context["api_documentation"] = await self.vector_store.search_api_documentation(
                    query, n_results=max_results // 3
                )
            
            return context
            
        except Exception as e:
            log.error(f"Error getting relevant context: {e}")
            return {
                "conversation_context": [],
                "test_knowledge": [],
                "api_documentation": []
            }
    
    def format_context_for_prompt(self, context: Dict[str, List[Dict]]) -> str:
        """Format context for use in prompts."""
        try:
            formatted_sections = []
            
            # Format conversation context
            if context.get("conversation_context"):
                conv_section = "**Recent Conversations:**\n"
                for item in context["conversation_context"][:3]:  # Limit to 3 most relevant
                    conv_section += f"- {item['content']}\n"
                formatted_sections.append(conv_section)
            
            # Format test knowledge
            if context.get("test_knowledge"):
                knowledge_section = "**Relevant Testing Knowledge:**\n"
                for item in context["test_knowledge"][:3]:  # Limit to 3 most relevant
                    knowledge_section += f"- {item['content']}\n"
                formatted_sections.append(knowledge_section)
            
            # Format API documentation
            if context.get("api_documentation"):
                api_section = "**API Documentation:**\n"
                for item in context["api_documentation"][:3]:  # Limit to 3 most relevant
                    api_section += f"- {item['content']}\n"
                formatted_sections.append(api_section)
            
            return "\n".join(formatted_sections) if formatted_sections else "No relevant context found."
            
        except Exception as e:
            log.error(f"Error formatting context: {e}")
            return "Error formatting context."
    
    async def generate_context_enhanced_response(self, 
                                               query: str, 
                                               conversation_history: List[Dict] = None) -> str:
        """Generate a response enhanced with relevant context."""
        try:
            if not self.llm:
                return self._get_fallback_response(query)
            
            # Get relevant context
            context = await self.get_relevant_context(query)
            formatted_context = self.format_context_for_prompt(context)
            
            # Format conversation history
            history_text = ""
            if conversation_history:
                history_items = []
                for msg in conversation_history[-5:]:  # Last 5 messages
                    if msg.get("role") == "user":
                        history_items.append(f"User: {msg.get('content', '')}")
                    elif msg.get("role") == "assistant":
                        history_items.append(f"AI: {msg.get('content', '')}")
                history_text = "\n".join(history_items)
            
            # Generate response using RAG
            prompt = self.rag_prompts["context_enhancement"].format(
                query=query,
                context=formatted_context,
                conversation_history=history_text
            )
            
            response = await self.llm.ainvoke(prompt)
            return response.content
            
        except Exception as e:
            log.error(f"Error generating context-enhanced response: {e}")
            return self._get_fallback_response(query)
    
    async def generate_intelligent_tests(self, 
                                       api_spec: str, 
                                       user_requirements: str) -> str:
        """Generate intelligent test cases using RAG."""
        try:
            if not self.llm:
                return self._get_fallback_test_generation(api_spec, user_requirements)
            
            # Get relevant testing best practices
            context = await self.get_relevant_context("API testing best practices", include_conversation=False)
            best_practices = self.format_context_for_prompt(context)
            
            # Generate tests using RAG
            prompt = self.rag_prompts["test_generation"].format(
                api_spec=api_spec,
                user_requirements=user_requirements,
                best_practices=best_practices
            )
            
            response = await self.llm.ainvoke(prompt)
            return response.content
            
        except Exception as e:
            log.error(f"Error generating intelligent tests: {e}")
            return self._get_fallback_test_generation(api_spec, user_requirements)
    
    async def generate_troubleshooting_guide(self, 
                                           error_description: str, 
                                           previous_attempts: str = "") -> str:
        """Generate troubleshooting guide using RAG."""
        try:
            if not self.llm:
                return self._get_fallback_troubleshooting(error_description)
            
            # Get relevant troubleshooting context
            context = await self.get_relevant_context("API testing troubleshooting error handling", include_conversation=False)
            troubleshooting_context = self.format_context_for_prompt(context)
            
            # Generate troubleshooting guide using RAG
            prompt = self.rag_prompts["troubleshooting"].format(
                error_description=error_description,
                context=troubleshooting_context,
                previous_attempts=previous_attempts
            )
            
            response = await self.llm.ainvoke(prompt)
            return response.content
            
        except Exception as e:
            log.error(f"Error generating troubleshooting guide: {e}")
            return self._get_fallback_troubleshooting(error_description)
    
    async def add_conversation_to_context(self, 
                                        user_input: str, 
                                        ai_response: str, 
                                        metadata: Optional[Dict] = None) -> str:
        """Add conversation to the vector store for future context."""
        try:
            result = await self.vector_store.add_conversation_context(
                user_input, ai_response, metadata
            )
            return result
        except Exception as e:
            log.error(f"Error adding conversation to context: {e}")
            return f"error: {str(e)}"
    
    async def add_knowledge_to_context(self, 
                                     knowledge_text: str, 
                                     category: str = "general",
                                     metadata: Optional[Dict] = None) -> str:
        """Add knowledge to the vector store for future context."""
        try:
            result = await self.vector_store.add_test_knowledge(
                knowledge_text, category, metadata
            )
            return result
        except Exception as e:
            log.error(f"Error adding knowledge to context: {e}")
            return f"error: {str(e)}"
    
    async def add_api_docs_to_context(self, 
                                    api_spec: str, 
                                    api_name: str,
                                    metadata: Optional[Dict] = None) -> str:
        """Add API documentation to the vector store for future context."""
        try:
            result = await self.vector_store.add_api_documentation(
                api_spec, api_name, metadata
            )
            return result
        except Exception as e:
            log.error(f"Error adding API docs to context: {e}")
            return f"error: {str(e)}"
    
    def _get_fallback_response(self, query: str) -> str:
        """Enhanced fallback response when LLM is not available."""
        query_lower = query.lower().strip()
        
        # Enhanced keyword-based responses
        if any(word in query_lower for word in ['hello', 'hi', 'hey', 'greetings']):
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

        elif any(word in query_lower for word in ['test', 'run', 'execute', 'check']):
            if any(word in query_lower for word in ['api', 'endpoint', 'url']):
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

        elif any(word in query_lower for word in ['create', 'generate', 'make', 'write']):
            if any(word in query_lower for word in ['test', 'case']):
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

        elif any(word in query_lower for word in ['help', 'what', 'how', 'explain']):
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

        elif any(word in query_lower for word in ['error', 'debug', 'fix', 'troubleshoot']):
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

        elif any(word in query_lower for word in ['report', 'results', 'status', 'show']):
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
    
    def _get_fallback_test_generation(self, api_spec: str, user_requirements: str) -> str:
        """Fallback test generation when LLM is not available."""
        base_url = api_spec.split()[0] if api_spec else 'https://your-api.com'
        
        return f"""- name: "Health Check"
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

- name: "Error Handling - 404"
  request:
    method: GET
    url: {base_url}/nonexistent
  expect:
    status: 404

- name: "Authentication Test"
  request:
    method: POST
    url: {base_url}/auth/login
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
    url: {base_url}/protected
    headers:
      Authorization: "Bearer {{token}}"
  expect:
    status: 200"""
    
    def _get_fallback_troubleshooting(self, error_description: str) -> str:
        """Fallback troubleshooting when LLM is not available."""
        return f"""🦖 Let me help you troubleshoot this issue:

**Error:** {error_description}

**Common Solutions:**
1. **Check API Status** - Verify the API is running and accessible
2. **Validate URL** - Ensure the endpoint URL is correct
3. **Check Authentication** - Verify tokens and credentials
4. **Review Request Format** - Check headers, body, and parameters
5. **Network Connectivity** - Test network access and firewalls
6. **Rate Limiting** - Check if you've hit API limits
7. **Error Logs** - Review server logs for more details

**Debugging Steps:**
• Test with a simple GET request first
• Use tools like Postman or curl to verify
• Check API documentation for correct usage
• Monitor network traffic for errors

Would you like me to help you test specific aspects of your API?"""
    
    async def get_rag_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system."""
        try:
            vector_stats = await self.vector_store.get_collection_stats()
            
            return {
                "rag_system": "active",
                "llm_model": self.model if self.llm else "fallback_mode",
                "vector_store_stats": vector_stats,
                "prompts_available": list(self.rag_prompts.keys())
            }
        except Exception as e:
            log.error(f"Error getting RAG stats: {e}")
            return {"error": str(e)}

# Global RAG system instance
_rag_system = None

def get_rag_system(api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> RAGSystem:
    """Get the global RAG system instance."""
    global _rag_system
    if _rag_system is None:
        _rag_system = RAGSystem(api_key, model)
    return _rag_system

async def test_rag_system():
    """Test the RAG system functionality."""
    print("🦖 Testing RAG System...")
    
    # Initialize RAG system
    rag_system = get_rag_system()
    
    # Test context retrieval
    print("🔍 Testing context retrieval...")
    context = await rag_system.get_relevant_context("API authentication testing")
    print(f"Found {len(context['test_knowledge'])} knowledge items")
    
    # Test response generation
    print("💬 Testing response generation...")
    response = await rag_system.generate_context_enhanced_response(
        "How do I test API authentication?"
    )
    print(f"Generated response: {response[:100]}...")
    
    # Test test generation
    print("🧪 Testing test generation...")
    tests = await rag_system.generate_intelligent_tests(
        "https://api.example.com",
        "Test user authentication endpoints"
    )
    print(f"Generated tests: {tests[:100]}...")
    
    # Get stats
    print("📊 Getting RAG stats...")
    stats = await rag_system.get_rag_stats()
    print(f"RAG Stats: {stats}")
    
    print("✅ RAG system test completed!")

def main():
    """Main function for testing the RAG system."""
    asyncio.run(test_rag_system())

if __name__ == "__main__":
    main() 