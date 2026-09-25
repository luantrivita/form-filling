#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== CodeGraph =="
if command -v codegraph >/dev/null 2>&1; then
  codegraph status || true
else
  echo "not installed"
fi

echo
echo "== Graphify =="
if command -v graphify >/dev/null 2>&1; then
  graphify hook status || true
  [[ -d graphify-out ]] && echo "graphify-out: present" || echo "graphify-out: not built"
  [[ -f graphify-out/needs_update ]] && echo "semantic docs update: needed" || true
else
  echo "not installed"
fi
