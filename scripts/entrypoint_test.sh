#!/usr/bin/env bash

set -euo pipefail

python3 -m manage setup_llmembedder
exec "${@}"
