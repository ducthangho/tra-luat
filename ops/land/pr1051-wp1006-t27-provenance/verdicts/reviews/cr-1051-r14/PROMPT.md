# Cross-review lượt 14 — PR ducthangho/tra-luat#1051 — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`, đủ lịch sử. `reviewed_sha` = `git -C cay-kho rev-parse HEAD` (phải bắt đầu `de55985`). Base master `b29da0b`.
  Diff toàn PR: `git -C cay-kho diff b29da0b HEAD` — chỉ `ops/lease_publish_test.py` (các ca `t26`/`t27` kiểm mục lục `ops/reviews/README.md`).
  Diff lượt này: `git -C cay-kho diff bc3bbb5 HEAD`.
- Lịch sử: `tham-chieu/cr-1051-r{1..13}-VERDICT.md` (cùng một lớp P2: t27 công nhận nội dung mà bảng hiển thị không có). Script phản chứng các lượt trước
  nằm ở `tham-chieu/cr-1051-r*-*.py` — dùng lại chúng (có thể phải sửa đường dẫn), không cần soạn đầu vào mới.
- Lượt 13 (P2): nhóm `So` chứa bảng chữ Latin khoanh tròn/đóng khung nên vẫn viết được chữ trước tên mục. Lượt 14: tiền tố là tập LITERAL — chỉ đúng tên mục, hoặc `⚠ ` + tên mục (đúng như mục lục thật).
- Lượt 12 (P2): tiền tố trước tên mục dùng lớp ký tự phủ định nên nhận một ký tự định dạng hướng chữ. Lượt 13: tiền tố theo danh sách CHO PHÉP — chỉ
  space/tab và ký hiệu Unicode thuộc nhóm `So`/`Sc` (mục lục thật dùng `⚠ `).

## Nhiệm vụ — CHẠY và ĐỘT BIẾN, không soạn chuỗi tấn công mới
(a) Chạy lại harness lượt 13 (`tham-chieu/cr-1051-r13-review_*.py` — đã thích nghi sẵn), script lượt 12 (`tham-chieu/cr-1051-r12-review_bidi.py`) và lượt 11 (`…-r11-review_current.py`, `…-r11-review_additional.py`) trên head:
    mọi đầu vào sai phải ĐỎ, đối chứng sửa đúng XANH.
(b) Đọc mã: tập tiền tố literal mới có còn cửa nào không (so sánh có chuẩn hoá nào ngầm không, `#` đóng, khoảng trắng)? Nêu bằng LỜI (không cần dựng) nếu thấy một nhóm ký tự `So`/`Sc` có thể làm chữ hiển
    thị của tiêu đề khác tên mục; executor sẽ tự dựng phản chứng.
(c) Răng: đột biến riêng từng chốt của PR trong bản sao tạm (ít nhất: quay tiền tố về lớp phủ định; chọn mục bằng chuỗi con của nguồn; bỏ chốt comment; bỏ chốt
    HTML; nới hàng gạch; bỏ chốt đoạn văn trước bảng; bỏ ngữ pháp ô tên/ô id; bỏ alias duy nhất) — mỗi cái phải làm ca
    `t27_phan_chung_ten_bien_nhan_sai_bi_TU_CHOI_kem_cach_chua_lam_XANH_ca_t26_t27` ĐỎ bằng AssertionError. SyntaxError không tính là giết.
(d) Hồi quy: chạy `python3 ops/lease_publish_test.py` đầy đủ ở head và base trong bản sao tạm ngoài `cay-kho/`; so delta (tách ca đỏ vì thiếu `shellcheck`).
    README thật: `_bang` cho cùng hàng như `12f21b2` (321 / 750) và t27 XANH. Ruff `--select F` delta so base.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
