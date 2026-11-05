# Cross-review lượt 4 — PR ducthangho/tra-luat#1051 — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`, đủ lịch sử. `reviewed_sha` = `git -C cay-kho rev-parse HEAD` (phải bắt đầu `3e03459`).
  Base master `b29da0b`; các lượt trước `4f9774a` → `82a5ef5` → `cceb0b3`. Diff toàn PR: `git -C cay-kho diff b29da0b HEAD`;
  diff lượt này: `git -C cay-kho diff cceb0b3 HEAD` — chỉ `ops/lease_publish_test.py`.
- Finding gốc `tham-chieu/kiem-toan-1007-VERDICT.md`; verdict các lượt `tham-chieu/cr-1051-r{1,2,3}-VERDICT.md`.
  Lượt 3 (P2): `_bang` bóc dấu nháy ngược của ô trước khi giao `_ten_tep`, nên ô `` `two x-verdict.receipt.yaml` `` thoả cho tệp
  `x-verdict.receipt.yaml`; ngoài span thiếu biên SAU token (`.yaml.bak`, `.yaml/child`).
- Thiết kế lượt 4 của executor (kiểm, đừng nhận): `_bang(van, tieu_de, giu_span=False)`; `giu_span=True` giữ nguyên ô dữ liệu (tiêu đề vẫn bóc),
  dùng ở `_kiem_muc_luc` cho cả hai bảng; cột `id` tự bóc dấu nháy theo từng token. `_ten_tep` ngoài span đòi biên trước VÀ sau token
  (`(?![\w\-/]|\.\w)` — dấu chấm/phẩy kết câu vẫn là biên). Ca phản chứng thêm bước (6) tích hợp qua bảng thật bằng `_kiem_muc_luc`.

## Nhiệm vụ
(a) P2 lượt 3 đã đóng? Lặp lại phản chứng lượt 3 (script của lượt 3 chép ở `tham-chieu/cr-1051-r3-review_extra.py`; có thể phải sửa đường dẫn) qua CLI t27
và `_kiem_muc_luc`: mọi ô tên KHÁC phải đỏ đúng chốt, tên đúng xanh, ở cả cột 'biên nhận', 'tệp verdict' của Mục lục và bảng cảnh báo.
(b) `giu_span=True` có làm hỏng hàng thật nào của `ops/reviews/README.md` (750 hàng cảnh báo, 306 hàng mục lục) không — so tập token/khớp
head với base cho từng ô tên và từng ô id. Có consumer nào khác của `_bang` (hoặc caller của `_kiem_muc_luc`) bị đổi hành vi không?
(c) Đường thứ ba cùng lớp "ô ghi tên khác thoả cho tên trên đĩa" còn sót? (nhiều span trong một ô, span lồng/không đóng, link Markdown trỏ tên khác
với chữ hiển thị, HTML entity, tên trong ô id, ký tự `|` thoát `\|`). Mỗi đường cần phản chứng chạy được qua bảng thật.
(d) Răng: đột biến riêng từng chốt (bỏ `giu_span`; bỏ biên sau; bỏ bóc nháy ở id; cùng các chốt lượt trước: chốt đuôi, chốt tên, ba lời gọi,
sidecar, IGNORECASE ngoài span, biên trước, đọc nguyên span) phải làm ca mới ĐỎ ở đúng bước — chạy thật trong bản sao tạm.
(e) Hồi quy: chạy `python3 ops/lease_publish_test.py` đầy đủ ở head và base trong bản sao tạm ngoài `cay-kho/`; so delta (tách ca đỏ vì thiếu công cụ
môi trường như shellcheck). Ruff `--select F` delta so base.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
