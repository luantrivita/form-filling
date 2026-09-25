# Generation Instructions — ESF V1

1. Generate conversation **from the supplied gold fact graph**.
2. Every fact with `must_mention=true` must be expressed with the same assertion and temporality.
3. Do not add a new diagnosis, treatment, clinician examination finding, laboratory/imaging result, or major symptom not present in the gold graph.
4. `NOT_MENTIONED` is represented by omission; never convert it to an explicit negative.
5. A resolved/historical condition must not be rewritten as currently active.
6. Self-correction must preserve the earlier statement in dialogue and provide clear later correction.
7. Use natural Vietnamese; colloquial language is encouraged only when requested by generation controls.
8. Preserve stable `turn_id`; align each supported gold fact to one or more evidence turns.
9. Code-switch and ASR noise are robustness variants, not defaults.
10. Return only objects that validate against the provided schemas.
