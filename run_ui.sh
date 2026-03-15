#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-5011}"
[ -f .venv/bin/activate ] || ./setup.sh
source .venv/bin/activate
python app_ui.py
