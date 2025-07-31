# 📁 Project Structure Overview

This document provides a detailed breakdown of the Restaceratops project structure and the purpose of each directory and file.

## 🏗️ Directory Organization

### 📁 Root Level
```
restaceratops/
├── README.md                 # Main project documentation
├── PROJECT_STRUCTURE.md      # This file - detailed structure guide
├── .gitignore               # Git ignore patterns
└── .DS_Store                # macOS system file
```

### 📁 config/ - Configuration Files
All configuration files are centralized here for easy management.

```
config/
├── pyproject.toml           # Python project configuration (Poetry)
├── poetry.lock              # Dependency lock file
├── requirements.txt         # Alternative pip requirements
├── Dockerfile              # Container configuration
├── vercel.json             # Vercel deployment configuration
├── .env                    # Environment variables (create this)
└── .env.backup             # Environment variables backup
```

**Purpose**: Centralized configuration management for easy deployment and environment setup.

### 📁 backend/ - Backend Source Code
The main backend application source code organized by functionality.

```
backend/
├── 📁 api/                 # API Layer
│   ├── backend.py          # Main FastAPI backend with WebSocket support
│   └── unified_backend.py  # Unified API backend for all features
│
├── 📁 core/                # Core Application Logic
│   ├── 📁 agents/          # AI Agent Implementations
│   │   ├── __init__.py
│   │   ├── enhanced_ai_system.py      # Enhanced AI system
│   │   ├── enhanced_chat_interface.py # Chat interface
│   │   ├── openrouter_ai_system.py    # OpenRouter integration
│   │   ├── rag_system.py              # RAG system
│   │   ├── unified_agent.py           # Unified agent
│   │   └── chat_interface.py          # Basic chat interface
│   │
│   ├── 📁 models/          # Data Models
│   │   ├── __init__.py
│   │   ├── auth_manager.py            # Authentication models
│   │   ├── test_input_manager.py      # Test input models
│   │   └── vector_store.py            # Vector database models
│   │
│   └── 📁 services/        # Business Logic Services
│       ├── __init__.py
│       ├── client.py                  # API client service
│       ├── dsl_loader.py              # DSL loader service
│       ├── enhanced_openapi_generator.py # OpenAPI generator
│       ├── openapi_generator.py       # Basic OpenAPI generator
│       ├── generator_llm.py           # LLM generator service
│       ├── runner.py                  # Test runner service
│       ├── assertions.py              # Assertion service
│       └── reporters/                 # Report generation services
│           ├── __init__.py
│           ├── console.py             # Console reporter
│           ├── html_reporter.py       # HTML reporter
│           ├── junit_xml.py           # JUnit XML reporter
│           └── prometheus_exporter.py # Prometheus exporter
│
├── 📁 web/                 # Web Interface Components
│   ├── templates/          # HTML templates
│   ├── static/             # Static assets
│   └── web_interface.py    # Flask web interface
│
├── 📁 utils/               # Utility Functions
│   ├── helpers/            # Helper functions
│   └── validators/         # Data validation utilities
│
├── 📁 examples/            # Example Configurations
│   ├── data/               # Sample data files
│   │   ├── products.json   # Sample product data
│   │   └── users.csv       # Sample user data
│   ├── demo-api.yaml       # Demo API specification
│   ├── integration_suite.yml # Integration test suite
│   └── sample-api.yaml     # Sample API specification
│
└── 📁 tests/               # Test Specifications
    ├── simple_test.yml     # Simple test example
    ├── demo.yml            # Demo test
    ├── feature_demo.yml    # Feature demonstration tests
    ├── advanced_features.yml # Advanced feature tests
    ├── comprehensive_test.yml # Comprehensive test suite
    ├── production_ready.yml # Production-ready tests
    ├── real-world-example.yml # Real-world test examples
    ├── my-api-example.yml  # API example tests
    ├── generated_*.yml     # AI-generated test files
    └── demo-generated.yml  # Demo generated tests
```

### 📁 frontend/ - React Frontend Application
Modern React application with TypeScript and Tailwind CSS.

```
frontend/
├── 📁 src/
│   ├── 📁 components/      # Reusable React components
│   │   └── Sidebar.tsx     # Sidebar navigation component
│   │
│   ├── 📁 pages/          # Page components
│   │   ├── ChatInterface.tsx # Chat interface page
│   │   ├── Dashboard.tsx   # Dashboard page
│   │   ├── Reports.tsx     # Reports page
│   │   ├── Settings.tsx    # Settings page
│   │   ├── TestBuilder.tsx # Test builder page
│   │   └── TestRunner.tsx  # Test runner page
│   │
│   ├── 📁 services/       # API services
│   │   ├── api.ts         # API client service
│   │   └── websocket.ts   # WebSocket service
│   │
│   ├── 📁 assets/         # Static assets
│   │   └── react.svg      # React logo
│   │
│   ├── App.tsx            # Main App component
│   ├── App.css            # App styles
│   ├── main.tsx           # Application entry point
│   └── index.css          # Global styles
│
├── 📁 public/             # Public assets
│   └── vite.svg           # Vite logo
│
├── package.json           # Node.js dependencies
├── package-lock.json      # Dependency lock file
├── tsconfig.json          # TypeScript configuration
├── vite.config.ts         # Vite build configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── postcss.config.js      # PostCSS configuration
└── eslint.config.js       # ESLint configuration
```

