# Cross-review lượt 3 — PR ducthangho/tra-luat#1051 — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`, đủ lịch sử. `reviewed_sha` = `git -C cay-kho rev-parse HEAD` (phải bắt đầu `cceb0b3`).
  Base master `b29da0b`; lượt 1 `4f9774a`, lượt 2 `82a5ef5`. Diff toàn PR: `git -C cay-kho diff b29da0b HEAD`; diff lượt này:
  `git -C cay-kho diff 82a5ef5 HEAD` — chỉ `ops/lease_publish_test.py`.
- Finding gốc `tham-chieu/kiem-toan-1007-VERDICT.md`; verdict lượt 1 `tham-chieu/cr-1051-r1-VERDICT.md`; lượt 2
  `tham-chieu/cr-1051-r2-VERDICT.md` (P2: tên có khoảng trắng — `_ten_tep` chỉ trích `words.receipt.yaml`, làm theo lời chữa vẫn đỏ).
- Thiết kế lượt 3 của executor (kiểm, đừng nhận): `_doi_ten_hop_le(ds, bien_nhan)` thay `_doi_duoi_bien_nhan_thuong`, áp cho biên nhận ở t26/t27
  và cho verdict ở t27: tên phải được `_ten_tep` trích NGUYÊN VẸN, biên nhận phải đuôi `.receipt.yaml` viết thường; mọi lỗi của một tệp nêu
  trong CÙNG một thông báo kèm "Đổi tên tệp". `_ten_tep` đọc NGUYÊN code span (span không trọn một tên ⇒ không cho tên nào) và đòi biên trước token
  ở phần ngoài span. Mục lục thật viết tên TRẦN (không code span) — đã đo 306/306 hàng. Ca mới
  `t27_phan_chung_ten_bien_nhan_sai_bi_TU_CHOI_kem_cach_chua_lam_XANH_ca_t26_t27` dùng biên nhận đủ (băm, https) để đo chiều XANH của cả t26 lẫn t27
  sau khi làm theo lời chữa.

## Nhiệm vụ
(a) P2 lượt 2 đã đóng? Lặp lại phản chứng lượt 2 (receipt v2 hợp lệ tên có khoảng trắng; đổi đuôi; đổi tên) — làm đúng lời chữa phải làm CẢ t26 và t27
xanh, và cổng v2 đọc được cùng tệp. Biên mới của `_ten_tep` có làm hỏng hàng thật nào của `ops/reviews/README.md` (cả hai bảng) không — kể cả tên trong
link Markdown, sau dấu phẩy, sau ngoặc, trong code span lẫn ngoài? Có tên nào `_doi_ten_hop_le` nhận mà v2/packet_loop/c38/c42 không đọc, hoặc ngược lại?
(b) Còn đường thứ ba cùng lớp "bộ liệt kê nhận ≠ bộ đọc nhận" chưa đóng không (ký tự Unicode, tên bắt đầu bằng `-`/`.`, đuôi `.yml`, tên chỉ khác dấu,
dấu `/` trong token)? Mỗi đường cần phản chứng chạy được.
(c) Răng: đột biến riêng từng chốt (bỏ chốt đuôi; bỏ chốt tên; bỏ từng lời gọi ở t27 biên nhận / t27 verdict / t26; sidecar không phân biệt hoa thường;
bỏ IGNORECASE ngoài span; bỏ biên trước token; bỏ đọc nguyên span) phải làm ca mới ĐỎ ở đúng bước — chạy thật trong bản sao tạm. Có chốt nào xanh mà không đo gì?
(d) Hồi quy: chạy `python3 ops/lease_publish_test.py` đầy đủ ở head và base trong bản sao tạm ngoài `cay-kho/`; so delta (tách ca đỏ vì thiếu công cụ môi trường
như shellcheck). Ruff `--select F` delta so base.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
