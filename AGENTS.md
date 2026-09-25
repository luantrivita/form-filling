# ESF Pre-Visit — Codex/agent instructions

## Current phase
Benchmark only. Fine-tuning/distillation implementation is intentionally deferred until the teacher/B1/B2 benchmark is complete and a decision ADR exists.

## Minimize context/token use
- Query **CodeGraph first** for code structure, call paths, and impact analysis; avoid broad grep/read unless graph coverage is insufficient or stale.
- Query **Graphify** for cross-code/docs/schema rationale; consult `graphify-out/GRAPH_REPORT.md` before reading multiple design documents.
- Use `docs/ai/PROJECT_CONTEXT.md` as the first project overview.
- Treat `tools/upstreams/` as third-party source and never use it as ESF implementation context.

## Frozen benchmark rules
- Tune/select on SYNUR DEV only.
- TEST remains locked until `docs/adr/` records the frozen model/prompt/retrieval/generation/scoring configuration.
- Same B1/B2 prompt contract and decoding policy across all teacher candidates.
- Never overwrite or silently edit raw benchmark outputs.

## Clinical data rules
`NOT_MENTIONED != NEGATIVE`; supported facts need evidence; no diagnosis/treatment/exam invention; preserve temporality/correction/conflict provenance.

## Before finishing a code task
Run `make check`; for harness changes also run `make smoke-local`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
