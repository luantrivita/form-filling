# ĐỀ XUẤT — Hệ thống Điền Biểu mẫu Bệnh sử Trước khám dựa trên Schema Chuẩn Bộ Y tế

**Dự án:** ESF / Cấu trúc hóa bệnh sử trước khám  
**Thời gian:** 8 tuần  
**Mục tiêu chính:** Chuyển hội thoại trước khám, có thể kết hợp dữ liệu HIS sẵn có, thành các clinical facts có bằng chứng và điền vào biểu mẫu Bộ Y tế / bệnh viện **mà không cần huấn luyện lại model cho từng form hoặc từng bệnh viện**.  
**Mục tiêu nghiên cứu:** Đánh giá một kiến trúc tách `canonical clinical facts` khỏi `hospital form schema`, tập trung vào unseen-form generalization, evidence grounding và khả năng tích hợp nhiều HIS.

---

## 0. Tóm tắt điều hành

Phiên bản V1 trong 8 tuần **không tự động hóa toàn bộ bệnh án** và không thay bác sĩ khám/chẩn đoán. Hệ thống chỉ tập trung vào thông tin bệnh nhân/người nhà có thể cung cấp trước khi gặp bác sĩ:

- lý do vào viện / lý do khám;
- triệu chứng chính;
- bệnh sử hiện tại;
- khởi phát, thời gian kéo dài, mức độ, diễn tiến;
- triệu chứng đi kèm;
- tiền sử bệnh, phẫu thuật, nhập viện;
- thuốc đang sử dụng;
- tiền sử dị ứng;
- tiền sử gia đình;
- yếu tố nguy cơ/xã hội;
- phần mở rộng theo chuyên khoa khi cần.

Kiến trúc cốt lõi:

```text
Biểu mẫu Bộ Y tế
+ đặc tả trường dữ liệu
+ hướng dẫn điền
        │
        ▼
Canonical Pre-Visit Registry
        │
   ┌────┴────┐
   ▼         ▼
VNPT HIS    FPT HIS
Adapter     Adapter
   │         │
   └────┬────┘
        ▼
Thông tin HIS đã có

Conversation trước khám
        │
        ▼
Retriever concept/field liên quan
        │
        ▼
Evidence extraction
        │
        ▼
Canonical atomic facts
        │
        ▼
Temporal / conflict reconciliation
        │
        ▼
Deterministic form projection
        │
        ▼
Schema + constraint validation
        │
        ▼
Filled JSON + evidence + review flags
```

**Nguyên tắc:** khác biệt giữa form của các bệnh viện phải được xử lý bằng schema/mapping/configuration trước; fine-tuning không phải mặc định.

---

# 1. Phạm vi

## 1.1 Trong phạm vi

| Nhóm | Ví dụ |
|---|---|
| Lý do khám | reason for visit, chief complaint |
| Bệnh sử hiện tại | onset, duration, course, severity |
| Triệu chứng | vị trí, tính chất, tần suất, triệu chứng đi kèm |
| Xử trí trước đó | cơ sở đã khám, điều trị trước, đáp ứng |
| Tiền sử bản thân | bệnh nền, bệnh cũ, nhập viện, phẫu thuật |
| Thuốc | thuốc đang dùng, liều/tần suất nếu có |
| Dị ứng | thuốc, thực phẩm, côn trùng, dị nguyên khác |
| Tiền sử gia đình | bệnh liên quan |
| Yếu tố nguy cơ | hút thuốc, rượu, nghề nghiệp/phơi nhiễm |
| Chuyên khoa | ENT, GI, tim mạch, sản phụ khoa... |

### Input runtime

```text
conversation JSON
target form schema JSON
optional HIS prior facts JSON
```

### Output

```text
canonical facts
evidence
target form fields
field status
source/provenance
conflict/uncertainty flags
```

## 1.2 Ngoài phạm vi 8 tuần

- tự động chẩn đoán mới;
- khuyến nghị điều trị;
- suy diễn khám thực thể từ lời bệnh nhân;
- full ICD coding;
- adaptive interviewer hoàn chỉnh;
- production UI;
- curate toàn bộ mọi form Bộ Y tế;
- deployment bệnh viện;
- train trên dữ liệu bệnh nhân thật;
- model riêng cho từng bệnh viện;
- multi-agent architecture phức tạp.

---

# 2. Nguồn Bộ Y tế, form và tài liệu hướng dẫn dùng làm schema gốc

## 2.1 Thứ tự ưu tiên nguồn — sửa so với plan cũ

Không bắt đầu bằng cách tự đọc PDF và nhập tay toàn bộ field nếu đã có đặc tả machine-readable. Thứ tự ưu tiên V2:

