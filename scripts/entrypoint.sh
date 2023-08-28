#!/usr/bin/env bash

set -euo pipefail

python3 -m manage migrate --noinput
python3 -m manage loaddata connect/fixtures/groups.json
exec "${@}"
