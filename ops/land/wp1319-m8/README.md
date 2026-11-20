# Bản lưu Git của biên bản M8 — packet #1319 và 6 WP con

Làn lưu trữ ADR-0060 (M8): bản ghi thụ động, không review bằng model, không chạy Windows.
**Nguồn có thẩm quyền là comment trên Issue**; tệp ở đây chỉ là bản chiếu.

Mỗi `m8-<issue>.yaml` là khối ```yaml``` của comment M8 trên Issue ấy. `readback-comment-<id>.json` là phản hồi REST
thô (`GET /repos/ducthangho/tra-luat/issues/comments/<id>`, đọc 2026-11-20 qua proxy phiên) — khối ```yaml``` trong
`body` của nó khớp từng byte với `m8-<issue>.yaml` (bỏ `\r`).

| Issue | WP | comment | sha256 (16 ký tự đầu) |
|---|---|---|---|
| #1401 | WP-PXA | 7022988362 | 232764cbd2b14ddf |
| #1405 | WP-NSIS | 7022997734 | e0b8286d65fac1ec |
| #1409 | WP-PXU | 7023002175 | b3952176630c7ea4 |
| #1410 | WP-U8 | 7023006731 | dc87287758ffb6cc |
| #1413 | WP-PXL | 7023011613 | 4cfcd91f71436868 |
| #1416 | WP-PXR | 7029053418 | ed8550453111bf64 |
| #1319 | wp1319 (packet gốc) | 7030386442 | 3843e33ec5a1f0d1 |

Mọi comment có `updated_at == created_at` lúc đọc (chưa ai sửa). Dữ kiện land của commit merge `d8cf2ab`
(M8 #1319, `moc_10_2_2`) nằm ở `../pr1440-wp1319-provenance/`.