```text
P0. CV292/TTYQG-DA + DacTaEMR-TT32.rar
    ↓
P1. Form gốc theo TT32/2023/TT-BYT
    ↓
P2. CV365/TTYQG-GPQLCL — cấu trúc trao đổi EMR/HIS
    ↓
P3. Danh mục thuật ngữ/mã chuẩn (ví dụ QĐ2805 cho allergy/finding)
    ↓
P4. Quy định chuyên môn theo chủ đề (ví dụ TT51 về phản vệ/dị ứng)
    ↓
P5. Internal filling guidance được clinical reviewer/PO duyệt
```

**Lý do:** CV292 mô tả bộ đặc tả cho 29 mẫu bệnh án và 56 mẫu giấy/phiếu theo TT32, gồm mô tả field, datatype, độ dài, nguồn tham chiếu và chuỗi JSON lưu trong EMR. Đây phải là nguồn kỹ thuật số 1 nếu tải được attachment.

Nguồn tải:
- Trang công bố CV292 + attachment `DacTaEMR-TT32.rar`: https://dongnaicdc.vn/huong-dan-dac-ta-cau-truc-thong-tin-cac-mau-benh-an-mau-giay-phieu-y-duoc-quy-dinh-tai-thong-tu-so-32-2023-tt-byt-ngay-31-12-2023-cua-bo-y-te
- PDF công văn nằm trên cùng trang; ưu tiên tải cả PDF và RAR, lưu checksum/version trong `registry/sources/`.

## 2.2 MS 29/BV-02 — Phiếu khám bệnh vào viện (target chính)

Dùng làm **Target Form A** vì gần nhất với ESF pre-visit. Chỉ encode các phần patient-reportable/HIS-relevant:

- lý do vào viện;
- hỏi bệnh;
- quá trình bệnh lý;
- tiền sử bệnh bản thân;
- tiền sử bệnh gia đình;
- các phần khác chỉ đưa vào nếu thuộc input scope hợp lệ.

Không auto-fill khám thực thể, chẩn đoán hoặc xử trí từ lời bệnh nhân.

Nguồn tải form:
- https://thuvienphapluat.vn/bieumau/27372/MAU-PHIEU-KHAM-BENH-VAO-VIEN-CHUNG

## 2.3 MS 15/BV-01 — Bệnh án Ngoại trú chung (target thứ hai)

**Sửa mã trong plan cũ:** dùng `15/BV-01`, không dùng `15/BV1` trong registry/file name.

Vai trò:
- Target Form B cho bối cảnh ngoại trú;
- dùng cùng canonical facts để test cross-form consistency;
- không encode toàn bộ clinician-only fields trong V1.

Nguồn tải form:
- https://thuvienphapluat.vn/bieumau/27319/MAU-BENH-AN-NGOAI-TRU-CHUNG
- Trang tổng hợp bản Word các phụ lục TT32: https://thuvienphapluat.vn/phap-luat/phu-luc-thong-tu-32-cua-bo-y-te-ban-word-tai-ve-chi-tiet-29-phu-luc-ban-hanh-kem-thong-tu-32-moi-nh-613909-230739.html

## 2.4 Dị ứng — dùng hai lớp nguồn, không coi TT51 là codebook duy nhất

### Semantics / nội dung khai thác
Thông tư 51/2017/TT-BYT dùng để tham chiếu các yếu tố lịch sử dị ứng/phản vệ, ví dụ loại dị nguyên, biểu hiện, tiền sử và xử trí.

Nguồn chính thức có DOC/PDF:
- https://vbpl.vn/boyte/Pages/vbpq-van-ban-goc.aspx?ItemID=128248

### Chuẩn hóa code/value
Quyết định 2805/QĐ-BYT (2025) ban hành danh mục mã dùng chung thuật ngữ lâm sàng đợt 3 cho **Dị ứng (allergy)** và **Phát hiện (finding)**. Khi làm normalization/mapping, ưu tiên danh mục này nếu concept tương ứng có trong danh mục.

Nguồn:
- https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Quyet-dinh-2805-QD-BYT-2025-Danh-muc-ma-dung-chung-thuat-ngu-y-hoc-lam-sang-Dot-3-672318.aspx

## 2.5 CV365/TTYQG-GPQLCL — interop/HIS

CV365 hỗ trợ hướng thiết kế adapter: EMR có thể đồng bộ từ hệ thống khác và kết xuất XML/JSON phục vụ liên thông. Dùng tài liệu này để xác định ranh giới giữa:

```text
vendor HIS payload → adapter → canonical facts → ESF
```

Nguồn:
- https://thuvienphapluat.vn/cong-van/Cong-nghe-thong-tin/Cong-van-365-TTYQG-GPQLCL-2025-yeu-cau-ky-thuat-trien-khai-phan-mem-ho-so-benh-an-dien-tu-671468.aspx

