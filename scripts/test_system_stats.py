#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.enhanced_chat_interface import EnhancedRestaceratopsChat

async def test_system_stats():
    print("Testing system stats...")
    
    try:
        # Create chat agent
        chat_agent = EnhancedRestaceratopsChat()
        
        # Initialize
        await chat_agent.initialize()
        
        # Test system stats
        stats = chat_agent.enhanced_ai.get_system_stats()
        print("System stats:", stats)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_system_stats()) 