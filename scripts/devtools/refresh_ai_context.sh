#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if command -v codegraph >/dev/null 2>&1 && [[ -d .codegraph ]]; then
  codegraph sync
else
  echo "CodeGraph not initialized; run make ai-setup"
fi

if [[ -f graphify-out/.graphify_python ]]; then
  PY="$(cat graphify-out/.graphify_python)"
  "$PY" -m graphify.watch --help >/dev/null 2>&1 || true
  if [[ -f graphify-out/needs_update ]]; then
    echo "Graphify reports docs/media needing semantic update. In Claude/Codex run: /graphify --update"
  else
    echo "Graphify has no semantic-update flag. Code changes are handled by watcher/hook when enabled."
  fi
else
  echo "Graphify initial graph not built yet. In Claude/Codex run: /graphify ."
fi
