# 🐳 Docker Deployment Guide for Restaceratops

This guide will help you deploy Restaceratops on AWS instances using Docker.

## 📋 Prerequisites

- Docker and Docker Compose installed on your AWS instance
- OpenRouter API key
- MongoDB Atlas account (recommended) or local MongoDB
- AWS EC2 instance with at least 2GB RAM

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd restaceratops

# Copy environment file
cp env.example .env

# Edit environment variables
nano .env
```

### 2. Configure Environment Variables

Edit `.env` file with your actual values:

```bash
# Required: OpenRouter API Key
OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key

# Required: MongoDB URI (use MongoDB Atlas for production)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/restaceratops

# Optional: Frontend API URL
VITE_API_BASE_URL=http://13.200.242.64:8000
```

### 3. Deploy with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

## 🌐 Access Your Application

- **Frontend**: http://13.200.242.64:80
- **Backend API**: http://13.200.242.64:8000
- **API Documentation**: http://13.200.242.64:8000/docs
- **Health Check**: http://13.200.242.64:8000/health

## 🔧 AWS EC2 Setup

### 1. Launch EC2 Instance

```bash
# Recommended instance type
Instance Type: t3.medium (2 vCPU, 4GB RAM)
AMI: Amazon Linux 2 or Ubuntu 22.04
Storage: 20GB GP3
Security Group: Allow ports 22, 80, 8000
```

### 2. Install Docker

**For Amazon Linux 2:**
```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again
exit
```

**For Ubuntu 22.04:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ubuntu

# Logout and login again
exit
```

### 3. Configure Security Groups

Open these ports in your EC2 security group:
- **Port 22**: SSH access
- **Port 80**: HTTP (frontend)
- **Port 8000**: Backend API
- **Port 27017**: MongoDB (if using local MongoDB)

## 📊 Production Deployment

### 1. Use MongoDB Atlas (Recommended)

```bash
# Get connection string from MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/restaceratops?retryWrites=true&w=majority
```

### 2. Set Up Domain and SSL

```bash
# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### 3. Production Docker Compose

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 Monitoring and Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Health Checks
```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend health
curl http://localhost/health

# Check container status
docker-compose ps
```

### Resource Usage
```bash
# Container resource usage
docker stats

# Disk usage
docker system df
```

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Backup Data
```bash
# Backup MongoDB data
docker exec restaceratops-mongodb mongodump --out /backup

# Copy backup from container
docker cp restaceratops-mongodb:/backup ./backup
```

### Clean Up
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune
```

## 🛠️ Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using the port
sudo netstat -tulpn | grep :8000

# Kill the process
sudo kill -9 <PID>
```

**2. Docker Permission Issues**
```bash
# Add user to docker group
sudo usermod -a -G docker $USER

# Restart Docker service
sudo systemctl restart docker
```

**3. Memory Issues**
```bash
# Check memory usage
free -h

# Increase swap space if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**4. Container Won't Start**
```bash
# Check container logs
docker-compose logs backend

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart backend
```

### Performance Optimization

**1. Resource Limits**
```yaml
# Add to docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

**2. Database Optimization**
```bash
# Add MongoDB indexes
docker exec -it restaceratops-mongodb mongosh
use restaceratops
db.test_executions.createIndex({timestamp: -1})
```

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use AWS Secrets Manager for production
aws secretsmanager create-secret --name restaceratops-secrets --secret-string file://secrets.json
```

### 2. Network Security
```bash
# Use internal networks
docker network create --internal restaceratops-internal

# Restrict external access
docker run --network restaceratops-internal backend
```

### 3. Container Security
```bash
# Run as non-root user
USER app

# Use specific image tags
FROM python:3.12-slim@sha256:abc123
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale backend service
docker-compose up -d --scale backend=3

# Use load balancer
docker run -d --name nginx-lb nginx:alpine
```

### Vertical Scaling
```bash
# Increase instance size
# t3.medium → t3.large → t3.xlarge

# Update resource limits
memory: 2G
cpus: '1.0'
```

## 🎯 Next Steps

1. **Set up monitoring** with AWS CloudWatch
2. **Configure auto-scaling** based on load
3. **Set up CI/CD** pipeline for automated deployments
4. **Implement backup strategy** for data persistence
5. **Add logging aggregation** with ELK stack

---

**🎉 Your Restaceratops agent is now ready for AWS deployment!**

For support, check the logs and refer to the troubleshooting section above.
