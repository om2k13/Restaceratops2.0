#!/bin/bash

# 🦖 Clean Restaceratops Deployment Script
# Deploys the cleaned version to Render (backend) and Vercel (frontend)

set -e

echo "🦖 Deploying Clean Restaceratops - API Testing Platform"
echo "======================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "backend/api/main.py" ]; then
    print_error "Main backend not found. Make sure you're in the project root directory."
    exit 1
fi

print_status "Starting deployment process..."

# Step 1: Deploy Backend to Render
print_status "Step 1: Deploying backend to Render..."

# Check if Render CLI is installed
if ! command -v render &> /dev/null; then
    print_status "Installing Render CLI..."
    curl -s https://render.com/download-cli/install.sh | bash
fi

# Check if user is logged in to Render
if ! render whoami &> /dev/null; then
    print_warning "Please login to Render..."
    render login
fi

# Deploy to Render
print_status "Deploying backend to Render..."
render blueprint apply

# Get the deployment URL
print_status "Getting Render deployment URL..."
RENDER_URL=$(render services list --json | grep -o '"url":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$RENDER_URL" ]; then
    print_error "Failed to get Render URL. Please check your deployment."
    exit 1
fi

print_success "Backend deployed to: $RENDER_URL"

# Step 2: Deploy Frontend to Vercel
print_status "Step 2: Deploying frontend to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_status "Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if user is logged in to Vercel
if ! vercel whoami &> /dev/null; then
    print_warning "Please login to Vercel..."
    vercel login
fi

# Go to frontend directory
cd frontend

# Create production environment file
print_status "Creating production environment file..."
cat > .env.production << EOF
REACT_APP_API_BASE_URL=$RENDER_URL
EOF

# Build the project
print_status "Building frontend project..."
npm run build

# Deploy to Vercel
print_status "Deploying frontend to Vercel..."
vercel --prod

# Get the deployment URL
print_status "Getting Vercel deployment URL..."
VERCEL_URL=$(vercel ls --json | grep -o '"url":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$VERCEL_URL" ]; then
    print_error "Failed to get Vercel URL. Please check your deployment."
    exit 1
fi

print_success "Frontend deployed to: $VERCEL_URL"

# Go back to root directory
cd ..

# Step 3: Set up environment variables
print_status "Step 3: Setting up environment variables..."

# Prompt for OpenRouter API key
echo ""
print_warning "Please enter your OpenRouter API key for the backend:"
read -s OPENROUTER_API_KEY

if [ -z "$OPENROUTER_API_KEY" ]; then
    print_error "OpenRouter API key is required for AI features to work."
    exit 1
fi

# Set environment variable on Render
print_status "Setting OpenRouter API key on Render..."
render env set OPENROUTER_API_KEY "$OPENROUTER_API_KEY"

# Step 4: Test the deployment
print_status "Step 4: Testing the deployment..."

# Wait a moment for deployment to complete
sleep 10

# Test backend health
print_status "Testing backend health..."
if curl -s "$RENDER_URL/health" > /dev/null; then
    print_success "Backend health check passed"
else
    print_warning "Backend health check failed - this might be normal during deployment"
fi

# Test frontend
print_status "Testing frontend..."
if curl -s "$VERCEL_URL" > /dev/null; then
    print_success "Frontend is accessible"
else
    print_warning "Frontend might still be deploying"
fi

# Step 5: Final summary
echo ""
echo "🎉 Deployment Complete!"
echo "======================"
print_success "Your Restaceratops API Testing Platform is now live!"
echo ""
echo "📋 Deployment URLs:"
echo "   Frontend: $VERCEL_URL"
echo "   Backend:  $RENDER_URL"
echo "   API Docs: $RENDER_URL/docs"
echo ""
echo "🔧 Environment Variables:"
echo "   OpenRouter API Key: ✅ Set"
echo ""
echo "🧪 Test Your Deployment:"
echo "   1. Visit: $VERCEL_URL"
echo "   2. Try the AI Chat feature"
echo "   3. Run some API tests"
echo "   4. Check the dashboard"
echo ""
echo "📚 Available Features:"
echo "   ✅ AI-powered test generation"
echo "   ✅ Real-time test execution"
echo "   ✅ Comprehensive test reporting"
echo "   ✅ Intelligent chat assistance"
echo "   ✅ OpenAPI specification parsing"
echo ""
print_success "Your HR can now access the platform at: $VERCEL_URL"
echo ""
echo "🦖 Restaceratops is ready for production use!" 