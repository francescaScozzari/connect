#!/usr/bin/env bash

set -euo pipefail

# This fix a Cypress issue: https://github.com/cypress-io/cypress-docker-images/issues/747
export DISPLAY=:1
Xvfb :1 -screen 0 1024x768x16 2>/dev/null &

yarn ci:e2e

unset DISPLAY
kill %1
