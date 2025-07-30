#!/usr/bin/env python3
"""
Test script for the enhanced chat interface
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.enhanced_chat_interface import EnhancedRestaceratopsChat

async def test_enhanced_chat():
    """Test the enhanced chat interface."""
    print("🧪 Testing Enhanced Chat Interface")
    print("=" * 50)
    
    # Initialize enhanced chat interface
    chat = EnhancedRestaceratopsChat()
    
    # Test conversations
    test_inputs = [
        "Hello!",
        "What can you help me with?",
        "Test my API at https://httpbin.org",
        "Show me the detailed error report",
        "How do I test API authentication?",
        "Explain JSON schema validation"
    ]
    
    for user_input in test_inputs:
        print(f"\n🤖 You: {user_input}")
        print("\n🦖 Restaceratops: ", end="", flush=True)
        
        response = await chat.handle_message(user_input)
        print(response)
        
        # Add a small delay for readability
        await asyncio.sleep(1)
    
    print("\n" + "=" * 50)
    print("✅ Enhanced chat interface test completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_enhanced_chat()) 