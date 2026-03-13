#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -f .venv/bin/activate ] || ./setup.sh
. .venv/bin/activate
PORT="${PORT:-5011}"
HOST="${HOST:-127.0.0.1}"
python app.py serve --host "$HOST" --port "$PORT"
