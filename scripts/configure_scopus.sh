#!/usr/bin/env bash

set -euo pipefail

python3 -m manage configure_scopus
exec "${@}"
