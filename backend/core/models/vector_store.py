#!/usr/bin/env python3
"""
🦖 Vector Store System for Restaceratops
Advanced vector database integration using ChromaDB for context-aware AI responses
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import asyncio

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

log = logging.getLogger("agent.vector_store")

class VectorStore:
    """Advanced vector database system for Restaceratops AI agent."""
    
    def __init__(self, persist_directory: str = "vector_db"):
        """Initialize the vector store system."""
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize collections
        self.conversation_collection = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "Conversation history and context"}
        )
        
        self.test_knowledge_collection = self.client.get_or_create_collection(
            name="test_knowledge",
            metadata={"description": "API testing knowledge and best practices"}
        )
        
        self.api_docs_collection = self.client.get_or_create_collection(
            name="api_documentation",
            metadata={"description": "API documentation and specifications"}
        )
        
        # Initialize sentence transformer for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        log.info(f"Vector store initialized at {self.persist_directory}")
    
    async def add_conversation_context(self, 
                                     user_input: str, 
                                     ai_response: str, 
                                     metadata: Optional[Dict] = None) -> str:
        """Add conversation context to the vector store."""
        try:
            # Create conversation document
            conversation_text = f"User: {user_input}\nAI: {ai_response}"
            
            # Generate embedding
            embedding = self.embedding_model.encode(conversation_text).tolist()
            
            # Prepare metadata
            doc_metadata = {
                "type": "conversation",
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "ai_response": ai_response,
                **(metadata or {})
            }
            
            # Add to collection
            self.conversation_collection.add(
                documents=[conversation_text],
                embeddings=[embedding],
                metadatas=[doc_metadata],
                ids=[f"conv_{datetime.now().timestamp()}"]
            )
            
            log.info(f"Added conversation context: {user_input[:50]}...")
            return "conversation_context_added"
            
        except Exception as e:
            log.error(f"Error adding conversation context: {e}")
            return f"error: {str(e)}"
    
    async def add_test_knowledge(self, 
                               knowledge_text: str, 
                               category: str = "general",
                               metadata: Optional[Dict] = None) -> str:
        """Add API testing knowledge to the vector store."""
        try:
            # Split text into chunks
            chunks = self.text_splitter.split_text(knowledge_text)
            
            # Generate embeddings for each chunk
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Prepare metadata for each chunk
            chunk_metadata = []
            chunk_ids = []
            
            for i, chunk in enumerate(chunks):
                chunk_metadata.append({
                    "type": "test_knowledge",
                    "category": category,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "timestamp": datetime.now().isoformat(),
                    **(metadata or {})
                })
                chunk_ids.append(f"knowledge_{category}_{datetime.now().timestamp()}_{i}")
            
            # Add to collection
            self.test_knowledge_collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=chunk_metadata,
                ids=chunk_ids
            )
            
            log.info(f"Added {len(chunks)} knowledge chunks for category: {category}")
            return f"knowledge_added_{len(chunks)}_chunks"
            
        except Exception as e:
            log.error(f"Error adding test knowledge: {e}")
            return f"error: {str(e)}"
    
    async def add_api_documentation(self, 
                                  api_spec: str, 
                                  api_name: str,
                                  metadata: Optional[Dict] = None) -> str:
        """Add API documentation to the vector store."""
        try:
            # Split API specification into chunks
            chunks = self.text_splitter.split_text(api_spec)
            
            # Generate embeddings for each chunk
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Prepare metadata for each chunk
            chunk_metadata = []
            chunk_ids = []
            
            for i, chunk in enumerate(chunks):
                chunk_metadata.append({
                    "type": "api_documentation",
                    "api_name": api_name,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "timestamp": datetime.now().isoformat(),
                    **(metadata or {})
                })
                chunk_ids.append(f"api_{api_name}_{datetime.now().timestamp()}_{i}")
            
            # Add to collection
            self.api_docs_collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=chunk_metadata,
                ids=chunk_ids
            )
            
            log.info(f"Added {len(chunks)} API documentation chunks for: {api_name}")
            return f"api_docs_added_{len(chunks)}_chunks"
            
        except Exception as e:
            log.error(f"Error adding API documentation: {e}")
            return f"error: {str(e)}"
    
    async def search_conversation_context(self, 
                                        query: str, 
                                        n_results: int = 5) -> List[Dict]:
        """Search for relevant conversation context."""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in conversation collection
            results = self.conversation_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
            
            log.info(f"Found {len(formatted_results)} relevant conversation contexts")
            return formatted_results
            
        except Exception as e:
            log.error(f"Error searching conversation context: {e}")
            return []
    
    async def search_test_knowledge(self, 
                                  query: str, 
                                  category: Optional[str] = None,
                                  n_results: int = 5) -> List[Dict]:
        """Search for relevant test knowledge."""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Prepare where clause if category is specified
            where_clause = None
            if category:
                where_clause = {"category": category}
            
            # Search in test knowledge collection
            results = self.test_knowledge_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
            
            log.info(f"Found {len(formatted_results)} relevant test knowledge items")
            return formatted_results
            
        except Exception as e:
            log.error(f"Error searching test knowledge: {e}")
            return []
    
    async def search_api_documentation(self, 
                                     query: str, 
                                     api_name: Optional[str] = None,
                                     n_results: int = 5) -> List[Dict]:
        """Search for relevant API documentation."""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Prepare where clause if api_name is specified
            where_clause = None
            if api_name:
                where_clause = {"api_name": api_name}
            
            # Search in API documentation collection
            results = self.api_docs_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
            
            log.info(f"Found {len(formatted_results)} relevant API documentation items")
            return formatted_results
            
        except Exception as e:
            log.error(f"Error searching API documentation: {e}")
            return []
    
    async def get_context_for_query(self, 
                                  query: str, 
                                  max_results: int = 10) -> Dict[str, List[Dict]]:
        """Get comprehensive context for a query from all collections."""
        try:
            # Search in all collections
            conversation_context = await self.search_conversation_context(
                query, n_results=max_results // 3
            )
            
            test_knowledge = await self.search_test_knowledge(
                query, n_results=max_results // 3
            )
            
            api_docs = await self.search_api_documentation(
                query, n_results=max_results // 3
            )
            
            return {
                "conversation_context": conversation_context,
                "test_knowledge": test_knowledge,
                "api_documentation": api_docs
            }
            
        except Exception as e:
            log.error(f"Error getting comprehensive context: {e}")
            return {
                "conversation_context": [],
                "test_knowledge": [],
                "api_documentation": []
            }
    
    async def initialize_default_knowledge(self) -> str:
        """Initialize the vector store with default API testing knowledge."""
        try:
            # Default API testing knowledge
            default_knowledge = [
                {
                    "category": "best_practices",
                    "content": """
                    API Testing Best Practices:
                    1. Always test both positive and negative scenarios
                    2. Validate response status codes and headers
                    3. Test with realistic data and edge cases
                    4. Implement proper error handling
                    5. Use environment variables for configuration
                    6. Test authentication and authorization
                    7. Monitor performance and response times
                    8. Document test cases and expected results
                    """
                },
                {
                    "category": "authentication",
                    "content": """
                    API Authentication Testing:
                    1. Test with valid authentication tokens
                    2. Test with expired tokens
                    3. Test with invalid tokens
                    4. Test with missing authentication
                    5. Test token refresh mechanisms
                    6. Test different authentication methods (Bearer, API Key, OAuth)
                    7. Test rate limiting with authentication
                    """
                },
                {
                    "category": "error_handling",
                    "content": """
                    API Error Handling Testing:
                    1. Test 400 Bad Request responses
                    2. Test 401 Unauthorized responses
                    3. Test 403 Forbidden responses
                    4. Test 404 Not Found responses
                    5. Test 500 Internal Server Error responses
                    6. Test timeout scenarios
                    7. Test network connectivity issues
                    8. Validate error response formats
                    """
                },
                {
                    "category": "performance",
                    "content": """
                    API Performance Testing:
                    1. Measure response times under normal load
                    2. Test concurrent request handling
                    3. Monitor memory and CPU usage
                    4. Test with large payloads
                    5. Validate timeout configurations
                    6. Test rate limiting behavior
                    7. Monitor database connection pools
                    8. Test caching mechanisms
                    """
                }
            ]
            
            # Add default knowledge to vector store
            for knowledge_item in default_knowledge:
                await self.add_test_knowledge(
                    knowledge_item["content"],
                    knowledge_item["category"]
                )
            
            log.info("Initialized vector store with default API testing knowledge")
            return "default_knowledge_initialized"
            
        except Exception as e:
            log.error(f"Error initializing default knowledge: {e}")
            return f"error: {str(e)}"
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store collections."""
        try:
            stats = {}
            
            # Get conversation collection stats
            conv_count = self.conversation_collection.count()
            stats["conversations"] = {
                "total_documents": conv_count,
                "collection_name": "conversations"
            }
            
            # Get test knowledge collection stats
            knowledge_count = self.test_knowledge_collection.count()
            stats["test_knowledge"] = {
                "total_documents": knowledge_count,
                "collection_name": "test_knowledge"
            }
            
            # Get API documentation collection stats
            api_docs_count = self.api_docs_collection.count()
            stats["api_documentation"] = {
                "total_documents": api_docs_count,
                "collection_name": "api_documentation"
            }
            
            return stats
            
        except Exception as e:
            log.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    async def reset_collections(self) -> str:
        """Reset all collections (use with caution)."""
        try:
            # Delete and recreate collections
            self.client.delete_collection("conversations")
            self.client.delete_collection("test_knowledge")
            self.client.delete_collection("api_documentation")
            
            # Recreate collections
            self.conversation_collection = self.client.create_collection(
                name="conversations",
                metadata={"description": "Conversation history and context"}
            )
            
            self.test_knowledge_collection = self.client.create_collection(
                name="test_knowledge",
                metadata={"description": "API testing knowledge and best practices"}
            )
            
            self.api_docs_collection = self.client.create_collection(
                name="api_documentation",
                metadata={"description": "API documentation and specifications"}
            )
            
            log.info("Reset all vector store collections")
            return "collections_reset"
            
        except Exception as e:
            log.error(f"Error resetting collections: {e}")
            return f"error: {str(e)}"

