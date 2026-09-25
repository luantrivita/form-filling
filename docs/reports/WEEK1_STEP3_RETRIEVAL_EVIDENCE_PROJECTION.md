# WEEK 1 / STEP 3 — Retrieval + Evidence + Deterministic Projection

**Status:** PASS (engineering checkpoint)  
**Important limitation:** regression retrieval/evidence numbers below use only the small manually authored regression suite and are **not** publication-level benchmark results.

## 1. What was implemented

### Candidate retrieval
- Internal `ConceptRetriever` over `canonical_concepts.v0.2.json`.
- Hybrid lexical index: word 1–2 gram TF-IDF + character 3–5 gram TF-IDF.
- Candidate set is:
  - all **target-form anchor concepts**; plus
  - dynamic top-K concepts.
- Low top-score can trigger **full-schema fallback**.
- Retrieval omission is never interpreted as clinical negation.

### Evidence-turn retrieval
- Concept-conditioned turn ranking.
- Returns existing turns only; no fabricated span or text.
- V1 uses turn-level evidence; exact span extraction remains later work.

### Deterministic form projection
Implemented for:
- `MOH_29_BV_02`;
- `MOH_15_BV_01`.

Rules:
- project canonical facts via versioned mapping registry;
- no unmapped fact is silently inserted into a form field;
- `NOT_MENTIONED` remains null, never becomes negative;
- conflicting values are flagged `CONFLICT`, never overwritten;
- source fact IDs are preserved;
- current narrative renderer is explicitly marked `DRAFT_RESEARCH_RENDERER` because MOH technical specs define target fields but do not provide a complete deterministic linguistic rendering manual for canonical atomic facts.

### Output validation
Checks include:
- valid field statuses;
- duplicate field IDs;
- `NOT_MENTIONED` cannot carry a value;
- `SUPPORTED` must preserve provenance.

### Prompt contracts
Created:
- `prompts/B1_FULL_SCHEMA_EXTRACTION.md`;
- `prompts/B2_RETRIEVAL_EXTRACTION.md`.

Both enforce evidence-only extraction and `NOT_MENTIONED != NEGATIVE`.

## 2. Regression results

### Candidate retrieval
Small regression suite: 10 manually authored cases.

| Dynamic K | Mean gold concept recall after anchor union | Cases with all gold covered |
|---:|---:|---:|
| 5 | 0.900 | 0.900 |
| 10 | 0.900 | 0.900 |
| 20 | 1.000 | 1.000 |

Interpretation: useful as a regression safety check only. The more meaningful external retrieval benchmark remains SYNUR, where hard pruning was shown to be risky.

### Evidence-turn retrieval
11 gold fact/evidence alignments available in the current regression suite:
- Hit@1: **0.455**
- Hit@2: **0.909**

Interpretation:
- current lexical evidence retrieval is insufficient as a final evidence selector;
- keeping multiple candidate turns is safer than forcing top-1;
- aliases, Vietnamese terminology, dense retrieval/reranking and model-based evidence verification should be evaluated later;
- this result must **not** be reported as clinical evidence accuracy because the sample is tiny and synthetic/manual.

### Projection regression
- 10 cases × 2 MOH forms = **20 projected outputs**.
- Validation errors: **0**.
- `NOT_MENTIONED`, cross-form reuse and conflict preservation are covered by unit tests.

## 3. Test status

Repository tests: **12/12 PASS**.

Key new regression tests:
- form-anchor concepts cannot be pruned;
- obvious evidence turn retrieval;
- `NOT_MENTIONED != NEGATIVE`;
- same canonical fact can project to both official forms;
- conflict is flagged instead of overwritten.

## 4. Architecture decision after Step 3

Retain the proposed architecture:

```text
conversation + optional HIS
        ↓
form anchors + dynamic retrieval
        ↓
evidence candidate turns
        ↓
schema-conditioned extraction
        ↓
canonical facts
        ↓
temporal/conflict reconciliation
        ↓
deterministic projection
        ↓
validator / review flags
```

Do **not** use retrieval as a hard clinical truth filter. The full-schema fallback remains mandatory until retrieval recall is proven sufficiently high on a larger relevant benchmark.

## 5. Next step

**Step 4 — Model-ready B1/B2 evaluation harness + typed SYNUR extraction protocol**

Planned work:
1. define exact B1/B2 JSON response schema;
2. build inference runner interface independent of model vendor;
3. prepare SYNUR dev subset and scoring pipeline for actual LLM extraction;
4. build typed value metrics by `SINGLE_SELECT`, `MULTI_SELECT`, `STRING`, `NUMERIC`;
5. add unsupported-fill / abstention accounting;
6. prepare 29/BV-02 + 15/BV-01 end-to-end demo inputs.

### Dependency
No additional public dataset is needed. To run a **true LLM baseline at scale**, a callable model runtime/API or local model endpoint will eventually be required. The harness can be completed before that dependency is provided.
