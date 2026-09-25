# Repo Setup Complete — Benchmark Phase

Date: 2026-09-25

## Status
The ESF project has been consolidated into a benchmark-ready research repository. Fine-tuning/distillation implementation is intentionally absent.

## Included
- TT32-derived form registry for 29/BV-02 and 15/BV-01.
- canonical concepts, form mappings, value sets, JSON schema contracts.
- SYNUR and MTS-Dialog dataset adapters + reproducible download script.
- public non-LLM baselines.
- candidate retrieval, evidence retrieval, deterministic projection, form validation.
- three-teacher OpenAI-compatible B1/B2 benchmark harness.
- TEST split guard.
- CI, Makefile, environment template, benchmark protocol and ADR structure.
- Claude/Codex instructions optimized for graph-first context retrieval.
- Graphify + CodeGraph upstream pins and initialization/update scripts.

## AI graph policy
CodeGraph is the primary source-code graph and auto-syncs during MCP-backed agent sessions. Graphify is supplementary for code + schema/docs architecture. Its live watcher handles code changes and its git hook refreshes committed code; changed docs may request an explicit semantic update.

Third-party upstream source under `tools/upstreams/` is excluded from the ESF Graphify corpus.

## Validation
`make check` passes all current contract and unit tests.
