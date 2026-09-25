# WEEK 1 — STEP 2B REPORT (CODE/HARNESS READY)

## Status
**CODE/HARNESS: PASS**
**FULL DATA INGESTION: WAITING FOR LOCAL PUBLIC DATA FILES**

## Completed
- Verified SYNUR public repository structure and split names.
- Verified MTS-Dialog repository structure and expected CSV schema.
- Kept SYNUR as primary external schema-constrained extraction benchmark.
- Kept MTS-Dialog as auxiliary dialogue/history benchmark.
- Implemented lightweight MTS loader with pre-visit section filtering.
- Implemented SYNUR JSONL loader and observation type audit.
- Implemented concept precision/recall/F1 and exact observation match helpers.
- Added public dataset audit script.
- Added download manifest/instructions.
- Test suite: 7/7 PASS.
- Data-generation contracts: PASS.

## External-source facts verified
SYNUR public repo exposes MEDIQA-SYNUR train/dev/test JSONL files and a 193-concept schema. The dataset card defines four value types: SINGLE_SELECT, MULTI_SELECT, STRING, NUMERIC.

MTS-Dialog exposes CSV files with columns ID, section_header, section_text, dialogue. It is not atomic-fact gold and must remain auxiliary.

## Required user action
Upload the files listed in `docs/PUBLIC_DATASET_DOWNLOADS.md`.

## Next after upload
1. Full dataset audit and split statistics.
2. Freeze public benchmark manifest.
3. Build/run B0/B1 baseline input-output contracts.
4. Start B2 retrieval benchmark and error taxonomy.