## 2.6 “Hướng dẫn điền form” — cách xử lý thực tế

Hiện chưa nên giả định có một tài liệu công khai duy nhất hướng dẫn từng dòng cho `29/BV-02` và `15/BV-01`. V2 dùng hierarchy sau:

1. **CV292 structured specification**: description, datatype, length, reference source, JSON.
2. **TT32 form itself**: label, section, cardinality/layout.
3. **Value/code lists**: ví dụ QĐ2805.
4. **Specialty regulation**: ví dụ TT51 cho allergy semantics.
5. **Clinical/PO-approved internal guidance** cho các field narrative hoặc field chưa có semantics đủ rõ.

Tạo `FIELD_GUIDANCE_V1.md` / `field_guidance.json` với mỗi field:

```text
form_id
field_id
label
patient_reportable: true/false
source_status
source_ref
source_description
canonical_concept_refs
value_type / allowed_values / unit
fill_rule
NOT_MENTIONED policy
negation policy
temporality policy
evidence requirement
examples
reviewer / reviewed_at / version
```

**Không dùng các quy định bệnh viện cũ đã hết/giảm hiệu lực làm filling manual mặc định nếu chưa kiểm tra tình trạng pháp lý hiện hành.**

## 2.7 Form mở rộng cho unseen-form test

Không cần curate nhiều form ngay từ đầu. Sau khi A/B ổn định, chọn **một form TT32 khác** có phần history tương đồng nhưng có specialty extension để hold-out hoàn toàn khỏi development. Đây là optional W7, không phải critical path.
# 3. Ba lớp schema bắt buộc

## 3.1 Canonical Concept Schema

```json
{
  "concept_id": "RESP.DYSPNEA",
  "canonical_name": "Dyspnea",
  "labels": {"vi": "Khó thở", "en": "Dyspnea"},
  "aliases": ["khó thở", "hụt hơi", "shortness of breath"],
  "description": "Cảm giác khó thở do bệnh nhân tự khai.",
  "input_scope": ["PATIENT_REPORTED", "HIS"],
  "value_type": "SINGLE_SELECT",
  "allowed_values": ["NONE", "MILD", "MODERATE", "SEVERE"],
  "supports_negation": true,
  "supports_temporality": true
}
```

Target V1: **80–150 canonical concepts**.

## 3.2 Form Field Schema

```json
{
  "form_id": "MOH_29_BV_02",
  "field_id": "history.present_illness",
  "label": "Quá trình bệnh lý",
  "concept_refs": [
    "ENCOUNTER.CHIEF_COMPLAINT",
    "HPI.ONSET",
    "HPI.COURSE"
  ],
  "value_type": "STRUCTURED_TEXT",
  "fill_policy": "PROJECT_FROM_FACTS",
  "regulatory_status": "OFFICIAL",
  "source_ref": {
    "document": "TT32_2023",
    "form": "29/BV-02",
    "section": "III. Hỏi bệnh"
  }
}
```

## 3.3 Canonical Clinical Fact Schema

```json
{
  "fact_id": "fact_012",
  "concept_id": "RESP.DYSPNEA",
  "value": "MILD",
  "assertion": "POSITIVE",
  "temporality": "CURRENT",
  "status": "ACTIVE",
  "experiencer": "PATIENT",
  "source": {"type": "CONVERSATION", "speaker": "PATIENT"},
  "evidence": [
    {"turn_id": 8, "text": "từ sáng tôi hơi khó thở"}
  ],
  "confidence": 0.94
}
```

Các trạng thái tối thiểu:

```text
assertion:
POSITIVE / NEGATIVE / UNCERTAIN

temporality:
CURRENT / HISTORICAL / RESOLVED / UNKNOWN

field status:
SUPPORTED / NOT_MENTIONED / AMBIGUOUS /
CONFLICT / INSUFFICIENT_EVIDENCE
```

**Quy tắc:** `NOT_MENTIONED` không được tự động chuyển thành `NEGATIVE`.

---

# 4. Tích hợp VNPT + FPT HIS

## 4.1 Yêu cầu Product Owner cung cấp trong Week 1

Cho cả VNPT và FPT:

- field/table/API property ID;
- field label;
- datatype;
- enum/value set;
- unit;
- required/nullable;
- description;
- source module;
- version;
- mapping sang form Bộ Y tế nếu có;
- vài payload synthetic/de-identified;
- JSON/XML/API contract;
- field là manual/measured/imported/derived.

Không cần dữ liệu định danh thật.

## 4.2 Không dùng VNPT/FPT làm canonical schema

```text
              Canonical / MOH Registry
                      │
           ┌──────────┴──────────┐
           ▼                     ▼
      VNPT Adapter           FPT Adapter
```

Mapping types:

