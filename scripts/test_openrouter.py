#!/usr/bin/env python3
"""
🦖 OpenRouter API Tester
Test your OpenRouter API key and see available free models
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_openrouter_models():
    """Test OpenRouter API and get available models."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in .env file")
        return
    
    print("🦖 Testing OpenRouter API...")
    print(f"API Key: {api_key[:20]}...")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Get available models
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                models_data = response.json()
                print("✅ Successfully connected to OpenRouter!")
                print(f"📊 Found {len(models_data.get('data', []))} models")
                
                # Filter for free models
                free_models = []
                for model in models_data.get('data', []):
                    model_id = model.get('id', '')
                    pricing = model.get('pricing', {})
                    
                    # Check if it's free (no input/output cost or very low cost)
                    input_cost = pricing.get('input', 0)
                    output_cost = pricing.get('output', 0)
                    
                    if input_cost == 0 and output_cost == 0:
                        free_models.append({
                            'id': model_id,
                            'name': model.get('name', 'Unknown'),
                            'description': model.get('description', 'No description')
                        })
                
                print(f"\n🎉 Found {len(free_models)} FREE models:")
                for i, model in enumerate(free_models[:10], 1):  # Show first 10
                    print(f"{i}. {model['id']}")
                    print(f"   {model['name']}")
                    print(f"   {model['description'][:100]}...")
                    print()
                
                if len(free_models) > 10:
                    print(f"... and {len(free_models) - 10} more free models")
                
                return free_models
                
            else:
                print(f"❌ Failed to get models: {response.status_code}")
                print(f"Response: {response.text}")
                return []
                
    except Exception as e:
        print(f"❌ Error testing OpenRouter: {e}")
        return []

async def test_openrouter_chat():
    """Test OpenRouter chat completion with a free model."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try with a common free model (adjust based on available models)
    test_models = [
        "openai/gpt-3.5-turbo",
        "anthropic/claude-3-haiku",
        "google/gemini-flash-1.5",
        "meta-llama/llama-3.1-8b-instruct"
    ]
    
    payload = {
        "model": "openai/gpt-3.5-turbo",  # Start with this
        "messages": [
            {"role": "user", "content": "Hello! Can you help me test my API?"}
        ],
        "max_tokens": 50
    }
    
    print("\n🧪 Testing chat completion...")
    
    for model in test_models:
        payload["model"] = model
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    print(f"✅ {model}: {content[:100]}...")
                    return model  # Found a working model
                else:
                    print(f"❌ {model}: {response.status_code} - {response.text[:100]}")
                    
        except Exception as e:
            print(f"❌ {model}: Error - {e}")
    
    return None

async def main():
    """Main test function."""
    print("🦖 OpenRouter API Tester")
    print("=" * 50)
    
    # Test models
    free_models = await test_openrouter_models()
    
    # Test chat
    working_model = await test_openrouter_chat()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"✅ Free models available: {len(free_models)}")
    print(f"✅ Working model: {working_model or 'None found'}")
    
    if working_model:
        print("\n🎉 Your OpenRouter API key is working!")
        print("You can now use it with Restaceratops!")
    else:
        print("\n⚠️ No working models found. Check your API key or try different models.")

if __name__ == "__main__":
    asyncio.run(main()) 