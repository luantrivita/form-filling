# WEEK 1 / STEP 2B — Public Dataset Audit + First Baselines

**Status:** PASS  
**Inputs:** user-provided `SYNUR.zip`, `MTS-Dialog.zip`  
**Purpose:** make the ESF research track independent of the synthetic-data pipeline while Data Team builds the Vietnamese generator.

## 1. Dataset integrity

### SYNUR
- Schema: **193 concepts**.
- Schema value types: **130 SINGLE_SELECT, 31 STRING, 20 NUMERIC, 12 MULTI_SELECT**.
- Splits loaded successfully:
  - train: **122** transcripts;
  - dev: **101**;
  - test: **199**.
- Mean gold concepts/transcript: ~13 on dev/test.
- This dataset is kept as an **external schema-constrained extraction benchmark**, not a Vietnamese MOH-form benchmark.

### MTS-Dialog
- Main splits loaded successfully:
  - train: **1,201 total / 1,072 pre-visit-history relevant**;
  - validation: **100 / 82**;
  - test-chat: **200 / 173**;
  - test-sum: **200 / 166**.
- Pre-visit sections used: `cc`, `genhx`, `pastmedicalhx`, `pastsurgical`, `allergy`, `medications`, `fam/sochx`, `gynhx`, `other_history`, `ros`.
- MTS-Dialog is used as an **auxiliary dialogue/section benchmark**. Its original gold labels are section headers + summaries, not ESF atomic clinical facts.

## 2. SYNUR concept-retrieval baseline

Baseline: hybrid TF-IDF using word 1–2 grams + character 3–5 grams. Index text contains concept name + allowed enum values. No LLM, no training on test data.

| Metric | Dev | Test |
|---|---:|---:|
| Recall@5 | 0.321 | 0.325 |
| Recall@10 | 0.554 | 0.543 |
| Recall@20 | 0.768 | 0.745 |
| Recall@30 | 0.850 | 0.826 |
| Recall@50 | **0.942** | **0.900** |
| All gold covered @30 | 0.149 | 0.151 |
| All gold covered @50 | **0.505** | **0.307** |
| MRR, first relevant | 0.956 | 0.909 |

### Interpretation
- Lexical retrieval can place at least one relevant concept very high, hence high first-relevant MRR.
- It is **not safe as a hard pruning stage**: even at K=50, all gold fields are present for only ~31% of test cases.
- Therefore the current architecture decision is retained:
  1. optimize for high recall;
  2. add lexical+dense/hybrid retrieval later;
  3. use **full-schema fallback** when retrieval confidence/coverage is insufficient.
- Do not optimize K only for average recall; missing one clinically relevant candidate can cause a false `NOT_MENTIONED` downstream.

## 3. MTS-Dialog section-classification baseline

Baseline: dialogue-only TF-IDF word 1–2 grams + balanced logistic regression trained on the official training split.

| Split | Rows | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| Validation | 82 | **0.817** | 0.601 | 0.811 |
| Test Chat | 173 | **0.786** | 0.615 | 0.782 |
| Test Sum | 166 | **0.831** | 0.649 | 0.825 |

### Interpretation
- Strong performance on frequent categories such as `fam/sochx` and `genhx` confirms that MTS-Dialog is useful for dialogue/section sanity checks.
- Macro F1 is much lower than accuracy because `gynhx` and `other_history` have extremely low support. These classes must not be used to make broad claims about robustness.
- This is **not a form-filling score** and will be reported separately from SYNUR/ESF extraction metrics.

## 4. Current conclusions for the 8-week plan

1. **Synthetic Data Team is no longer on the critical path for Weeks 1–4.**
2. SYNUR supports development of retrieval, typed extraction, schema-valid output and error analysis now.
3. MTS-Dialog supports dialogue understanding, section routing and evidence experiments, but does not provide ESF atomic-fact gold.
4. A future Vietnamese synthetic dataset remains necessary for:
   - Vietnamese colloquial language;
   - patient/caregiver speaker turns;
   - assertion / negation;
   - historical vs current vs resolved;
   - self-correction;
   - HIS vs conversation conflict;
   - code-switch and ASR noise;
   - evidence-grounded evaluation against the Vietnamese canonical registry.
5. SYNUR should not be mixed into the Vietnamese final test set. It remains an external benchmark.

## 5. Engineering status

- Public dataset manifest with SHA-256: complete.
- SYNUR loader: PASS.
- MTS-Dialog loader: PASS.
- Public metrics: PASS.
- SYNUR retrieval baseline: complete.
- MTS section baseline: complete.
- Repository unit tests: **7/7 PASS**.
- Existing generation-contract validation: remains PASS.

## 6. Next step

**Step 3 — Retrieval + evidence + deterministic projection:**
- implement retriever interface and full-schema fallback policy;
- create evidence-turn retrieval baseline;
- add candidate-recall error logging;
- formalize `NOT_MENTIONED` guardrail;
- implement deterministic projection from canonical facts to `29/BV-02` and `15/BV-01`;
- validate projection with regression cases;
- prepare B1/B2 prompt contracts for actual model inference.

No additional user-provided file is required for Step 3.
