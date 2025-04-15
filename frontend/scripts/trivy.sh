#!/usr/bin/env sh

set -e

time trivy image --clear-cache
time trivy image --download-db-only --no-progress
time trivy image \
    --exit-code 0 \
    --format template \
    --output "/trivy/report.html" \
    --scanners vuln \
    --template "@contrib/html.tpl" \
    "${TARGET_IMAGE}"
time trivy image \
    --exit-code 0 \
    --scanners vuln \
    "${TARGET_IMAGE}"
trivy image \
    --exit-code 1 \
    --ignore-unfixed \
    --scanners vuln \
    --severity CRITICAL,HIGH \
    "${TARGET_IMAGE}"
