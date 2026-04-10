#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

SMOKE_PORT="${SMOKE_PORT:-5011}"
SMOKE_LOG="$(mktemp -t beermannbot-smoke-ui.XXXXXX.log)"

cleanup() {
  if [[ -n "${SMOKE_SERVER_PID:-}" ]]; then
    kill "${SMOKE_SERVER_PID}" >/dev/null 2>&1 || true
    wait "${SMOKE_SERVER_PID}" >/dev/null 2>&1 || true
  fi
  rm -f "${SMOKE_LOG}"
}
trap cleanup EXIT

echo "[smoke] CLI happy path"
cli_output="$(./run_cli.sh hello)"
if [[ "${cli_output}" != "Hello, world!" ]]; then
  echo "[smoke] unexpected CLI output: ${cli_output}"
  exit 1
fi

echo "[smoke] Starting HTTP server on :${SMOKE_PORT}"
PORT="${SMOKE_PORT}" ./run_ui.sh >"${SMOKE_LOG}" 2>&1 &
SMOKE_SERVER_PID=$!

echo "[smoke] Waiting for /health"
for _ in $(seq 1 40); do
  if curl -fsS "http://127.0.0.1:${SMOKE_PORT}/health" >/dev/null; then
    break
  fi
  sleep 0.25
done

curl -fsS "http://127.0.0.1:${SMOKE_PORT}/health" >/dev/null

echo "[smoke] HTTP happy path"
run_response="$(curl -fsS -X POST "http://127.0.0.1:${SMOKE_PORT}/run" \
  -H "Content-Type: application/json" \
  --data '{"command":"hello"}')"

python - "${run_response}" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
assert payload["ok"] is True, payload
assert payload["command"] == "hello", payload
assert payload["output"] == "Hello, world!\n", payload
print("[smoke] passed")
PY
