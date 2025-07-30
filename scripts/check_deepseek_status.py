#!/usr/bin/env python3
"""
🦖 DeepSeek Account Status Checker
Check which of your DeepSeek API keys are active and ready to use
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_deepseek_account(api_key: str, account_name: str):
    """Check if a DeepSeek API key is active."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test payload
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 10
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return {
                    "account": account_name,
                    "status": "✅ ACTIVE",
                    "message": "Account is active and ready to use"
                }
            elif response.status_code == 401:
                return {
                    "account": account_name,
                    "status": "❌ INVALID KEY",
                    "message": "API key is invalid or expired"
                }
            elif response.status_code == 402:
                return {
                    "account": account_name,
                    "status": "⚠️ NEEDS ACTIVATION",
                    "message": "Account needs activation or has insufficient balance"
                }
            elif response.status_code == 429:
                return {
                    "account": account_name,
                    "status": "⚠️ RATE LIMITED",
                    "message": "Rate limit exceeded - account is active but needs cooldown"
                }
            else:
                return {
                    "account": account_name,
                    "status": "❓ UNKNOWN",
                    "message": f"Unexpected status: {response.status_code}"
                }
                
    except Exception as e:
        return {
            "account": account_name,
            "status": "❌ ERROR",
            "message": f"Connection error: {str(e)}"
        }

async def main():
    """Check all DeepSeek accounts."""
    print("🦖 DeepSeek Account Status Checker")
    print("=" * 50)
    
    # Get all DeepSeek API keys from environment
    deepseek_keys = [
        ("DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY")),
        ("DEEPSEEK_API_KEY_2", os.getenv("DEEPSEEK_API_KEY_2")),
        ("DEEPSEEK_API_KEY_3", os.getenv("DEEPSEEK_API_KEY_3")),
        ("DEEPSEEK_API_KEY_4", os.getenv("DEEPSEEK_API_KEY_4")),
        ("DEEPSEEK_API_KEY_5", os.getenv("DEEPSEEK_API_KEY_5"))
    ]
    
    print(f"Checking {len(deepseek_keys)} DeepSeek accounts...\n")
    
    # Check each account
    results = []
    for env_name, api_key in deepseek_keys:
        if api_key and api_key != "your-deepseek-api-key-here":
            result = await check_deepseek_account(api_key, env_name)
            results.append(result)
            print(f"{result['status']} {result['account']}")
            print(f"   {result['message']}")
            print()
        else:
            print(f"❌ {env_name}: Not configured")
            print()
    
    # Summary
    print("=" * 50)
    print("📊 SUMMARY:")
    active_count = sum(1 for r in results if "ACTIVE" in r['status'])
    needs_activation = sum(1 for r in results if "NEEDS ACTIVATION" in r['status'])
    
    print(f"✅ Active accounts: {active_count}")
    print(f"⚠️ Needs activation: {needs_activation}")
    print(f"❌ Issues: {len(results) - active_count - needs_activation}")
    
    if needs_activation > 0:
        print("\n🔧 To activate accounts:")
        print("1. Visit: https://platform.deepseek.com/")
        print("2. Sign in with each account's email")
        print("3. Complete email verification")
        print("4. Add payment method (required for free tier)")
        print("5. Claim free credits (1M tokens/month)")

if __name__ == "__main__":
    asyncio.run(main()) 