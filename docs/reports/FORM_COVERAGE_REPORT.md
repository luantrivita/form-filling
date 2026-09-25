# FORM COVERAGE REPORT — TT32 Technical Specification

## Archive audit
- Non-SVN documents: **90**
- Bệnh án: **30**
- Phiếu/giấy: **56**
- Target documents found: `15.Ngoại trú chung.docx`, `29.Phiếu khám bệnh vào viện.docx`.

## 29/BV-02 — Phiếu khám bệnh vào viện
- Technical fields: **52**
- Pre-visit/history target fields: **4**
- Target technical names: `LyDoVaoVien, QuaTrinhBenhLi, TienSuBenhBanThan, TienSuBenhGiaDinh`

## 15/BV-01 — Bệnh án Ngoại trú chung
- Technical form ID in specification: **414**
- Technical fields in main table: **71** (plus nested object definitions such as `DauSinhTon`, `HoSo`).
- Pre-visit/history target fields: **4**
- Target technical names: `LyDoVaoVien, QuaTrinhBenhLy, TienSuBenhBanThan, TienSuBenhGiaDinh`

## Key finding
Both target national forms encode the history section mainly as four narrative fields: reason for visit, present illness, personal history and family history. The technical specifications do **not** expose dedicated medication or allergy fields in these two target forms. Therefore medication/allergy may remain canonical facts for extraction, but V1 must not silently force them into a national-form field without an explicit hospital/form mapping.

## V1 autofill boundary
- Allowed: patient-reported history fields + HIS administrative facts where mapping is known.
- Measured-only: vital signs and measurements.
- Clinician-only: examination, diagnosis, treatment, discharge/summary fields.
- `NOT_MENTIONED` must remain distinct from `NEGATIVE`.

## Source vs research design
The field names, types, lengths, references and JSON examples come from `DacTaEMR-TT32.rar`. Canonical concept decomposition and form→concept mappings in this repo are a research/product design layer and are **not** claimed to be official Ministry mappings.
