#!/bin/bash

# Docker Hub Setup Verification Script
# Run this script to verify your Docker Hub setup

echo "🐳 Docker Hub Setup Verification"
echo "================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    exit 1
fi

echo "✅ Docker is installed"

# Check Docker version
echo "📋 Docker version:"
docker --version

# Test Docker Hub login (will prompt for credentials)
echo ""
echo "🔑 Testing Docker Hub login..."
echo "Enter your Docker Hub username:"
read DOCKER_USERNAME

echo "Enter your Docker Hub token (will be hidden):"
read -s DOCKER_TOKEN

# Test login
echo "$DOCKER_TOKEN" | docker login --username "$DOCKER_USERNAME" --password-stdin

if [ $? -eq 0 ]; then
    echo "✅ Docker Hub login successful!"
    
    # Test repository access
    echo ""
    echo "🔍 Testing repository access..."
    
    # Try to pull a small test image and tag it
    docker pull hello-world:latest
    docker tag hello-world:latest $DOCKER_USERNAME/student-performance-ml:test
    
    echo "📤 Testing push to repository..."
    docker push $DOCKER_USERNAME/student-performance-ml:test
    
    if [ $? -eq 0 ]; then
        echo "✅ Repository push successful!"
        echo "🧹 Cleaning up test image..."
        docker rmi $DOCKER_USERNAME/student-performance-ml:test
        
        # Clean up from Docker Hub (optional manual step)
        echo ""
        echo "📝 Note: You may want to manually delete the 'test' tag from Docker Hub repository"
        echo "   Repository URL: https://hub.docker.com/r/$DOCKER_USERNAME/student-performance-ml"
    else
        echo "❌ Repository push failed!"
        echo "   Check repository exists and permissions are correct"
    fi
    
    docker logout
else
    echo "❌ Docker Hub login failed!"
    echo "   Check your username and token"
fi

echo ""
echo "🎯 GitHub Secrets Setup"
echo "======================="
echo "Add these secrets to your GitHub repository:"
echo ""
echo "DOCKERHUB_USERNAME: $DOCKER_USERNAME"
echo "DOCKERHUB_TOKEN: [The token you just used]"
echo ""
echo "Repository Settings → Secrets and variables → Actions → New repository secret"