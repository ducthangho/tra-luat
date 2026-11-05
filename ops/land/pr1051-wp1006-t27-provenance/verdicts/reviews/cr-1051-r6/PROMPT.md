# Cross-review lượt 6 — PR ducthangho/tra-luat#1051 — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`, đủ lịch sử. `reviewed_sha` = `git -C cay-kho rev-parse HEAD` (phải bắt đầu `7c4bc17`).
  Base master `b29da0b`; lượt 5 review `000e0fa`. Diff toàn PR: `git -C cay-kho diff b29da0b HEAD`; diff lượt này:
  `git -C cay-kho diff 000e0fa HEAD` — chỉ `ops/lease_publish_test.py`.
- Finding gốc `tham-chieu/kiem-toan-1007-VERDICT.md`; verdict các lượt `tham-chieu/cr-1051-r{1..5}-VERDICT.md`; script phản chứng các lượt
  ở `tham-chieu/cr-1051-r*-*.py` (có thể phải sửa đường dẫn). Lượt 5 (P2): link tham chiếu, HTML, ảnh, link trong span, entity, span dính
  tiền tố vẫn thoả; alias basename ở bảng cảnh báo chỉ so với `ds_verdict` nên `VERDICT.md`/`report.md` gốc và hai thư mục con cùng basename va nhau.
- Thiết kế lượt 6 của executor (kiểm, đừng nhận). Năm lượt cùng MỘT lớp ⇒ đổi từ "đọc Markdown" sang NGỮ PHÁP CHO PHÉP trong `_ten_tep`:
  ô tên phải BẮT ĐẦU bằng một hay nhiều MỤC — `` `TÊN` `` (một nháy, trọn một tên) hoặc `[NHÃN](ĐƯỜNG)` với NHÃN bằng basename của ĐƯỜNG hay là
  đuôi bắt đầu bằng `.` của nó; sau mục là hết ô, `,` (rồi PHẢI là mục nữa) hoặc khoảng trắng (phần còn lại là chú thích, bỏ qua). Mọi dạng khác
  ở đầu ô cho tập RỖNG (hỏng về phía an toàn: thiếu tên ⇒ t27 ĐỎ). Chốt tên của tệp nay hỏi `_ten_tep(f"`{tên}`")`. Alias basename ở bảng cảnh báo
  chỉ cấp khi basename xác định DUY NHẤT một danh tính trong {đường dẫn verdict của MỌI biên nhận} ∪ {verdict trên đĩa ở gốc}.

## Nhiệm vụ
(a) P2 lượt 5 đã đóng? Lặp lại phản chứng lượt 5 qua CLI t27 và `_kiem_muc_luc` (ba ô tên + bảng cảnh báo + ba dạng basename trùng).
(b) Ngữ pháp có còn đường nào làm t27 XANH SAI không: chuỗi MỤC hợp lệ ghép với một mục khác lệch danh tính, chú thích sau khoảng trắng chứa
cú pháp làm người đọc hiểu ô là tên khác, mục sau dấu phẩy, nhãn link chứa ký tự lạ, ĐƯỜNG có `..`/`./`/`//`, Unicode trong tên, đuôi `.yml`.
Chỉ báo đường làm t27 XANH SAI; ĐỎ an toàn (từ chối hẹp hơn) là có chủ ý.
(c) README thật: mọi ô tên (ba cột) cho CÙNG tập hoặc TẬP CON so với `000e0fa` và mọi kết luận theo hàng không đổi? Alias basename mới có làm hàng
thật nào đổi kết luận không?
(d) Răng: đột biến riêng từng chốt (bỏ IGNORECASE; nhận ảnh như link; bỏ luật nhãn; nhãn `.` bất kỳ; nhận ký tự dính sau mục; span cho khoảng trắng;
bỏ giữ span; tách ô bỏ thoát; mục lục dùng basename; bỏ alias; alias không cần duy nhất; tập danh tính chỉ từ ds_verdict; cùng chốt đuôi/tên/ba lời
gọi/sidecar) phải làm ca mới ĐỎ ở đúng bước — chạy thật trong bản sao tạm. Đột biến nào làm SyntaxError thì không tính là giết.
(e) Hồi quy: chạy `python3 ops/lease_publish_test.py` đầy đủ ở head và base trong bản sao tạm ngoài `cay-kho/`; so delta (tách ca đỏ vì thiếu công cụ
như shellcheck). `ops/cong_cu_test.py` import module này — chạy nó ở head. Ruff `--select F` delta so base; SyntaxWarning delta so base.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
