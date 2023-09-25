#!/usr/bin/env bash

# Copy files with author ids into ./data
# Import authors from scopus:
# > ./scripts/import_authors.sh ./data/<author_ids_file>.txt

set -euo pipefail

source .env

export BACKEND_IMAGE=`docker images --format "{{.Repository}}:{{.Tag}}" | grep backend | sed -n 1p`

author_paths=$1
date_timestamp=$(date +%Y%m%d%H%M)
echo "STARTED AT: $(date '+%Y-%m-%d %H:%M:%S')" > ./data/import_authors_$date_timestamp.logs
docker run --rm \
    --entrypoint="/tmp/scripts/configure_scopus.sh" \
    --env-file .env \
    --env DJANGO_QDRANT_API_KEY=$QDRANT_API_KEY \
    --env DJANGO_QDRANT_TIMEOUT=$QDRANT_TIMEOUT \
    --env DJANGO_QDRANT_URL=$QDRANT_URL \
    --env PYB_CONFIG_FILE="/app/scopus/tests/config/pybliometrics.cfg" \
    --env SENTRY_DSN=$BACKEND_SENTRY_DSN \
    --name connect_import_authors_$date_timestamp \
    --volume=$(pwd)/data/:/app/data/ \
    --volume=$(pwd)/scripts/:/tmp/scripts/ \
    --volume=$(pwd)/.cache/pybliometrics:/home/appuser/.cache/pybliometrics/\
    $BACKEND_IMAGE \
    /bin/bash -sc \
    "python3 -m manage import_authors --author-paths $author_paths --populate-documents -v 3 >> /app/data/import_authors_$date_timestamp.logs"
echo "FINISHED AT: $(date '+%Y-%m-%d %H:%M:%S')" >> ./data/import_authors_$date_timestamp.logs
