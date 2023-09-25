#!/usr/bin/env bash

# Copy scopus app fixture into ./data/scopus.json.xz
# > ./scripts/load_scopus_data.sh

set -euo pipefail

export BACKEND_IMAGE=`docker images --format "{{.Repository}}:{{.Tag}}" | grep backend | sed -n 1p`

date_timestamp=$(date +%Y%m%d%H%M)
echo "STARTED AT: $(date '+%Y-%m-%d %H:%M:%S')" > ./data/load_scopus_data_$date_timestamp.logs
docker compose run --rm \
    --entrypoint="" \
    --env PYB_CONFIG_FILE="/app/scopus/tests/config/pybliometrics.cfg" \
    --name connect_load_scopus_data_$date_timestamp \
    --volume=$(pwd)/data/:/app/data/ \
    backend \
    /bin/bash -sc \
    "python3 -m manage loaddata data/scopus.json.xz >> /app/data/load_scopus_data_$date_timestamp.logs"
echo "FINISHED AT: $(date '+%Y-%m-%d %H:%M:%S')" >> ./data/load_scopus_data_$date_timestamp.logs
