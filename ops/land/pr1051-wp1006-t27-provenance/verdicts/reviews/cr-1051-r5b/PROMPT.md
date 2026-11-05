# Cross-review lượt 5 — PR ducthangho/tra-luat#1051 — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`, đủ lịch sử. `reviewed_sha` = `git -C cay-kho rev-parse HEAD` (phải bắt đầu `000e0fa`).
  Base master `b29da0b`; các lượt trước `4f9774a` → `82a5ef5` → `cceb0b3` → `3e03459`. Diff toàn PR: `git -C cay-kho diff b29da0b HEAD`;
  diff lượt này: `git -C cay-kho diff 3e03459 HEAD` (ba commit: `5ad81f2`; `877d3e0` basename-gốc-trùng; `000e0fa` thư mục fixture không tên `con` — tên thiết bị dành riêng của Windows — và docstring chuỗi thô) — chỉ `ops/lease_publish_test.py`.
- Finding gốc `tham-chieu/kiem-toan-1007-VERDICT.md`; verdict các lượt `tham-chieu/cr-1051-r{1,2,3,4}-VERDICT.md`; script phản chứng các lượt
  trước ở `tham-chieu/cr-1051-r*-*.py` (có thể phải sửa đường dẫn). Lượt 4 (P2): span NHIỀU dấu nháy và `\|` làm ô ghi tên/cột KHÁC vẫn thoả;
  `+backup`/`@backup` dính sau tên; nhãn link và đích link khác nhau đều thoả.
- Thiết kế lượt 5 của executor (kiểm, đừng nhận). Bốn lượt cùng MỘT lớp, nên executor đổi sang đọc theo đúng ba dạng mục lục THẬT dùng:
  · `_tach_o`: tách ô theo `|` KHÔNG thoát, trả `\|` về `|` (GFM §4.10), dùng cho cả tiêu đề lẫn dữ liệu trong `_bang`.
  · `_ten_tep`: link `[nhãn](đích)` ⇒ danh tính là ĐÍCH; nhãn là tên KHÁC basename đích ⇒ không cho tên nào. Code span theo dãy n nháy mở/đóng
    ĐÚNG n (GFM §6.3), trọn span là một tên hoặc không gì. Chữ trần: biên TRƯỚC và SAU đều là danh sách CHO PHÉP. Link/span đã đọc thay bằng NUL
    (không phải biên). Tên không được bắt đầu bằng `.` (tệp ẩn).
  · `_kiem_muc_luc`: danh tính verdict trong Mục lục = đường dẫn tính từ thư mục verdict (đo: 22 verdict ở thư mục con, mục lục link theo đường
    dẫn); bảng cảnh báo nhận thêm basename (đo: cả 22 hàng cảnh báo của chúng viết basename) — CHỈ khi ở gốc không có verdict cùng basename.
  · Executor khai: trên README thật, mọi ô tên cho CÙNG tập token hoặc TẬP CON so với `3e03459`; t27 xanh.
  · Ca `t27_phan_chung_ten_bien_nhan_sai_bi_TU_CHOI_kem_cach_chua_lam_XANH_ca_t26_t27` bước (6) phủ các ô sai ở ba cột, `\|`, thư mục con.

## Nhiệm vụ
(a) P2 lượt 4 đã đóng? Lặp lại phản chứng lượt 4 qua CLI t27 và `_kiem_muc_luc`.
(b) Kiểm lời khai "README thật: cùng tập hoặc tập con" — từng ô tên (ba cột) và ô id; có hàng thật nào đổi kết luận không. Thiết kế "nhận basename
ở bảng cảnh báo cho verdict thư mục con" có mở lối cho một hàng cảnh báo của verdict GỐC cùng basename thoả caveat của verdict thư mục con (hoặc
ngược lại) không — dựng phản chứng nếu có.
(c) Đường còn sót của lớp "ô ghi tên/cột khác thoả cho tên trên đĩa" — HTML (`<code>`, `<a href>`), entity (`&#96;`), autolink `<x.md>`, link
tham chiếu `[x][1]`, ảnh `![x](y)`, nhãn link lồng span nhiều nháy, đích có `#anchor`/`?q`/ngoặc nhọn, ký tự thoát `\``. Chỉ báo đường nào làm
t27 XANH SAI trên một ô có thể xuất hiện; không cần báo cú pháp mà t27 ĐỎ an toàn (từ chối hẹp hơn là có chủ ý).
(d) Răng: đột biến riêng từng chốt (tách ô bỏ thoát; bỏ luật nhãn link; span một nháy; NUL→khoảng trắng; biên trước/sau rỗng hoặc nới; mục lục
dùng basename; cảnh báo bỏ basename; cùng các chốt lượt trước) phải làm ca mới ĐỎ ở đúng bước — chạy thật trong bản sao tạm.
(e) Hồi quy: chạy `python3 ops/lease_publish_test.py` đầy đủ ở head và base trong bản sao tạm ngoài `cay-kho/`; so delta (tách ca đỏ vì thiếu
công cụ như shellcheck). `ops/cong_cu_test.py` import module này — chạy nó ở head. Ruff `--select F` delta so base.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
