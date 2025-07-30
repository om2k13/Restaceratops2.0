# 🦖 Restaceratops - AI-Powered API Testing Platform

A comprehensive, AI-augmented API testing platform with real-time execution, WebSocket support, and intelligent test generation.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Poetry (for Python dependency management)

### Backend Setup
```bash
# Install Python dependencies
poetry install

# Start the FastAPI backend
poetry run uvicorn backend.api.backend:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the React development server
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
restaceratops/
├── 📁 config/                 # Configuration files
│   ├── requirements.txt      # Alternative requirements
│   ├── Dockerfile           # Container configuration
│   ├── vercel.json          # Vercel deployment config
│   ├── .env                 # Environment variables
│   └── .env.backup          # Environment backup
│
├── pyproject.toml            # Python project configuration
├── poetry.lock               # Dependency lock file
│
├── 📁 backend/               # Backend source code
│   ├── 📁 api/              # API endpoints
│   │   ├── backend.py       # Main FastAPI backend
│   │   └── unified_backend.py # Unified API backend
│   │
│   ├── 📁 core/             # Core application logic
│   │   ├── 📁 agents/       # AI agent implementations
│   │   ├── 📁 models/       # Data models
│   │   └── 📁 services/     # Business logic services
│   │
│   ├── 📁 examples/         # Example configurations
│   └── 📁 tests/            # Test specifications
│
├── 📁 frontend/              # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── package.json
│
├── 📁 docs/                  # Documentation
│   ├── README.md           # Main documentation
│   ├── DEPLOYMENT_GUIDE.md # Deployment instructions
│   ├── FREE_AI_SETUP.md    # Free AI setup guide
│   └── MULTI_AI_SETUP.md   # Multi-AI setup guide
│
├── 📁 scripts/               # Utility scripts
│   ├── demo_*.py           # Demo scripts
│   ├── test_*.py           # Test scripts
│   └── debug_*.py          # Debug scripts
│
├── 📁 data/                  # Data storage
│   ├── reports/            # Test reports
│   └── vector_db/          # Vector database
│
├── 📁 deployments/          # Deployment configurations
├── 📁 tools/                # Development tools
└── 📁 .vercel/              # Vercel configuration
```

## 🎯 Key Features

### 🤖 AI-Powered Testing
- **Intelligent Test Generation**: Generate tests from OpenAPI specifications
- **Natural Language Interface**: Chat with AI to create and modify tests
- **Multi-AI Support**: Integration with OpenAI, DeepSeek, and free AI models
- **RAG System**: Retrieval-Augmented Generation for context-aware responses

### 🔄 Real-Time Execution
- **WebSocket Support**: Real-time test execution updates
- **Live Dashboard**: Monitor test execution progress
- **Parallel Testing**: Run multiple tests simultaneously
- **Interactive Reports**: Detailed test results and analytics

### 🛠️ Advanced Features
- **Credential Management**: Secure storage and management of API credentials
- **Data Source Integration**: Support for CSV, JSON, and database sources
- **Template System**: Reusable test templates
- **Assertion Framework**: Comprehensive assertion capabilities
- **Vector Database**: Semantic search and context management

## 🚀 Deployment Options

### Local Development
```bash
# Backend
poetry run uvicorn backend.api.backend:app --reload

# Frontend
cd frontend && npm run dev
```

### Docker Deployment
```bash
docker build -f config/Dockerfile -t restaceratops .
docker run -p 8000:8000 restaceratops
```

### Cloud Deployment
- **Vercel**: See `config/vercel.json`
- **AWS Lambda**: See `deployments/aws-lambda.yml`
- **Kubernetes**: See `deployments/kubernetes-cronjob.yml`
- **Heroku**: See `deployments/heroku-app.json`

## 📚 Documentation

- **[Main Documentation](docs/README.md)**: Comprehensive project overview
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)**: Detailed deployment instructions
- **[Free AI Setup](docs/FREE_AI_SETUP.md)**: Guide for using free AI models
- **[Multi-AI Setup](docs/MULTI_AI_SETUP.md)**: Configuration for multiple AI providers

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the `config/` directory:

```env
# AI Provider Configuration
OPENAI_API_KEY=your_openai_key
DEEPSEEK_API_KEY=your_deepseek_key
OPENROUTER_API_KEY=your_openrouter_key

# Database Configuration
DATABASE_URL=your_database_url

# Security
SECRET_KEY=your_secret_key
```

### AI Model Configuration
The platform supports multiple AI providers:
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **DeepSeek**: DeepSeek-Coder, DeepSeek-Chat
- **OpenRouter**: Access to multiple AI models
- **Free Models**: Ollama, HuggingFace models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the `docs/` directory
- **Examples**: See `src/examples/` for usage examples

---

**🦖 Restaceratops** - Making API testing intelligent and accessible! 