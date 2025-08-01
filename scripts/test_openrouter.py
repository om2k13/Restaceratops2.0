#!/usr/bin/env python3
"""
Test OpenRouter API key and Qwen3 model
"""

import os
import asyncio
import httpx
import json

async def test_openrouter_api():
    """Test OpenRouter API with the current API key."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ No OpenRouter API key found in environment")
        return False
    
    print(f"🔑 Testing API key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "qwen/qwen3-coder:free",
                    "messages": [
                        {"role": "user", "content": "Hello! Can you help me with API testing?"}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                print("✅ OpenRouter API working!")
                print(f"🤖 Response: {ai_response[:100]}...")
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"❌ Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

async def main():
    """Main test function."""
    print("🧪 Testing OpenRouter API...")
    
    success = await test_openrouter_api()
    
    if success:
        print("🎉 OpenRouter API is working correctly!")
    else:
        print("💥 OpenRouter API test failed!")
        print("\n🔧 Troubleshooting:")
        print("1. Check if API key is valid")
        print("2. Verify OpenRouter account has credits")
        print("3. Check network connectivity")

if __name__ == "__main__":
    asyncio.run(main()) 