```text
EXACT
ENUM_REMAP
COMPOSITE
SPLIT
DERIVED
UNMAPPED
AMBIGUOUS
```

Cần report:

- % concept pre-visit đã có trong HIS;
- % phải hỏi qua conversation;
- % clinician-only;
- % ambiguous/unmapped.

## 4.3 Conflict HIS vs Conversation

Không overwrite im lặng. Giữ provenance và trả về `CONFLICT` hoặc `UPDATE_CANDIDATE`.

---

# 5. Kế hoạch dataset — V2 không phụ thuộc Synthetic Data Team trong tháng đầu

## 5.1 Nguyên tắc mới

Trong plan cũ, Week 3–4 phụ thuộc trực tiếp vào synthetic pilot/scale. Đây là critical-path risk vì Data Team chưa có pipeline. V2 tách thành hai luồng:

```text
TRACK A — Research/Engineering (không bị block)
SYNUR + MTS-Dialog + manually-authored regression cases
→ baseline → retrieval/evidence → canonical facts → projector/validator → demo

TRACK B — Data Team (chạy song song)
Canonical schema + gold fact contract
→ synthetic generation pipeline
→ pilot QA
→ Vietnamese synthetic dataset khi sẵn sàng
```

**Month-1 demo không được phụ thuộc vào việc Track B hoàn tất.**

## 5.2 SYNUR / MEDIQA-SYNUR — public benchmark chính

SYNUR phù hợp nhất với phần **schema-constrained extraction**:

- input là clinical/nursing dictation transcript;
- output là `observations` có ID, tên, `value_type`, value;
- schema đầy đủ có 193 observation concepts;
- value types chính: `SINGLE_SELECT`, `MULTI_SELECT`, `STRING`, `NUMERIC`.

Dùng SYNUR để:

1. benchmark B1 `full schema → structured extraction`;
2. benchmark B2 `candidate retrieval → extraction`;
3. đo Recall@K/MRR của concept retrieval;
4. đo exact/typed value extraction;
5. test strict JSON/schema validation;
6. test effect của candidate pruning/evidence filtering;
7. nếu cần SFT sau này, dùng như auxiliary task chứ không coi là Vietnamese MOH training data.

**Không dùng SYNUR để chứng minh trực tiếp rằng model điền form Bộ Y tế tốt**, vì domain là nurse observation/dictation, tiếng Anh, và ontology không phải pre-visit history của TT32.

Nguồn: https://huggingface.co/datasets/microsoft/SYNUR

## 5.3 MTS-Dialog — auxiliary dialogue benchmark, không phải gold form-filling dataset

MTS-Dialog có khoảng 1.7k doctor-patient conversations và summary/section headers. Các section phù hợp scope ESF gồm:

```text
cc
 genhx
 pastmedicalhx
 pastsurgical
 allergy
 medications
 fam/sochx
 gynhx (khi cần)
 other_history (có kiểm soát)
```

Dùng MTS-Dialog để:

1. test section/concept-family routing từ hội thoại;
2. test evidence localization theo turn/span;
3. test dialogue understanding trên HPI/history;
4. auxiliary evaluation cho summarization/factuality;
5. sanity check conversation ingestion.

**Không dùng MTS-Dialog như gold atomic-fact extraction benchmark** nếu chưa có human annotation, vì gold target gốc chủ yếu là section summary/section label, không có canonical concept ID, assertion, temporality và `NOT_MENTIONED` theo contract ESF.

Nếu tạo pseudo-label bằng LLM để debug, phải gắn `SILVER`, không đưa vào final test hoặc claim chính.

Nguồn: https://github.com/abachaa/MTS-Dialog

## 5.4 So sánh vai trò hai public datasets

| Tiêu chí | SYNUR | MTS-Dialog |
|---|---|---|
| Structured schema gold | Mạnh | Yếu/không có ở mức atomic concept |
| Dialogue doctor-patient | Không phải mục tiêu chính | Mạnh |
| Value type / enum | Có | Không theo ESF contract |
| Retrieval benchmark | Rất phù hợp | Phù hợp ở section/concept-family |
| Evidence extraction | Có thể xây tốt | Tốt cho turn-level, nhưng gold cần bổ sung |
| Assertion/temporality gold | Hạn chế so với ESF | Không đầy đủ |
| Vietnamese MOH form | Không | Không |
| Vai trò V2 | **Primary external benchmark** | **Auxiliary dialogue benchmark** |

## 5.5 Regression set nội bộ trong lúc chờ Data Team

Research Engineer tự viết **20–50 gold fact graphs + conversations ngắn** chỉ để integration/regression, không gọi đây là training dataset và không dùng để claim performance tổng quát.

