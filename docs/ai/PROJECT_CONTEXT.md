# ESF Pre-Visit — Compact Project Context

## Goal
Convert a completed pre-visit clinical conversation (optionally plus canonicalized HIS facts) into evidence-grounded canonical clinical facts, then deterministically project supported facts into a target MOH/hospital form schema without retraining per form.

## Current architecture
`conversation -> candidate concepts -> evidence -> canonical facts -> reconciliation -> deterministic projection -> validation`

## Current official targets
- `29/BV-02` — Phiếu khám bệnh vào viện chung.
- `15/BV-01` — Bệnh án ngoại trú chung.

The TT32 specifications expose four coarse patient-history narrative fields relevant to V1: reason for visit/admission, present illness, personal history, family history. Medication/allergy remain canonical facts unless a target form has an explicit supported mapping.

## Public benchmarks
- **SYNUR**: primary external schema-constrained extraction benchmark; 193 observation concepts. DEV selects configuration; TEST is locked.
- **MTS-Dialog**: auxiliary dialogue/history section benchmark only, not ESF atomic-fact gold.

## Teacher candidates for Step 4
1. `Qwen/Qwen3-30B-A3B-Instruct-2507`
2. `google/medgemma-27b-text-it`
3. `baichuan-inc/Baichuan-M2-32B`

Each teacher is evaluated on:
- B1 `full_schema`
- B2 `retrieval_top50`

## Primary metrics
Micro/macro concept F1, typed-value accuracy, exact observation match, unsupported-fill rate, schema-valid rate. Secondary: exact concept set, latency p50/p95, output tokens.

## Frozen invariants
- `NOT_MENTIONED != NEGATIVE`.
- Every `SUPPORTED` fact requires provenance/evidence.
- No new diagnosis/treatment/exam inference.
- Preserve historical/resolved/uncertain/correction/conflict state.
- Known form mappings use deterministic projection.

## Out of scope until benchmark finishes
Fine-tuning, LoRA, distillation, student models, teacher-generated silver training corpus, RL/GRPO.

## Key files
- `configs/benchmarks/synur_teacher_benchmark.json`
- `configs/models/*.json`
- `prompts/B1_FULL_SCHEMA_EXTRACTION.md`
- `prompts/B2_RETRIEVAL_EXTRACTION.md`
- `scripts/benchmark_synur_llm.py`
- `src/esf/evaluation/synur_llm_metrics.py`
- `registry/`
- `schemas/`
