#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.enhanced_ai_system import MultiProviderAI

def test_deepseek():
    print("Testing DeepSeek integration...")
    
    # Check environment variable
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    print(f"DeepSeek API Key: {deepseek_key[:10]}..." if deepseek_key else "Not found")
    
    # Create multi-provider AI
    multi_provider = MultiProviderAI()
    
    print(f"Total providers: {len(multi_provider.providers)}")
    for provider in multi_provider.providers:
        print(f"  - {provider['name']} ({provider['type']}) - Priority: {provider['priority']}")
    
    # Test provider creation
    if multi_provider.providers:
        first_provider = multi_provider.providers[0]
        print(f"\nTesting provider: {first_provider['name']}")
        
        try:
            llm = multi_provider.create_llm(first_provider)
            if llm:
                print("✅ LLM created successfully")
            else:
                print("❌ Failed to create LLM")
        except Exception as e:
            print(f"❌ Error creating LLM: {e}")

if __name__ == "__main__":
    test_deepseek() 