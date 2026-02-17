#!/bin/bash
# Script to check the status of the latest GitHub Actions run for the current branch.

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Checking latest CI run status..."

# Get the latest run for the current branch (assuming main if detached, but better to detect)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" == "HEAD" ]; then
    BRANCH="main"
fi

# Fetch run info
RUN_INFO=$(gh run list --branch "$BRANCH" --limit 1 --json databaseId,status,conclusion,url --jq '.[0]')

if [ -z "$RUN_INFO" ]; then
    echo -e "${YELLOW}No runs found for branch: $BRANCH${NC}"
    exit 0
fi

ID=$(echo "$RUN_INFO" | jq -r '.databaseId')
STATUS=$(echo "$RUN_INFO" | jq -r '.status')
CONCLUSION=$(echo "$RUN_INFO" | jq -r '.conclusion')
URL=$(echo "$RUN_INFO" | jq -r '.url')

echo "Run ID: $ID"
echo "URL:    $URL"

if [ "$STATUS" == "completed" ]; then
    if [ "$CONCLUSION" == "success" ]; then
        echo -e "${GREEN}✅ CI Passed${NC}"
        exit 0
    else
        echo -e "${RED}❌ CI Failed ($CONCLUSION)${NC}"
        echo "Fetching failure logs..."
        gh run view "$ID" --log-failed
        exit 1
    fi
else
    echo -e "${YELLOW}⏳ CI In Progress ($STATUS)${NC}"
    # Optionally watch
    # gh run watch "$ID"
    exit 0
fi
