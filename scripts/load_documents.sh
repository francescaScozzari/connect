#!/usr/bin/env bash

# Load documents to qdrant
# > ./scripts/load_documents.sh
# If you want limit number of documents to process (for ex. from 0 to 100):
# > ./scripts/load_documents.sh 0 100

set -euo pipefail

source .env

export BACKEND_IMAGE=`docker images --format "{{.Repository}}:{{.Tag}}" | grep backend | sed -n 1p`

from="${1-""}"
to="${2-""}"
date_timestamp=$(date +%Y%m%d%H%M)
echo "STARTED AT: $(date '+%Y-%m-%d %H:%M:%S')" > ./data/load_documents_$date_timestamp.logs
docker run --rm \
    --entrypoint="" \
    --env-file .env \
    --env QDRANT_API_KEY=$QDRANT_API_KEY \
    --env QDRANT_DOCUMENTS_COLLECTION=$QDRANT_DOCUMENTS_COLLECTION \
    --env QDRANT_TIMEOUT=$QDRANT_TIMEOUT \
    --env QDRANT_URL=$QDRANT_URL \
    --env PYB_CONFIG_FILE="/app/scopus/tests/config/pybliometrics.cfg" \
    --env SENTRY_DSN=$BACKEND_SENTRY_DSN \
    --name connect_load_documents_$date_timestamp \
    --volume=$(pwd)/data/:/app/data/ \
    $BACKEND_IMAGE \
    /bin/bash -sc \
    "python3 -m manage load_documents -v 3 \
    `if [ $from != "" ]; then echo "--from $from"; fi` \
    `if [ $to != "" ]; then echo "--to $to"; fi` \
    >> /app/data/load_documents_$date_timestamp.logs"
echo "FINISHED AT: $(date '+%Y-%m-%d %H:%M:%S')" >> ./data/load_documents_$date_timestamp.logs
