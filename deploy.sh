#!/bin/bash

# LINE Bot ADK Cloud Run Deployment Script
# Usage: ./deploy.sh [--no-cleanup]  # --no-cleanup skips cleanup after deployment
set -e

# Bypass pyenv-win shims on Windows to avoid "--sort-by was unexpected at this time" errors
if command -v pyenv >/dev/null 2>&1; then
    REAL_PYTHON=$(pyenv which python 2>/dev/null | tr '\\' '/')
    if [ -n "$REAL_PYTHON" ]; then
        export CLOUDSDK_PYTHON="$REAL_PYTHON"
    fi
fi


# Parse command line arguments
SKIP_CLEANUP=false
if [[ "$1" == "--no-cleanup" ]]; then
    SKIP_CLEANUP=true
    echo "⚠️  Cleanup will be SKIPPED after deployment"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load environment variables from .env file
if [ -f .env ]; then
    echo -e "${YELLOW}📋 Loading environment variables from .env file...${NC}"
    set -o allexport
    source .env
    set +o allexport
else
    echo -e "${YELLOW}⚠️  No .env file found, using system environment variables${NC}"
fi

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT}
REGION="asia-east1"
SERVICE_NAME=${SERVICE_NAME:-"linebot-adk"}  # 可透過環境變數覆蓋

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
OPTIONAL_VARS=("STATIC_BASE_URL" "ADMIN_USER_IDS" "TIMEZONE" "GOOGLE_API_KEY_FALLBACK")
for var in "${OPTIONAL_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${YELLOW}⚠️  $var is not set (will use default)${NC}"
    else
        echo -e "${GREEN}✅ $var is set${NC}"
    fi
done

# Check MongoDB configuration (either full URI or split components)
if [ -n "$MONGODB_URI" ]; then
    echo -e "${GREEN}✅ MONGODB_URI is set${NC}"
    echo -e "${GREEN}   Value: ${MONGODB_URI:0:60}...${NC}"
elif [ -n "$MONGODB_USERNAME" ] && [ -n "$MONGODB_PASSWORD" ] && [ -n "$MONGODB_CLUSTER" ]; then
    echo -e "${GREEN}✅ MongoDB credentials set (split components)${NC}"
    echo -e "${GREEN}   Username: $MONGODB_USERNAME${NC}"
    echo -e "${GREEN}   Cluster: $MONGODB_CLUSTER${NC}"
else
    echo -e "${YELLOW}⚠️  MongoDB not configured (AI toggle feature will be disabled)${NC}"
fi

# Build and deploy
echo -e "${YELLOW}🏗️  Building and deploying to Cloud Run...${NC}"
echo -e "${YELLOW}📋 Passing environment variables via --set-env-vars${NC}"

gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --region="$REGION" \
    --platform=managed \
    --allow-unauthenticated \
    --port=8080 \
    --memory=1Gi \
    --cpu=1 \
    --max-instances=10 \
    --set-env-vars="ChannelSecret=${ChannelSecret}" \
    --set-env-vars="ChannelAccessToken=${ChannelAccessToken}" \
    --set-env-vars="GOOGLE_API_KEY=${GOOGLE_API_KEY}" \
    --set-env-vars="GOOGLE_API_KEY_FALLBACK=${GOOGLE_API_KEY_FALLBACK}" \
    --set-env-vars="STATIC_BASE_URL=${STATIC_BASE_URL}" \
    --set-env-vars="ADMIN_USER_IDS=${ADMIN_USER_IDS}" \
    --set-env-vars="TIMEZONE=${TIMEZONE}" \
    --set-env-vars="MONGODB_USERNAME=${MONGODB_USERNAME}" \
    --set-env-vars="MONGODB_PASSWORD=${MONGODB_PASSWORD}" \
    --set-env-vars="MONGODB_CLUSTER=${MONGODB_CLUSTER}" \
    --set-env-vars="MONGODB_DATABASE=${MONGODB_DATABASE}" \
    --set-env-vars="MONGODB_APP_NAME=${MONGODB_APP_NAME}"

# Get the service URL
# Note: gcloud's value()/table() output formats print nothing under Git Bash (MSYS),
# so parse the JSON output instead
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --format=json | sed -n 's/.*"url": *"\(https:[^"]*\)".*/\1/p' | head -1)

# Keepalive: Cloud Scheduler pings /health every 5 minutes to keep the instance warm
# (background tasks inside the container can't do this - CPU is throttled when idle)
if [ -z "$SERVICE_URL" ]; then
    echo -e "${RED}⚠️  Could not determine service URL; skipping keepalive setup${NC}"
else
    echo -e "${YELLOW}⏰ Setting up keepalive scheduler job...${NC}"
    gcloud services enable cloudscheduler.googleapis.com
    KEEPALIVE_JOB="${SERVICE_NAME}-keepalive"
    if gcloud scheduler jobs describe "$KEEPALIVE_JOB" --location="$REGION" >/dev/null 2>&1; then
        SCHEDULER_ACTION="update"
    else
        SCHEDULER_ACTION="create"
    fi
    gcloud scheduler jobs "$SCHEDULER_ACTION" http "$KEEPALIVE_JOB" \
        --location="$REGION" \
        --schedule="*/5 * * * *" \
        --uri="${SERVICE_URL}/health" \
        --http-method=GET
    echo -e "${GREEN}✅ Keepalive job '${KEEPALIVE_JOB}' pings ${SERVICE_URL}/health every 5 minutes${NC}"
fi

# Clean up old resources (default behavior)
if [ "$SKIP_CLEANUP" = false ]; then
    echo ""
    echo -e "${YELLOW}🧹 Running cleanup script...${NC}"
    bash scripts/cleanup_old_resources.sh "$SERVICE_NAME" "$REGION"
else
    echo ""
    echo -e "${YELLOW}⚠️  Cleanup skipped (use ./deploy.sh to enable cleanup)${NC}"
fi

echo ""
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Service URL: ${SERVICE_URL}${NC}"
echo -e "${GREEN}🔗 Webhook URL: ${SERVICE_URL}/webhook${NC}"
echo -e "${YELLOW}📋 Don't forget to update your LINE Bot webhook URL!${NC}"