Phải cover ít nhất:
- positive current;
- explicit negative;
- historical;
- resolved;
- uncertain;
- self-correction;
- not mentioned;
- multi-value;
- numeric + unit;
- HIS conflict;
- caregiver;
- code-switch/ASR-noise ở một subset nhỏ.

Mục tiêu: bảo đảm projector, reconciliation, validator và evidence contract chạy đúng trước khi synthetic pipeline hoàn tất.

## 5.6 Synthetic data vẫn phải fact-first

```text
Canonical Schema
      ↓
Gold Fact Graph
      ↓
Generation Controls
      ↓
Generate Conversation
      ↓
Evidence Alignment
      ↓
Automatic Validation
      ↓
Human QA
      ↓
Deterministic Form Projection
```

Không generate conversation trước rồi để một LLM khác tự suy ra “gold”.

## 5.7 Package gửi Synthetic Data Team ngay, không đợi model hoàn thiện

```text
data_generation_contract/
├── README.md
├── schemas/
│   ├── canonical_concept.schema.json
│   ├── clinical_fact.schema.json
│   ├── fact_graph.schema.json
│   ├── conversation.schema.json
│   ├── generation_case.schema.json
│   └── evidence_alignment.schema.json
├── registry/
│   ├── canonical_concepts.v0.1.json
│   └── value_sets.v0.1.json
├── specs/
│   ├── scenario_matrix.json
│   ├── generation_instructions.md
│   ├── validation_rules.json
│   └── ACCEPTANCE_CRITERIA.md
└── examples/
    └── example_case_001.json
```

Schema có thể gửi ngay từ W1 ở version `v0.1`; concept inventory/value sets được cập nhật versioned, không breaking change âm thầm.

## 5.8 Acceptance gate cho data từ Data Team

Trước khi ingest vào train/dev/test:

- 100% JSON schema-valid;
- 100% concept IDs tồn tại trong registry version khai báo;
- intended facts được thể hiện trong conversation;
- negation/temporality/correction không bị đảo nghĩa;
- không tự thêm major clinical facts ngoài fact graph;
- không thêm clinician-only exam/diagnosis/treatment mới;
- stable turn IDs;
- evidence mapping hợp lệ;
- split theo `base_case_id` trước khi generate variants;
- pilot 50–100 samples phải được human audit trước khi scale.

## 5.9 Quy mô synthetic — chuyển thành conditional milestone

Không đặt `≥2,000 conversations` làm DoD tháng 1 nữa.

- Pilot khi pipeline sẵn sàng: 100–200 conversations.
- Sau khi pass quality gate: 1,000–2,000 base/valid conversations cho V1 nếu resource cho phép.
- Dev/test human-reviewed: 200–300 là target sau khi generation ổn định.

Nếu Data Team trễ tới W6–W7, project vẫn hoàn thành public-data benchmark + end-to-end architecture; Vietnamese synthetic benchmark được report thành dependency chưa hoàn tất, không làm fail toàn bộ PoC.
# 6. Model pipeline

## B0 — Direct

```text
conversation → full form
```

## B1 — Full Schema

```text
conversation + full target schema → form
```

## B2 — Retrieval

```text
conversation → relevant concepts → extraction → form
```

## Proposed

```text
conversation + optional HIS
        ↓
concept retrieval
        ↓
evidence retrieval
        ↓
schema-conditioned fact extraction
        ↓
canonical facts
        ↓
temporal/conflict reconciliation
        ↓
deterministic projection
        ↓
validator + abstention
```

Không thêm multi-agent nếu chưa có evidence cần thiết.

---

# 7. Fine-tuning

Không train trong tháng đầu.

Chỉ train sau W5 nếu:

- dataset đã sạch;
- open/local model là bottleneck;
- lỗi không phải do schema/data/retrieval.

Training target:

```text
conversation
+ candidate concept schema
+ optional HIS facts
→ canonical facts
+ assertion
+ temporality
+ evidence
```

Không train model nhớ một form bệnh viện cụ thể.

---

# 8. Evidence từ paper

1. **Corbeil et al., EMNLP Industry 2025 / SYNUR** — schema-guided clinical extraction và synthetic data cho clinical IE.
2. **MEDIQA-SYNUR 2026** — observation extraction + normalization + ontology mapping.
3. **Note2Chat, AAAI 2026** — sinh multi-turn clinical history conversation từ structured/note information.
4. **Woo et al., npj Digital Medicine 2025** — synthetic clinical IE data có thể fine-tune smaller open models hiệu quả.
5. **MTS-Dialog, EACL 2023** — public doctor-patient dialogue có nhiều pre-visit/history sections phù hợp.

---

# 9. Metrics

