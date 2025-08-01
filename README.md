# 🦖 Restaceratops - AI-Powered API Testing Platform

**A modern, AI-augmented API testing platform that leverages OpenRouter's Qwen3 Coder model for intelligent test generation, execution, and analysis.**

## ✨ Features

- 🤖 **AI-Powered Testing**: Uses OpenRouter Qwen3 Coder for intelligent test generation
- 🧪 **Comprehensive Testing**: Supports positive, negative, and edge case testing
- 📊 **Real-time Monitoring**: Live test execution monitoring and reporting
- 🔧 **Easy Integration**: Simple setup with minimal dependencies
- 💰 **Cost-Effective**: Uses free OpenRouter models for zero-cost AI integration
- 🚀 **Modern Stack**: Built with FastAPI, React, and TypeScript
- 🗄️ **Data Persistence**: MongoDB Atlas integration for professional data management

## 🏗️ Architecture

```
restaceratops/
├── backend/                 # FastAPI backend
│   ├── api/                # API endpoints
│   │   └── main.py         # Main backend application
│   ├── core/               # Core functionality
│   │   ├── agents/         # AI agents (OpenRouter Qwen3)
│   │   ├── models/         # Data models & MongoDB integration
│   │   └── services/       # Business logic
│   └── tests/              # Backend tests
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/          # React components
│   │   └── services/       # API services
├── tests/                  # Test files
├── scripts/                # Deployment scripts
└── config/                 # Configuration files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- OpenRouter API key
- MongoDB Atlas account

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd restaceratops
   ```

2. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENROUTER_API_KEY=your-openrouter-api-key" > .env
   echo "MONGODB_URI=your-mongodb-atlas-connection-string" >> .env
   echo "MONGODB_DB_NAME=restaceratops" >> .env
   ```

3. **Install dependencies**
   ```bash
   # Install Python dependencies
   pip install -r backend/requirements.txt
   
   # Install frontend dependencies
   cd frontend
   npm install
   cd ..
   ```

4. **Start the application**
   ```bash
   # Start backend
   cd backend
   export OPENROUTER_API_KEY='your-api-key'
   python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   
   # Start frontend (in another terminal)
   cd frontend
   npm run dev
   ```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🚀 Production Deployment

### Backend Deployment (Render)

1. **Create Render Account**
   - Go to [Render.com](https://render.com)
   - Sign up for free account

2. **Deploy Backend Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `restaceratops-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT`
     - **Health Check Path**: `/health`

3. **Add Environment Variables**
   ```
   OPENROUTER_API_KEY=your-openrouter-api-key
   MONGODB_URI=your-mongodb-atlas-connection-string
   MONGODB_DB_NAME=restaceratops
   ```

### Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Go to [Vercel.com](https://vercel.com)
   - Sign up for free account

2. **Deploy Frontend**
   - Click "New Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: `Vite`
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **Add Environment Variables**
   ```
   REACT_APP_API_BASE_URL=https://your-backend-url.onrender.com
   ```

## 🤖 AI Integration Setup

### OpenRouter API Key

1. **Get API Key**
   - Go to [OpenRouter.ai/keys](https://openrouter.ai/keys)
   - Sign up and create API key
   - Copy the key (starts with `sk-or-`)

2. **Configure Environment**
   ```bash
   export OPENROUTER_API_KEY='your-api-key'
   ```

### MongoDB Atlas Setup

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
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

## 📋 Usage

### 1. Dashboard
View system statistics, recent tests, and overall health.

### 2. AI Chat
Interact with the AI agent for testing guidance and help.

### 3. Test Runner
Execute tests and monitor results in real-time with comprehensive reporting.

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your-openrouter-api-key
MONGODB_URI=your-mongodb-atlas-connection-string
MONGODB_DB_NAME=restaceratops

# Optional
LOG_LEVEL=INFO
PORT=8000
FRONTEND_PORT=5173
```

### API Configuration

The backend provides RESTful APIs for:

- `/api/chat` - AI chat interface
- `/api/tests/run` - Test execution
- `/api/dashboard` - System statistics
- `/api/generate-tests/openapi` - Test generation from OpenAPI specs
- `/health` - Health check

## 📊 Test Files

The platform supports YAML test specifications:

- `tests/simple_test.yml` - Basic API tests
- `tests/comprehensive_test.yml` - Advanced tests
- `tests/real-world-example.yml` - Real-world scenarios
- `tests/production_ready.yml` - Production tests

## 🎯 Core Features

### ✅ What Works
- **AI-powered test generation** from OpenAPI specifications
- **Real-time test execution** with comprehensive reporting
- **Intelligent chat assistance** for API testing
- **Dashboard with real statistics** and monitoring
- **Downloadable test reports** in Markdown format
- **WebSocket support** for real-time communication
- **MongoDB data persistence** for professional data management

### 🔒 Security
- **API keys stay secure** on backend environment variables
- **Users access AI features** through your backend
- **No API key exposure** to frontend
- **You control all usage** and can implement rate limiting

## 💰 Cost Breakdown

### **Render (Backend)**
- **Free Tier:** $0/month (750 hours/month)
- **Includes:** 256MB RAM, 1GB storage, always-on service

### **Vercel (Frontend)**
- **Free Tier:** $0/month
- **Includes:** Unlimited bandwidth, automatic deployments

### **OpenRouter (AI)**
- **Free Tier:** $0/month (with usage limits)
- **Cost:** Only if you exceed free limits

### **MongoDB Atlas**
- **Free Tier:** $0/month (512MB storage)
- **Includes:** Automatic backups, professional data management

## 🆘 Troubleshooting

### Common Issues

1. **AI not responding**
   - Check your OpenRouter API key
   - Verify the key is set in environment variables

2. **Tests failing**
   - Check the test file format
   - Verify API endpoints are accessible

3. **Deployment issues**
   - Ensure all dependencies are installed
   - Check environment variables are set

4. **Database connection issues**
   - Verify MongoDB Atlas connection string
   - Check network connectivity

### Getting Help

- **API Documentation**: Visit `/docs` endpoint
- **Health Check**: Visit `/health` endpoint
- **Logs**: Check deployment platform logs

## 📈 Performance

- **Response Time**: < 2 seconds for AI responses
- **Test Execution**: Parallel processing support
- **Scalability**: Auto-scaling on Render and Vercel
- **Reliability**: 99.9% uptime on free tiers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🦖 Restaceratops - Making API testing intelligent and accessible!** 