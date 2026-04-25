#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Curso de Chinês - Deploy Script${NC}\n"

# Options
DEPLOY_TO=${1:-render}

deploy_render() {
    echo -e "${BLUE}📦 Deploying to Render.com...${NC}"
    
    if [ -z "$RENDER_API_KEY" ]; then
        echo -e "${RED}Error: RENDER_API_KEY not set${NC}"
        exit 1
    fi
    
    echo "Creating Render Blueprint..."
    curl -X POST "https://api.render.com/v1/blueprints" \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        -H "Content-Type: application/json" \
        -d @render.json
    
    echo -e "${GREEN}✅ Render deployment initiated!${NC}"
}

deploy_fly() {
    echo -e "${BLUE}📦 Deploying to Fly.io...${NC}"
    
    if ! command -v flyctl &> /dev/null; then
        echo "Installing flyctl..."
        curl -L https://fly.io/install.sh | sh
    fi
    
    if [ -z "$FLY_API_TOKEN" ]; then
        echo -e "${RED}Error: FLY_API_TOKEN not set${NC}"
        exit 1
    fi
    
    flyctl auth login
    flyctl launch --copy-config --no-deploy
    
    echo "Deploying..."
    flyctl deploy --remote-only
    
    echo -e "${GREEN}✅ Fly.io deployment complete!${NC}"
    flyctl info
}

deploy_docker() {
    echo -e "${BLUE}📦 Building Docker image...${NC}"
    
    docker build -t curso-chines:latest .
    
    echo "Running container..."
    docker-compose up -d
    
    echo -e "${GREEN}✅ Docker deployment complete!${NC}"
}

deploy_railway() {
    echo -e "${BLUE}📦 Deploying to Railway...${NC}"
    
    if ! command -v railway &> /dev/null; then
        echo "Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    railway login
    railway init
    railway up
    
    echo -e "${GREEN}✅ Railway deployment complete!${NC}"
}

case $DEPLOY_TO in
    render)
        deploy_render
        ;;
    fly)
        deploy_fly
        ;;
    docker)
        deploy_docker
        ;;
    railway)
        deploy_railway
        ;;
    all)
        deploy_render
        deploy_fly
        deploy_railway
        ;;
    *)
        echo -e "${RED}Unknown deployment target: $DEPLOY_TO${NC}"
        echo "Usage: ./deploy.sh [render|fly|docker|railway|all]"
        exit 1
        ;;
esac

echo -e "\n${GREEN}🎉 Deployment finished!${NC}"