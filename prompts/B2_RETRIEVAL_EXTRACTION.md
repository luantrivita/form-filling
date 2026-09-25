# B2 — Retrieval-Conditioned Extraction Prompt Contract

Input:
- completed conversation;
- target form ID;
- candidate canonical concepts from retriever;
- retrieved evidence turns;
- optional canonical HIS facts.

Safety rule: form-anchor concepts are always present. Dynamic retrieval must not be treated as proof that omitted concepts are negative. If retrieval confidence is insufficient, use full-schema fallback.

Output and clinical rules are identical to B1.
