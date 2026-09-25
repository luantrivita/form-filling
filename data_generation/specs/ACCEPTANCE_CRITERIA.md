# Acceptance Criteria — ESF Synthetic Pilot

## Hard gates
- 100% JSON Schema valid.
- 100% concept IDs exist in declared registry version.
- All `must_mention=true` facts are supported by conversation evidence.
- Negation, temporality and correction semantics are preserved.
- No new major clinical fact, diagnosis, treatment or clinician-only examination finding.
- Evidence turn IDs exist and belong to the same conversation.
- `base_case_id` is stable across variants; train/dev/test split occurs before variant generation.

## Pilot before scale
1. Data Team returns 3–5 handshake samples.
2. Research validates contract and returns errors.
3. Data Team generates 100–200 pilot samples.
4. Automatic QA runs on all samples.
5. Human audit 50–100 samples.
6. Scale only after hard gates pass and major semantic error rate is acceptable to Research/Clinical reviewer.