| Layer | Metric |
|---|---|
| Retriever | Recall@K, MRR |
| Concept extraction | micro/macro F1 |
| Single-select | Accuracy/F1 |
| Multi-select | micro/macro F1 |
| Numeric | exact/tolerance accuracy |
| Free text | token F1 + factuality review |
| Negation | F1 |
| Temporality | F1 |
| NOT_MENTIONED | P/R/F1 |
| Evidence | span/turn F1 |
| Hallucination | unsupported-fill rate |
| Structure | schema-valid rate |
| Full form | exact match / field F1 |
| Generalization | unseen-form F1 |
| Cross-form | consistency |
| HIS adapter | mapping coverage |

```text
Unseen Form Gap = Seen-Form F1 - Unseen-Form F1
```

---

# 10. Timeline 8 tuần — public-data-first, synthetic chạy song song

## TUẦN 1 — Freeze nguồn, form, schema contracts + handoff cho Data Team

**Research/Engineering**
- tải và archive CV292 PDF + `DacTaEMR-TT32.rar`;
- tải `29/BV-02`, `15/BV-01`, TT51, QĐ2805, CV365;
- sửa toàn bộ code/registry từ `15/BV1` → `15/BV-01`;
- tạo source registry + checksum/version;
- freeze pre-visit scope;
- freeze JSON schemas v0.1;
- dựng loaders skeleton cho SYNUR/MTS-Dialog;
- viết 10 regression cases đầu tiên.

**Data Team handoff**
- gửi `ESF_DATA_GEN_HANDOFF_V1` ngay;
- walkthrough fact-first generation;
- chốt acceptance criteria và versioning handshake.

**Output**
```text
regulatory_source_registry.md
ESF_NGUON_FORM_VA_HUONG_DAN_V1.md
canonical_concept.schema.json
clinical_fact.schema.json
form_field.schema.json
conversation.schema.json
generation_case.schema.json
ESF_DATA_GEN_HANDOFF_V1/
```

**Manager report**
> Đã loại dependency synthetic khỏi critical path tháng 1. Nguồn form/đặc tả được freeze; contract generation v0.1 đã gửi Data Team. Research track bắt đầu ngay trên SYNUR/MTS-Dialog.

**DoD:** source package tải được + schema package Data Team validate được + một manual case chạy schema-valid.

---

## TUẦN 2 — MOH Registry + public dataset adapters + baseline đầu tiên

**Tasks**
- parse/curate pre-visit subset của `29/BV-02` + `15/BV-01`;
- ưu tiên converter từ CV292 attachment nếu format cho phép;
- build 60–100 core concepts trước; mở rộng lên 80–150 sau khi deduplicate;
- build allergy normalization từ TT51 + QĐ2805;
- hoàn thiện SYNUR adapter;
- lọc MTS-Dialog về pre-visit/history sections;
- chạy B0/B1 trên SYNUR;
- chạy MTS section-routing baseline;
- nâng regression set lên 20–30 cases.

**Output**
```text
canonical_concepts.v0.1.json
moh_29_bv02.json
moh_15_bv01.json
allergy_mapping_v0.1.json
src/datasets/synur.py
src/datasets/mts_dialog.py
week2_public_baseline.md
```

**Manager report**
> Đã có machine-readable MOH form registry và external benchmark đầu tiên. SYNUR được dùng cho structured extraction; MTS-Dialog dùng cho dialogue/history routing, không đánh đồng hai dataset.

---

## TUẦN 3 — Retrieval + evidence + projector/validator, không chờ synthetic

**Tasks**
- lexical/dense/hybrid candidate retrieval;
- đo Recall@K/MRR trên SYNUR;
- evidence retrieval;
- B2 retrieval → extraction;
- build canonical fact converter;
- deterministic facts→form projector;
- schema/constraint validator;
- MTS turn-level evidence prototype;
- regression tests negation/history/resolved/correction/not-mentioned.

**Output**
```text
src/retrieval/
src/evidence/
src/projection/
src/validation/
week3_b2_benchmark.md
regression_suite_v0.1/
```

**Manager report**
> Critical pipeline đã tiến tới retrieval/evidence/projector mà không phụ thuộc Data Team. Đã tách được retrieval error, extraction error và projection error.

---

## TUẦN 4 — Full P1 pipeline + Month-1 Demo độc lập synthetic

**Tasks**
- schema-conditioned atomic fact extraction;
- assertion + temporality + provenance;
- reconciliation trên manually-authored cases;
- abstention/NOT_MENTIONED;
- end-to-end projection sang 29/BV-02 và 15/BV-01;
- B0/B1/B2/P1 benchmark trên SYNUR;
- MTS dialogue sanity benchmark;
- error taxonomy.

**Output**
```text
src/pipeline/
experiments/public_benchmarks/
month1_demo.md
week4_error_taxonomy.md
```

