#!/usr/bin/env bash
set -euo pipefail
# Endpoints must already be serving the matching HF model through an OpenAI-compatible API.
QWEN_ENDPOINT=${QWEN_ENDPOINT:-http://localhost:8001}
MEDGEMMA_ENDPOINT=${MEDGEMMA_ENDPOINT:-http://localhost:8002}
BAICHUAN_ENDPOINT=${BAICHUAN_ENDPOINT:-http://localhost:8003}
LIMIT=${LIMIT:-0}
EXTRA=()
if [[ "$LIMIT" != "0" ]]; then EXTRA+=(--limit "$LIMIT"); fi

run_one () {
  local cfg=$1 endpoint=$2
  python scripts/benchmark_synur_llm.py --model-config "$cfg" --endpoint "$endpoint" --split dev --mode full_schema --resume "${EXTRA[@]}"
  python scripts/benchmark_synur_llm.py --model-config "$cfg" --endpoint "$endpoint" --split dev --mode retrieval_top50 --resume "${EXTRA[@]}"
}

run_one configs/models/qwen3_30b_a3b_instruct_2507.json "$QWEN_ENDPOINT"
run_one configs/models/medgemma_27b_text_it.json "$MEDGEMMA_ENDPOINT"
run_one configs/models/baichuan_m2_32b.json "$BAICHUAN_ENDPOINT"
python scripts/summarize_teacher_benchmarks.py --dir experiments/llm_baselines
