#!/bin/bash
# Project AI runner: Claude/Codex/Copilot/Aider (Ollama local)
# Usage: ./ai-run.sh <file> <message...>
set -euo pipefail
FILE="${1:?Usage: ./ai-run.sh <file> <message...>}"
shift
MSG="$*"
if [ -z "$MSG" ]; then
  echo "Error: message required" >&2
  exit 1
fi
exec /home/shares/beermann/scripts/aider-task.sh "$(pwd)" "$FILE" "$MSG"
