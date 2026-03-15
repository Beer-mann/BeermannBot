#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -f .venv/bin/activate ] || ./setup.sh
source .venv/bin/activate
PORT="${PORT:-5011}"
export PORT
python server.py
