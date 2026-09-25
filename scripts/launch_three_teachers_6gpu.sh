#!/usr/bin/env bash
set -euo pipefail
# Designed for a 6-GPU slice. For A100-40GB, keep benchmark max-model-len modest;
# SYNUR does not need 128K/256K context. For 80GB GPUs this remains conservative.
: "${HF_TOKEN:=}"
mkdir -p logs

CUDA_VISIBLE_DEVICES=0,1 nohup vllm serve Qwen/Qwen3-30B-A3B-Instruct-2507 \
  --host 0.0.0.0 --port 8001 --tensor-parallel-size 2 --dtype bfloat16 \
  --max-model-len 16384 --gpu-memory-utilization 0.88 > logs/qwen3_30b.log 2>&1 &

echo $! > logs/qwen3_30b.pid

CUDA_VISIBLE_DEVICES=2,3 nohup vllm serve google/medgemma-27b-text-it \
  --host 0.0.0.0 --port 8002 --tensor-parallel-size 2 --dtype bfloat16 \
  --max-model-len 16384 --gpu-memory-utilization 0.88 > logs/medgemma27b.log 2>&1 &

echo $! > logs/medgemma27b.pid

CUDA_VISIBLE_DEVICES=4,5 nohup vllm serve baichuan-inc/Baichuan-M2-32B \
  --host 0.0.0.0 --port 8003 --tensor-parallel-size 2 --dtype bfloat16 \
  --max-model-len 16384 --gpu-memory-utilization 0.88 > logs/baichuan_m2.log 2>&1 &

echo $! > logs/baichuan_m2.pid

echo "Started 3 servers on ports 8001/8002/8003. Check logs/*.log before benchmarking."
