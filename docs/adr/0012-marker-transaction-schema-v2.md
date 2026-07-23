# ADR-0012 — Marker write là transaction chứng minh được; schema v2 có fingerprint, rollout 2 pha

- **Trạng thái:** Accepted (2026-07-23, r184 — review p9 v1.35.12; R2 thi hành r186; file ADR bổ sung r188)
- **Bối cảnh:** `_marker_write` cũ báo thành công giả: readback chỉ so 3 trường (marker cụt/lệch
  trường khác vẫn "verified"), enumeration nuốt `except: pass` (duplicate sót vẫn cleanup_ok), không
  chứng minh "chỉ còn MỘT marker" sau cleanup. Marker là NGUỒN SỰ THẬT định danh profile (ADR-0003)
  nên false-success ở đây làm hỏng mọi quyết định phía sau.
- **Quyết định:**
  1. `_marker_write` = state machine journaled: intent → upload → **FULL readback** (so TRỌN
     payload) → enumerate (lỗi list = PARTIAL tường minh) → cleanup → **prove-one** (re-list chứng
     minh 0 marker dư) → commit. Không chứng minh được hậu điều ⇒ `PARTIAL`/`FAILED`, `ok=False`,
     journal giữ dữ kiện repair.
  2. Schema v2 `tra_luat_profile.v2`: bộ trường bắt buộc theo `manifestScope` (own ⇒
     notebookId/registryDocId/manifestId; mọi profile ⇒ profile/rootFolderId/metaFolderId) +
     `fingerprint` = sha256 canonical-JSON toàn payload trừ chính trường fingerprint.
  3. Rollout 2 pha: **R1 (r184)** reader hiểu v1+v2, writer GIỮ v1 (compat 1 phiên bản);
     **R2 (r186, sau khi reader v1/v2 LIVE)** writer phát v2 + fail-closed TRƯỚC upload
     (`REJECTED` khi body không hợp lệ — 0 mutation Drive); migration v1→v2 qua
     `profile-doctor --plan-marker-migration` (DRY, canary-trước) + `profile-backfill-markers
     --profile-name <p> --apply --force` do user duyệt.
  4. `_marker_mutation_guard` chung: mutation profile chỉ chạy khi trạng thái marker KHÔNG mơ hồ
     (đọc lỗi / duplicate / invalid / thuộc profile khác ⇒ CHẶN với lỗi hành động được).
- **Phương án đã loại:**
  - *Flip writer v2 một pha* — client cũ (reader chỉ v1) coi marker mới là SCHEMA_MISMATCH.
  - *Giữ readback 3 trường* — chính là false-success đã trả giá.
  - *Auto-migrate khi doctor gặp v1* — mutation LIVE không qua user duyệt, trái quy trình.
- **Hệ quả:** 6 caller (rename/adopt/create/backfill/promote/set-meta) chuyển điều kiện thành
  `ok` trọn chuỗi hậu điều; fixture test vá trường sau `_marker_body` phải re-mint fingerprint;
  own-scope thiếu notebookId/registryDocId/manifestId nay bị chặn từ lúc ghi thay vì lộ ra ở doctor.
