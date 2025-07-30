#!/bin/bash

# 🦖 Restaceratops Startup Script
# This script starts both the backend and frontend services

echo "🦖 Starting Restaceratops..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first."
    echo "Visit: https://python-poetry.org/docs/#installation"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "📦 Installing dependencies..."

# Install backend dependencies
echo "Installing Python dependencies..."
poetry install

# Install frontend dependencies
echo "Installing Node.js dependencies..."
cd frontend
npm install
cd ..

echo "🚀 Starting services..."

# Start backend in background
echo "Starting backend server..."
poetry run python start_backend.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Restaceratops is starting up!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "💚 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait 