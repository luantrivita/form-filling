# GPU Runbook — Three Teacher Benchmark

## Goal
Benchmark the same extraction task under identical prompt/metric rules for:
- `Qwen/Qwen3-30B-A3B-Instruct-2507`
- `google/medgemma-27b-text-it`
- `baichuan-inc/Baichuan-M2-32B`

## Before running

1. Install a recent vLLM release that supports Qwen3 MoE and Gemma 3.
2. Log in to Hugging Face on the cluster.
3. Accept the Health AI Developer Foundations terms for MedGemma in the Hugging Face account that owns the token.
4. Export `HF_TOKEN` on the cluster; do not commit it to the repo.

## GPU allocation

The supplied launcher uses 2 GPUs/model and caps benchmark context at 16K because SYNUR does not need the models' maximum 128K/256K context. This reduces KV-cache pressure. Approximate BF16 weight storage before runtime overhead is ~61 GB for Qwen3-30B, ~54 GB for MedGemma-27B and ~66 GB for Baichuan-M2-32B, so 2×A100 per model is a conservative cross-A100-40/80GB setup.

If memory is insufficient, lower `--gpu-memory-utilization`, reduce `--max-model-len` to 8192, or use more tensor-parallel GPUs. Do not quantize only one teacher in the primary comparison; that would confound the benchmark. Quantized deployment can be evaluated after teacher selection.

## Smoke test

Start servers:
```bash
bash scripts/launch_three_teachers_6gpu.sh
```

Check:
```bash
tail -f logs/qwen3_30b.log
```

Run 10 DEV examples per configuration:
```bash
LIMIT=10 bash scripts/run_teacher_dev_matrix.sh
```

Only if all six runs produce valid JSONL/summary files, run full DEV:
```bash
LIMIT=0 bash scripts/run_teacher_dev_matrix.sh
```

## Do not run TEST yet

Use DEV to choose:
- full-schema vs retrieval-top50;
- any purely formatting-related prompt correction;
- output token cap if necessary.

After these are frozen, run TEST exactly once for the selected configuration of each teacher. Preserve all raw outputs.

## Outputs to upload back for analysis

Upload the entire folder:
```text
experiments/llm_baselines/
```

It contains raw JSONL traces and `.summary.json` files. No model weights or HF token are needed.
