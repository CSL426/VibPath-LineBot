#!/bin/bash

# Cloud Run Resource Cleanup Script
# Cleans up old revisions and Docker images from Artifact Registry
# Usage: ./scripts/cleanup_old_resources.sh [SERVICE_NAME] [REGION]

set -e

# Bypass pyenv-win shims on Windows to avoid "--sort-by was unexpected at this time" errors
if command -v pyenv >/dev/null 2>&1; then
    REAL_PYTHON=$(pyenv which python 2>/dev/null | tr '\\' '/')
    if [ -n "$REAL_PYTHON" ]; then
        export CLOUDSDK_PYTHON="$REAL_PYTHON"
    fi
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
SERVICE_NAME=${1:-"linebot-adk"}
REGION=${2:-"asia-east1"}
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ No active Google Cloud project set${NC}"
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

# Artifact Registry path used by `gcloud run deploy --source .`
AR_REPO="${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/${SERVICE_NAME}"

echo -e "${GREEN}🧹 Starting cleanup for Cloud Run service: ${SERVICE_NAME}${NC}"
echo -e "${YELLOW}   Project: ${PROJECT_ID}${NC}"
echo -e "${YELLOW}   Region: ${REGION}${NC}"
echo -e "${YELLOW}   AR Repo: ${AR_REPO}${NC}"
echo ""

# ========================================
# Clean up old Cloud Run revisions
# ========================================
echo -e "${YELLOW}🗑️  Cleaning up old Cloud Run revisions...${NC}"

REVISIONS_TO_DELETE=$(gcloud run revisions list \
    --service="$SERVICE_NAME" \
    --region="$REGION" \
    --filter="servingState:INACTIVE" \
    --format="value(metadata.name)" 2>/dev/null)

if [ -z "$REVISIONS_TO_DELETE" ]; then
    echo -e "${GREEN}   ✨ No old revisions to clean up.${NC}"
else
    REVISION_COUNT=$(echo "$REVISIONS_TO_DELETE" | wc -l)
    echo -e "${YELLOW}   Found $REVISION_COUNT inactive revision(s)${NC}"

    echo "$REVISIONS_TO_DELETE" | while read revision; do
        if [ ! -z "$revision" ]; then
            echo -e "${YELLOW}   - Deleting revision: $revision...${NC}"

            DELETE_OUTPUT=$(gcloud run revisions delete "$revision" \
                --region="$REGION" \
                --quiet 2>&1)

            if [ $? -eq 0 ]; then
                echo -e "${GREEN}     ✓ Successfully deleted${NC}"
            else
                echo -e "${RED}     ✗ Failed to delete: $DELETE_OUTPUT${NC}"
            fi
        fi
    done
    echo -e "${GREEN}   ✅ Revision cleanup complete${NC}"
fi

echo ""

# ========================================
# Clean up old Docker images
# ========================================
echo -e "${YELLOW}🐳 Cleaning up old Docker images in Artifact Registry...${NC}"
echo -e "${YELLOW}   Registry: ${AR_REPO}${NC}"

# List all image digests (sorted by creation time, newest first)
IMAGE_DIGESTS=$(gcloud artifacts docker images list "$AR_REPO" \
    --format="get(version)" \
    --sort-by=~UPDATE_TIME)

if [ -z "$IMAGE_DIGESTS" ]; then
    echo -e "${GREEN}   ✨ No images found in registry.${NC}"
else
    TOTAL_IMAGES=$(echo "$IMAGE_DIGESTS" | wc -l)
    echo -e "${YELLOW}   Found $TOTAL_IMAGES image(s) in registry${NC}"

    # Keep the latest 2 images, delete the rest
    KEEP_COUNT=2
    IMAGES_TO_DELETE=$(echo "$IMAGE_DIGESTS" | tail -n +$((KEEP_COUNT + 1)))

    if [ -z "$IMAGES_TO_DELETE" ]; then
        echo -e "${GREEN}   ✨ No old images to clean up (keeping latest $KEEP_COUNT)${NC}"
    else
        DELETE_COUNT=$(echo "$IMAGES_TO_DELETE" | wc -l)
        echo -e "${YELLOW}   Deleting $DELETE_COUNT old image(s) (keeping latest $KEEP_COUNT)...${NC}"

        echo "$IMAGES_TO_DELETE" | while read digest; do
            if [ ! -z "$digest" ]; then
                IMAGE_WITH_DIGEST="${AR_REPO}@${digest}"
                echo -e "${YELLOW}   - Deleting: ${digest:0:20}...${NC}"

                DELETE_OUTPUT=$(gcloud artifacts docker images delete "$IMAGE_WITH_DIGEST" \
                    --quiet --delete-tags 2>&1)

                if [ $? -eq 0 ]; then
                    echo -e "${GREEN}     ✓ Successfully deleted${NC}"
                else
                    echo -e "${RED}     ✗ Failed to delete: $DELETE_OUTPUT${NC}"
                fi
            fi
        done
        echo -e "${GREEN}   ✅ Image cleanup complete${NC}"
    fi
fi
# ========================================
# Clean up old source zip files in Cloud Storage
# ========================================
echo -e "${YELLOW}📦 Cleaning up old source zip files in Cloud Storage...${NC}"
GCS_BUCKET="gs://run-sources-${PROJECT_ID}-${REGION}"
GCS_PATH="${GCS_BUCKET}/services/${SERVICE_NAME}"

# List all source zips, sorted (oldest first because of timestamp prefix)
ZIP_LIST=$(gcloud storage ls "${GCS_PATH}/*.zip" 2>/dev/null | sort)

if [ -z "$ZIP_LIST" ]; then
    echo -e "${GREEN}   ✨ No source zip files found in GCS.${NC}"
else
    TOTAL_ZIPS=$(echo "$ZIP_LIST" | wc -l)
    echo -e "${YELLOW}   Found $TOTAL_ZIPS source zip file(s) in GCS${NC}"

    # Keep the latest 2 zip files, delete the rest
    KEEP_ZIPS_COUNT=2
    if [ "$TOTAL_ZIPS" -gt "$KEEP_ZIPS_COUNT" ]; then
        ZIPS_TO_DELETE=$(echo "$ZIP_LIST" | head -n -$KEEP_ZIPS_COUNT)
        DELETE_ZIP_COUNT=$(echo "$ZIPS_TO_DELETE" | wc -l)
        echo -e "${YELLOW}   Deleting $DELETE_ZIP_COUNT old zip file(s) (keeping latest $KEEP_ZIPS_COUNT)...${NC}"

        echo "$ZIPS_TO_DELETE" | while read zip_file; do
            if [ -n "$zip_file" ]; then
                echo -e "${YELLOW}   - Deleting: $(basename "$zip_file")...${NC}"
                gcloud storage rm "$zip_file" >/dev/null 2>&1 || gsutil rm "$zip_file" >/dev/null 2>&1
            fi
        done
        echo -e "${GREEN}   ✅ Cloud Storage cleanup complete${NC}"
    else
        echo -e "${GREEN}   ✨ No old zip files to clean up (keeping latest $KEEP_ZIPS_COUNT)${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ Cleanup completed successfully!${NC}"

