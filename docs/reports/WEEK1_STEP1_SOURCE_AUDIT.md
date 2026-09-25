# Week 1 — Step 1 Source Audit & Bootstrap Report

**Date:** 2026-09-25  
**Status:** COMPLETE, except official CV292 binary attachment requires user upload.

## 1. Completed

1. Created standalone ESF research workspace/repository skeleton.
2. Copied and versioned ESF schema contracts + Data Team handoff v0.1.
3. Verified regulatory/technical sources for TT32, 29/BV-02, 15/BV-01, CV292, TT51, QĐ2805 and CV365.
4. Corrected outpatient form code from `15/BV1` to `15/BV-01`.
5. Verified SYNUR structure and role as the primary external schema-constrained extraction benchmark.
6. Verified MTS-Dialog repository, CSV contract and role as an auxiliary dialogue/history benchmark.
7. Implemented initial dataset adapters:
   - `src/esf/datasets/synur.py`
   - `src/esf/datasets/mts_dialog.py`
8. Added schema/contract validator: `scripts/validate_contracts.py`.
9. Added 10 regression cases covering current positive, explicit negative, historical, resolved, uncertain, self-correction, NOT_MENTIONED, indirect wording, code-switching and caregiver report.
10. Ran contract validation: original handoff example + all 10 regression cases PASS.
11. Ran unit tests: **4 passed**.

## 2. Key architecture decision confirmed

Month-1 research work must not depend on the Synthetic Data Team. Until their generator is ready:

- SYNUR = primary external extraction/retrieval benchmark.
- MTS-Dialog = auxiliary dialogue/history/section benchmark.
- MOH registry + deterministic projection = built from official Vietnamese regulatory/form specifications.
- Synthetic Vietnamese conversations = parallel track and later evaluation/training asset, not a Week-1/Month-1 blocker.

## 3. Blocking item requiring user action

The official public page exposes `DacTaEMR-TT32.rar`, but binary retrieval is not supported from the current execution environment.

**User action:** download `DacTaEMR-TT32.rar` from the official Dong Nai CDC CV292 page and upload the `.rar` file into this chat.

Once uploaded, the next task is to:
1. inspect archive structure;
2. identify `29/BV-02` and `15/BV-01` specifications;
3. parse field descriptions, datatypes, lengths, references and JSON definitions;
4. generate versioned machine-readable MOH form registry;
5. build form→canonical-concept crosswalk.

## 4. Non-blocking inputs that can arrive later

For HIS portability work (not needed to continue Week 1), obtain when available from VNPT/FPT/Product/Engineering:

- API/JSON/XML contract;
- field/property IDs and labels;
- datatype and enum/value sets;
- unit;
- nullable/required;
- description/source module/version;
- 2–5 synthetic or de-identified payload examples;
- any existing mapping to MOH forms.

## 5. Next step after this checkpoint

### Step 2A — Official MOH Registry
Requires `DacTaEMR-TT32.rar` upload.

### Step 2B — Public Dataset Baselines
Can proceed independently using SYNUR and MTS-Dialog while waiting for the RAR.
