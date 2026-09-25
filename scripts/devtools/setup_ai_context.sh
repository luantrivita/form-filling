#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

need () { command -v "$1" >/dev/null 2>&1 || { echo "ERROR: missing $1" >&2; exit 1; }; }
need python3

# Graphify: install a pinned release in an isolated uv tool environment.
if command -v uv >/dev/null 2>&1; then
  uv tool install --force 'graphifyy[watch]==0.9.67'
elif command -v pipx >/dev/null 2>&1; then
  pipx install --force 'graphifyy[watch]==0.9.67'
else
  echo "ERROR: install uv (recommended) or pipx first for pinned Graphify setup." >&2
  exit 1
fi

graphify claude install --project
graphify codex install --project
graphify hook install || true

# CodeGraph: use a pinned npm release. We deliberately do not curl|sh automatically.
if command -v npm >/dev/null 2>&1; then
  npm install -g '@colbymchenry/codegraph@1.6.0'
else
  echo "ERROR: npm/Node is required for the pinned CodeGraph install in this script." >&2
  echo "Alternative: install CodeGraph with its official standalone installer, then run: codegraph upgrade 1.6.0" >&2
  exit 1
fi

codegraph install
if [[ -d .codegraph ]]; then
  codegraph sync
else
  codegraph init
fi

cat <<'MSG'
AI context setup complete.
- CodeGraph is initialized; its MCP watcher auto-syncs during Claude/Codex sessions.
- Graphify project skills are installed for Claude + Codex and its post-commit hook is enabled.
- Build the initial Graphify project graph from your coding assistant with `/graphify .`, then optionally run `make graphify-watch` during editing.
MSG