### 📁 docs/ - Documentation
Comprehensive documentation for the project.

```
docs/
├── README.md                    # Main documentation
├── DEPLOYMENT_GUIDE.md         # Deployment instructions
├── DEPLOYMENT.md               # Alternative deployment guide
├── FREE_AI_SETUP.md            # Free AI setup guide
├── MULTI_AI_SETUP.md           # Multi-AI setup guide
├── PROJECT_IMPLEMENTATION_TRACKER.md # Implementation tracking
└── PROJECT_PROGRESS.md         # Project progress documentation
```

### 📁 scripts/ - Utility Scripts
Scripts for development, testing, and demonstration.

```
scripts/
├── 📁 demo/                   # Demo scripts
│   ├── demo_chat.py           # Chat demo
│   ├── demo_enhanced_features.py # Enhanced features demo
│   ├── enhanced_demo.py       # Enhanced demo
│   └── advanced_demo.py       # Advanced demo
│
├── 📁 test/                   # Test scripts
│   ├── test_deepseek.py       # DeepSeek testing
│   ├── test_openrouter.py     # OpenRouter testing
│   ├── test_enhanced_chat.py  # Enhanced chat testing
│   └── test_system_stats.py   # System statistics testing
│
├── 📁 debug/                  # Debug scripts
│   ├── debug_test.py          # Test debugging
│   └── debug_full_test.py     # Full test debugging
│
└── 📁 tools/                  # Utility tools
    ├── check_deepseek_status.py # DeepSeek status checker
    └── show_fallback_hierarchy.py # Fallback hierarchy display
```

### 📁 data/ - Data Storage
All data files, logs, and persistent storage.

```
data/
├── 📁 logs/                   # Application logs
├── 📁 cache/                  # Cache files
├── 📁 backups/                # Backup files
├── 📁 reports/                # Test reports
│   └── test_report.html       # HTML test report
├── 📁 vector_db/              # Vector database
│   ├── chroma.sqlite3         # ChromaDB database
│   └── [uuid]/                # Vector collections
│       ├── data_level0.bin
│       ├── header.bin
│       ├── length.bin
│       └── link_lists.bin
└── report.xml                 # Test report in XML format
```

### 📁 deployments/ - Deployment Configurations
Configuration files for various deployment platforms.

```
deployments/
├── aws-lambda.yml            # AWS Lambda configuration
├── github-actions.yml        # GitHub Actions CI/CD
├── heroku-app.json           # Heroku deployment
├── kubernetes-cronjob.yml    # Kubernetes cronjob
└── serverless-costs.md       # Serverless cost analysis
```

### 📁 tools/ - Development Tools
Additional development and utility tools.

```
tools/
└── [future development tools]
```

## 🔄 File Naming Conventions

### Python Files
- **snake_case**: All Python files use snake_case naming
- **Descriptive names**: Files are named based on their functionality
- **Module prefixes**: Related files are grouped with prefixes (e.g., `test_*`, `demo_*`, `debug_*`)

### Configuration Files
- **Standard extensions**: `.toml`, `.json`, `.yml`, `.yaml`
- **Environment files**: `.env` for environment variables
- **Lock files**: `poetry.lock`, `package-lock.json` for dependency locking

### Documentation Files
- **Markdown format**: All documentation uses `.md` extension
- **Descriptive names**: Clear, descriptive file names
- **Hierarchical organization**: Related docs grouped in subdirectories

## 🎯 Key Organizational Principles

### 1. **Separation of Concerns**
- **API Layer**: Handles HTTP requests and responses
- **Core Logic**: Contains business logic and AI agents
- **Web Interface**: Manages user interface components
- **Utilities**: Provides helper functions and tools

### 2. **Configuration Centralization**
- All configuration files in `config/` directory
- Environment variables in `.env` files
- Deployment configs in `deployments/` directory

### 3. **Data Organization**
- Persistent data in `data/` directory
- Logs, cache, and backups properly categorized
- Vector database with proper structure

### 4. **Documentation Structure**
- Main docs in `docs/` directory
- README files for quick reference
- Detailed guides for specific topics

### 5. **Script Organization**
- Demo scripts for showcasing features
- Test scripts for validation
- Debug scripts for troubleshooting
- Utility tools for maintenance

## 🚀 Benefits of This Structure

1. **Easy Navigation**: Clear directory structure makes it easy to find files
2. **Scalability**: Organized structure supports project growth
3. **Maintainability**: Related files are grouped together
4. **Deployment Ready**: Configuration files are properly organized
5. **Developer Friendly**: Intuitive structure for new contributors
6. **Documentation**: Comprehensive documentation structure
7. **Testing**: Organized test files and specifications

This structure provides a clean, professional, and maintainable codebase that's easy to navigate and understand. 