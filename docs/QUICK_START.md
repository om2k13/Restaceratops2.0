# 🚀 Quick Start Guide

Get Restaceratops up and running in minutes!

## 📋 Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **Poetry** (Python package manager)
- **Git**

## ⚡ Fast Setup (5 minutes)

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd restaceratops
```

### 2. Backend Setup
```bash
# Install Python dependencies
cd config
poetry install

# Start the backend server
poetry run uvicorn backend.api.backend:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup (New Terminal)
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the frontend
npm run dev
```

### 4. Access Your Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Configuration

### Environment Setup
Create a `.env` file in the `config/` directory:

```env
# AI Provider Keys (choose one or more)
OPENAI_API_KEY=your_openai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Optional: Database URL
DATABASE_URL=sqlite:///data/restaceratops.db

# Optional: Secret key for sessions
SECRET_KEY=your_secret_key_here
```

### AI Model Selection
The platform supports multiple AI providers:

1. **OpenAI** (Recommended for production)
   - GPT-4, GPT-3.5-turbo
   - Most reliable and feature-rich

2. **DeepSeek** (Good alternative)
   - DeepSeek-Coder, DeepSeek-Chat
   - Cost-effective for coding tasks

3. **OpenRouter** (Multiple models)
   - Access to various AI models
   - Good for experimentation

4. **Free Models** (No API key required)
   - Ollama (local models)
   - HuggingFace models

## 🎯 First Steps

### 1. Explore the Interface
- Visit http://localhost:5173
- Navigate through the different pages
- Check out the dashboard

### 2. Try the Chat Interface
- Go to the Chat page
- Ask questions like:
  - "Create a test for a user API"
  - "Generate tests from this OpenAPI spec"
  - "Help me debug this test failure"

### 3. Run Your First Test
- Go to the Test Runner page
- Select a test file from `src/tests/`
- Click "Run Tests" and watch the real-time execution

### 4. Check API Documentation
- Visit http://localhost:8000/docs
- Explore the available endpoints
- Try out the API directly

## 📁 Key Directories

```
restaceratops/
├── config/           # Configuration files
├── backend/          # Backend source code
│   ├── api/         # Backend APIs
│   ├── core/        # Core logic
│   ├── tests/       # Test specifications
│   └── examples/    # Example configurations
├── frontend/         # React frontend
├── docs/            # Documentation
├── scripts/         # Utility scripts
└── data/            # Data storage
```

## 🛠️ Development Commands

### Backend Development
```bash
# Run with auto-reload
poetry run uvicorn backend.api.backend:app --reload

# Run specific backend
poetry run uvicorn backend.api.unified_backend:app --reload

# Run Flask web interface (alternative to React frontend)
# poetry run python backend/web/web_interface.py
```

### Frontend Development
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing
```bash
# Run Python tests
poetry run pytest

# Run specific test file
poetry run python scripts/test_enhanced_chat.py
```

## 🚀 Deployment Options

### Local Development
```bash
# Backend
poetry run uvicorn backend.api.backend:app --reload

# Frontend
cd frontend && npm run dev
```

### Docker
```bash
# Build and run
docker build -f config/Dockerfile -t restaceratops .
docker run -p 8000:8000 restaceratops
```

### Cloud Platforms
- **Vercel**: See `config/vercel.json`
- **AWS Lambda**: See `deployments/aws-lambda.yml`
- **Heroku**: See `deployments/heroku-app.json`
- **Kubernetes**: See `deployments/kubernetes-cronjob.yml`

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Poetry not found**
   ```bash
   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Node modules issues**
   ```bash
   # Clear and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Environment variables not loading**
   ```bash
   # Check if .env file exists
   ls -la config/.env
   ```

### Getting Help

- **Documentation**: Check the `docs/` directory
- **Examples**: See `backend/examples/` for usage examples
- **Issues**: Create an issue on GitHub
- **API Docs**: Visit http://localhost:8000/docs

## 🎉 Next Steps

1. **Read the Documentation**: Check out `docs/README.md`
2. **Explore Examples**: Look at `src/examples/`
3. **Try Different AI Models**: Configure multiple AI providers
4. **Create Your Own Tests**: Use the test builder interface
5. **Deploy to Production**: Follow the deployment guides

---

**🦖 Happy Testing with Restaceratops!** 