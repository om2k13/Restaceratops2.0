#!/bin/bash

# 🦖 Restaceratops Docker Deployment Script
# This script automates the deployment of Restaceratops on AWS instances

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="restaceratops"
DOCKER_COMPOSE_FILE="docker-compose.yml"
PROD_COMPOSE_FILE="docker-compose.prod.yml"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root. Please run as a regular user with sudo privileges."
    fi
}

# Check Docker installation
check_docker() {
    log "Checking Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check if user is in docker group
    if ! groups $USER | grep -q docker; then
        warn "User is not in docker group. Adding user to docker group..."
        sudo usermod -a -G docker $USER
        log "Please logout and login again, then run this script."
        exit 0
    fi
    
    log "Docker and Docker Compose are properly installed."
}

# Check environment file
check_env() {
    log "Checking environment configuration..."
    
    if [[ ! -f ".env" ]]; then
        if [[ -f "env.example" ]]; then
            log "Creating .env file from env.example..."
            cp env.example .env
            warn "Please edit .env file with your actual configuration values."
            error "After editing .env file, run this script again."
        else
            error ".env file not found and env.example not available."
        fi
    fi
    
    # Check required environment variables
    source .env
    
    if [[ -z "$OPENROUTER_API_KEY" ]]; then
        error "OPENROUTER_API_KEY is not set in .env file."
    fi
    
    if [[ -z "$MONGODB_URI" ]]; then
        warn "MONGODB_URI is not set. Using local MongoDB."
    fi
    
    log "Environment configuration is valid."
}

# Stop existing containers
stop_containers() {
    log "Stopping existing containers..."
    
    if docker-compose ps | grep -q "Up"; then
        docker-compose down
        log "Existing containers stopped."
    else
        log "No running containers found."
    fi
}

# Clean up Docker resources
cleanup() {
    log "Cleaning up Docker resources..."
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused volumes
    docker volume prune -f
    
    # Remove unused networks
    docker network prune -f
    
    log "Cleanup completed."
}

# Build images
build_images() {
    log "Building Docker images..."
    
    # Build backend
    log "Building backend image..."
    docker-compose build backend
    
    # Build frontend
    log "Building frontend image..."
    docker-compose build frontend
    
    log "All images built successfully."
}

# Start services
start_services() {
    log "Starting services..."
    
    # Start services in background
    docker-compose up -d
    
    log "Services started. Waiting for health checks..."
    
    # Wait for services to be healthy
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if docker-compose ps | grep -q "healthy"; then
            log "All services are healthy!"
            break
        fi
        
        log "Waiting for services to be healthy... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done
    
    if [[ $attempt -gt $max_attempts ]]; then
        warn "Services may not be fully healthy. Check logs with: docker-compose logs"
    fi
}

# Check service status
check_status() {
    log "Checking service status..."
    
    echo -e "\n${BLUE}Container Status:${NC}"
    docker-compose ps
    
    echo -e "\n${BLUE}Service URLs:${NC}"
    echo "Frontend: http://13.200.242.64:80"
    echo "Backend API: http://13.200.242.64:8000"
    echo "API Documentation: http://13.200.242.64:8000/docs"
    echo "Health Check: http://13.200.242.64:8000/health"
    
    echo -e "\n${BLUE}Resource Usage:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
}

# Show logs
show_logs() {
    log "Recent logs from all services:"
    docker-compose logs --tail=20
}

# Backup function
backup() {
    log "Creating backup..."
    
    local backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup environment file
    cp .env "$backup_dir/"
    
    # Backup uploads directory
    if [[ -d "backend/uploads" ]]; then
        cp -r backend/uploads "$backup_dir/"
    fi
    
    # Backup MongoDB data if running locally
    if docker-compose ps | grep -q "mongodb.*Up"; then
        log "Backing up MongoDB data..."
        docker exec restaceratops-mongodb mongodump --out /backup
        docker cp restaceratops-mongodb:/backup "$backup_dir/mongodb_backup"
    fi
    
    log "Backup created in: $backup_dir"
}

# Main deployment function
deploy() {
    log "Starting Restaceratops deployment..."
    
    check_root
    check_docker
    check_env
    stop_containers
    cleanup
    build_images
    start_services
    check_status
    
    log "Deployment completed successfully!"
    log "Your Restaceratops agent is now running on AWS!"
}

# Production deployment
deploy_prod() {
    log "Starting production deployment..."
    
    check_root
    check_docker
    check_env
    
    # Use production compose file
    export COMPOSE_FILE=$PROD_COMPOSE_FILE
    
    stop_containers
    cleanup
    build_images
    start_services
    check_status
    
    log "Production deployment completed successfully!"
}

# Update function
update() {
    log "Updating Restaceratops..."
    
    # Pull latest changes
    git pull origin main
    
    # Rebuild and restart
    stop_containers
    cleanup
    build_images
    start_services
    check_status
    
    log "Update completed successfully!"
}

# Show help
show_help() {
    echo -e "${BLUE}Restaceratops Docker Deployment Script${NC}"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy      Deploy Restaceratops (development)"
    echo "  deploy-prod Deploy Restaceratops (production)"
    echo "  update      Update existing deployment"
    echo "  stop        Stop all services"
    echo "  start       Start all services"
    echo "  restart     Restart all services"
    echo "  status      Show service status"
    echo "  logs        Show recent logs"
    echo "  backup      Create backup"
    echo "  cleanup     Clean up Docker resources"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy        # Deploy for development"
    echo "  $0 deploy-prod   # Deploy for production"
    echo "  $0 update        # Update existing deployment"
    echo "  $0 status        # Check service status"
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "deploy-prod")
        deploy_prod
        ;;
    "update")
        update
        ;;
    "stop")
        log "Stopping services..."
        docker-compose down
        ;;
    "start")
        log "Starting services..."
        docker-compose up -d
        ;;
    "restart")
        log "Restarting services..."
        docker-compose restart
        ;;
    "status")
        check_status
        ;;
    "logs")
        show_logs
        ;;
    "backup")
        backup
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        error "Unknown command: $1. Use '$0 help' for usage information."
        ;;
esac