**Month-1 Demo**
```text
conversation
→ retrieved concepts/evidence
→ canonical facts
→ 29/BV-02 JSON / 15/BV-01 JSON
→ validation + review flags
```

**DoD:** demo chạy được dù Data Team chưa generate một sample nào.

---

## TUẦN 5 — Robustness + ablation + conditional synthetic pilot

**Always-run tasks**
- retrieval/evidence tuning;
- full-schema vs retrieval ablation;
- validator/guidance/canonical-layer ablation;
- code-switch/ASR/long-context perturbations trên regression/public subset;
- finalize evaluation harness.

**Nếu Data Team sẵn sàng**
- ingest pilot 100–200;
- automatic QA;
- human audit 50–100;
- reject/feedback theo error taxonomy;
- **chưa scale** nếu chưa pass gate.

**Nếu chưa sẵn sàng**
- không block; tiếp tục benchmark/robustness và hoàn thiện product contracts.

---

## TUẦN 6 — HIS integration + reconciliation + optional SFT

**Tasks**
- MockHISAdapter hoàn chỉnh;
- VNPT/FPT mapping nếu đã nhận API/schema;
- temporal/conflict reconciliation HIS vs conversation;
- coverage report;
- benchmark P1 final trên public data;
- chỉ chạy LoRA/SFT nếu có dataset đủ sạch và W5 chứng minh model capability là bottleneck.

**Decision gate:** data/retrieval/schema bug phải được xử lý trước fine-tuning.

---

## TUẦN 7 — Vietnamese synthetic evaluation nếu có; nếu không, public-data fallback

**Path A — synthetic available**
- freeze `base_case_id` split;
- ingest V1;
- reviewed test set;
- seen/unseen form;
- negative/temporality/correction/conflict robustness;
- compare zero-shot/few-shot/SFT nếu có.

**Path B — synthetic chưa available**
- freeze public benchmark results;
- test unseen-form bằng manual/regression cases + form-level structural tests;
- hoàn tất HIS portability/robustness/ablation;
- ghi rõ Vietnamese synthetic performance là pending dependency, không tạo pseudo-result.

---

## TUẦN 8 — Freeze + reproducibility + two-tier report

**Tasks**
- code/schema/registry freeze;
- clean rerun;
- reproduce guide;
- source/legal appendix;
- model/dataset cards tương ứng dữ liệu thực có;
- final demo;
- production gap list;
- paper feasibility review.

**Final report tách hai tầng**
1. **Independent results:** public datasets + architecture + projector/validator + HIS adapter.
2. **Conditional results:** Vietnamese synthetic benchmark nếu Data Team đã deliver dataset qua quality gate.

**Manager report**
> PoC không bị trễ chỉ vì data-generation pipeline. Kết quả độc lập và kết quả phụ thuộc synthetic được báo cáo riêng, tránh nhập nhằng readiness.
# 11. Phân công nguồn lực

| Role | Trách nhiệm |
|---|---|
| Research Engineer | schema, pipeline, model, evaluation |
| Product Owner | VNPT/FPT schema, semantics, hospital constraints |
| Synthetic Data Team | fact-first generation |
| Clinical reviewer | schema/data/test review |
| Engineering | integration/deployment sau V1 |

---

# 12. Rủi ro và fallback

| Rủi ro | Phương án |
|---|---|
| Không lấy được CV292 attachments | encode subset pre-visit bằng tay |
| VNPT/FPT chậm | generic adapter + mock payload |
| Synthetic data noisy | pilot trước scale |
| Scope quá lớn | cap 80–150 concepts |
| Retriever miss | tăng K / full-schema fallback |
| Open model yếu | strong LLM baseline |
| SFT fail | SFT không phải critical path |
| Form bệnh viện khác | mapping/configuration |
| Luật/form thay đổi | versioned registry |
| HIS conflict | preserve provenance + flag |
| Paper novelty chưa đủ | tập trung regulatory schema + fact-first dataset + unseen-form/HIS portability |

---

# 13. Tiêu chí thành công sau 8 tuần

**Bắt buộc, không phụ thuộc Data Team:**
- regulatory/source registry có provenance;
- CV292/TT32/CV365 source package;
- canonical pre-visit registry;
- 29/BV-02 + 15/BV-01 machine-readable pre-visit subset;
- Data Team generation contract + acceptance gate;
- SYNUR external benchmark;
- MTS-Dialog auxiliary dialogue benchmark;
- ≥3 baselines + proposed pipeline;
- evidence-grounded extraction;
- deterministic projector/validator;
- regression set cho negation/temporality/correction/not-mentioned/conflict;
- HIS mock adapter và VNPT/FPT adapter nếu schema được cung cấp;
- robustness/error analysis;
- reproducible code + final report.

**Conditional theo Data Team:**
- Vietnamese synthetic dataset V1;
- human-reviewed Vietnamese dev/test;
- Vietnamese seen/unseen-form performance;
- SFT trên synthetic data.

