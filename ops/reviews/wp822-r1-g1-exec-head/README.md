# wp822 (#822 `KG-RANG-TEST`) — hiện vật executor `wp822-r1-g1-claude`, DỪNG ở review lượt 3

Thư mục này là **bản lưu bền** của nhánh thi hành `agent/wp822-g1-claude`. Nhánh ấy CHƯA đẩy: chính sách lease là
"push một lần sau khi review cục bộ approve", và review chưa approve. Hiện vật được định danh bằng **băm**, không bằng
tên nhánh.

- Base: `f712205aa39e0b54d04a5bd8145fa69a84601fed`.
- Head cục bộ: `ee853d32e2e55592a1d7caf4c5f16714cd25dad2`, tree `37f9c4a2f591df0df532cacac0672b8348cdd931`.
- Dựng lại head: `git checkout -b x f712205 && git am ops/reviews/wp822-r1-g1-exec-head/*.patch`, rồi kiểm tree bằng
  `git rev-parse HEAD^{tree}` (phải ra tree trên). SHA commit có thể khác vì `git am` ghi committer mới.
- Đặc tả: `ops/specs/wp822.md`, sha256 `6bcac189…0b07`.
- Lease: `origin/ops/wp822-spec:ops/leases/wp822-r1-g1-claude.yaml`.

| lượt | reviewed commit | run | kết quả |
|---|---|---|---|
| 1 | `08aa096` | `f64b71ab`, rc 0, 1709 s | `changes_requested — P0=0 P1=0 P2=4 P3=0` |
| 2 | `cffd44e` | `b85fb5cb`, rc 1, 994 s | **DỞ DANG**: bộ lọc nội dung của nền chặn khi reviewer tự soạn mã giả traceback; bản dở ghi P2=5 |
| 3 | `ee853d3` | `3979431d`, rc 0, 1955 s | `changes_requested — P0=0 P1=0 P2=5 P3=0` |

**Vì sao dừng.** Hai điều kiện dừng đã chạm cùng lúc:

1. Lớp `tin-dung-giet-sai` có mặt ở cả ba lượt. Ở lượt 3 nó mang nhãn "vá hờ": phần còn lại là chốt tự kiểm M6 cho
   đường chỉ có `__cause__` và đường banner chỉ nằm trong đối số.
2. HINT lượt 3 đưa diff lên +449/450 (ADR-0053) mà vẫn chưa đóng phần cause-only.

Gate tại chỗ trên `ee853d3`:

- suite: `nền: 597/597 đạt · BỎ QUA: 1 · TỔNG: ĐẠT`;
- `doctrine-scan` và `adr-song`: rc 0;
- ruff F: delta 0;
- kích thước: 1 tệp, +428/−19.

Evidence đầy đủ (khoảng 47 MB) KHÔNG commit. `EVIDENCE_SHA256SUMS` của từng lượt là băm của các tệp evidence ấy lúc
chạy. Bản gốc nằm trong scratchpad của phiên executor và mất khi container bị thu hồi.
