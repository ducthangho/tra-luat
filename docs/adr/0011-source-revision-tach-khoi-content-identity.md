# ADR-0011 — SourceRevision tách khỏi Content Identity; claim key không đội lốt content_hash

- **Trạng thái:** Accepted (2026-07-23, r184 — review p9 v1.35.12; file ADR bổ sung vào cây r188)
- **Bối cảnh:** `identity_hash_for_drive_source` nhét `sha256(drive_id)` vào slot `content_hash` —
  một định danh METADATA đội lốt định danh NỘI DUNG, cùng payload shape với identity thật. Claim
  (khóa chống 2 host cùng ingest) và dedup dùng chung giá trị này nên không phân biệt được "cùng
  nguồn" với "cùng nội dung"; resume theo tên file đơn lẻ có thể nối tiếp NHẦM nguồn.
- **Quyết định:**
  1. `build_source_revision(kind, source_id, revision=None)` — định danh NGUỒN với
     `identity_strength` tường minh (`revision` khi có revision Drive; `metadata` khi chỉ có id);
     payload KHÔNG có trường `content_hash`.
  2. `claim_key_for_source` — khóa claim riêng, payload không chứa content_hash; `observed_at`
     CỐ Ý nằm ngoài khóa. Giá trị claim key ĐỔI so bản cũ — 2 host lệch version không khóa chéo
     trong cửa sổ rollout (TTL 5 phút, chấp nhận có ghi nhận).
  3. Resume `profile-ingest`: name-only chỉ được DRY REPAIR (0 mutation); `--apply` đòi
     `--journal <run_id>` HOẶC `--drive-id` với fingerprint khớp registry (`_resume_identity_gate`
     PURE). Journal đời cũ → `LEGACY_JOURNAL_REPLAN_REQUIRED`; lệch → `RESUME_IDENTITY_MISMATCH`.
- **Phương án đã loại:**
  - *Giữ sha256(drive_id) làm content_hash* — masquerade: dedup/claim ra quyết định trên bằng
    chứng giả về nội dung.
  - *Resume theo tên file* — tên không phải identity (CONTEXT.md); nối tiếp nhầm nguồn là mất
    dữ liệu im lặng.
- **Hệ quả:** `profile-ingest` apply có journal (name/sha256/identity_hash/plan_hash/drive_id +
  run_end); các phiên bản client cũ/mới chạy song song trong cửa sổ rollout không thấy claim của
  nhau (TTL ngắn); test r184 khóa cả chiều tái tạo giá trị masquerade cũ để chứng minh đã tách.
