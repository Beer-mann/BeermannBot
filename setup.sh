#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

recreate_venv() {
  rm -rf .venv
  python3 -m venv .venv
}

if [ ! -f .venv/bin/activate ]; then
  recreate_venv
fi

. .venv/bin/activate

if ! python -m pip --version >/dev/null 2>&1; then
  deactivate 2>/dev/null || true
  recreate_venv
  . .venv/bin/activate
fi

python -m ensurepip --upgrade >/dev/null
python -m pip install -U pip >/dev/null

if [ -f "requirements.txt" ]; then
  python -m pip install -r "requirements.txt"
else
  python -m pip install flask flask-cors requests python-dotenv
fi
