# ESF Pre-Visit Benchmark

Evidence-grounded, schema-driven pre-visit clinical information extraction and MOH-form projection. **Current phase: three-teacher B1/B2 benchmarking only.** Fine-tuning and distillation are deliberately deferred.

## Current benchmark question
Compare, under one frozen harness:

- `Qwen/Qwen3-30B-A3B-Instruct-2507`
- `google/medgemma-27b-text-it`
- `baichuan-inc/Baichuan-M2-32B`

on:

- **B1** — full SYNUR schema
- **B2** — retrieval Top-50 schema

Selection uses SYNUR DEV. SYNUR TEST is locked until an ADR freezes the final configuration.

## Repository map

```text
.
├── AGENTS.md / CLAUDE.md       # token-efficient agent instructions
├── configs/
│   ├── benchmarks/             # frozen benchmark protocol config
│   └── models/                 # 3 teacher serving configs only
├── data/
│   ├── external/               # raw public datasets (gitignored)
│   └── manifests/              # checksums / provenance
├── data_generation/            # schema contract handed to Data Team; not on benchmark critical path
├── docs/
│   ├── adr/                    # architecture/research decisions
│   ├── ai/                     # compact context + graph setup
│   ├── benchmark/              # benchmark protocol
│   ├── regulatory/             # MOH/TT32 field guidance
│   ├── reports/                # historical checkpoints
│   └── roadmap/                # planning only; no SFT/distill implementation
├── experiments/
│   ├── public_baselines/       # completed non-LLM baselines
│   ├── step3_projection_demo/  # deterministic projection demo
│   └── llm_baselines/          # 3 teachers × B1/B2 outputs (gitignored)
├── prompts/                    # B1/B2 contracts
├── registry/                   # canonical concepts/forms/mappings/value sets
├── schemas/                    # JSON contracts
├── scripts/                    # data, benchmark, validation, AI context tooling
├── src/esf/                    # reusable package code
├── tests/
└── tools/upstreams/            # Graphify + CodeGraph submodules after `make upstream-init`
```

## Quick start

If you received the portable source ZIP, initialize git + pinned upstream submodules first:

```bash
make repo-init
```

Then:

```bash
python3 -m venv .venv
source .venv/bin/activate
make setup
make data
make check
```

The delivered artifact already contains the user-supplied SYNUR/MTS-Dialog files for convenience; `.gitignore` prevents accidental commits. A fresh clone can recreate them with `make data`.

## AI coding context setup

The repo is designed for Claude Code + Codex without repeatedly reading the whole tree.

```bash
make ai-setup
make upstream-init     # optional source mirrors, pinned commits
```

Then in Claude/Codex initialize Graphify once with:

```text
/graphify .
```

During long coding sessions you may run:

```bash
make graphify-watch
```

CodeGraph auto-syncs changes through its MCP watcher during agent sessions. Graphify's post-commit hook is installed by `make ai-setup`; its live watcher refreshes code changes, while changed docs may request an explicit `/graphify --update`.

See `docs/ai/AI_CONTEXT_SETUP.md`.

## Run the teacher benchmark

### 1. GPU environment
Install a compatible vLLM environment on the GPU cluster and accept MedGemma's gated model terms on Hugging Face. Export `HF_TOKEN` where required.

### 2. Start three endpoints
The supplied launcher uses GPUs 0–5 (2 GPUs/model):

```bash
bash scripts/launch_three_teachers_6gpu.sh
```

Check `logs/*.log` until all endpoints are ready.

### 3. Smoke run on DEV

```bash
make benchmark-smoke
```

Only fix operational problems here (OOM, endpoint/model mismatch, parser crash). Do not use smoke scores to silently tune the benchmark protocol.

### 4. Full DEV matrix

```bash
make benchmark-dev
make benchmark-summary
```

This creates six runs: 3 teachers × B1/B2.

### 5. Do not run TEST yet
TEST requires a post-DEV ADR that freezes model, prompt, retrieval K, generation parameters, and scorer version. The runner contains a TEST guard.

## Frozen clinical invariants
- `NOT_MENTIONED != NEGATIVE`.
- Every supported fact requires evidence/provenance.
- No new diagnosis/treatment/physical-exam inference from patient conversation.
- Preserve negation, uncertainty, temporality, correction, and source conflict.
- Known form mappings project deterministically.

## Completed checkpoints
- TT32 specifications ingested for `29/BV-02` and `15/BV-01`.
- canonical registry + mappings + schema validators.
- SYNUR/MTS-Dialog adapters and non-LLM baselines.
- candidate/evidence retrieval and deterministic projection.
- three-teacher OpenAI-compatible LLM evaluation harness.

## Deferred
No fine-tuning/distillation code is included in this phase. See `docs/roadmap/AFTER_BENCHMARK.md`.
