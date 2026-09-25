# ADR-0001: Complete teacher/B1/B2 benchmark before adaptation

- Status: Accepted
- Date: 2026-09-25

## Context
Three teacher candidates and two extraction modes must be compared fairly before deciding whether model adaptation is necessary.

## Decision
The current repository phase includes benchmark/evaluation code only. Fine-tuning, LoRA, distillation, student models, RL/GRPO, and teacher-generated silver training pipelines are deferred.

## Evidence
The benchmark harness, schemas, public datasets, retrieval/evidence/projection modules, and DEV evaluation protocol are already available. Adaptation before a fair baseline would confound backbone, retrieval, prompt, and data effects.

## Consequences
Any PR adding adaptation code before a post-benchmark ADR should be rejected or deferred.
