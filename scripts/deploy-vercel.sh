#!/bin/bash

# 🦖 Vercel Deployment Script for Restaceratops Frontend
# This script deploys the frontend to Vercel for free

set -e

echo "🦖 Deploying Restaceratops Frontend to Vercel"
echo "=============================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel..."
    vercel login
fi

# Go to frontend directory
cd frontend

# Check if Railway backend URL is provided
if [ -z "$RAILWAY_BACKEND_URL" ]; then
    echo "🔧 Please enter your Railway backend URL (e.g., https://your-app.railway.app):"
    read RAILWAY_BACKEND_URL
fi

# Create production environment file
echo "🔧 Creating production environment file..."
cat > .env.production << EOF
REACT_APP_API_BASE_URL=$RAILWAY_BACKEND_URL
EOF

# Build the project
echo "🔨 Building the project..."
npm run build

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

# Get the deployment URL
DEPLOYMENT_URL=$(vercel ls --json | grep -o '"url":"[^"]*"' | head -1 | cut -d'"' -f4)

echo ""
echo "✅ Deployment successful!"
echo "🌐 Your frontend is available at: $DEPLOYMENT_URL"
echo ""
echo "📋 Your Restaceratops application is now live!"
echo "🔗 Frontend: $DEPLOYMENT_URL"
echo "🔗 Backend: $RAILWAY_BACKEND_URL"
echo ""
echo "🎉 Users can now access your AI-powered API testing platform!" 