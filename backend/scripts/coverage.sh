#!/usr/bin/env bash

set -euo pipefail

PYB_CONFIG_FILE="./scopus/tests/config/pybliometrics.cfg" \
python3 -m coverage run manage.py test --configuration=Testing --noinput --parallel --shuffle --buffer
