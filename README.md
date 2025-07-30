# 🦖 Restaceratops - AI-Powered API Testing Platform

A comprehensive, AI-augmented API testing platform with advanced workflow management, real-time monitoring, and intelligent test generation capabilities.

## 🚀 Quick Reference

| Service | URL | Command |
|---------|-----|---------|
| **Frontend** | http://localhost:5173 | `cd frontend && npm run dev` |
| **Backend API** | http://localhost:8000 | `poetry run python start_backend.py` |
| **API Docs** | http://localhost:8000/docs | - |
| **Health Check** | http://localhost:8000/health | - |
| **WebSocket** | ws://localhost:8000/ws | - |

### Quick Start Commands
```bash
# Option 1: Use the startup script (recommended)
./start.sh

# Option 2: Manual startup
# Terminal 1: Backend
poetry install && poetry run python start_backend.py

# Terminal 2: Frontend  
cd frontend && npm install && npm run dev
```

## 🚀 Features

- **🤖 AI-Powered Test Generation** - Automatically generate comprehensive test cases using advanced AI models
- **🔄 Advanced Workflow Management** - Create and manage complex testing workflows
- **📊 Real-time Test Monitoring** - Monitor test execution with live performance metrics
- **🏢 Enterprise Features** - Multi-platform support, CI/CD integration, and security compliance
- **💬 Enhanced Chat Interface** - Interactive AI assistant for testing guidance
- **📈 Comprehensive Analytics** - Detailed reporting and performance analysis
- **🔗 Jira Integration** - Seamless integration with project management tools
- **🌐 Multi-AI Provider Support** - Support for OpenAI, OpenRouter, and local AI models

## 🏗️ Architecture

```
restaceratops/
├── backend/                 # FastAPI backend with AI services
│   ├── api/                # API endpoints and routers
│   ├── core/               # Core business logic
│   │   ├── agents/         # AI agents and chat interfaces
│   │   ├── models/         # Data models and managers
│   │   └── services/       # Business services
│   └── tests/              # Backend test files
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── tests/              # Frontend test files
├── config/                 # Configuration files
├── scripts/                # Utility scripts
└── deployments/            # Deployment configurations
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Python 3.12** - Latest Python version
- **Poetry** - Dependency management
- **LangChain** - AI/LLM integration
- **ChromaDB** - Vector database for RAG
- **PyJWT** - Authentication
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS
- **Framer Motion** - Animation library
- **React Router** - Client-side routing
- **Vitest** - Testing framework

### AI/ML
- **OpenAI GPT Models** - Primary AI provider
- **OpenRouter** - Multi-model AI access
- **Ollama** - Local AI models
- **Sentence Transformers** - Text embeddings
- **RAG System** - Retrieval-augmented generation

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Poetry (Python package manager)

### Backend Setup
```bash
# Install dependencies
poetry install

# Start the backend server

## Option 1: Unified Backend (Recommended)
```bash
# Start the unified backend that provides access to ALL functionality
poetry run python start_unified_backend.py
```

**Unified Backend URLs:**
- **🦖 Main Dashboard**: http://localhost:8000 (Comprehensive interface for all features)
- **📚 API Documentation (Swagger)**: http://localhost:8000/docs
- **🔍 API Documentation (ReDoc)**: http://localhost:8000/redoc
- **💚 Health Check**: http://localhost:8000/health
- **📊 Dashboard API**: http://localhost:8000/api/dashboard
- **🤖 Chat API**: http://localhost:8000/api/chat
- **🧪 Tests API**: http://localhost:8000/api/tests
- **🔄 Workflow API**: http://localhost:8000/api/workflow
- **🏢 Enterprise API**: http://localhost:8000/api/enterprise
- **🔗 Jira Integration**: http://localhost:8000/api/jira
- **📡 WebSocket**: ws://localhost:8000/ws

## Option 2: Standard Backend
```bash
# Start the standard backend
poetry run python start_backend.py
```

**Standard Backend URLs:**
- **Main API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Dashboard API**: http://localhost:8000/api/dashboard
- **Chat API**: http://localhost:8000/api/chat
- **Tests API**: http://localhost:8000/api/tests
- **Workflow API**: http://localhost:8000/api/workflow
- **Enterprise API**: http://localhost:8000/api/enterprise
- **Jira Integration**: http://localhost:8000/api/jira
- **WebSocket**: ws://localhost:8000/ws

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend URLs:**
- **Main Application**: http://localhost:5173
- **Dashboard**: http://localhost:5173/
- **AI Chat**: http://localhost:5173/chat
- **Workflow**: http://localhost:5173/workflow
- **Test Generator**: http://localhost:5173/test-generator
- **Test Monitor**: http://localhost:5173/test-monitor
- **Analytics**: http://localhost:5173/analytics
- **Enterprise**: http://localhost:5173/enterprise
- **Test Builder**: http://localhost:5173/test-builder
- **Test Runner**: http://localhost:5173/test-runner
- **Reports**: http://localhost:5173/reports
- **Settings**: http://localhost:5173/settings

