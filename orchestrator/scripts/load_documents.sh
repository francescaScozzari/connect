#!/usr/bin/env bash

# Load documents to qdrant
# > ./scripts/load_documents.sh
# If you want limit number of documents to process (for ex. from 0 to 100):
# > ./scripts/load_documents.sh 0 100

set -euo pipefail

source .env

BACKEND_IMAGE=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep backend | sed -n 1p)
export BACKEND_IMAGE

from="${1-""}"
to="${2-""}"
date_timestamp=$(date +%Y%m%d%H%M)
echo "STARTED AT: $(date '+%Y-%m-%d %H:%M:%S')" > ./data/load_documents_"$date_timestamp".logs
docker run \
    --entrypoint="" \
    --env-file .env \
    --env QDRANT_API_KEY=$QDRANT_API_KEY \
    --env QDRANT_DOCUMENTS_COLLECTION=$QDRANT_DOCUMENTS_COLLECTION \
    --env QDRANT_TIMEOUT=$QDRANT_TIMEOUT \
    --env QDRANT_URL=$QDRANT_URL \
    --env PYB_CONFIG_FILE="/app/scopus/tests/config/pybliometrics.cfg" \
    --env SENTRY_DSN=$BACKEND_SENTRY_DSN \
    --name connect_load_documents_"$date_timestamp" \
    "$BACKEND_IMAGE" \
    /bin/bash -sc \
    "echo \"STARTED AT: $(date '+%Y-%m-%d %H:%M:%S')\" > /tmp/load_documents_$date_timestamp.logs & \
    python3 -m manage load_documents -v 3 \
    $(if [ "$from" != "" ]; then echo "--from $from"; fi) \
    $(if [ "$to" != "" ]; then echo "--to $to"; fi) \
    >> /tmp/load_documents_$date_timestamp.logs"
docker cp connect_load_documents_"$date_timestamp":/tmp/load_documents_"$date_timestamp".logs ./data/
docker rm connect_load_documents_"$date_timestamp"
echo "FINISHED AT: $(date '+%Y-%m-%d %H:%M:%S')" >> ./data/load_documents_"$date_timestamp".logs
