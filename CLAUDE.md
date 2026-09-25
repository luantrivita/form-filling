# ESF Pre-Visit — Claude Code instructions

## Scope now
The repository is in **benchmark-only phase**. Do not implement fine-tuning, LoRA, distillation, RL/GRPO, teacher-generated silver data, or student-model code until the benchmark decision is explicitly recorded in `docs/adr/`.

## Context-efficiency rules
1. For code questions, use **CodeGraph first** to locate symbols, callers/callees, impact radius, and relevant source. Do not begin with broad recursive grep/read.
2. For architecture, schema, regulatory mapping, and design rationale, use **Graphify** / `graphify-out/GRAPH_REPORT.md` before opening many documents.
3. Read raw files only when the graph does not contain the needed detail, a staleness warning is shown, or the task is about non-indexed data/config.
4. Never inspect/index `tools/upstreams/` as ESF source. Those are third-party tools.
5. Prefer the compact project context in `docs/ai/PROJECT_CONTEXT.md` before historical reports.

## Benchmark integrity
- SYNUR DEV is for model/prompt/mode selection.
- SYNUR TEST is locked. Do not run TEST until an ADR freezes model, prompt, retrieval K, generation settings, and scoring version.
- Compare all three teacher candidates under the same protocol.
- B1 = full schema; B2 = retrieval Top-K. Do not silently change prompts or decoding between models.
- Every result must preserve raw output + parse/validation status + per-case score + aggregate summary.

## Safety/data invariants
- `NOT_MENTIONED != NEGATIVE`.
- Supported clinical facts require evidence/provenance.
- No new diagnosis, treatment, or physical-exam inference from patient conversation.
- Form projection is deterministic when mappings are known.

## Required checks after code changes
Run:
```bash
make check
```
For benchmark-harness changes also run:
```bash
make smoke-local
```

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
