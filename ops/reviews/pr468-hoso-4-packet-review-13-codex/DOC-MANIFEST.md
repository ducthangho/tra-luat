# Gói hiện vật cross-review lượt 13 (PR #468, head f77f198)

`ARTIFACTS.sha256` là manifest của reviewer (48 tệp), đường dẫn tính từ gốc sandbox: `VERDICT.md` = `../pr468-hoso-4-packet-review-13-codex-verdict.md`, `do-review13/` = thư mục này. Đối chiếu khi chép: 48/48, rc=0. Thư mục `do-review13/tmp/` (kho giả của selftest) và `do-review13/manifest12-layout/` (bản bố trí tạm để reviewer kiểm lại manifest lượt 12 — trùng gói lượt 12 đã có trong kho) KHÔNG chép và KHÔNG nằm trong manifest.

Các tệp `bundle-*` là đầu vào executor giao cho reviewer (EVIDENCE, PROMPT + băm, readback `ai-dang-giu` 20:45Z, `ls-remote` 303 nhánh + phép so tập) — vá P1 `mirror-thieu-ref-khong-du-do-a9` của lượt 12 bằng mirror đủ ref. P3 `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu`: nhận là nợ chất lượng gói; gợi ý của reviewer ở `goi-y-evidence.md`, áp cho EVIDENCE của lượt kế (nếu có).
