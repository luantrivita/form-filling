#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -b main
fi

# Initialize pinned third-party submodules. This converts the portable source ZIP
# into a normal git repo with real gitlink entries.
bash scripts/devtools/init_upstreams.sh

echo
echo "Repository initialized. Recommended next steps:"
echo "  make setup"
echo "  make check"
echo "  make ai-setup"
echo "  # then in Claude/Codex: /graphify ."
