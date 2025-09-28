#!/bin/bash

# LINE Bot ADK Cloud Run Deployment Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load environment variables from .env file
if [ -f .env ]; then
    echo -e "${YELLOW}📋 Loading environment variables from .env file...${NC}"
    export $(grep -v '^#' .env | xargs)
else
    echo -e "${YELLOW}⚠️  No .env file found, using system environment variables${NC}"
fi

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT}
REGION="asia-east1"
SERVICE_NAME=${SERVICE_NAME:-"linebot-adk"}  # 可透過環境變數覆蓋
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo -e "${YELLOW}📋 Service Name: ${SERVICE_NAME}${NC}"

echo -e "${GREEN}🚀 Starting LINE Bot ADK deployment to Cloud Run${NC}"

# Check if project ID is set
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ GOOGLE_CLOUD_PROJECT environment variable is not set${NC}"
    echo "Please set it in .env file or export GOOGLE_CLOUD_PROJECT=your-project-id"
    exit 1
fi

# Check if required environment variables are set
echo -e "${YELLOW}📋 Checking required environment variables...${NC}"
REQUIRED_VARS=("ChannelSecret" "ChannelAccessToken" "GOOGLE_API_KEY")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}❌ $var is not set${NC}"
        echo "Please set all required environment variables"
        exit 1
    fi
done

# Build and deploy
echo -e "${YELLOW}🏗️  Building and deploying to Cloud Run...${NC}"

gcloud run deploy $SERVICE_NAME \
    --source . \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --port=8080 \
    --memory=1Gi \
    --cpu=1 \
    --max-instances=10 \
    --set-env-vars="ChannelSecret=${ChannelSecret}" \
    --set-env-vars="ChannelAccessToken=${ChannelAccessToken}" \
    --set-env-vars="GOOGLE_API_KEY=${GOOGLE_API_KEY}"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Service URL: ${SERVICE_URL}${NC}"
echo -e "${GREEN}🔗 Webhook URL: ${SERVICE_URL}/webhook${NC}"
echo -e "${YELLOW}📋 Don't forget to update your LINE Bot webhook URL!${NC}"