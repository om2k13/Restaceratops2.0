#!/usr/bin/env python3
"""
🦖 AI Provider Fallback Hierarchy Display
Show the complete fallback chain for Restaceratops AI system
"""

import asyncio
from dotenv import load_dotenv
from agent.openrouter_ai_system import get_openrouter_ai_system
from agent.enhanced_ai_system import get_enhanced_ai_system

# Load environment variables
load_dotenv()

def show_fallback_hierarchy():
    """Display the complete AI provider fallback hierarchy."""
    print("🦖 Restaceratops AI Provider Fallback Hierarchy")
    print("=" * 60)
    
    # Get OpenRouter system
    openrouter_ai = get_openrouter_ai_system()
    openrouter_stats = openrouter_ai.get_system_stats()
    
    # Get Enhanced AI system
    enhanced_ai = get_enhanced_ai_system()
    enhanced_stats = enhanced_ai.get_system_stats()
    
    print("1️⃣ PRIMARY: OpenRouter AI System")
    print("   └── 10 Free Models (Automatic Rotation)")
    print("       ├── openai/gpt-3.5-turbo")
    print("       ├── anthropic/claude-3-haiku")
    print("       ├── google/gemini-2.5-flash-lite")
    print("       ├── qwen/qwen3-235b-a22b-2507:free")
    print("       ├── z-ai/glm-4.5-air")
    print("       ├── meta-llama/llama-3.1-8b-instruct")
    print("       ├── microsoft/phi-3.5-mini-128k")
    print("       ├── deepseek-ai/deepseek-coder-6.7b-instruct")
    print("       ├── mistralai/mistral-7b-instruct")
    print("       └── nousresearch/nous-hermes-2-mixtral-8x7b-dpo")
    print()
    
    print("2️⃣ FALLBACK: Enhanced AI System")
    print("   └── Multiple Provider Support")
    
    # Show enhanced AI providers from the multi-provider component
    if hasattr(enhanced_ai, 'multi_provider_ai'):
        for i, provider in enumerate(enhanced_ai.multi_provider_ai.providers, 1):
            status = "✅" if provider["name"] not in enhanced_ai.multi_provider_ai.failed_providers else "❌"
            print(f"       {i}. {status} {provider['name']} ({provider['type']})")
    else:
        print("       • DeepSeek API Keys (5 accounts)")
        print("       • Hugging Face API Tokens (5 accounts)")
        print("       • Ollama Local Model")
        print("       • OpenAI API (if configured)")
    
    print()
    print("🔄 FALLBACK LOGIC:")
    print("   • OpenRouter tries each model in sequence")
    print("   • If a model fails (rate limit, error), moves to next")
    print("   • If all OpenRouter models fail, switches to Enhanced AI")
    print("   • Enhanced AI tries DeepSeek → HuggingFace → Ollama")
    print("   • If all fail, uses built-in fallback responses")
    print()
    
    print("📊 CURRENT STATUS:")
    print(f"   • OpenRouter: {openrouter_stats['working_models']}/{openrouter_stats['total_models']} models ready")
    print(f"   • Enhanced AI: {enhanced_stats['working_providers']}/{enhanced_stats['total_providers']} providers ready")
    print(f"   • Current OpenRouter Model: {openrouter_stats['current_model']}")
    print(f"   • Current Enhanced AI Provider: {enhanced_stats['current_provider']}")
    print()
    
    print("✅ Your system is configured for maximum reliability!")
    print("   With 319+ free models available through OpenRouter + fallback providers")

if __name__ == "__main__":
    show_fallback_hierarchy() 