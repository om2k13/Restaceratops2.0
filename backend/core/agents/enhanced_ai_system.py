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

from backend.core.models.vector_store import get_vector_store, setup_vector_store

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
            return None
        
        try:
            return ChatOpenAI(
                model=self.model,
                openai_api_key=self.api_key,
                openai_api_base=self.base_url,
                temperature=0.7,
                max_tokens=1000
            )
        except Exception as e:
            log.error(f"Failed to create OpenRouter LLM: {e}")
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
        """Handle user conversation using OpenRouter Qwen3 Coder."""
        try:
            llm = self.openrouter_ai.create_llm()
            if not llm:
                return self._get_fallback_response(user_input)
            
            # Get conversation history
            chat_history = self.conversation_memory.chat_memory.messages
            
            # Create messages
            messages = []
            for msg in chat_history[-6:]:  # Last 6 messages for context
                if isinstance(msg, HumanMessage):
                    messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    messages.append({"role": "assistant", "content": msg.content})
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Get response
            response = await llm.agenerate([messages])
            ai_response = response.generations[0][0].text
            
            # Update memory
            self.conversation_memory.chat_memory.add_user_message(user_input)
            self.conversation_memory.chat_memory.add_ai_message(ai_response)
            
            return ai_response
            
        except Exception as e:
            log.error(f"Error in conversation: {e}")
            return self._get_fallback_response(user_input)
    
    async def generate_intelligent_tests(self, api_spec: str, requirements: str) -> str:
        """Generate intelligent test cases using OpenRouter Qwen3 Coder."""
        try:
            llm = self.openrouter_ai.create_llm()
            if not llm:
                return self._get_fallback_test_template(api_spec)
            
            prompt = f"""Generate comprehensive API test cases for the following API specification:

API Specification:
{api_spec}

Requirements:
{requirements}

Please provide:
1. Test cases in YAML format
2. Positive and negative test scenarios
3. Edge cases and error handling
4. Performance considerations

Format the response clearly with explanations for each test case."""

            response = await llm.agenerate([[{"role": "user", "content": prompt}]])
            return response.generations[0][0].text
            
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
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Get fallback response when AI is unavailable."""
        return f"""I'm currently experiencing technical difficulties with my AI system. 

However, I can still help you with API testing! Here are some general tips:

🔧 **API Testing Basics:**
- Test all HTTP methods (GET, POST, PUT, DELETE)
- Verify status codes (200, 400, 401, 404, 500)
- Check response data structure and content
- Test with valid and invalid inputs
- Monitor response times

📋 **What you asked:** {user_input}

Would you like me to help you with specific API testing scenarios once the system is back online?"""
    
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