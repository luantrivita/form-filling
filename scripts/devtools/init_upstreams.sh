#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: initialize this directory as a git repository first: git init" >&2
  exit 1
fi

add_or_update () {
  local name="$1" url="$2" path="$3" commit="$4"
  mode=$(git ls-files --stage "$path" 2>/dev/null | awk '{print $1}' || true)
  if [[ "$mode" == "160000" ]]; then
    echo "[$name] submodule gitlink already declared"
  else
    # Source ZIPs retain .gitmodules but not the original git index. Remove any
    # stale section before adding the real gitlink.
    git config -f .gitmodules --remove-section "submodule.${path}" 2>/dev/null || true
    rm -rf "$path"
    git submodule add "$url" "$path"
  fi
  git submodule update --init --recursive "$path"
  git -C "$path" fetch --all --tags --prune
  git -C "$path" checkout "$commit"
  git add .gitmodules "$path"
  echo "[$name] pinned to $(git -C "$path" rev-parse HEAD)"
}

add_or_update graphify https://github.com/Graphify-Labs/graphify.git tools/upstreams/graphify 4c735618f3d56fd622c2049771584621c31ba9ff
add_or_update codegraph https://github.com/colbymchenry/codegraph.git tools/upstreams/codegraph ba3c21e50d9129d2f5f3843ec3728868ae6d47a1

echo "Upstream submodules initialized. Commit .gitmodules + gitlinks if this is the first run."
