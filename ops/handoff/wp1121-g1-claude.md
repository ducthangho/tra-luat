# Handoff wp1121 g1 — DOC-CLAIMS-XOA (packet #1121)

- Đặc tả có hiệu lực: `ops/specs/DOC-CLAIMS-XOA-r5.md`, sha256 `d4626ecbe5389ea4fc15c7b453b2001728ac629a1928deb9cdaaf053eeab2a3b`
  (chủ kho duyệt; r4 `62ecdfc3…` duyệt trước đó). Lease `wp1121-r5-g1-claude` (thay `wp1121-r4-g1-claude`, bia mộ hai chiều).
- PR thi công #1125, nhánh `agent/wp1121-g1-claude`, head `683ae454b9bbfa7c5732953941d5ca646f390a57`, base `c82047d`.
  PR đặc tả #1123 (head `0832d3d`).
- Trạng thái lúc ghi (01-11-2026 ~18:05Z): đủ M-1..M-4 của lease; chờ chủ kho merge. Executor KHÔNG merge.

## Đã làm
- `scripts/tl_core/workflow.py`: L1 cờ `PATH_DELETED` cho tài liệu sống; advisory `PATH_DELETED_IN_HISTORICAL_DOC` cho tài liệu
  lịch sử; `_doc_claims_is_historical` (mục kết thúc `/` = tiền tố thư mục, còn lại so bằng) dùng ở `historical` và L9.
- Fragment `scripts/test_fragments/wp1121_doc_claims_xoa.py` (8 ca a–h, 4 tiền điều kiện).
- Tái sinh bundle fragment và `RELEASE_MANIFEST.json` (`file_count` 198).

## Bằng chứng
- CI `683ae45`: mọi check xanh; `gate` `== tl selftest 1775/1775 ==`, 0 `[FAIL]` (log tải bằng REST, job 124915448585).
- Codex: 7 lời gọi / trần 10 (ADR-0055) — 2 offline đặc tả, 4 connector đặc tả/thi công, 1 connector head cuối
  (`Reviewed commit: 683ae454b9`, sạch).
- Tại chỗ (Linux): đột biến D1–D11 đều đỏ đúng ca đích; N3 rc=2 / nền rc=0; N4 nền rc=0, 0 cờ, ngoài L1 không đổi (219/219);
  `release-verify --strict` ok; ruff F delta 0.
- Windows local (ASUS-LAPTOP, ADR-0057..0059): fragment head True / nền False; `bundle_fragment_check` ok; N3 head rc=2 /
  nền rc=0; sổ đo `D:\tl-win\do-luong.csv` dòng 34; khoá đã nhả.

## Lệch so với đặc tả và lý do
- Selftest đầy đủ KHÔNG chạy tại chỗ (chủ kho chỉ thị "chỉ chạy những gì mới"); N1 lấy từ CI. Hệ quả đo được: ca trần gói
  (`r291_docs_ngoai_goi`, `r357_agents_ngoai_goi`, `wp44_release_bundle_topology_under_200`) chỉ lộ ở CI trên `f9e4342`
  (1772/1775) ⇒ r5 bỏ `changelog.d/wp-1121.md` (Q9).
- Fragment so bộ năm (lớp, tệp, claim, mã, advisory) thay vì bộ ba của đặc tả — chặt hơn, không lỏng hơn.

## Việc còn mở
- Nợ `DOC-CLAIMS-XOA-F1-GOC-MAT`: L1 bỏ token có gốc thư mục đã mất và token `./`, `../`.
- Đề xuất packet riêng: đưa `changelog.d/` ra khỏi gói phát hành (15 tệp đang chiếm khe; gói ở trần 198).
- Phiên land: hợp nhất changelog từ comment trên #1121 (không có `changelog.d/wp-1121.md`).
