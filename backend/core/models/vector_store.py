#!/usr/bin/env python3
"""
🦖 Simplified Vector Store System for Restaceratops
Lightweight file-based storage for conversation context
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

log = logging.getLogger("agent.vector_store")

class VectorStore:
    """Simplified file-based storage system for Restaceratops AI agent."""
    
    def __init__(self, persist_directory: str = "vector_db"):
        """Initialize the simplified vector store system."""
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        
        # File paths for different data types
        self.conversations_file = self.persist_directory / "conversations.json"
        self.knowledge_file = self.persist_directory / "knowledge.json"
        self.api_docs_file = self.persist_directory / "api_docs.json"
        
        # Initialize files if they don't exist
        self._initialize_files()
        
        log.info(f"Simplified vector store initialized at {self.persist_directory}")
    
    def _initialize_files(self):
        """Initialize storage files if they don't exist."""
        files = [
            (self.conversations_file, []),
            (self.knowledge_file, []),
            (self.api_docs_file, [])
        ]
        
        for file_path, default_data in files:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    def _load_data(self, file_path: Path) -> List[Dict]:
        """Load data from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, file_path: Path, data: List[Dict]):
        """Save data to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    async def add_conversation_context(self, 
                                     user_input: str, 
                                     ai_response: str, 
                                     metadata: Optional[Dict] = None) -> str:
        """Add conversation context to storage."""
        try:
            conversation_data = {
                "id": f"conv_{datetime.now().timestamp()}",
                "user_input": user_input,
                "ai_response": ai_response,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            conversations = self._load_data(self.conversations_file)
            conversations.append(conversation_data)
            
            # Keep only last 100 conversations
            if len(conversations) > 100:
                conversations = conversations[-100:]
            
            self._save_data(self.conversations_file, conversations)
            
            log.info(f"Added conversation context: {user_input[:50]}...")
            return "conversation_context_added"
            
        except Exception as e:
            log.error(f"Error adding conversation context: {e}")
            return f"error: {str(e)}"
    
    async def add_test_knowledge(self, 
                               knowledge_text: str, 
                               category: str = "general",
                               metadata: Optional[Dict] = None) -> str:
        """Add test knowledge to storage."""
        try:
            knowledge_data = {
                "id": f"knowledge_{datetime.now().timestamp()}",
                "text": knowledge_text,
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            knowledge = self._load_data(self.knowledge_file)
            knowledge.append(knowledge_data)
            self._save_data(self.knowledge_file, knowledge)
            
            log.info(f"Added test knowledge: {category}")
            return "test_knowledge_added"
            
        except Exception as e:
            log.error(f"Error adding test knowledge: {e}")
            return f"error: {str(e)}"
    
    async def add_api_documentation(self, 
                                  api_spec: str, 
                                  api_name: str,
                                  metadata: Optional[Dict] = None) -> str:
        """Add API documentation to storage."""
        try:
            api_data = {
                "id": f"api_{datetime.now().timestamp()}",
                "name": api_name,
                "spec": api_spec,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            api_docs = self._load_data(self.api_docs_file)
            api_docs.append(api_data)
            self._save_data(self.api_docs_file, api_docs)
            
            log.info(f"Added API documentation: {api_name}")
            return "api_documentation_added"
            
        except Exception as e:
            log.error(f"Error adding API documentation: {e}")
            return f"error: {str(e)}"
    
    async def search_conversation_context(self, 
                                        query: str, 
                                        n_results: int = 5) -> List[Dict]:
        """Search conversation context (simple keyword matching)."""
        try:
            conversations = self._load_data(self.conversations_file)
            results = []
            
            query_lower = query.lower()
            for conv in conversations:
                score = 0
                if query_lower in conv.get('user_input', '').lower():
                    score += 2
                if query_lower in conv.get('ai_response', '').lower():
                    score += 1
                
                if score > 0:
                    results.append({
                        **conv,
                        'score': score
                    })
            
            # Sort by score and return top results
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:n_results]
            
        except Exception as e:
            log.error(f"Error searching conversation context: {e}")
            return []
    
    async def search_test_knowledge(self, 
                                  query: str, 
                                  category: Optional[str] = None,
                                  n_results: int = 5) -> List[Dict]:
        """Search test knowledge (simple keyword matching)."""
        try:
            knowledge = self._load_data(self.knowledge_file)
            results = []
            
            query_lower = query.lower()
            for item in knowledge:
                if category and item.get('category') != category:
                    continue
                
                score = 0
                if query_lower in item.get('text', '').lower():
                    score += 2
                if query_lower in item.get('category', '').lower():
                    score += 1
                
                if score > 0:
                    results.append({
                        **item,
                        'score': score
                    })
            
            # Sort by score and return top results
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:n_results]
            
        except Exception as e:
            log.error(f"Error searching test knowledge: {e}")
            return []
    
    async def search_api_documentation(self, 
                                     query: str, 
                                     api_name: Optional[str] = None,
                                     n_results: int = 5) -> List[Dict]:
        """Search API documentation (simple keyword matching)."""
        try:
            api_docs = self._load_data(self.api_docs_file)
            results = []
            
            query_lower = query.lower()
            for doc in api_docs:
                if api_name and doc.get('name') != api_name:
                    continue
                
                score = 0
                if query_lower in doc.get('name', '').lower():
                    score += 2
                if query_lower in doc.get('spec', '').lower():
                    score += 1
                
                if score > 0:
                    results.append({
                        **doc,
                        'score': score
                    })
            
            # Sort by score and return top results
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:n_results]
            
        except Exception as e:
            log.error(f"Error searching API documentation: {e}")
            return []
    
    async def get_context_for_query(self, 
                                  query: str, 
                                  max_results: int = 10) -> Dict[str, List[Dict]]:
        """Get relevant context for a query from all collections."""
        try:
            conversations = await self.search_conversation_context(query, max_results // 3)
            knowledge = await self.search_test_knowledge(query, n_results=max_results // 3)
            api_docs = await self.search_api_documentation(query, n_results=max_results // 3)
            
            return {
                "conversations": conversations,
                "knowledge": knowledge,
                "api_documentation": api_docs
            }
            
        except Exception as e:
            log.error(f"Error getting context for query: {e}")
            return {
                "conversations": [],
                "knowledge": [],
                "api_documentation": []
            }
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about stored data."""
        try:
            conversations = self._load_data(self.conversations_file)
            knowledge = self._load_data(self.knowledge_file)
            api_docs = self._load_data(self.api_docs_file)
            
            return {
                "total_conversations": len(conversations),
                "total_knowledge_items": len(knowledge),
                "total_api_docs": len(api_docs),
                "storage_path": str(self.persist_directory),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            log.error(f"Error getting collection stats: {e}")
            return {
                "error": str(e),
                "storage_path": str(self.persist_directory)
            }
    
    async def reset_collections(self) -> str:
        """Reset all collections."""
        try:
            self._initialize_files()
            log.info("All collections reset successfully")
            return "collections_reset"
            
        except Exception as e:
            log.error(f"Error resetting collections: {e}")
            return f"error: {str(e)}"

def get_vector_store() -> VectorStore:
    """Get vector store instance."""
    return VectorStore()

async def setup_vector_store() -> str:
    """Setup vector store with default knowledge."""
    try:
        store = get_vector_store()
        
        # Add some default test knowledge
        default_knowledge = [
            {
                "text": "API testing should include positive tests, negative tests, and edge cases.",
                "category": "best_practices"
            },
            {
                "text": "Always test authentication, authorization, and error handling in APIs.",
                "category": "security"
            },
            {
                "text": "Monitor response times and performance metrics during API testing.",
                "category": "performance"
            }
        ]
        
        for item in default_knowledge:
            await store.add_test_knowledge(item["text"], item["category"])
        
        return "vector_store_setup_complete"
        
    except Exception as e:
        log.error(f"Error setting up vector store: {e}")
        return f"error: {str(e)}"

def main():
    """Main function for testing the vector store."""
    async def test_vector_store():
        store = get_vector_store()
        
        # Test adding conversation
        result = await store.add_conversation_context(
            "Hello, how do I test APIs?",
            "I can help you test APIs! Here are some tips..."
        )
        print(f"Add conversation result: {result}")
        
        # Test adding knowledge
        result = await store.add_test_knowledge(
            "Always test both valid and invalid inputs",
            "testing_tips"
        )
        print(f"Add knowledge result: {result}")
        
        # Test searching
        results = await store.search_conversation_context("test APIs")
        print(f"Search results: {len(results)} found")
        
        # Test stats
        stats = await store.get_collection_stats()
        print(f"Stats: {stats}")
    
    import asyncio
    asyncio.run(test_vector_store())

if __name__ == "__main__":
    main() 