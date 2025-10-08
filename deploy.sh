#!/bin/bash

# LINE Bot ADK Cloud Run Deployment Script
# Usage: ./deploy.sh [--clean-all]  # --clean-all deletes ALL old revisions
set -e

# Parse command line arguments
CLEAN_ALL=false
if [[ "$1" == "--clean-all" ]]; then
    CLEAN_ALL=true
    echo "🗑️  Will clean ALL old revisions after deployment"
fi

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

# Check optional but recommended environment variables
echo -e "${YELLOW}📋 Checking optional environment variables...${NC}"
OPTIONAL_VARS=("STATIC_BASE_URL")
for var in "${OPTIONAL_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${YELLOW}⚠️  $var is not set (will use default)${NC}"
    else
        echo -e "${GREEN}✅ $var is set${NC}"
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
    --set-env-vars="GOOGLE_API_KEY=${GOOGLE_API_KEY}" \
    --set-env-vars="STATIC_BASE_URL=${STATIC_BASE_URL}"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

# Clean up old revisions
echo -e "${YELLOW}🧹 Cleaning up old revisions...${NC}"

# Determine which revisions to delete
if [ "$CLEAN_ALL" = true ]; then
    # All revisions except the latest one
    REVISIONS_TO_DELETE=$(gcloud run revisions list --service=$SERVICE_NAME --region=$REGION --format="value(metadata.name)" --sort-by="~metadata.creationTimestamp" | tail -n +2)
    echo -e "${YELLOW}🗑️  Attempting to delete ALL old revisions (keeping only the latest).${NC}"
else
    # All revisions except the latest 3
    REVISIONS_TO_DELETE=$(gcloud run revisions list --service=$SERVICE_NAME --region=$REGION --format="value(metadata.name)" --sort-by="~metadata.creationTimestamp" | tail -n +4)
    echo -e "${YELLOW}🗑️  Attempting to delete old revisions (keeping the latest 3).${NC}"
fi

if [ -z "$REVISIONS_TO_DELETE" ]; then
    echo -e "${GREEN}✨ No old revisions to clean up.${NC}"
else
    echo -e "${YELLOW}   The following old revisions will be processed for deletion:${NC}"
    echo "${REVISIONS_TO_DELETE}"
    echo "${REVISIONS_TO_DELETE}" | while read revision; do
        if [ ! -z "$revision" ]; then
            echo -e "${YELLOW}   - Processing revision: $revision...${NC}"
            # Attempt to delete, and capture any error output
            DELETE_OUTPUT=$(gcloud run revisions delete "$revision" --region=$REGION --quiet 2>&1)
            
            # Check the exit code of the delete command
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}     ✓ Successfully deleted.${NC}"
            else
                # If deletion fails, print the error message from gcloud
                echo -e "${RED}     ✗ Failed to delete revision '$revision'. Reason:${NC}"
                echo -e "${RED}       $DELETE_OUTPUT${NC}"
            fi
        fi
    done
fi

echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Service URL: ${SERVICE_URL}${NC}"
echo -e "${GREEN}🔗 Webhook URL: ${SERVICE_URL}/webhook${NC}"
echo -e "${YELLOW}📋 Don't forget to update your LINE Bot webhook URL!${NC}"