Không định nghĩa success là chắc chắn SOTA, accepted paper, patent hoặc số lượng synthetic samples khi upstream pipeline chưa sẵn sàng.
# 14. Hướng paper tiềm năng

**Tên tạm:**  
*Regulatory-Schema-Grounded Pre-Visit Clinical History Structuring for Heterogeneous Vietnamese Medical Forms*

Contribution tiềm năng:

1. regulatory-grounded Vietnamese pre-visit schema;
2. fact-first Vietnamese synthetic dialogue dataset;
3. evidence + assertion + temporality;
4. form-independent fact extraction + deterministic projection;
5. unseen-form generalization;
6. VNPT/FPT portability không cần per-form fine-tuning;
7. external evaluation trên SYNUR.

---

# 15. Nguồn tham chiếu

## Việt Nam

- TT32 form list: https://thuvienphapluat.vn/chinh-sach-phap-luat-moi/vn/bieu-mau/65497/29-mau-benh-an-ban-hanh-kem-theo-thong-tu-32-2023-tt-byt-moi-nhat-2024
- 29/BV-02: https://thuvienphapluat.vn/bieumau/27372/MAU-PHIEU-KHAM-BENH-VAO-VIEN-CHUNG
- TT51/2017: https://vbpl.vn/boyte/Pages/vbpq-van-ban-goc.aspx?ItemID=128248
- TT51 allergy appendix: https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Thong-tu-51-2017-TT-BYT-huong-dan-phong-chan-doan-va-xu-tri-phan-ve-320095.aspx?tab=4
- TT13/2025: https://vbpl.vn/boyte/Pages/vbpq-toanvan.aspx?ItemID=178219
- CV365/TTYQG-GPQLCL: https://thuvienphapluat.vn/cong-van/Cong-nghe-thong-tin/Cong-van-365-TTYQG-GPQLCL-2025-yeu-cau-ky-thuat-trien-khai-phan-mem-ho-so-benh-an-dien-tu-671468.aspx
- CV292/TTYQG-DA: https://dongnaicdc.vn/UserFiles/Docs/2026/VBBYT/CV%20h%20%20ng%20d%20n%20b%20nh%20%C3%A1n%20%20i%20n%20t%20.signed.pdf
- QĐ2805/QĐ-BYT: https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Quyet-dinh-2805-QD-BYT-2025-Danh-muc-ma-dung-chung-thuat-ngu-y-hoc-lam-sang-Dot-3-672318.aspx
- CV65/KCB: https://thuvienphapluat.vn/cong-van/The-thao-Y-te/Cong-van-65-KCB-QLCL-CDT-2024-trien-khai-mau-giay-phieu-y-theo-Thong-tu-32-2023-TT-BYT-595191.aspx

## Paper / Dataset

- SYNUR paper: https://aclanthology.org/2025.emnlp-industry.58/
- MEDIQA-SYNUR 2026: https://aclanthology.org/2026.clinicalnlp-1.3/
- SYNUR dataset: https://huggingface.co/datasets/microsoft/SYNUR
- Note2Chat: https://ojs.aaai.org/index.php/AAAI/article/view/40821
- Synthetic clinical IE: https://www.nature.com/articles/s41746-025-01681-4
- MTS-Dialog: https://github.com/abachaa/MTS-Dialog
- MTS-Dialog paper: https://aclanthology.org/2023.eacl-main.168/

---

# 16. Việc cần làm ngay trong 48 giờ

1. **Tải CV292 PDF + `DacTaEMR-TT32.rar` trước tiên**; kiểm tra attachment có schema/JSON cho 29/BV-02 và 15/BV-01 hay không.
2. Tải và version `29/BV-02`, `15/BV-01`, TT51, QĐ2805, CV365.
3. Sửa toàn repo/spec từ `15/BV1` → `15/BV-01`.
4. Freeze pre-visit scope và `input_scope` từng field.
5. Freeze schema contracts v0.1 + gửi `ESF_DATA_GEN_HANDOFF_V1` cho Data Team ngay.
6. Data Team chỉ cần ack: JSON schema parse được, hiểu fact-first flow, và trả 3–5 sample thử theo contract trước khi build scale pipeline.
7. Implement SYNUR loader + baseline B1 ngay; không chờ Data Team.
8. Implement MTS-Dialog loader với whitelist pre-visit sections; không pseudo-label atomic facts thành gold.
9. Viết 10–20 manually-authored regression cases để test projector/validator/reconciliation.
10. Xin VNPT/FPT API/JSON contract song song; nếu chậm dùng MockHISAdapter.
11. Không fine-tune và không scale synthetic trước khi evaluation harness + quality gate ổn định.
