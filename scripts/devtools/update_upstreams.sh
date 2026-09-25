#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

# This script intentionally does not auto-bump pins. It reports upstream HEADs
# versus reviewed pins so upgrades are explicit/reviewable, not silent.
for path in tools/upstreams/graphify tools/upstreams/codegraph; do
  if [[ ! -d "$path/.git" && ! -f "$path/.git" ]]; then
    echo "$path: not initialized (run make upstream-init)"
    continue
  fi
  git -C "$path" fetch origin --prune
  local_sha=$(git -C "$path" rev-parse HEAD)
  branch=$(git -C "$path" remote show origin | sed -n '/HEAD branch/s/.*: //p')
  remote_sha=$(git -C "$path" rev-parse "origin/${branch}")
  echo "$path"
  echo "  pinned/current: $local_sha"
  echo "  upstream HEAD : $remote_sha"
  if [[ "$local_sha" == "$remote_sha" ]]; then echo "  status        : up to date"; else echo "  status        : update available (review before bumping)"; fi
done
