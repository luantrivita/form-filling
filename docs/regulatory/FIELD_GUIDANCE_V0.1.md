# FIELD GUIDANCE V0.1 — ESF Pre-Visit

This guidance is derived from the TT32 technical specification plus the ESF scope. It does not claim to replace a clinical documentation manual.

| Target field | Fill policy | Canonical source | Evidence rule |
|---|---|---|---|
| `LyDoVaoVien` | PATIENT_OR_HIS | `ENCOUNTER.REASON_FOR_VISIT`, `ENCOUNTER.CHIEF_COMPLAINT` | Must be explicitly stated or imported with provenance |
| `QuaTrinhBenhLi` / `QuaTrinhBenhLy` | PATIENT_OR_HIS | HPI atomic facts | Render only supported facts; preserve temporality/corrections |
| `TienSuBenhBanThan` | PATIENT_OR_HIS | chronic/past condition, hospitalization, surgery | Do not infer absent disease from silence |
| `TienSuBenhGiaDinh` | PATIENT_OR_HIS | family condition | Keep experiencer=family; do not convert to patient diagnosis |

## Medication and allergy
The two selected national forms do not contain dedicated medication/allergy technical fields. Keep these as canonical facts, but projection requires a target form/hospital field that explicitly supports them.

## Hard rules
1. `NOT_MENTIONED != NEGATIVE`.
2. Historical/resolved facts must not become current positive.
3. Self-correction keeps provenance and latest supported state.
4. No clinician-only field is auto-filled from patient dialogue.
5. Narrative rendering may compress facts but must not introduce new facts.
