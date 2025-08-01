#!/bin/bash

# 🦖 Railway Deployment Script for Restaceratops Backend
# This script deploys the backend to Railway for free

set -e

echo "🦖 Deploying Restaceratops Backend to Railway"
echo "=============================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    railway login
fi

# Initialize Railway project if not already done
if [ ! -f "railway.json" ]; then
    echo "🚀 Initializing Railway project..."
    railway init
fi

# Set environment variables
echo "🔧 Setting up environment variables..."
echo "Please enter your OpenRouter API key:"
read -s OPENROUTER_API_KEY

railway variables set OPENROUTER_API_KEY="$OPENROUTER_API_KEY"

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

# Get the deployment URL
DEPLOYMENT_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)

echo ""
echo "✅ Deployment successful!"
echo "🌐 Your backend is available at: $DEPLOYMENT_URL"
echo ""
echo "📋 Next steps:"
echo "   1. Update frontend/src/services/api.ts with this URL"
echo "   2. Deploy frontend to Vercel"
echo "   3. Test the application"
echo ""
echo "🔗 API Documentation: $DEPLOYMENT_URL/docs"
echo "🔗 Health Check: $DEPLOYMENT_URL/health" 