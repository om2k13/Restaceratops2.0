import os
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging

log = logging.getLogger(__name__)

class DatabaseManager:
    """MongoDB database manager for Restaceratops."""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.db_name = os.getenv("MONGODB_DB_NAME", "restaceratops")
        
    async def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            log.info(f"✅ Connected to MongoDB: {self.db_name}")
            
            # Create indexes
            await self._create_indexes()
            
        except Exception as e:
            log.error(f"❌ MongoDB connection failed: {e}")
            # Fallback to in-memory storage
            self.client = None
            self.db = None
    
    async def _create_indexes(self):
        """Create database indexes."""
        try:
            # Test executions index
            await self.db.test_executions.create_index([("execution_id", 1)], unique=True)
            await self.db.test_executions.create_index([("timestamp", -1)])
            
            # Test results index
            await self.db.test_results.create_index([("execution_id", 1)])
            await self.db.test_results.create_index([("timestamp", -1)])
            
            # Dashboard stats index
            await self.db.dashboard_stats.create_index([("timestamp", -1)])
            
            log.info("✅ Database indexes created")
        except Exception as e:
            log.error(f"❌ Failed to create indexes: {e}")
    
    async def save_test_execution(self, execution_data: Dict[str, Any]) -> str:
        """Save test execution data."""
        try:
            if self.db is None:
                return "no_db"
            
            execution_id = execution_data.get("execution_id")
            execution_data["timestamp"] = datetime.utcnow()
            
            # Convert to JSON-serializable format
            clean_execution_data = self._clean_for_json(execution_data)
            
            await self.db.test_executions.update_one(
                {"execution_id": execution_id},
                {"$set": clean_execution_data},
                upsert=True
            )
            
            # Save individual test results
            for result in execution_data.get("results", []):
                clean_result = self._clean_for_json(result)
                clean_result["execution_id"] = execution_id
                clean_result["timestamp"] = datetime.utcnow()
                await self.db.test_results.insert_one(clean_result)
            
            log.info(f"✅ Saved test execution: {execution_id}")
            return execution_id
            
        except Exception as e:
            log.error(f"❌ Failed to save test execution: {e}")
            return "error"
    
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get aggregated dashboard statistics."""
        try:
            if self.db is None:
                return self._get_empty_stats()
            
            # Get total tests
            total_tests = await self.db.test_results.count_documents({})
            
            # Get passed tests
            passed_tests = await self.db.test_results.count_documents({"status": "passed"})
            
            # Calculate success rate
            success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            # Get average response time
            pipeline = [
                {"$group": {"_id": None, "avg_response_time": {"$avg": "$response_time"}}}
            ]
            result = await self.db.test_results.aggregate(pipeline).to_list(1)
            avg_response_time = result[0]["avg_response_time"] if result else 0
            
            # Get recent results (last 10)
            recent_results = await self.db.test_results.find().sort("timestamp", -1).limit(10).to_list(10)
            
            # Format recent results
            formatted_results = []
            for result in recent_results:
                formatted_results.append({
                    "test_name": result.get("test_name", ""),
                    "status": result.get("status", ""),
                    "response_time": result.get("response_time", 0),
                    "response_code": result.get("response_code", 0),
                    "timestamp": result.get("timestamp", datetime.utcnow()).isoformat(),
                    "error": result.get("error")
                })
            
            log.info(f"📊 Dashboard stats: {total_tests} total tests, {passed_tests} passed, {success_rate}% success rate")
            
            return {
                "total_tests": total_tests,
                "success_rate": round(success_rate, 2),
                "avg_response_time": round(avg_response_time, 2),
                "running_tests": 0,  # Will be updated when we add real-time tracking
                "recent_results": formatted_results
            }
            
        except Exception as e:
            log.error(f"❌ Failed to get dashboard stats: {e}")
            return self._get_empty_stats()
    
    def _get_empty_stats(self) -> Dict[str, Any]:
        """Get empty dashboard stats."""
        return {
            "total_tests": 0,
            "success_rate": 0,
            "avg_response_time": 0,
            "running_tests": 0,
            "recent_results": []
        }
    
    async def save_chat_message(self, user_message: str, ai_response: str, timestamp: datetime = None) -> str:
        """Save chat message to database."""
        try:
            if self.db is None:
                return "no_db"
            
            if timestamp is None:
                timestamp = datetime.utcnow()
            
            chat_data = {
                "user_message": user_message,
                "ai_response": ai_response,
                "timestamp": timestamp,
                "session_id": "default"
            }
            
            result = await self.db.chat_messages.insert_one(chat_data)
            log.info(f"✅ Saved chat message: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            log.error(f"❌ Failed to save chat message: {e}")
            return "error"
    
    async def get_chat_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history."""
        try:
            if self.db is None:
                return []
            
            history = await self.db.chat_messages.find().sort("timestamp", -1).limit(limit).to_list(limit)
            return history
            
        except Exception as e:
            log.error(f"❌ Failed to get chat history: {e}")
            return []
    
    async def get_test_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get test execution history."""
        try:
            if self.db is None:
                return []
            
            history = await self.db.test_executions.find().sort("timestamp", -1).limit(limit).to_list(limit)
            return history
            
        except Exception as e:
            log.error(f"❌ Failed to get test history: {e}")
            return []
    
    def _clean_for_json(self, obj: Any) -> Any:
        """Clean object for JSON serialization."""
        if isinstance(obj, dict):
            return {k: self._clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_for_json(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return self._clean_for_json(obj.__dict__)
        elif hasattr(obj, 'isoformat'):  # datetime objects
            return obj.isoformat()
        elif hasattr(obj, '__str__'):
            return str(obj)
        else:
            return obj
    
    async def close(self):
        """Close database connection."""
        if self.client:
            self.client.close()
            log.info("✅ MongoDB connection closed")

# Global database instance
db_manager = DatabaseManager()

async def get_db_manager() -> DatabaseManager:
    """Get database manager instance."""
    return db_manager 