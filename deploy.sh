#!/bin/bash

# 🦖 Team Agentosaurus - Restaceratops Deployment Script
# This script helps deploy the Restaceratops API testing agent

set -e

echo "🦖 Deploying Restaceratops - API Testing Agent"
echo "=============================================="

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker found - building container..."
    docker build -t restaceratops .
    echo "✅ Container built successfully!"
    
    echo ""
    echo "🐳 To run with Docker:"
    echo "   docker run --rm -e BASE_URL=https://your-api.com restaceratops"
    echo "   docker run --rm -v \$(pwd)/tests:/app/tests restaceratops"
else
    echo "⚠️  Docker not found - using local installation"
fi

# Check if Poetry is available
if command -v poetry &> /dev/null; then
    echo "✅ Poetry found - installing dependencies..."
    poetry install --no-root
    echo "✅ Dependencies installed!"
    
    echo ""
    echo "🏃‍♂️ To run locally:"
    echo "   poetry run python -m agent.runner --tests tests"
    echo "   poetry run python -m agent.runner --tests tests --concurrency 5"
else
    echo "⚠️  Poetry not found - please install Poetry first"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
fi

# Run a quick test
echo ""
echo "🧪 Running quick test..."
if command -v poetry &> /dev/null; then
    poetry run python -m agent.runner --tests tests/demo.yml
elif command -v docker &> /dev/null; then
    docker run --rm restaceratops
else
    echo "⚠️  Cannot run test - neither Poetry nor Docker available"
fi

echo ""
echo "🎉 Restaceratops is ready for deployment!"
echo ""
echo "📚 Next steps:"
echo "   1. Create your test files in the tests/ directory"
echo "   2. Set environment variables (BASE_URL, BEARER_TOKEN)"
echo "   3. Deploy to your preferred platform"
echo "   4. Set up monitoring with Prometheus (optional)"
echo ""
echo "🦖 Welcome to Team Agentosaurus!" 