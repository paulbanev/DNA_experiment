#!/bin/bash
# Quick Docker deployment script for DNA Simulation

set -e  # Exit on error

echo "🐳 DNA Transport Simulation - Docker Deployment"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Install from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "Install from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker $(docker --version)"
echo "✅ $(docker-compose --version)"
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    echo "Please run this script from the DNA_experiment directory"
    exit 1
fi

# Stop existing containers
echo "📦 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build images
echo ""
echo "🔨 Building Docker images..."
docker-compose build

# Start services
echo ""
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to start..."
sleep 5

# Check status
echo ""
echo "📊 Service Status:"
docker-compose ps

# Test backend
echo ""
echo "🔍 Testing backend..."
if curl -sf http://localhost:5000/api/health > /dev/null; then
    echo "✅ Backend is healthy"
    curl -s http://localhost:5000/api/health | python3 -m json.tool 2>/dev/null || echo ""
else
    echo "⚠️  Backend health check failed"
fi

# Test frontend
echo ""
echo "🔍 Testing frontend..."
if curl -sf http://localhost/ > /dev/null; then
    echo "✅ Frontend is accessible"
else
    echo "⚠️  Frontend check failed"
fi

echo ""
echo "================================================"
echo "🎉 Deployment Complete!"
echo "================================================"
echo ""
echo "Access your app:"
echo "  🌐 Web Interface: http://localhost/"
echo "  🔌 API Health:    http://localhost/api/health"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f              # View logs"
echo "  docker-compose ps                   # Check status"
echo "  docker-compose down                 # Stop all"
echo "  docker-compose restart              # Restart all"
echo ""
echo "Documentation:"
echo "  📖 Full guide: DOCKER_GUIDE.md"
echo ""
