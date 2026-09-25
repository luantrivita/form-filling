#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [[ ! -f graphify-out/.graphify_python ]]; then
  echo "ERROR: Graphify graph has not been initialized. In Claude/Codex run: /graphify ." >&2
  exit 1
fi
PY="$(cat graphify-out/.graphify_python)"
exec "$PY" -m graphify.watch "$ROOT" --debounce 3
