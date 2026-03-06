#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Minimal UI endpoint for project status/docs
python3 -m http.server 5003
