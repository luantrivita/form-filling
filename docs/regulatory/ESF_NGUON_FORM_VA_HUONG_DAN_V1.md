# ESF — Nguồn tải Form, đặc tả và hướng dẫn điền (V1)

## Ưu tiên tải ngay

| Priority | Tài liệu | Vai trò | Nguồn tải |
|---|---|---|---|
| P0 | CV292/TTYQG-DA + `DacTaEMR-TT32.rar` | Structured technical specification cho 29 bệnh án + 56 giấy/phiếu; field description/datatype/length/reference/JSON | https://dongnaicdc.vn/huong-dan-dac-ta-cau-truc-thong-tin-cac-mau-benh-an-mau-giay-phieu-y-duoc-quy-dinh-tai-thong-tu-so-32-2023-tt-byt-ngay-31-12-2023-cua-bo-y-te |
| P1 | MS 29/BV-02 | Target Form A: phiếu khám bệnh vào viện | https://thuvienphapluat.vn/bieumau/27372/MAU-PHIEU-KHAM-BENH-VAO-VIEN-CHUNG |
| P1 | MS 15/BV-01 | Target Form B: bệnh án ngoại trú chung | https://thuvienphapluat.vn/bieumau/27319/MAU-BENH-AN-NGOAI-TRU-CHUNG |
| P1 | TT32 appendices Word | Bản Word phụ lục để đối chiếu/parse | https://thuvienphapluat.vn/phap-luat/phu-luc-thong-tu-32-cua-bo-y-te-ban-word-tai-ve-chi-tiet-29-phu-luc-ban-hanh-kem-thong-tu-32-moi-nh-613909-230739.html |
| P2 | CV365/TTYQG-GPQLCL | EMR interoperability; XML/JSON; adapter boundary | https://thuvienphapluat.vn/cong-van/Cong-nghe-thong-tin/Cong-van-365-TTYQG-GPQLCL-2025-yeu-cau-ky-thuat-trien-khai-phan-mem-ho-so-benh-an-dien-tu-671468.aspx |
| P3 | QĐ2805/QĐ-BYT | Chuẩn hóa terminology/code cho allergy/finding | https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Quyet-dinh-2805-QD-BYT-2025-Danh-muc-ma-dung-chung-thuat-ngu-y-hoc-lam-sang-Dot-3-672318.aspx |
| P4 | TT51/2017/TT-BYT | Semantics/reference cho allergy/anaphylaxis history | https://vbpl.vn/boyte/Pages/vbpq-van-ban-goc.aspx?ItemID=128248 |

## Dataset public

- SYNUR: https://huggingface.co/datasets/microsoft/SYNUR
- MTS-Dialog: https://github.com/abachaa/MTS-Dialog
- SYNUR paper: https://aclanthology.org/2025.emnlp-industry.58/
- MEDIQA-SYNUR 2026: https://aclanthology.org/2026.clinicalnlp-1.3/
- MTS-Dialog paper: https://aclanthology.org/2023.eacl-main.168/

## Hướng dẫn điền: rule cần dùng

Không giả định có một “filling manual” công khai hoàn chỉnh cho từng dòng 29/BV-02/15-BV-01. Dùng hierarchy:

1. CV292 field description/datatype/reference/JSON.
2. TT32 form labels/layout.
3. Official code/value lists như QĐ2805.
4. Specialty regulation như TT51.
5. `FIELD_GUIDANCE_V1` do Clinical Reviewer + Product Owner duyệt cho phần còn mơ hồ.

Mỗi field guidance phải giữ provenance, version, reviewer và ngày review.
