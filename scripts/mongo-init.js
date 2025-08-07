// MongoDB initialization script for Restaceratops
// This script runs when the MongoDB container starts for the first time

// Create database and collections
db = db.getSiblingDB('restaceratops');

// Create collections with proper indexes
db.createCollection('test_executions');
db.createCollection('chat_messages');
db.createCollection('system_stats');

// Create indexes for better performance
db.test_executions.createIndex({ "timestamp": -1 });
db.test_executions.createIndex({ "execution_id": 1 });
db.test_executions.createIndex({ "status": 1 });

db.chat_messages.createIndex({ "timestamp": -1 });
db.chat_messages.createIndex({ "user_message": "text", "ai_response": "text" });

db.system_stats.createIndex({ "timestamp": -1 });

// Insert initial system stats
db.system_stats.insertOne({
    timestamp: new Date(),
    total_tests: 0,
    success_rate: 100.0,
    avg_response_time: 0.0,
    running_tests: 0,
    system_status: "initialized"
});

print("✅ MongoDB initialized for Restaceratops");
print("📊 Database: restaceratops");
print("📋 Collections: test_executions, chat_messages, system_stats");
print("🔍 Indexes created for optimal performance");
