# Three-Teacher B1/B2 Benchmark Protocol

## Research question
Under the same structured-extraction contract, which teacher backbone and which schema-conditioning mode provide the best balance of extraction quality, unsupported-fill control, schema validity, and runtime cost?

## Models
- Qwen3-30B-A3B-Instruct-2507
- MedGemma-27B-text-it
- Baichuan-M2-32B

## Required DEV matrix
Exactly six primary runs:

| Model | B1 Full Schema | B2 Retrieval Top-50 |
|---|---:|---:|
| Qwen3-30B-A3B-Instruct-2507 | required | required |
| MedGemma-27B-text-it | required | required |
| Baichuan-M2-32B | required | required |

All runs use the same DEV examples, prompt contract, temperature, maximum output budget, schema version, scorer version, and retrieval implementation.

## Selection split and locked split
- `dev`: development and selection.
- `test`: final locked evaluation only after configuration freeze.

Do not inspect TEST results to choose model, prompt, K, parser heuristics, or decoding settings.

## Primary metrics
1. micro concept F1
2. macro concept F1
3. typed value accuracy on matched concepts
4. exact observation match rate
5. unsupported-fill rate
6. schema-valid rate

## Secondary metrics
- exact concept-set rate
- latency p50/p95
- mean output tokens
- parse failure rate

## Runtime policy
Serve each teacher through an OpenAI-compatible endpoint. The supplied 6-GPU launcher uses two GPUs per teacher and caps model context at 16K because SYNUR does not require native 128K/262K context.

## Execution order
1. `make check`
2. start teacher endpoints
3. `make benchmark-smoke` (small DEV subset)
4. inspect only operational failures (OOM, endpoint/model mismatch, parser crash)
5. `make benchmark-dev`
6. `make benchmark-summary`
7. produce a DEV decision report + ADR
8. only then unlock and run TEST once

## What may be fixed after smoke
Operational bugs only: endpoint URL, server launch flags, incorrect model name, serialization/parser crash, missing dependency. Do not tune prompt content or retrieval K from smoke results and then claim the same run as pre-registered.