### Development Commands

#### Backend Commands
```bash
# Start unified backend (recommended - all features in one place)
poetry run python start_unified_backend.py

# Start standard backend
poetry run python start_backend.py

# Run backend tests
poetry run python -m pytest backend/tests/ -v

# Run specific test file
poetry run python -m pytest backend/tests/test_api.py -v

# Install new dependency
poetry add package_name

# Update dependencies
poetry update

# Show installed packages
poetry show
```

#### Frontend Commands
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test:run

# Run tests in watch mode
npm test

# Run tests with UI
npm run test:ui

# Lint code
npm run lint
```

### Quick Development Workflow
```bash
# Option 1: Use startup script (easiest)
./start.sh

# Option 2: Manual workflow
# Terminal 1: Start Backend
poetry run python start_backend.py

# Terminal 2: Start Frontend
cd frontend && npm run dev

# Terminal 3: Run Tests (optional)
poetry run python -m pytest backend/tests/ -v
cd frontend && npm run test:run
```

### One-Command Startup
```bash
# Start everything with one command
./start.sh

# This will:
# 1. Install all dependencies
# 2. Start backend server
# 3. Start frontend server
# 4. Show all URLs
# 5. Handle graceful shutdown with Ctrl+C
```

## 🧪 Testing

### Backend Tests
```bash
# Run all backend tests
poetry run python -m pytest backend/tests/ -v

# Run specific test file
poetry run python -m pytest backend/tests/test_api.py -v
```

### Frontend Tests
```bash
cd frontend

# Run all frontend tests
npm run test:run

# Run tests in watch mode
npm test
```

## 📋 API Endpoints

### Core Endpoints
- `GET /` - API information and status
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Chat & AI
- `POST /api/chat` - AI chat interface
- `GET /api/chat/system-stats` - System statistics

### Testing
- `POST /api/tests/run` - Execute test suites
- `POST /api/tests/load` - Load test configurations

### Workflow
- `GET /api/workflow/` - List workflows
- `POST /api/workflow/` - Create workflow

### Enterprise
- `GET /api/enterprise/overview` - Enterprise dashboard
- `GET /api/enterprise/platforms` - Platform configurations

### Jira Integration
- `POST /api/jira/connect` - Connect to Jira
- `GET /api/jira/stories` - Get Jira stories

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# AI Configuration
OPENAI_API_KEY=your_openai_key
OPENROUTER_API_KEY=your_openrouter_key

# Database
DATABASE_URL=your_database_url

# Security
JWT_SECRET_KEY=your_jwt_secret

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

### Quick Environment Setup
```bash
# Create environment file
cp .env.example .env  # if available
# or create manually:
touch .env

# Edit with your API keys
nano .env  # or use your preferred editor
```

### Configuration Files
- `pyproject.toml` - Python dependencies and project config
- `frontend/package.json` - Node.js dependencies
- `config/requirements.txt` - Additional Python requirements

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker
docker build -t restaceratops .
docker run -p 8000:8000 restaceratops
```

### Vercel Deployment
```bash
# Deploy frontend to Vercel
cd frontend
vercel --prod
```

### AWS Lambda
```bash
# Deploy backend to AWS Lambda
cd deployments
./deploy-serverless.sh
```

## 📊 Monitoring & Analytics

### Real-time Metrics
- Test execution performance
- API response times
- Error rates and success rates
- Resource utilization

### Reporting
- Comprehensive test reports
- Performance analytics
- Compliance reports
- Audit logs

## 🔒 Security Features

- **JWT Authentication** - Secure user authentication
- **RBAC (Role-Based Access Control)** - Enterprise-grade permissions
- **Audit Logging** - Comprehensive activity tracking
- **Encryption** - Data encryption at rest and in transit
- **Session Management** - Secure session handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` directory
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join community discussions

## 🔧 Troubleshooting

### Common Issues

#### Backend Issues
```bash
# Port 8000 already in use
lsof -ti:8000 | xargs kill -9

# Poetry environment issues
poetry env remove python
poetry install

# Missing dependencies
poetry install --sync
```

#### Frontend Issues
```bash
# Port 5173 already in use
lsof -ti:5173 | xargs kill -9

# Node modules issues
rm -rf node_modules package-lock.json
npm install

# Vite cache issues
rm -rf node_modules/.vite
npm run dev
```

#### Connection Issues
- **Frontend can't connect to backend**: Ensure backend is running on port 8000
- **CORS errors**: Backend CORS is configured for `http://localhost:5173`
- **WebSocket connection failed**: Check if backend WebSocket endpoint is accessible

### Health Checks
```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend is serving
curl http://localhost:5173

# Test API endpoints
curl http://localhost:8000/
```

## 🗺️ Roadmap

- [ ] Enhanced AI model support
- [ ] Advanced workflow automation
- [ ] Mobile app development
- [ ] Cloud-native deployment options
- [ ] Advanced analytics and ML insights
- [ ] Multi-language support
- [ ] Plugin system for extensibility

---

**🦖 Built with ❤️ by the Restaceratops Team** 