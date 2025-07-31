# 🦖 Restaceratops

**AI-Powered API Testing Agent using OpenRouter Qwen3 Coder**

Restaceratops is a modern, AI-augmented API testing platform that leverages the power of OpenRouter's Qwen3 Coder model to provide intelligent test generation, execution, and analysis.

## ✨ Features

- 🤖 **AI-Powered Testing**: Uses OpenRouter Qwen3 Coder for intelligent test generation
- 🧪 **Comprehensive Testing**: Supports positive, negative, and edge case testing
- 📊 **Real-time Monitoring**: Live test execution monitoring and reporting
- 🔧 **Easy Integration**: Simple setup with minimal dependencies
- 💰 **Cost-Effective**: Uses free OpenRouter models for zero-cost AI integration
- 🚀 **Modern Stack**: Built with FastAPI, React, and TypeScript

## 🏗️ Architecture

```
restaceratops/
├── backend/                 # FastAPI backend
│   ├── api/                # API endpoints
│   ├── core/               # Core functionality
│   │   ├── agents/         # AI agents (OpenRouter Qwen3)
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   └── tests/              # Backend tests
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/          # React components
│   │   └── services/       # API services
├── docs/                   # Documentation
│   └── md/                 # Markdown files
├── scripts/                # Utility scripts
└── data/                   # Data storage
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- OpenRouter API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd restaceratops
   ```

2. **Set up environment**
   ```bash
   # Create .env file
   echo "OPENROUTER_API_KEY=your-api-key-here" > .env
   ```

3. **Install dependencies**
   ```bash
   # Install Python dependencies
   poetry install
   
   # Install frontend dependencies
   cd frontend
   npm install
   cd ..
   ```

4. **Start the application**
   ```bash
   # Use the startup script
   ./start.sh
   ```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🤖 AI Integration

### OpenRouter Qwen3 Coder

Restaceratops uses OpenRouter's Qwen3 Coder model for:

- **Test Generation**: Create comprehensive test cases from API specifications
- **Conversation**: Intelligent chat interface for API testing guidance
- **Analysis**: Analyze API responses and provide insights
- **Troubleshooting**: Debug API issues with AI assistance

### Configuration

The AI system is configured to use only OpenRouter Qwen3 Coder:

```python
# Single model configuration
model = "qwen/qwen3-coder:free"
api_key = os.getenv("OPENROUTER_API_KEY")
```

## 📋 Usage

### 1. Dashboard
View system statistics, recent tests, and overall health.

### 2. AI Chat
Interact with the AI agent for testing guidance and help.

### 3. Test Generator
Generate test cases from API specifications or URLs.

### 4. Test Runner
Execute tests and monitor results in real-time.

### 5. Test Monitor
Track test execution progress and performance.

### 6. Reports
Generate detailed test reports and analytics.

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your-openrouter-api-key

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
- `/api/workflow/*` - Workflow management

## 📊 Monitoring

### Logs
- Application logs: `conversation_logs.txt`
- AI conversation logs: Detailed in conversation_logs.txt

### Metrics
- Test execution statistics
- AI model usage
- System performance metrics

## 🛠️ Development

### Backend Development

```bash
# Run backend in development mode
poetry run python start_backend.py

# Run tests
poetry run pytest
```

### Frontend Development

```bash
# Run frontend in development mode
cd frontend
npm run dev
```

### Code Quality

```bash
# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy .

# Linting
poetry run flake8 .
```

## 📚 Documentation

All documentation is organized in the `docs/` directory:

- `docs/md/` - Markdown documentation files
- API documentation available at `/docs` endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

1. Check the documentation in `docs/md/`
2. Review the API documentation at `/docs`
3. Open an issue on GitHub

---

**Built with ❤️ using OpenRouter Qwen3 Coder** 