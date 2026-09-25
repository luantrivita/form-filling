# B1 — Full Schema Extraction Prompt Contract

Input:
- completed conversation;
- full candidate canonical schema;
- optional canonical HIS facts.

Output: strict JSON list of canonical facts only.

Hard rules:
1. Evidence-supported only.
2. `NOT_MENTIONED != NEGATIVE`.
3. Preserve explicit negation, uncertainty, historical/resolved state and self-correction.
4. Do not infer examination findings, diagnosis or treatment.
5. Every supported fact must cite existing conversation turn IDs or HIS provenance.
6. If evidence is insufficient, abstain instead of guessing.
7. Output canonical facts; do not write hospital-form fields directly.
