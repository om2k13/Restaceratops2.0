#!/usr/bin/env python3
"""
🦖 Restaceratops Chat Demo
Demonstrates the conversational interface for the API testing agent
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.chat_interface import RestaceratopsChat

async def demo_conversation():
    """Demo the conversational interface."""
    print("🦖 Restaceratops Chat Demo")
    print("=" * 50)
    print("This demo shows how you can talk to Restaceratops in simple English!")
    print("=" * 50)
    
    # Initialize chat interface
    chat = RestaceratopsChat()
    
    # Demo conversations
    demo_inputs = [
        "Hello!",
        "Help me understand how to use you",
        "Test my API at https://httpbin.org",
        "Create tests for my authentication endpoint",
        "Show me the test results",
        "Goodbye"
    ]
    
    for user_input in demo_inputs:
        print(f"\n🤖 You: {user_input}")
        print("\n🦖 Restaceratops: ", end="", flush=True)
        
        response = await chat.handle_message(user_input)
        print(response)
        
        # Add a small delay for readability
        await asyncio.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed! Your Restaceratops is now conversational!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(demo_conversation()) 