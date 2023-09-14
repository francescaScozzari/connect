#!/usr/bin/env bash

# Load documents to qdrant
# Run ./scripts/load_documents.sh
# If you want limit number of documents (for ex. 100):
# Run ./scripts/load_documents.sh 100

set -euo pipefail

limit="${1-""}"
date_timestamp=$(date +%Y%m%d%H%M)
echo "STARTED AT: $(date '+%Y-%m-%d %H:%M:%S')" > ./data/load_documents_$date_timestamp.logs
docker compose run --rm \
    --entrypoint="" \
    --env PYB_CONFIG_FILE="/app/scopus/tests/config/pybliometrics.cfg" \
    --name connect_load_documents_$date_timestamp \
    --volume=$(pwd)/data/:/app/data/ \
    backend \
    /bin/bash -sc \
    "python3 -m manage load_documents -v 3 `if [ $limit != "" ]; then echo "--limit $limit"; fi` >> /app/data/load_documents_$date_timestamp.logs"
echo "FINISHED AT: $(date '+%Y-%m-%d %H:%M:%S')" >> ./data/load_documents_$date_timestamp.logs
