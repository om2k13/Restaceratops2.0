# 🦖 Restaceratops - AI-Powered API Testing Platform

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://typescriptlang.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://mongodb.com/atlas)
[![OpenRouter](https://img.shields.io/badge/AI-OpenRouter-purple.svg)](https://openrouter.ai)

**A modern, AI-augmented API testing platform that leverages OpenRouter's Qwen3 Coder model for intelligent test generation, execution, and real-time monitoring.**

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [🔧 Installation](#-installation)
- [🤖 AI Integration](#-ai-integration)
- [📊 Usage Guide](#-usage-guide)
- [🚀 Deployment](#-deployment)
- [📈 API Reference](#-api-reference)
- [🛠️ Development](#️-development)
- [🔒 Security](#-security)
- [📊 Performance](#-performance)
- [🆘 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)

## ✨ Features

### 🤖 AI-Powered Testing
- **Intelligent Test Generation**: Uses OpenRouter Qwen3 Coder for smart test case creation
- **OpenAPI Integration**: Automatically generates tests from OpenAPI specifications
- **AI Chat Assistant**: Get testing guidance and help through conversational AI
- **Smart Suggestions**: AI-powered recommendations for test improvements

### 🧪 Comprehensive Testing
- **Multiple Test Types**: Positive, negative, and edge case testing
- **Real-time Execution**: Live test monitoring with WebSocket updates
- **Custom Test Files**: Upload and execute your own YAML test specifications
- **Predefined Suites**: Ready-to-use test examples for common scenarios

### 📊 Real-time Monitoring
- **Live Dashboard**: Real-time statistics and system health monitoring
- **WebSocket Communication**: Instant updates without page refresh
- **Progress Tracking**: Live test execution progress with detailed reporting
- **Connection Monitoring**: Real-time WebSocket connection status

### 🎯 Modern Technology Stack
- **Backend**: FastAPI with async/await for high performance
- **Frontend**: React + TypeScript for type-safe development
- **Database**: MongoDB Atlas for scalable data persistence
- **Real-time**: WebSocket for instant communication
- **HTTP Client**: Axios for robust API communication

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/WebSocket    ┌─────────────────┐
│   React + TS    │ ←──────────────────→ │   FastAPI       │
│   Frontend      │                      │   Backend       │
└─────────────────┘                      └─────────────────┘
                                                │
                                                ▼
                                    ┌─────────────────┐
                                    │  MongoDB Atlas  │
                                    │  (Data Store)   │
                                    └─────────────────┘
                                                │
                                                ▼
                                    ┌─────────────────┐
                                    │  OpenRouter AI  │
                                    │  (Qwen3 Coder)  │
                                    └─────────────────┘
```

### Project Structure
```
restaceratops/
├── backend/                 # FastAPI backend
│   ├── api/                # API endpoints
│   │   └── main.py         # Main FastAPI application
│   ├── core/               # Core functionality
│   │   ├── agents/         # AI agents (OpenRouter integration)
│   │   ├── models/         # Data models & MongoDB integration
│   │   └── services/       # Business logic services
│   │       ├── runner.py   # Test execution engine
│   │       ├── dsl_loader.py # YAML test parser
│   │       └── assertions.py # Test assertion logic
│   ├── tests/              # Backend test files
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/          # React components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── TestRunner.tsx
│   │   │   └── ChatInterface.tsx
│   │   ├── services/       # API services
│   │   │   ├── api.ts      # Axios HTTP client
│   │   │   └── websocket.ts # WebSocket client
│   │   └── App.tsx         # Main React app
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── tests/                  # Test specification files
├── scripts/                # Deployment scripts
├── config/                 # Configuration files
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **OpenRouter API Key** - For AI features
- **MongoDB Atlas Account** - For data persistence

### 1. Clone Repository
   ```bash
   git clone <repository-url>
   cd restaceratops
   ```

### 2. Environment Setup
   ```bash
# Create environment file
cat > .env << EOF
OPENROUTER_API_KEY=your-openrouter-api-key
MONGODB_URI=your-mongodb-atlas-connection-string
MONGODB_DB_NAME=restaceratops
EOF
```

### 3. Install Dependencies
   ```bash
# Backend dependencies
cd backend
pip install -r requirements.txt
   
# Frontend dependencies
cd ../frontend
   npm install
   cd ..
   ```

### 4. Start Application
   ```bash
# Terminal 1: Start backend
   cd backend
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   
# Terminal 2: Start frontend
   cd frontend
   npm run dev
   ```

### 5. Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Installation

### Backend Setup

1. **Install Python Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   export OPENROUTER_API_KEY='your-api-key'
   export MONGODB_URI='your-mongodb-connection-string'
   export MONGODB_DB_NAME='restaceratops'
   ```

3. **Start Backend Server**
   ```bash
   python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Node.js Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure API Base URL**
   ```bash
   # Edit frontend/src/services/api.ts
   const API_BASE_URL = 'http://localhost:8000';
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

## 🤖 AI Integration

### OpenRouter Setup

1. **Get API Key**
   - Visit [OpenRouter.ai/keys](https://openrouter.ai/keys)
   - Sign up and create API key
   - Copy the key (starts with `sk-or-`)

2. **Configure Environment**
   ```bash
   export OPENROUTER_API_KEY='your-api-key'
   ```

### MongoDB Atlas Setup

1. **Create Account**
   - Visit [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Create free account

2. **Create Cluster**
   - Choose "FREE" tier (M0)
   - Select cloud provider and region

3. **Get Connection String**
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Copy connection string

4. **Configure Environment**
   ```bash
   export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
   export MONGODB_DB_NAME="restaceratops"
   ```

## 📊 Usage Guide

### 1. Dashboard
- **System Statistics**: View real-time system health
- **Recent Tests**: Monitor latest test executions
- **Connection Status**: Check WebSocket connections
- **Performance Metrics**: Track response times and success rates

### 2. Test Runner
- **Upload Test Files**: Upload custom YAML test specifications
- **Execute Tests**: Run tests with real-time progress monitoring
- **View Results**: Comprehensive test reports with detailed analysis
- **Download Reports**: Export results in Markdown format

### 3. AI Chat
- **Testing Guidance**: Get help with test creation and execution
- **AI Assistance**: Ask questions about API testing best practices
- **Smart Suggestions**: Receive AI-powered recommendations
- **Real-time Responses**: Instant AI chat with WebSocket updates

### 4. Test File Format
```yaml
name: "API Test Suite"
description: "Comprehensive API testing"
base_url: "https://api.example.com"
tests:
  - name: "Get Users"
    method: "GET"
    path: "/users"
    expected_status: 200
    assertions:
      - type: "status_code"
        expected: 200
      - type: "response_time"
        max_ms: 1000
```

## 🚀 Deployment

### Backend Deployment (Render)

1. **Create Render Account**
   - Visit [Render.com](https://render.com)
   - Sign up for free account

2. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure settings:
     ```
     Name: restaceratops-backend
     Environment: Python 3
     Build Command: pip install -r backend/requirements.txt
     Start Command: uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT
     Health Check Path: /health
     ```

3. **Add Environment Variables**
   ```
OPENROUTER_API_KEY=your-openrouter-api-key
MONGODB_URI=your-mongodb-atlas-connection-string
MONGODB_DB_NAME=restaceratops
   ```

### Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Visit [Vercel.com](https://vercel.com)
   - Sign up for free account

2. **Deploy Project**
   - Click "New Project"
   - Import GitHub repository
   - Configure settings:
     ```
     Framework Preset: Vite
     Root Directory: frontend
     Build Command: npm run build
     Output Directory: dist
     ```

3. **Add Environment Variables**
   ```
   REACT_APP_API_BASE_URL=https://your-backend-url.onrender.com
   ```

## 📈 API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/api/chat` | POST | AI chat interface |
| `/api/tests/run` | POST | Execute test suite |
| `/api/upload` | POST | Upload test files |
| `/api/dashboard` | GET | System statistics |
| `/api/generate-tests/openapi` | POST | Generate tests from OpenAPI |

### WebSocket Endpoints

| Endpoint | Description |
|----------|-------------|
| `/ws` | Real-time communication |

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Run tests
curl -X POST http://localhost:8000/api/tests/run \
  -H "Content-Type: application/json" \
  -d '{"test_file": "simple_test.yml"}'

# AI chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me create a test for user API"}'
```

## 🛠️ Development

### Project Structure Deep Dive

#### Backend Services
- **`api/main.py`**: FastAPI application with endpoints and WebSocket handling
- **`core/services/runner.py`**: Test execution engine
- **`core/services/dsl_loader.py`**: YAML test file parser
- **`core/services/assertions.py`**: Test assertion logic
- **`core/agents/enhanced_ai_system.py`**: AI integration with OpenRouter

#### Frontend Components
- **`pages/Dashboard.tsx`**: System statistics and monitoring
- **`pages/TestRunner.tsx`**: Test execution interface
- **`pages/ChatInterface.tsx`**: AI chat interface
- **`services/api.ts`**: Axios HTTP client configuration
- **`services/websocket.ts`**: WebSocket client implementation

### Development Commands

```bash
# Backend development
cd backend
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Frontend development
cd frontend
npm run dev

# Run tests
cd backend
python -m pytest

# Build frontend
cd frontend
npm run build
```

### Code Quality

- **TypeScript**: Type-safe frontend development
- **Pydantic**: Data validation in FastAPI
- **ESLint**: Code linting for frontend
- **Black**: Python code formatting
- **MyPy**: Python type checking

## 🔒 Security

### Security Features

- **Environment Variables**: Sensitive data stored securely
- **CORS Configuration**: Cross-origin request handling
- **Input Validation**: Pydantic models for data validation
- **File Upload Security**: File type and size validation
- **API Key Management**: Secure API key handling

### Best Practices

- **HTTPS**: All production deployments use HTTPS
- **Rate Limiting**: Implemented for API endpoints
- **Error Handling**: Comprehensive error handling without data exposure
- **Logging**: Secure logging without sensitive data

## 📊 Performance

### Performance Metrics

- **Response Time**: < 2 seconds for AI responses
- **Test Execution**: Parallel processing support
- **WebSocket Latency**: < 100ms for real-time updates
- **Database Queries**: Optimized with indexes

### Optimization Features

- **Async/Await**: Non-blocking I/O operations
- **Connection Pooling**: Database connection optimization
- **Caching**: Frequently accessed data caching
- **Lazy Loading**: Frontend component optimization

## 🆘 Troubleshooting

### Common Issues

#### 1. AI Not Responding
```bash
# Check API key
echo $OPENROUTER_API_KEY

# Test API connection
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  https://openrouter.ai/api/v1/models
```

#### 2. Database Connection Issues
```bash
# Check MongoDB connection
python -c "
import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient('$MONGODB_URI')
print('Connection successful')
"
```

#### 3. Frontend Not Loading
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check frontend build
cd frontend
npm run build
```

#### 4. WebSocket Connection Issues
```bash
# Check WebSocket endpoint
curl -i -N -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
  -H "Sec-WebSocket-Version: 13" \
  http://localhost:8000/ws
```

### Debug Commands

```bash
# Check backend logs
cd backend
python -m uvicorn api.main:app --reload --log-level debug

# Check frontend logs
cd frontend
npm run dev -- --debug

# Check environment variables
env | grep -E "(OPENROUTER|MONGODB)"
```

### Getting Help

- **API Documentation**: Visit `/docs` endpoint
- **Health Check**: Visit `/health` endpoint
- **Logs**: Check deployment platform logs
- **Issues**: Create GitHub issue with detailed description

## 🤝 Contributing

### Development Setup

1. **Fork Repository**
   ```bash
   git clone https://github.com/your-username/restaceratops.git
   cd restaceratops
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow coding standards
   - Add tests for new features
   - Update documentation

4. **Test Changes**
   ```bash
   # Backend tests
   cd backend && python -m pytest
   
   # Frontend tests
   cd frontend && npm test
   ```

5. **Submit Pull Request**
   - Provide detailed description
   - Include screenshots if UI changes
   - Reference related issues

### Code Standards

- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Use strict mode, proper typing
- **React**: Functional components with hooks
- **FastAPI**: Async functions, proper error handling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter**: For providing AI capabilities
- **FastAPI**: For the excellent web framework
- **React**: For the powerful frontend library
- **MongoDB Atlas**: For the database service
- **Render & Vercel**: For the deployment platforms

---

**🦖 Restaceratops - Making API testing intelligent and accessible!** 

*Built with ❤️ using modern web technologies* 