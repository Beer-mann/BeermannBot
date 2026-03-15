#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -f .venv/bin/activate ] || ./setup.sh
source .venv/bin/activate
export PORT="${PORT:-5011}"
python app_ui.py
