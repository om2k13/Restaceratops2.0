#!/bin/bash

# 🦖 Render Deployment Script for Restaceratops Backend
# This script deploys the backend to Render for free

set -e

echo "🦖 Deploying Restaceratops Backend to Render"
echo "============================================="

# Check if Render CLI is installed
if ! command -v render &> /dev/null; then
    echo "📦 Installing Render CLI..."
    curl -s https://render.com/download-cli/install.sh | bash
fi

# Check if user is logged in
if ! render whoami &> /dev/null; then
    echo "🔐 Please login to Render..."
    render login
fi

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found. Creating it..."
    cat > render.yaml << 'EOF'
services:
  - type: web
    name: restaceratops-backend
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: uvicorn backend.api.unified_backend:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: OPENROUTER_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.12.0
EOF
fi

# Initialize Render project
echo "🚀 Initializing Render project..."
render blueprint apply

# Set environment variables
echo "🔧 Setting up environment variables..."
echo "Please enter your OpenRouter API key:"
read -s OPENROUTER_API_KEY

render env set OPENROUTER_API_KEY "$OPENROUTER_API_KEY"

# Deploy to Render
echo "🚀 Deploying to Render..."
render deploy

# Get the deployment URL
echo ""
echo "✅ Deployment successful!"
echo ""
echo "📋 Next steps:"
echo "   1. Check your Render dashboard for the deployment URL"
echo "   2. Update frontend/src/services/api.ts with this URL"
echo "   3. Deploy frontend to Vercel"
echo "   4. Test the application"
echo ""
echo "🔗 Your backend will be available at: https://your-app-name.onrender.com"
echo "🔗 API Documentation: https://your-app-name.onrender.com/docs"
echo "🔗 Health Check: https://your-app-name.onrender.com/health" 