# Global vector store instance
_vector_store = None

def get_vector_store() -> VectorStore:
    """Get the global vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store

async def setup_vector_store() -> str:
    """Set up the vector store with default knowledge."""
    try:
        vector_store = get_vector_store()
        result = await vector_store.initialize_default_knowledge()
        return result
    except Exception as e:
        log.error(f"Error setting up vector store: {e}")
        return f"error: {str(e)}"

def main():
    """Main function for testing the vector store."""
    import asyncio
    
    async def test_vector_store():
        print("🦖 Testing Vector Store System...")
        
        # Initialize vector store
        vector_store = get_vector_store()
        
        # Test adding conversation context
        print("📝 Adding conversation context...")
        result = await vector_store.add_conversation_context(
            "How do I test API authentication?",
            "To test API authentication, you should test with valid tokens, expired tokens, and invalid tokens.",
            {"test": True}
        )
        print(f"Result: {result}")
        
        # Test adding test knowledge
        print("📚 Adding test knowledge...")
        result = await vector_store.add_test_knowledge(
            "API testing involves validating endpoints, status codes, and response formats.",
            "general"
        )
        print(f"Result: {result}")
        
        # Test searching
        print("🔍 Searching for context...")
        results = await vector_store.get_context_for_query("authentication testing")
        print(f"Found {len(results['conversation_context'])} conversation contexts")
        print(f"Found {len(results['test_knowledge'])} knowledge items")
        
        # Get stats
        print("📊 Getting collection stats...")
        stats = await vector_store.get_collection_stats()
        print(f"Stats: {stats}")
        
        print("✅ Vector store test completed!")
    
    asyncio.run(test_vector_store())

if __name__ == "__main__":
    main() 