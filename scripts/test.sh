#!/usr/bin/env bash

set -euo pipefail

yarn ci:lint
yarn ci:audit
yarn ci:unit-test
