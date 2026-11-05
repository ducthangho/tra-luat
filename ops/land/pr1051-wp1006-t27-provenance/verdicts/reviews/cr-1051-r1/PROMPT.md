# Cross-review lượt 1 — PR ducthangho/tra-luat#1051 (vá P2 kiểm toán sau merge #1007) — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`, đủ lịch sử. `reviewed_sha` = `4f9774aecfb14340fcbe59e89d5781d9603457b7`; base master `b29da0b`
  (cha trực tiếp). Trước mọi việc: `git -C cay-kho rev-parse HEAD` phải bằng `reviewed_sha`. Diff: `git -C cay-kho diff b29da0b 4f9774a`
  — chỉ `ops/lease_publish_test.py`.
- Finding gốc: `tham-chieu/kiem-toan-1007-VERDICT.md` (P2 `wp1006-case-insensitive-listing-case-sensitive-consumer`). Đặc tả packet gốc
  `tham-chieu/wp1006.md` (sha256 `6c21bd26b64aa5a57925875789a8d9f9f3132a00ae53416b1ac4d0ad703e3eef`).
- Lời khai executor (kiểm): `_ten_tep` so đuôi `re.IGNORECASE`, giữ hoa thường của TÊN; `_bien_nhan_cua` tìm sidecar trong danh sách đã liệt kê
  (tiền tố BẰNG stem, đuôi không phân biệt hoa thường; ≥2 ứng viên ⇒ ĐỎ "MƠ HỒ"); ca mới
  `t27_phan_chung_bien_nhan_duoi_HOA_co_hang_phai_XANH_va_sidecar_HOA_tim_duoc`. Windows thật (`tra-luat-win`) t26 1/1, t27_* 3/3.

## Nhiệm vụ
(a) Finding P2 đã đóng? Lặp lại phép tái hiện của kiểm toán (alias `.RECEIPT.YAML` có hàng đúng cột ⇒ xanh; bỏ hàng ⇒ đỏ đúng cột).
(b) Tự liệt kê MỌI chỗ trong `ops/lease_publish_test.py` (và test khác đọc `ops/reviews`) còn so tên/đuôi biên nhận hoặc verdict phân biệt hoa
thường, dựng cứng tên, hoặc gộp tên bằng lower/casefold — đường thứ ba cùng lớp mà bản vá bỏ sót? (vd. caveat `_ten_tep` ở bảng cảnh báo,
`ten_verdict = Path(...).name`, các ca khác dùng `_ten_tep`). Mỗi đường cần chốt riêng.
(c) Răng: đột biến riêng từng chốt (bỏ IGNORECASE; sidecar dựng cứng; bỏ chốt mơ hồ) phải làm ca mới ĐỎ ở đúng bước — chạy thật trong bản sao tạm.
Ca có nhánh "hệ tệp không phân biệt hoa thường thì bỏ qua bước 4" — chốt ấy có thể xanh mà không đo gì trên Linux không? Kiểm điều kiện `phan_biet`.
(d) Hồi quy: chạy `python3 ops/lease_publish_test.py` đầy đủ ở head và base trong bản sao tạm ngoài `cay-kho/`; so delta (phân biệt ca đỏ vì thiếu công cụ
môi trường như shellcheck).

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
