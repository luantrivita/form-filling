#!/usr/bin/env bash
set -euo pipefail
for p in logs/qwen3_30b.pid logs/medgemma27b.pid logs/baichuan_m2.pid; do
  if [[ -f "$p" ]]; then kill "$(cat "$p")" 2>/dev/null || true; fi
done
