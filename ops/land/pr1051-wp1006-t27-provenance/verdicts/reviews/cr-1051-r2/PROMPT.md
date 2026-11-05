# Cross-review lượt 2 — PR ducthangho/tra-luat#1051 — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`, đủ lịch sử. `reviewed_sha` = `82a5ef5` (đầy đủ: lấy bằng `git -C cay-kho rev-parse HEAD`, phải bắt đầu `82a5ef5`).
  Base master `b29da0b`; lượt 1 review `4f9774a`. Diff toàn PR: `git -C cay-kho diff b29da0b HEAD`; diff lượt này: `git -C cay-kho diff 4f9774a HEAD`
  — chỉ `ops/lease_publish_test.py`.
- Finding gốc: `tham-chieu/kiem-toan-1007-VERDICT.md` (P2 `wp1006-case-insensitive-listing-case-sensitive-consumer`).
  Verdict lượt 1: `tham-chieu/cr-1051-r1-VERDICT.md` (P2: nhận biên nhận đuôi HOA ở t26/t27 mở lối vòng cổng v2 vì `ops/bien_nhan_v2.py`,
  `--sinh-no`, c38/c42, `packet_loop._doc_bien_nhan` duyệt `glob("*.receipt.yaml")`).
- Thiết kế lượt 2 của executor (kiểm, đừng nhận): thay vì đồng bộ năm bộ đọc ngoài PR, t26/t27 vẫn THẤY tên đuôi không viết thường trên mọi nền
  rồi TỪ CHỐI (`_doi_duoi_bien_nhan_thuong`), lời chữa là đổi tên. Sidecar tra theo tên NGUYÊN `{stem}.receipt.yaml` trong tập đã liệt kê;
  bỏ `_bien_nhan_cua` và chốt "MƠ HỒ". Thân t26 tách thành `_kiem_bam_bien_nhan(thu_muc, goc)`. Ca mới
  `t27_phan_chung_bien_nhan_duoi_HOA_bi_TU_CHOI_kem_cach_chua_lam_duoc` thay ca lượt 1.

## Nhiệm vụ
(a) P2 lượt 1 đã đóng? Lặp lại phản chứng của lượt 1 (alias đuôi HOA, `schema_version: 999`, có hàng mục lục): t26 và t27 bây giờ phải ĐỎ,
bản đuôi thường vẫn bị cổng v2 chặn. Có còn tên nào t26/t27 CHẤP NHẬN mà cổng v2/packet_loop KHÔNG đọc (hoặc ngược lại) không — kể cả
đuôi mixed case, tên có khoảng trắng, symlink, thư mục mang đuôi?
(b) P2 gốc của kiểm toán #1007 còn đóng không: thông báo đỏ cho tên đuôi HOA giờ phải là lời chữa LÀM ĐƯỢC (làm theo ⇒ xanh). Thiết kế
"từ chối" có mâu thuẫn hợp đồng nào khác của kho (README `ops/reviews`, protocol, `bien_nhan_v2.py`) không?
(c) Răng: đột biến riêng từng chốt (bỏ chốt đuôi trong hàm; bỏ lời gọi ở t27; bỏ lời gọi ở t26; sidecar so tiền tố không phân biệt hoa thường;
bỏ IGNORECASE ở `_ten_tep`) phải làm ca mới ĐỎ ở đúng bước — chạy thật trong bản sao tạm. Ca có nhánh nào xanh mà không đo gì không?
Đường thứ ba cùng lớp mà bản vá bỏ sót?
(d) Hồi quy: chạy `python3 ops/lease_publish_test.py` đầy đủ ở head và base trong bản sao tạm ngoài `cay-kho/`; so delta (phân biệt ca đỏ vì thiếu
công cụ môi trường như shellcheck). Ruff `--select F` delta so base.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
