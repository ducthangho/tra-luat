# ADR-0013 — ZIP ingest: immutable plan bundle — apply không được tự lập kế hoạch mới

- **Trạng thái:** Accepted (2026-07-23, r184 — review p9 v1.35.12; siết 1-extract r185, subprocess=0 r187; file ADR bổ sung r188)
- **Bối cảnh:** DRY của `ingest-zip`/`profile-ingest-zip` trước r184 chỉ đưa plan_hash CHA (parent);
  apply tự chạy child DRY rồi tự `--confirm yes` với hash con mà user CHƯA từng thấy — apply
  tự-phê-duyệt kế hoạch con, drift giữa bản duyệt và bản chạy không bị bắt.
- **Quyết định:**
  1. DRY lập ĐẦY ĐỦ child plan cho từng member (in-process, 0 mutation) →
     `plan_hash` = fingerprint TOÀN bundle (`ingest_zip_bundle.v1`: archive_sha256 + member list
     + MỌI child plan_hash). Xác nhận hash này = duyệt đúng BỘ kế hoạch con.
  2. Apply authorize trên bundle hash; khác bản duyệt ⇒ `PLAN_DRIFT_REPLAN_REQUIRED`, 0 mutation.
     `--confirm yes` cho child CHỈ hợp lệ với child_plan_hash NẰM TRONG bundle đã duyệt.
  3. Hiệu năng không phá an toàn: 1 extract + 1 lượt hash member/invocation (r185); child chạy
     in-process qua engine chung, hash nguồn memo trong run_scope (r187 — ADR-0004). Guard nội
     dung thẩm quyền là so sha256 TỪNG member lúc extract (ZIP_MEMBER_CHANGED_OR_CORRUPT).
  4. Journal: record `plan` bundle + intent/commit per-member; plan hash ZIP đời cũ (chỉ parent)
     hết hợp lệ — DRY lại để lấy bundle hash.
- **Phương án đã loại:**
  - *Apply tự chạy child DRY rồi tự confirm* — tự-phê-duyệt, chính là lỗ hổng đã vá.
  - *Hash bytes container zip làm identity* — zipfile khác phiên bản ghi header khác → key lệch
    cross-machine (đã trả giá v1.33.61); identity nội dung theo member.
- **Hệ quả:** DRY vbqppl không `--cat` chỉ là DRY phân loại (plan_hash không apply được —
  note_bundle nói rõ); mọi thay đổi archive/member/child option giữa DRY và apply đều chặn từ
  authorize; child độc lập + idempotent, apply xử lý MỌI member rồi báo partial tường minh.
