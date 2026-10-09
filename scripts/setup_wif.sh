#!/bin/bash
# 一次性設定：建立 GitHub Actions 部署 Cloud Run 用的 Workload Identity Federation
# Usage: bash scripts/setup_wif.sh
set -e

PROJECT_ID="vibpath"
GITHUB_REPO="CSL426/VibPath-LineBot"
POOL="github-pool"
PROVIDER="github-provider"
SA_NAME="github-deployer"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Git Bash 下 gcloud 的 value() 輸出為空，改解析 JSON
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format=json | sed -n 's/.*"projectNumber": *"\([0-9]*\)".*/\1/p' | head -1)

gcloud services enable iamcredentials.googleapis.com cloudbuild.googleapis.com \
    run.googleapis.com artifactregistry.googleapis.com --project="$PROJECT_ID"

gcloud iam service-accounts create "$SA_NAME" \
    --project="$PROJECT_ID" --display-name="GitHub Actions deployer"

for ROLE in roles/run.admin roles/cloudbuild.builds.editor \
            roles/iam.serviceAccountUser roles/storage.admin \
            roles/artifactregistry.writer roles/serviceusage.serviceUsageConsumer; do
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:${SA_EMAIL}" --role="$ROLE" --condition=None
done

gcloud iam workload-identity-pools create "$POOL" \
    --project="$PROJECT_ID" --location=global --display-name="GitHub pool"

# attribute-condition 限定只有此 repo 能換取憑證
gcloud iam workload-identity-pools providers create-oidc "$PROVIDER" \
    --project="$PROJECT_ID" --location=global --workload-identity-pool="$POOL" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
    --attribute-condition="assertion.repository=='${GITHUB_REPO}'"

gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
    --project="$PROJECT_ID" --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/attribute.repository/${GITHUB_REPO}"

echo ""
echo "✅ 完成。請在 GitHub repo 的 Settings > Secrets and variables > Actions 新增："
echo "GCP_SERVICE_ACCOUNT = ${SA_EMAIL}"
echo "GCP_WIF_PROVIDER    = projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/providers/${PROVIDER}"
