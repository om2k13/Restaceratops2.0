import os
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging
import re

log = logging.getLogger(__name__)

class DatabaseManager:
    """MongoDB database manager for Restaceratops."""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.mongo_uri = os.getenv("MONGODB_URI", "")
        self.db_name = os.getenv("MONGODB_DB_NAME", "Restaceratops")
        # In-memory storage for fallback
        self._in_memory_test_results = []
        self._in_memory_executions = []
        self._validate_connection_string()
        
    def _validate_connection_string(self):
        """Validate and fix MongoDB connection string."""
        if not self.mongo_uri:
            log.warning("⚠️ No MongoDB URI provided - using fallback mode")
            return
            
        # Check if it's a valid MongoDB URI
        if not self.mongo_uri.startswith(("mongodb://", "mongodb+srv://")):
            log.error("❌ Invalid MongoDB URI format")
            self.mongo_uri = ""
            return
            
        # Fix common issues with MongoDB Atlas connection strings
        if "mongodb+srv://" in self.mongo_uri:
            # Ensure proper format for MongoDB Atlas
            if "?retryWrites=true&w=majority" not in self.mongo_uri:
                self.mongo_uri += "?retryWrites=true&w=majority"
                
        log.info(f"🔗 MongoDB URI configured for database: {self.db_name}")
    
    def _create_atlas_connection_string(self):
        """Create a proper MongoDB Atlas connection string."""
        # This is a template - you'll need to replace with your actual cluster details
        username = "om2k13"
        password = "om2k13"
        cluster_name = "cluster0"  # This might need to be updated
        project_id = "your-project-id"  # This needs to be your actual project ID
        
        # Try different cluster name patterns
        possible_clusters = [
            f"mongodb+srv://{username}:{password}@{cluster_name}.{project_id}.mongodb.net/?retryWrites=true&w=majority",
            f"mongodb+srv://{username}:{password}@{cluster_name}.mongodb.net/?retryWrites=true&w=majority",
            f"mongodb+srv://{username}:{password}@{cluster_name}.xxxxx.mongodb.net/?retryWrites=true&w=majority"
        ]
        
        return possible_clusters[1]  # Use the most common format
        
    async def connect(self):
        """Connect to MongoDB with improved error handling."""
        if not self.mongo_uri:
            log.warning("⚠️ No MongoDB URI - using in-memory fallback")
            self.client = None
            self.db = None
            return
            
        # Try multiple connection string formats
        connection_strings = [
            self.mongo_uri,
            self._create_atlas_connection_string()
        ]
        
        for i, conn_str in enumerate(connection_strings):
            if not conn_str:
                continue
                
            try:
                log.info(f"🔗 Attempting MongoDB connection (attempt {i+1})...")
                
                # Set connection timeout
                self.client = AsyncIOMotorClient(
                    conn_str,
                    serverSelectionTimeoutMS=10000,  # 10 second timeout
                    connectTimeoutMS=10000,
                    socketTimeoutMS=10000
                )
                
                self.db = self.client[self.db_name]
                
                # Test connection with timeout
                await asyncio.wait_for(
                    self.client.admin.command('ping'),
                    timeout=10.0
                )
                
                log.info(f"✅ Successfully connected to MongoDB: {self.db_name}")
                
                # Create indexes
                await self._create_indexes()
                return  # Success - exit the loop
                
            except asyncio.TimeoutError:
                log.error(f"❌ MongoDB connection timeout (attempt {i+1})")
                self._fallback_to_memory()
            except Exception as e:
                log.error(f"❌ MongoDB connection failed (attempt {i+1}): {e}")
                self._fallback_to_memory()
        
        # If all attempts failed
        log.warning("⚠️ All MongoDB connection attempts failed - using in-memory fallback")
        self._fallback_to_memory()
    
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
            execution_id = execution_data.get("execution_id")
            execution_data["timestamp"] = datetime.utcnow()
            
            # Convert to JSON-serializable format
            clean_execution_data = self._clean_for_json(execution_data)
            
            if self.db is not None:
                # Try MongoDB first
                try:
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
                    
                    log.info(f"✅ Saved test execution to MongoDB: {execution_id}")
                except Exception as mongo_error:
                    log.warning(f"⚠️ MongoDB save failed, using in-memory: {mongo_error}")
                    self._save_to_memory(execution_data)
            else:
                # Use in-memory storage
                self._save_to_memory(execution_data)
            
            return execution_id
            
        except Exception as e:
            log.error(f"❌ Failed to save test execution: {e}")
            return "error"
    
    def _save_to_memory(self, execution_data: Dict[str, Any]):
        """Save test execution to in-memory storage."""
        try:
            # Save execution
            self._in_memory_executions.append(execution_data)
            
            # Save individual results
            for result in execution_data.get("results", []):
                result_copy = result.copy()
                result_copy["execution_id"] = execution_data.get("execution_id")
                result_copy["timestamp"] = datetime.utcnow()
                self._in_memory_test_results.append(result_copy)
            
            # Keep only last 1000 results to prevent memory issues
            if len(self._in_memory_test_results) > 1000:
                self._in_memory_test_results = self._in_memory_test_results[-1000:]
            
            log.info(f"✅ Saved test execution to memory: {execution_data.get('execution_id')}")
        except Exception as e:
            log.error(f"❌ Failed to save to memory: {e}")
    
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get aggregated dashboard statistics."""
        try:
            if self.db is not None:
                # Try MongoDB first
                try:
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
                    
                    log.info(f"📊 Dashboard stats from MongoDB: {total_tests} total tests, {passed_tests} passed, {success_rate}% success rate")
                    
                    return {
                        "total_tests": total_tests,
                        "success_rate": round(success_rate, 2),
                        "avg_response_time": round(avg_response_time, 2),
                        "running_tests": 0,  # Will be updated when we add real-time tracking
                        "recent_results": formatted_results
                    }
                except Exception as mongo_error:
                    log.warning(f"⚠️ MongoDB stats failed, using in-memory: {mongo_error}")
                    return self._get_stats_from_memory()
            else:
                # Use in-memory storage
                return self._get_stats_from_memory()
            
        except Exception as e:
            log.error(f"❌ Failed to get dashboard stats: {e}")
            return self._get_empty_stats()
    
    def _get_stats_from_memory(self) -> Dict[str, Any]:
        """Get dashboard stats from in-memory storage."""
        try:
            total_tests = len(self._in_memory_test_results)
            passed_tests = len([r for r in self._in_memory_test_results if r.get("status") == "passed"])
            success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            # Calculate average response time
            response_times = [r.get("response_time", 0) for r in self._in_memory_test_results]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Get recent results (last 10)
            recent_results = sorted(self._in_memory_test_results, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
            
            # Format recent results
            formatted_results = []
            for result in recent_results:
                formatted_results.append({
                    "test_name": result.get("test_name", ""),
                    "status": result.get("status", ""),
                    "response_time": result.get("response_time", 0),
                    "response_code": result.get("response_code", 0),
                    "timestamp": result.get("timestamp", datetime.utcnow()).isoformat() if isinstance(result.get("timestamp"), datetime) else str(result.get("timestamp", "")),
                    "error": result.get("error")
                })
            
            log.info(f"📊 Dashboard stats from memory: {total_tests} total tests, {passed_tests} passed, {success_rate}% success rate")
            
            return {
                "total_tests": total_tests,
                "success_rate": round(success_rate, 2),
                "avg_response_time": round(avg_response_time, 2),
                "running_tests": 0,
                "recent_results": formatted_results
            }
        except Exception as e:
            log.error(f"❌ Failed to get memory stats: {e}")
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
    
    def _fallback_to_memory(self):
        """Fallback to in-memory storage when MongoDB is unavailable."""
        log.warning("⚠️ Falling back to in-memory storage")
        if self.client:
            try:
                self.client.close()
            except:
                pass
        self.client = None
        self.db = None

# Global database instance
db_manager = DatabaseManager()

async def get_db_manager() -> DatabaseManager:
    """Get database manager instance."""
    return db_manager 